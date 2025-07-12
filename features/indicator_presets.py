import pandas as pd

from features.adx import add_adx
from features.atr import add_atr
from features.bollinger_bands import add_bollinger_bands
from features.cci import add_cci
from features.candle_patterns import add_candle_patterns
from features.daily_return import add_daily_return
from features.ema import add_ema
from features.macd import add_macd
from features.momentum import add_momentum
from features.obv import add_obv
from features.previous_ohlc import add_previous_ohlc
from features.roc import add_roc
from features.rsi import add_rsi
from features.sma import add_sma
from features.stochastic import add_stochastic
from features.support_resistance import add_support_resistance
from features.volatility import add_volatility
from features.volume_ma import add_volume_ma
from features.volatility_breakout import add_volatility_breakout

def get_preset_parameters(preset: str) -> dict:
    """
    Return a dict of indicator parameters based on timeframe preset.
    """
    if preset == 'daily':
        return dict(
            adx_period=14, atr_period=14,
            bollinger_window=20, bollinger_std=2.0,
            cci_period=20,
            doji_threshold=0.1, hammer_body_threshold=0.3, hammer_shadow_multiplier=2.0,
            return_period=1,
            ema_windows=[10, 20, 50], macd_fast=12, macd_slow=26, macd_signal=9,
            momentum_period=10, roc_period=10, rsi_period=14,
            sma_windows=[20, 50, 200], stochastic_k=14, stochastic_d=3,
            support_resistance_window=20, volatility_window=10,
            volume_ma_windows=[20, 50], vol_breakout_window=20
        )
    # elif preset == '1H':
    #     return dict(
    #         adx_period=14, atr_period=14,
    #         bollinger_window=20, bollinger_std=2.0,
    #         cci_period=20,
    #         doji_threshold=0.1, hammer_body_threshold=0.3, hammer_shadow_multiplier=2.0,
    #         return_period=1,
    #         ema_windows=[10, 30, 60], macd_fast=8, macd_slow=21, macd_signal=5,
    #         momentum_period=6, roc_period=6, rsi_period=14,
    #         sma_windows=[10, 30, 60], stochastic_k=14, stochastic_d=3,
    #         support_resistance_window=12, volatility_window=14,
    #         volume_ma_windows=[10, 30], vol_breakout_window=14
    #     )
    # elif preset == '4h':
    #     return dict(
    #         adx_period=14, atr_period=14,
    #         bollinger_window=20, bollinger_std=2.0,
    #         cci_period=20,
    #         doji_threshold=0.1, hammer_body_threshold=0.3, hammer_shadow_multiplier=2.0,
    #         return_period=1,
    #         ema_windows=[20, 60, 100], macd_fast=12, macd_slow=26, macd_signal=9,
    #         momentum_period=8, roc_period=8, rsi_period=14,
    #         sma_windows=[20, 60, 100], stochastic_k=14, stochastic_d=3,
    #         support_resistance_window=20, volatility_window=14,
    #         volume_ma_windows=[20, 50], vol_breakout_window=14
    #     )
    # elif preset == 'weekly':
    #     return dict(
    #         adx_period=10, atr_period=10,
    #         bollinger_window=20, bollinger_std=2.0,
    #         cci_period=10,
    #         doji_threshold=0.1, hammer_body_threshold=0.3, hammer_shadow_multiplier=2.0,
    #         return_period=1,
    #         ema_windows=[4, 12, 26], macd_fast=5, macd_slow=13, macd_signal=9,
    #         momentum_period=4, roc_period=4, rsi_period=14,
    #         sma_windows=[4, 12, 52], stochastic_k=10, stochastic_d=3,
    #         support_resistance_window=4, volatility_window=10,
    #         volume_ma_windows=[4, 12], vol_breakout_window=10
    #     )
    else:
        raise ValueError(f"Unknown preset: {preset}")

def apply_all_indicators(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    """Apply all features to df based on preset parameters."""
    p = get_preset_parameters(preset)

    df = add_adx(df, period=p['adx_period'])
    df = add_atr(df, period=p['atr_period'])
    df = add_bollinger_bands(df, window=p['bollinger_window'], num_std=p['bollinger_std'])
    df = add_cci(df, period=p['cci_period'])
    df = add_candle_patterns(
        df,
        doji_threshold=p['doji_threshold'],
        hammer_body_threshold=p['hammer_body_threshold'],
        hammer_shadow_multiplier=p['hammer_shadow_multiplier']
    )
    df = add_daily_return(df, period=p['return_period'])
    df = add_ema(df, windows=p['ema_windows'])
    df = add_macd(
        df,
        fast_period=p['macd_fast'],
        slow_period=p['macd_slow'],
        signal_period=p['macd_signal']
    )
    df = add_momentum(df, period=p['momentum_period'])
    df = add_obv(df)
    df = add_previous_ohlc(df, period=1)
    df = add_roc(df, period=p['roc_period'])
    df = add_rsi(df, window=p['rsi_period'])
    df = add_sma(df, windows=p['sma_windows'])
    df = add_stochastic(df, k_period=p['stochastic_k'], d_period=p['stochastic_d'])
    df = add_support_resistance(df, window=p['support_resistance_window'])
    df = add_volatility(df, window=p['volatility_window'])
    df = add_volume_ma(df, windows=p['volume_ma_windows'])
    df = add_volatility_breakout(df, atr_period=p['vol_breakout_window'], multiplier=1.5)

    return df
