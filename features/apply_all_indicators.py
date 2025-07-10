import pandas as pd

# Import indicator functions (assumed to be in the same folder or as a module)
from features.sma import add_sma
from features.ema import add_ema
from features.macd import add_macd
from features.rsi import add_rsi
from features.roc import add_roc
from features.momentum import add_momentum

from features.bollinger_bands import add_bollinger_bands
from features.atr import add_atr
from features.volatility import add_volatility

from features.obv import add_obv
from features.volume_ma import add_volume_ma

from features.previous_ohlc import add_previous_ohlc
from features.candle_patterns import add_candle_patterns

from features.daily_return import add_daily_return
from features.volatility_breakout import add_volatility_breakout
from features.support_resistance import add_support_resistance

from features.adx import add_adx
from features.cci import add_cci
from features.stochastic import add_stochastic

def get_preset_parameters(preset):
    if preset == 'daily':
        return {
            'sma_windows': [20, 50, 200],
            'ema_windows': [20, 50, 100],
            'macd_params': (12, 26, 9),
            'rsi_window': 14,
            'roc_period': 12,
            'momentum_period': 10,
            'bollinger_window': 20,
            'bollinger_std': 2.0,
            'atr_period': 14,
            'volatility_window': 14,
            'volume_ma_windows': [20, 50],
            'breakout_atr_period': 14,
            'breakout_multiplier': 1.5,
            'support_resistance_window': 20,
            'adx_period': 14,
            'cci_period': 20,
            'stochastic_k': 14,
            'stochastic_d': 3,
            'return_period': 1,
            'prev_ohlc_period': 1,
            'doji_threshold': 0.1,
            'hammer_body_threshold': 0.3,
            'hammer_shadow_multiplier': 2.0
        }
    elif preset == 'hourly':
        return {
            'sma_windows': [10, 30, 60],
            'ema_windows': [10, 30, 60],
            'macd_params': (8, 21, 5),
            'rsi_window': 14,
            'roc_period': 6,
            'momentum_period': 6,
            'bollinger_window': 20,
            'bollinger_std': 2.0,
            'atr_period': 14,
            'volatility_window': 14,
            'volume_ma_windows': [10, 30],
            'breakout_atr_period': 14,
            'breakout_multiplier': 1.5,
            'support_resistance_window': 12,
            'adx_period': 14,
            'cci_period': 20,
            'stochastic_k': 14,
            'stochastic_d': 3,
            'return_period': 1,
            'prev_ohlc_period': 1,
            'doji_threshold': 0.1,
            'hammer_body_threshold': 0.3,
            'hammer_shadow_multiplier': 2.0
        }
    elif preset == '4h':
        return {
            'sma_windows': [20, 60, 100],
            'ema_windows': [20, 60, 100],
            'macd_params': (12, 26, 9),
            'rsi_window': 14,
            'roc_period': 8,
            'momentum_period': 8,
            'bollinger_window': 20,
            'bollinger_std': 2.0,
            'atr_period': 14,
            'volatility_window': 14,
            'volume_ma_windows': [20, 50],
            'breakout_atr_period': 14,
            'breakout_multiplier': 1.5,
            'support_resistance_window': 20,
            'adx_period': 14,
            'cci_period': 20,
            'stochastic_k': 14,
            'stochastic_d': 3,
            'return_period': 1,
            'prev_ohlc_period': 1,
            'doji_threshold': 0.1,
            'hammer_body_threshold': 0.3,
            'hammer_shadow_multiplier': 2.0
        }
    elif preset == 'weekly':
        return {
            'sma_windows': [4, 12, 52],
            'ema_windows': [4, 12, 26],
            'macd_params': (5, 13, 9),
            'rsi_window': 14,
            'roc_period': 4,
            'momentum_period': 4,
            'bollinger_window': 20,
            'bollinger_std': 2.0,
            'atr_period': 10,
            'volatility_window': 10,
            'volume_ma_windows': [4, 12],
            'breakout_atr_period': 10,
            'breakout_multiplier': 1.5,
            'support_resistance_window': 4,
            'adx_period': 10,
            'cci_period': 10,
            'stochastic_k': 10,
            'stochastic_d': 3,
            'return_period': 1,
            'prev_ohlc_period': 1,
            'doji_threshold': 0.1,
            'hammer_body_threshold': 0.3,
            'hammer_shadow_multiplier': 2.0
        }
    else:
        raise ValueError("Unsupported preset. Choose from: 'daily', 'hourly', '4h', or 'weekly'.")

def apply_all_indicators(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    """
    Apply all technical indicators to a GLD dataframe using preset configurations.
    """
    params = get_preset_parameters(preset)

    df = add_sma(df, windows=params['sma_windows'])
    df = add_ema(df, windows=params['ema_windows'])
    df = add_macd(df, *params['macd_params'])
    df = add_rsi(df, window=params['rsi_window'])
    df = add_roc(df, period=params['roc_period'])
    df = add_momentum(df, period=params['momentum_period'])

    df = add_bollinger_bands(df, window=params['bollinger_window'], num_std=params['bollinger_std'])
    df = add_atr(df, period=params['atr_period'])
    df = add_volatility(df, window=params['volatility_window'])

    df = add_obv(df)
    df = add_volume_ma(df, windows=params['volume_ma_windows'])

    df = add_previous_ohlc(df, period=params['prev_ohlc_period'])
    df = add_candle_patterns(
        df,
        doji_threshold=params['doji_threshold'],
        hammer_body_threshold=params['hammer_body_threshold'],
        hammer_shadow_multiplier=params['hammer_shadow_multiplier']
    )

    df = add_daily_return(df, period=params['return_period'])
    df = add_volatility_breakout(df, atr_period=params['breakout_atr_period'], multiplier=params['breakout_multiplier'])
    df = add_support_resistance(df, window=params['support_resistance_window'])

    df = add_adx(df, period=params['adx_period'])
    df = add_cci(df, period=params['cci_period'])
    df = add_stochastic(df, k_period=params['stochastic_k'], d_period=params['stochastic_d'])

    return df