import sys
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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    news=get_latest_news_titles_and_summaries()

    try:
        prompt.append(
            f"You are a professional financial market analyst specializing in {target_symbol} (SPDR Gold Shares ETF), not gold futures or spot gold.\n"
            f"The following is {duration} candle-based indicator data for the past {history} days up to {date} for {target_symbol} and correlated macro assets.\n\n"
            "If you mention any technical indicator, use its entire name. "
            "If you mention any symbols, use their full names (e.g., 'SPDR Gold Shares ETF' for GLD).\n"
            "Please mention indicators like RSI, MACD, or Bollinger Bands always linking them to specific price levels.\n"
            "Always express confirmation/invalidation as actual price triggers (e.g., 'MACD bullish crossover confirmed if price > $308.40').\n"
            "I don't have a chart neither technical indicators graph — I rely entirely on precise numbers and the technical indicators, including their and time frames.\n"
            "Your task is to analyze the data:\n"
            "**Return ONLY valid JSON. No markdown, no explanation. Structure it exactly like this:**\n"
            f"For your analysis, must consider the effect of these news articles (on top of the technical) to the {target_symbol}: {news}"
            "{\n"
            "  \"directional_bias\": \"bullish | bearish | neutral — and why\",\n"
            "  \"key_drivers\": \"top indicators or price signals, with details explaining their significance\",\n"
            "  \"macro_alignment\": \"supportive | conflicting | mixed — must include with details explaining why it is so\",\n"
            "  \"risk_signals\": \"any red flags (e.g. volatility, overbought RSI) with details explaining why it is so\",\n"
            "  \"short_term_outlook\": \"expected price action or range over 7–14 days\",\n"
            "  \"entry_price\": \"recommended entry point {target_symbol} level for today or tomorrow if any)\",\n"
            "  \"target_price\": \"expected price target within for today or tomorrow if any\",\n"
            "  \"stop_loss\": \"price level to exit if trade fails\",\n"
            "  \"confidence_level\": \"low | medium | high\",\n"
            "  \"confidence_score\": number between 0 and 100,\n"
            "  \"confirmation_trigger\": \"signal that validates the trade setup within 1-2 days or longer period, explain in details with price level and the exact time frame estimation\",\n"
            "  \"invalidation_level\": \"signal or price level that invalidates setup within 1-2 days or longer period, explain in details with price level and the exact time frame estimation\",\n"
            "  \"buy/sell/hold\": \"buy | sell | hold\",\n"
            "  \"summary\": \"a concise summary of your analysis about the price trend, level etc, in simple language without the technical analysis, indicators, or news articles\"\n"
            "  \"detail_summary\": \"a concise detail summary of your analysis in with more technical information and news articles.\"\n"
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
            "short_term_outlook", "entry_price", "target_price", "stop_loss",
            "confidence_level", "confidence_score", "confirmation_trigger",
            "invalidation_level", "buy/sell/hold", "summary", "detail_summary"
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
            short_term_outlook=parsed["short_term_outlook"],
            entry_price=parse_price(parsed["entry_price"], "entry_price"),
            target_price=parse_price(parsed["target_price"], "target_price"),
            stop_loss=parse_price(parsed["stop_loss"], "stop_loss"),
            confidence_level=parsed["confidence_level"],
            confidence_score=int(parsed["confidence_score"]),
            confirmation_trigger=parsed["confirmation_trigger"],
            invalidation_level=parsed["invalidation_level"],
            trade_signal=parsed["buy/sell/hold"],
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
        short_term_outlook=response.short_term_outlook,
        entry_price=response.entry_price,
        target_price=response.target_price,
        stop_loss=response.stop_loss,
        confidence_level=response.confidence_level,
        confidence_score=response.confidence_score,
        confirmation_trigger=response.confirmation_trigger,
        invalidation_level=response.invalidation_level,
        trade_signal=response.trade_signal,
        summary=response.summary,
        detail_summary=response.detail_summary
    ).on_conflict_do_update(
        index_elements=["date", "symbol"],
        set_={ 
            "directional_bias": response.directional_bias,
            "key_drivers": response.key_drivers,
            "macro_alignment": response.macro_alignment,
            "risk_signals": response.risk_signals,
            "short_term_outlook": response.short_term_outlook,
            "entry_price": response.entry_price,
            "target_price": response.target_price,
            "stop_loss": response.stop_loss,
            "confidence_level": response.confidence_level,
            "confidence_score": response.confidence_score,
            "confirmation_trigger": response.confirmation_trigger,
            "invalidation_level": response.invalidation_level,
            "trade_signal": response.trade_signal,
            "summary": response.summary,
            "detail_summary": response.detail_summary
        }
    )
    db.execute(stmt)
    db.commit()

if __name__ == "__main__":
    # Example: for hourly
    # asyncio.run(generate_prompt("GLD", "2025-07-19 09:00", "1H", 3))
    # Example: for daily
    asyncio.run(generate_prompt("GLD", "2025-07-19", "1D", 14))
