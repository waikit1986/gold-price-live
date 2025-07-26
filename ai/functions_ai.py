import os
import re
import json
import asyncio
import datetime
from typing import Any
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import and_

from openai import AsyncOpenAI
from db.database import SessionLocal
from ai.models_ai import AiAnalysis1H, AiAnalysis1D
from ai.schema_ai import AiResponse
from news.functions_news import get_latest_news_titles_and_summaries
from indicators.models_features import (
    IndicatorFeatureGLD_1H, IndicatorFeatureGCF_1H, IndicatorFeatureIAU_1H,
    IndicatorFeatureSIF_1H, IndicatorFeaturePPLT_1H, IndicatorFeaturePALL_1H,
    IndicatorFeatureDXY_1H, IndicatorFeatureTNX_1H, IndicatorFeatureTIP_1H,
    IndicatorFeatureCLF_1H, IndicatorFeatureVIX_1H, IndicatorFeatureGSPC_1H,
    IndicatorFeatureGLD_1D, IndicatorFeatureGCF_1D, IndicatorFeatureIAU_1D,
    IndicatorFeatureSIF_1D, IndicatorFeaturePPLT_1D, IndicatorFeaturePALL_1D,
    IndicatorFeatureDXY_1D, IndicatorFeatureTNX_1D, IndicatorFeatureTIP_1D,
    IndicatorFeatureCLF_1D, IndicatorFeatureVIX_1D, IndicatorFeatureGSPC_1D
)

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

correlated_symbols = [
    "GCF", "IAU", "SIF", "PPLT", "PALL",
    "DXY", "TNX", "TIP", "CLF", "VIX", "GSPC"
]

def get_indicator_model_map(duration: str):
    is_hourly = duration == "1H"
    return {
        "GLD": IndicatorFeatureGLD_1H if is_hourly else IndicatorFeatureGLD_1D,
        "GCF": IndicatorFeatureGCF_1H if is_hourly else IndicatorFeatureGCF_1D,
        "IAU": IndicatorFeatureIAU_1H if is_hourly else IndicatorFeatureIAU_1D,
        "SIF": IndicatorFeatureSIF_1H if is_hourly else IndicatorFeatureSIF_1D,
        "PPLT": IndicatorFeaturePPLT_1H if is_hourly else IndicatorFeaturePPLT_1D,
        "PALL": IndicatorFeaturePALL_1H if is_hourly else IndicatorFeaturePALL_1D,
        "DXY": IndicatorFeatureDXY_1H if is_hourly else IndicatorFeatureDXY_1D,
        "TNX": IndicatorFeatureTNX_1H if is_hourly else IndicatorFeatureTNX_1D,
        "TIP": IndicatorFeatureTIP_1H if is_hourly else IndicatorFeatureTIP_1D,
        "CLF": IndicatorFeatureCLF_1H if is_hourly else IndicatorFeatureCLF_1D,
        "VIX": IndicatorFeatureVIX_1H if is_hourly else IndicatorFeatureVIX_1D,
        "GSPC": IndicatorFeatureGSPC_1H if is_hourly else IndicatorFeatureGSPC_1D,
    }

def fetch_historical_indicators(session: Session, model, dt_obj: datetime.datetime, history: int, duration: str):
    if duration == "1H":
        start_dt = dt_obj - datetime.timedelta(hours=history - 1)
        rows = session.query(model).filter(
            and_(model.timestamp >= start_dt, model.timestamp <= dt_obj)
        ).all()
        by_time = {}
        for row in rows:
            key = row.timestamp.strftime("%Y-%m-%d %H:%M")
            if key not in by_time:
                by_time[key] = {"price": row.price}
            by_time[key][row.indicator] = row.value
    else:
        start_date = dt_obj.date() - datetime.timedelta(days=history - 1)
        rows = session.query(model).filter(
            and_(model.date >= start_date, model.date <= dt_obj.date())
        ).all()
        by_time = {}
        for row in rows:
            key = row.date.isoformat()
            if key not in by_time:
                by_time[key] = {"price": row.price}
            by_time[key][row.indicator] = row.value
    return by_time

async def format_section(symbol: str, history_data: dict) -> str:
    lines = [f"### {symbol}"]
    for time_key in sorted(history_data.keys()):
        data = history_data[time_key]
        price = data.get("price", "N/A")
        lines.append(f"{time_key}  |  Price: {round(price, 2) if price else 'N/A'}")
        for k, v in sorted(data.items()):
            if k == "price":
                continue
            lines.append(f"  - {k}: {round(v, 2)}")
        lines.append("")
    return "\n".join(lines)

async def generate_prompt(target_symbol: str, date: str, duration: str = "1D", history: int = 3):
    session = SessionLocal()
    prompt = []
    model_map = get_indicator_model_map(duration)
    is_hourly = duration == "1H"
    dt_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") if is_hourly else datetime.datetime.strptime(date, "%Y-%m-%d")

    news = get_latest_news_titles_and_summaries()

    try:
        prompt.append(
            f"You are a professional financial market analyst specializing in the {target_symbol} symbol in trading.\n"
            f"The following is {duration} candle-based indicator data for the past {history} days up to {date} which is today, for {target_symbol} and correlated macro assets.\n\n"
            "If you mention any technical indicator, use its entire name. "
            "If you mention any symbols, use their full names (e.g., 'SPDR Gold Shares ETF' for GLD).\n"
            "Please mention indicators like RSI, MACD, or Bollinger Bands always linking them to specific price levels.\n"
            "Always express confirmation/invalidation as actual price triggers (e.g., 'MACD bullish crossover confirmed if price > $308.40').\n"
            "I don't have a chart or technical indicator graph — I rely entirely on precise numbers and indicator values, including their time frames.\n"
            f"For your analysis, you must consider the effect of these news articles (on top of the technical indicators) to the {target_symbol}: {news}\n\n"
            "Your task is to analyze the data:\n"
            "**Return ONLY valid JSON. No markdown, no explanation. Structure it exactly like this:**\n"
            "{\n"
            "  \"directional_bias\": \"...\",\n"
            "  \"key_drivers\": \"...\",\n"
            "  \"macro_alignment\": \"...\",\n"
            "  \"risk_signals\": \"...\",\n"
            "  \"today_outlook\": \"...\",\n"
            "  \"today_entry_price\": \"...\",\n"
            "  \"today_target_price\": \"...\",\n"
            "  \"today_stop_loss\": \"...\",\n"
            "  \"today_confidence_level\": \"...\",\n"
            "  \"today_confidence_score\": ...,\n"
            "  \"today_confirmation_trigger\": \"...\",\n"
            "  \"today_invalidation_level\": \"...\",\n"
            "  \"today_trade_signal\": \"...\",\n"
            "  \"short_term_outlook\": \"...\",\n"
            "  \"short_term_entry_price\": \"...\",\n"
            "  \"short_term_target_price\": \"...\",\n"
            "  \"short_term_stop_loss\": \"...\",\n"
            "  \"short_term_confidence_level\": \"...\",\n"
            "  \"short_term_confidence_score\": ...,\n"
            "  \"short_term_confirmation_trigger\": \"...\",\n"
            "  \"short_term_invalidation_level\": \"...\",\n"
            "  \"short_term_trade_signal\": \"...\",\n"
            "  \"summary\": \"...\",\n"
            "  \"detail_summary\": \"...\"\n"
            "}\n\n"
        )

        target_model = model_map[target_symbol]
        target_data = fetch_historical_indicators(session, target_model, dt_obj, history, duration)
        prompt.append(await format_section(target_symbol, target_data))

        for symbol in correlated_symbols:
            model = model_map[symbol]
            symbol_data = fetch_historical_indicators(session, model, dt_obj, history, duration)
            prompt.append(await format_section(symbol, symbol_data))

        full_prompt = "\n\n".join(prompt)
        ai_response = await get_gold_analysis_from_deepseek(full_prompt)

        save_analysis(
            response=ai_response,
            symbol=target_symbol,
            dt=dt_obj,
            db=session,
            duration=duration
        )

    finally:
        session.close()

async def get_gold_analysis_from_deepseek(prompt: str) -> AiResponse:
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=1.5,
            stream=False
        )
        raw = response.choices[0].message.content
        print("🔍 Raw output from DeepSeek:\n", raw)

        parsed = json.loads(raw)

        required_keys = [
            "directional_bias", "key_drivers", "macro_alignment", "risk_signals",
            "today_outlook", "today_entry_price", "today_target_price", "today_stop_loss",
            "today_confidence_level", "today_confidence_score", "today_confirmation_trigger",
            "today_invalidation_level", "today_trade_signal",
            "short_term_outlook", "short_term_entry_price", "short_term_target_price", "short_term_stop_loss",
            "short_term_confidence_level", "short_term_confidence_score", "short_term_confirmation_trigger",
            "short_term_invalidation_level", "short_term_trade_signal",
            "summary", "detail_summary"
        ]
        missing = [k for k in required_keys if k not in parsed]
        if missing:
            raise ValueError(f"Missing keys in DeepSeek response: {missing}")

        def parse_price(val: Any, field: str) -> float:
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, str):
                cleaned = re.sub(r"[^\d.]", "", val)
                if not cleaned:
                    raise ValueError(f"Invalid price in {field}: {val}")
                return float(cleaned)
            raise TypeError(f"Invalid type for {field}: {type(val)}")

        return AiResponse(
            directional_bias=parsed["directional_bias"],
            key_drivers=parsed["key_drivers"],
            macro_alignment=parsed["macro_alignment"],
            risk_signals=parsed["risk_signals"],

            today_outlook=parsed["today_outlook"],
            today_entry_price=parse_price(parsed["today_entry_price"], "today_entry_price"),
            today_target_price=parse_price(parsed["today_target_price"], "today_target_price"),
            today_stop_loss=parse_price(parsed["today_stop_loss"], "today_stop_loss"),
            today_confidence_level=parsed["today_confidence_level"],
            today_confidence_score=int(parsed["today_confidence_score"]),
            today_confirmation_trigger=parsed["today_confirmation_trigger"],
            today_invalidation_level=parsed["today_invalidation_level"],
            today_trade_signal=parsed["today_trade_signal"],

            short_term_outlook=parsed["short_term_outlook"],
            short_term_entry_price=parse_price(parsed["short_term_entry_price"], "short_term_entry_price"),
            short_term_target_price=parse_price(parsed["short_term_target_price"], "short_term_target_price"),
            short_term_stop_loss=parse_price(parsed["short_term_stop_loss"], "short_term_stop_loss"),
            short_term_confidence_level=parsed["short_term_confidence_level"],
            short_term_confidence_score=int(parsed["short_term_confidence_score"]),
            short_term_confirmation_trigger=parsed["short_term_confirmation_trigger"],
            short_term_invalidation_level=parsed["short_term_invalidation_level"],
            short_term_trade_signal=parsed["short_term_trade_signal"],

            summary=parsed["summary"],
            detail_summary=parsed["detail_summary"]
        )

    except Exception as e:
        raise RuntimeError(f"❌ DeepSeek response error: {e}")

def save_analysis(response: AiResponse, symbol: str, dt: datetime.datetime, db: Session, duration: str):
    model = AiAnalysis1H if duration == "1H" else AiAnalysis1D
    insert_time = dt.replace(minute=0, second=0, microsecond=0) if duration == "1H" else dt.date()

    stmt = insert(model).values(
        date=insert_time,
        symbol=symbol,
        directional_bias=response.directional_bias,
        key_drivers=response.key_drivers,
        macro_alignment=response.macro_alignment,
        risk_signals=response.risk_signals,

        today_outlook=response.today_outlook,
        today_entry_price=response.today_entry_price,
        today_target_price=response.today_target_price,
        today_stop_loss=response.today_stop_loss,
        today_confidence_level=response.today_confidence_level,
        today_confidence_score=response.today_confidence_score,
        today_confirmation_trigger=response.today_confirmation_trigger,
        today_invalidation_level=response.today_invalidation_level,
        today_trade_signal=response.today_trade_signal,

        short_term_outlook=response.short_term_outlook,
        short_term_entry_price=response.short_term_entry_price,
        short_term_target_price=response.short_term_target_price,
        short_term_stop_loss=response.short_term_stop_loss,
        short_term_confidence_level=response.short_term_confidence_level,
        short_term_confidence_score=response.short_term_confidence_score,
        short_term_confirmation_trigger=response.short_term_confirmation_trigger,
        short_term_invalidation_level=response.short_term_invalidation_level,
        short_term_trade_signal=response.short_term_trade_signal,

        summary=response.summary,
        detail_summary=response.detail_summary
    ).on_conflict_do_update(
        index_elements=["date", "symbol"],
        set_={
            "directional_bias": response.directional_bias,
            "key_drivers": response.key_drivers,
            "macro_alignment": response.macro_alignment,
            "risk_signals": response.risk_signals,

            "today_outlook": response.today_outlook,
            "today_entry_price": response.today_entry_price,
            "today_target_price": response.today_target_price,
            "today_stop_loss": response.today_stop_loss,
            "today_confidence_level": response.today_confidence_level,
            "today_confidence_score": response.today_confidence_score,
            "today_confirmation_trigger": response.today_confirmation_trigger,
            "today_invalidation_level": response.today_invalidation_level,
            "today_trade_signal": response.today_trade_signal,

            "short_term_outlook": response.short_term_outlook,
            "short_term_entry_price": response.short_term_entry_price,
            "short_term_target_price": response.short_term_target_price,
            "short_term_stop_loss": response.short_term_stop_loss,
            "short_term_confidence_level": response.short_term_confidence_level,
            "short_term_confidence_score": response.short_term_confidence_score,
            "short_term_confirmation_trigger": response.short_term_confirmation_trigger,
            "short_term_invalidation_level": response.short_term_invalidation_level,
            "short_term_trade_signal": response.short_term_trade_signal,

            "summary": response.summary,
            "detail_summary": response.detail_summary
        }
    )
    db.execute(stmt)
    db.commit()

# Example: for hourly
# asyncio.run(generate_prompt("GLD", "2025-07-19 09:00", "1H", 3))
# Example: for daily
asyncio.run(generate_prompt("GLD", "2025-07-26", "1D", 14))
