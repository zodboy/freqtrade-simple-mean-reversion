# Simple Mean Reversion

A minimal, self-contained [Freqtrade](https://www.freqtrade.io/) strategy that buys oversold conditions using Bollinger Bands and RSI.

## Strategy Logic

```
Entry:  Price < Lower Bollinger Band(20, 2σ)  AND  RSI(14) < 35
Exit:   ROI table (5% → 3% → 1% → -1%)  OR  Stop Loss (-15%)
```

The strategy captures **mean reversion** — when price deviates 2 standard deviations below its 20-period moving average *and* RSI confirms oversold (<35), we enter long expecting price to bounce back toward the mean.

## Why This Strategy?

| Criteria | Status |
|----------|--------|
| **Simple** | 2 indicators, 2 conditions, no external deps |
| **Self-contained** | Single file, just Freqtrade + Pandas |
| **Long-only** | No shorting complexity |
| **All market states** | Works in bull, range, and bear (with wider stops) |
| **Low drawdown** | 15% hard stop prevents catastrophic loss |

## Quick Start

### 1. Install Freqtrade

```bash
pip install freqtrade
```

### 2. Clone the repo

```bash
git clone https://github.com/zodboy/freqtrade-simple-mean-reversion.git
cd freqtrade-simple-mean-reversion
```

### 3. Configure

```bash
cp config.example.json config.json
```

Edit `config.json`:
- Set your `exchange.name` (binance, okx, gateio, etc.)
- Set your `exchange.key` and `exchange.secret`
- Set `pair_whitelist` to the pairs you want to trade
- Set `stake_amount` or `tradable_balance_ratio`

### 4. Run

```bash
# Dry-run (paper trading)
freqtrade trade --config config.json --strategy SimpleMeanReversion
```

### 5. Backtest

```bash
freqtrade backtesting --config config.json --strategy SimpleMeanReversion --timerange 20240101-
```

## Recommended Pairs

Liquid pairs with enough volatility for mean reversion to matter:

```
BTC/USDT, ETH/USDT, SOL/USDT, DOGE/USDT, XRP/USDT
```

## Risk Management

- **Stake per trade**: 5-10% of wallet (`tradable_balance_ratio`)
- **Max open trades**: 3 (`max_open_trades`)
- **Stop loss**: -15% (adjust based on your risk tolerance)
- **Leverage**: 1x only (no leverage)

## Indicator Details

### Bollinger Bands (20, 2σ)
Approximately 95% of price action falls within the bands. Price below lower band → statistically "cheap."

### RSI (14)
Wilder's smoothing. Values < 30 → oversold. We use < 35 for slightly earlier entry to avoid missing bounces.

### Why 20/14?
Standard parameters from John Bollinger and Welles Wilder — no optimization needed, work across all liquid markets.

## Limitations

- **No exit signal**: Relies entirely on ROI + stoploss. Trades may stay open for days.
- **Whipsaw risk**: In strong downtrends, price can keep falling below the band.
- **Not for 1m/5m**: This is an hourly strategy. Lower timeframes have too much noise.

## License

MIT

## Author

[zodboy](https://github.com/zodboy) — zodboy1024@gmail.com