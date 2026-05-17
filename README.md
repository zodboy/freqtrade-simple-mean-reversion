<div align="center">

<img src="https://img.shields.io/badge/Freqtrade-2026.4-blue?style=flat-square&logo=python" alt="Freqtrade">
<img src="https://img.shields.io/badge/Timeframe-1h-green?style=flat-square" alt="1h">
<img src="https://img.shields.io/badge/Type-Mean%20Reversion-orange?style=flat-square" alt="Mean Reversion">
<img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="MIT">

</div>

---

# 📉 Simple Mean Reversion

> A minimal, self-contained [Freqtrade](https://www.freqtrade.io/) strategy that captures mean reversion using Bollinger Bands and RSI.

---

## 🎯 Strategy at a Glance

```
 ENTRY:  Price < Lower Bollinger Band (20, 2σ)  ⋂  RSI(14) < 35

  EXIT:  ROI table (5% → 3% → 1% → −1%)   OR   Stop Loss (−15%)
```

When price falls **2 standard deviations below its 20-period mean** *and* RSI confirms oversold, we enter long. Price tends to revert — that's the edge.

---

## ✨ Why This Strategy?

| | |
|---|---|
| 🧩 **2 indicators** | Bollinger Bands + RSI. No black magic. |
| 📦 **Single file** | Zero external dependencies beyond Freqtrade & Pandas. |
| 📈 **Long-only** | No shorting. Simpler psychology, simpler execution. |
| 🛡️ **15% hard stop** | Prevents catastrophic slides in trend days. |
| ⚙️ **No optimization** | Uses Bollinger's & Wilder's original parameters (20/14). |

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/zodboy/freqtrade-simple-mean-reversion.git
cd freqtrade-simple-mean-reversion

# 2. Install Freqtrade
pip install freqtrade

# 3. Configure
cp config.example.json config.json
# → Edit config.json: set exchange, pairs, stake amount

# 4. Dry-run (paper trade)
freqtrade trade --config config.json --strategy SimpleMeanReversion

# 5. Backtest
freqtrade backtesting --config config.json --strategy SimpleMeanReversion --timerange 20240101-
```

---

## 📊 Indicator Breakdown

### Bollinger Bands `(20, 2σ)`

| Band | Formula | Meaning |
|------|---------|---------|
| Mid | 20-period SMA | Local "fair value" |
| Lower | Mid − 2σ | ∼2.5th percentile — cheap |
| Upper | Mid + 2σ | ∼97.5th percentile — expensive |

95% of price action lives inside the bands. A close below the lower band is statistically rare and often mean-reverts.

### RSI `(14, Wilder)`

| Zone | RSI | Action |
|------|-----|--------|
| Oversold | < 30 | Potential bounce |
| Neutral | 30–70 | No edge |
| Overbought | > 70 | Potential pullback |

We enter at **< 35** (not 30) — slightly early, to catch bounces before the crowd.

---

## 💰 Recommended Setup

| Setting | Value | Why |
|---------|-------|-----|
| **Pairs** | BTC, ETH, SOL, DOGE, XRP | Liquid, volatile enough |
| **Stake/trade** | 5–10% of wallet | Diversify across max 3 trades |
| **Timeframe** | 1h | Sweet spot: enough signal, not too noisy |
| **Leverage** | 1× | This is a spot strategy |

```json
// In config.json:
{
    "max_open_trades": 3,
    "tradable_balance_ratio": 0.99,
    "stake_amount": "unlimited"
}
```

---

## ⚠️ Limitations

- **Trending markets**: Price can "walk the band" in strong downtrends. The −15% stoploss is your safety net.
- **No exit signal**: Exits rely entirely on ROI + stoploss. Trades may sit for hours or days.
- **1h only**: Tested on hourly candles. 1m/5m has too much noise for this logic.
- **Crypto-focused**: Generalizes to any liquid market, but backtest your own data.

---

## 🗺️ Roadmap

- [ ] Add volume filter (avoid low-liquidity entries)
- [ ] Add trailing stop after +3%
- [ ] Daily trend filter (don't fight the trend)
- [ ] Multi-timeframe confirmation

---

## 📄 License

MIT — do whatever you want. A star ⭐ is appreciated if you find it useful.

---

<div align="center">

Made with ☕ by **[zodboy](https://github.com/zodboy)** · zodboy1024@gmail.com

</div>