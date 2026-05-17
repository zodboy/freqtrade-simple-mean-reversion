"""
SimpleMeanReversion - A minimal Bollinger Band + RSI mean reversion strategy for Freqtrade.

Strategy Logic
==============
Entry (Long):
  - Price closes below the lower Bollinger Band (20-period, 2 standard deviations)
  - RSI(14) falls below 35
  → Both conditions indicate an oversold state likely to revert.

Exit:
  - Default: Hold until price reverts (no exit signal)
  - ROI: Take profit at +5%, time-decay to -1% after 48 hours
  - Stoploss: -15% hard stop

Parameters are deliberately simple. This is a "weak but steady" baseline
that should produce positive expectancy in most market conditions with
proper position sizing and risk management.

Author: zodboy (zodboy1024@gmail.com)
License: MIT
"""

from freqtrade.strategy import IStrategy
from pandas import DataFrame
import pandas as pd


class SimpleMeanReversion(IStrategy):
    INTERFACE_VERSION = 3

    # ── Timeframe ──────────────────────────────────────────────
    timeframe = "1h"

    # ── Long only ──────────────────────────────────────────────
    can_short = False

    # ── Minimal ROI table ──────────────────────────────────────
    # Sell immediately at +5%, decay to -1% after 48 hours
    # (forces exit even if reversion hasn't happened)
    minimal_roi = {
        "0":    0.05,   # 5% instant profit
        "720":  0.03,   # 3% after 30 days
        "1440": 0.01,   # 1% after 60 days
        "2880": -0.01,  # exit at -1% after 120 days
    }

    # ── Stop Loss ──────────────────────────────────────────────
    stoploss = -0.15

    # ── Trailing Stop (disabled by default) ────────────────────
    trailing_stop = False

    # ── Order Types ────────────────────────────────────────────
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # ── Startup candles for indicator warmup ───────────────────
    # Bollinger Band(20) + RSI(14) + std(20) = ~100 candles minimum
    startup_candle_count = 150

    # ── Position Management ────────────────────────────────────
    process_only_new_candles = True
    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # ── Max number of concurrent trades ────────────────────────
    max_open_trades = 3

    # ═══════════════════════════════════════════════════════════
    # Indicator calculation
    # ═══════════════════════════════════════════════════════════

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate Bollinger Bands and RSI.
        """
        close = dataframe["close"]

        # Bollinger Bands: 20-period, 2 standard deviations
        bb_mid = close.rolling(window=20).mean()
        bb_std = close.rolling(window=20).std()
        dataframe["bb_lower"] = bb_mid - 2.0 * bb_std
        dataframe["bb_mid"] = bb_mid
        dataframe["bb_upper"] = bb_mid + 2.0 * bb_std

        # RSI(14) - Wilder's smoothing
        dataframe["rsi"] = self._rsi(close, period=14)

        return dataframe

    # ═══════════════════════════════════════════════════════════
    # Entry signal
    # ═══════════════════════════════════════════════════════════

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Enter long when price is below the lower Bollinger Band AND RSI is oversold.
        """
        dataframe.loc[
            (
                (dataframe["close"] < dataframe["bb_lower"])
                & (dataframe["rsi"] < 35)
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "mean_reversion_entry")

        return dataframe

    # ═══════════════════════════════════════════════════════════
    # Exit signals (none - rely on ROI + stoploss)
    # ═══════════════════════════════════════════════════════════

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        No exit signal. Exits are handled by ROI table and stoploss.
        """
        return dataframe

    # ═══════════════════════════════════════════════════════════
    # Leverage (1x for spot or low-leverage futures)
    # ═══════════════════════════════════════════════════════════

    def leverage(
        self,
        pair: str,
        current_time,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag: str,
        side: str,
        **kwargs,
    ) -> float:
        return 1.0

    # ═══════════════════════════════════════════════════════════
    # Helper: RSI calculation (Wilder's smoothing)
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        return 100.0 - (100.0 / (1.0 + rs))