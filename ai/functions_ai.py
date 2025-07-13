import sys
import os
from typing import Any
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
import json
import re
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import Date
from openai import AsyncOpenAI
import asyncio

from db.database import SessionLocal
from currencies.models_currencies import Xau, Xag, Xpd, Xpt
from ai.models_ai import AiAnalysis
from ai.schema_ai import AiResponse
from indicators.models_features import (
    IndicatorFeatureGLD, IndicatorFeatureGCF, IndicatorFeatureIAU,
    IndicatorFeatureSIF, IndicatorFeaturePPLT, IndicatorFeaturePALL,
    IndicatorFeatureDXY, IndicatorFeatureTNX, IndicatorFeatureTIP,
    IndicatorFeatureCLF, IndicatorFeatureVIX, IndicatorFeatureGSPC
)

# Load .env
load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

indicator_model_map = {
    "GLD": IndicatorFeatureGLD,
    "GCF": IndicatorFeatureGCF,
    "IAU": IndicatorFeatureIAU,
    "SIF": IndicatorFeatureSIF,
    "PPLT": IndicatorFeaturePPLT,
    "PALL": IndicatorFeaturePALL,
    "DXY": IndicatorFeatureDXY,
    "TNX": IndicatorFeatureTNX,
    "TIP": IndicatorFeatureTIP,
    "CLF": IndicatorFeatureCLF,
    "VIX": IndicatorFeatureVIX,
    "GSPC": IndicatorFeatureGSPC,
}

correlated_symbols = [
    "GCF", "IAU", "SIF", "PPLT", "PALL",
    "DXY", "TNX", "TIP", "CLF", "VIX", "GSPC"
]

def fetch_historical_indicators(session: Session, model, date: datetime.date, history_days: int):
    from sqlalchemy import and_
    start_date = date - datetime.timedelta(days=history_days - 1)

    rows = session.query(model).filter(
        and_(
            model.date >= start_date,
            model.date <= date
        )
    ).all()

    by_date = {}
    for row in rows:
        d = row.date.isoformat()
        if d not in by_date:
            by_date[d] = {"price": row.price}
        by_date[d][row.indicator] = row.value

    return by_date

async def format_section(symbol: str, history_data: dict) -> str:
    lines = [f"### {symbol}"]
    for date_str in sorted(history_data.keys()):
        day = history_data[date_str]
        price = day.get("price", "N/A")
        lines.append(f"{date_str}  |  Price: {round(price, 2) if price else 'N/A'}")
        for k, v in sorted(day.items()):
            if k == "price":
                continue
            lines.append(f"  - {k}: {round(v, 2)}")
        lines.append("")
    return "\n".join(lines)

async def generate_prompt(target_symbol: str, date: str, duration: str = "1D", history_days: int = 3):
    session = SessionLocal()
    prompt = []

    try:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        prompt.append(
            f"You are a professional financial market analyst specializing in GLD (SPDR Gold Shares ETF), not gold futures or spot gold.\n"
            f"The following is {duration} candle-based indicator data for the past {history_days} days up to {parsed_date} for GLD and correlated macro assets.\n\n"
            "If you mention any technical indicator, use its entire name. "
            "Please do NOT mention indicators like RSI, MACD, or Bollinger Bands without linking them to specific price levels.\n"
            "Always express confirmation/invalidation as actual price triggers (e.g., 'MACD bullish crossover confirmed if price > $308.40').\n"
            "I don't have a chart — I rely entirely on precise numbers and the technical indicators.\n"
            "Your task is to analyze the data and return:\n"
            "1. Directional bias (bullish, bearish, neutral)\n"
            "2. Key technical drivers\n"
            "3. Macro confirmations or conflicts\n"
            "4. Risk or volatility warnings\n"
            "5. Short-term outlook (7–14 days)\n"
            "6. Entry price\n"
            "7. Target price\n"
            "8. Stop-loss level\n"
            "9. Confidence level (low, medium, high)\n"
            "10. Confidence score (0–100)\n"
            "11. Confirmation trigger\n"
            "12. Invalidation level\n"
            "13. Simple action signal: buy, sell, or hold\n\n"
            "**Return ONLY valid JSON. No markdown, no explanation. Structure it exactly like this:**\n"
            "{\n"
            "  \"directional_bias\": \"bullish | bearish | neutral — and why\",\n"
            "  \"key_drivers\": \"top indicators or price signals\",\n"
            "  \"macro_alignment\": \"supportive | conflicting | mixed — and why\",\n"
            "  \"risk_signals\": \"any red flags (e.g. volatility, overbought RSI)\",\n"
            "  \"short_term_outlook\": \"expected price action or range over 7–14 days\",\n"
            "  \"entry_price\": \"recommended entry point (GLD level)\",\n"
            "  \"target_price\": \"expected price target within 1–2 weeks\",\n"
            "  \"stop_loss\": \"price level to exit if trade fails\",\n"
            "  \"confidence_level\": \"low | medium | high\",\n"
            "  \"confidence_score\": number between 0 and 100,\n"
            "  \"confirmation_trigger\": \"signal that validates the trade setup\",\n"
            "  \"invalidation_level\": \"signal or price level that invalidates setup\",\n"
            "  \"buy/sell/hold\": \"buy | sell | hold\"\n"
            "}\n\n"
            "Return only valid JSON. Do not include any commentary, heading, explanation, or markdown."
        )

        target_model = indicator_model_map[target_symbol]
        hist_data = fetch_historical_indicators(session, target_model, parsed_date, history_days)
        prompt.append(await format_section(target_symbol, hist_data))

        for symbol in correlated_symbols:
            model = indicator_model_map[symbol]
            hist_data = fetch_historical_indicators(session, model, parsed_date, history_days)
            prompt.append(await format_section(symbol, hist_data))

        full_prompt = "\n\n".join(prompt)
        answer = await get_gold_analysis_from_deepseek(full_prompt)
        saveAnalysis(response=answer, symbol=target_symbol, date=parsed_date, db=session)

        print(json.dumps(answer.model_dump(), indent=2))

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
        raw_output = response.choices[0].message.content
        print("🔍 Raw output from DeepSeek:\n", raw_output)

        parsed_output = json.loads(raw_output)

        required_keys = [
            "directional_bias", "key_drivers", "macro_alignment", "risk_signals",
            "short_term_outlook", "entry_price", "target_price", "stop_loss",
            "confidence_level", "confidence_score", "confirmation_trigger",
            "invalidation_level", "buy/sell/hold"
        ]

        missing = [key for key in required_keys if key not in parsed_output]
        if missing:
            raise ValueError(f"Missing keys in DeepSeek response: {missing}")

        price_fields = ["entry_price", "target_price", "stop_loss"]
        for field in price_fields:
            val = parsed_output[field]
            if not re.search(r"\d", str(val)):
                raise ValueError(f"Field '{field}' must contain numeric value, got: {val}")

        def parse_price(value: Any, field_name: str) -> float:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                cleaned = re.sub(r"[^0-9.]", "", value)
                if not cleaned:
                    raise ValueError(f"Field '{field_name}' contains non-numeric value: '{value}'")
                return float(cleaned)
            raise ValueError(f"Field '{field_name}' has unsupported type: {type(value)}")

        return AiResponse(
            directional_bias=parsed_output["directional_bias"],
            key_drivers=parsed_output["key_drivers"],
            macro_alignment=parsed_output["macro_alignment"],
            risk_signals=parsed_output["risk_signals"],
            short_term_outlook=parsed_output["short_term_outlook"],
            entry_price=parse_price(parsed_output["entry_price"], "entry_price"),
            target_price=parse_price(parsed_output["target_price"], "target_price"),
            stop_loss=parse_price(parsed_output["stop_loss"], "stop_loss"),
            confidence_level=parsed_output["confidence_level"],
            confidence_score=int(parsed_output["confidence_score"]),
            confirmation_trigger=parsed_output["confirmation_trigger"],
            invalidation_level=parsed_output["invalidation_level"],
            trade_signal=parsed_output["buy/sell/hold"]
        )

    except Exception as e:
        print("❌ DeepSeek API call or JSON parsing failed.")
        raise RuntimeError(f"DeepSeek response error: {e}")

def saveAnalysis(response: AiResponse, symbol: str, date: Date, db: Session):
    analysis = AiAnalysis(
        date=date,
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
        trade_signal=response.trade_signal
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

if __name__ == "__main__":
    asyncio.run(generate_prompt(target_symbol="GLD", date="2025-07-07", duration="1D", history_days=7))
