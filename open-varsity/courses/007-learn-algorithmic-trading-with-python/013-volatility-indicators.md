Chapters
Module C · Technical Indicators - Chapter 13
# Volatility Indicators
ATR, Bollinger Bands, Keltner and Donchian channels for range and risk.
NSEMCX
What you'll learn
  * ·ATR & NATR
  * ·Bollinger Bands
  * ·Keltner Channel
  * ·Donchian Channel
  * ·Chandelier Exit
  * ·BB width & %B


We've covered _which way_ the market is going and _how hard_ it's pushing. This chapter is about _how wild_ - **volatility** , the size of price's swings. It's the most underrated family of indicators for beginners, because volatility doesn't tell you direction at all. What it tells you is arguably more important: **how much room to give a trade, where to put your stop, and how big a position you can responsibly take.**
Here's the mindset shift. Two stocks can both be in clean uptrends, but if one swings 1% a day and the other swings 5%, they are completely different risks. Buy the same rupee amount of each and you've quietly taken five times the risk on the second. Volatility tools fix that. They also define **ranges** - the bands price tends to stay inside - so you can spot when it's stretched, and catch the quiet "squeeze" that often comes right before a big move.
Same imports, same care with shapes:

```
from openalgo import api, ta

```

The plain readings (`atr`, `natr`, `bbpercent`, `bbwidth`, `hv`) return a single **Series** ; the channels (`bbands`, `keltner`, `donchian`) return a **tuple of three** (upper, middle, lower); and `chandelier_exit` returns a **tuple of two**.
## ATR: the unit of risk
The **Average True Range (ATR)** is the cornerstone of risk management. It measures the average distance price travels in a single bar - including any overnight gaps - and reports it in the instrument's own units (rupees for a stock, points for a future). If RELIANCE has an ATR of 25, then 25 rupees is a _normal_ day's range; a 25-rupee move is noise, not signal.
That single number quietly powers half of professional trading. The most common use: set your **stop-loss a multiple of ATR away** from entry - far enough that ordinary wiggle won't stop you out, close enough to cap the damage if you're wrong.
`ta.atr(...)` returns a single Series.
EX 1ATR and an ATR-based stopNSEch13/01_atr.py
Copy
```
# ATR: the average distance price travels in a bar -- the building block of risk sizing.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

df["ATR14"] = ta.atr(df["high"], df["low"], df["close"], 14)
price = df["close"].iloc[-1]
atr = df["ATR14"].iloc[-1]

print("RELIANCE close:", round(price, 2))
print("ATR(14)       :", round(atr, 2), "rupees of typical daily range")

# A common rule: stop-loss = 2 x ATR away from entry.
stop = price - 2 * atr
print("Example stop  :", round(stop, 2), "(entry minus 2 x ATR)")
print("Risk per share:", round(price - stop, 2))
```

Live output

```
RELIANCE close: 1306.0
ATR(14)       : 27.52 rupees of typical daily range
Example stop  : 1250.97 (entry minus 2 x ATR)
Risk per share: 55.03
```

Key idea
Why ATR instead of a flat "50-rupee stop"? Because a flat stop ignores the instrument. Fifty rupees is a tight leash on a volatile stock and a loose one on a calm stock. An ATR-based stop **adapts** - it's automatically wider when the market is jumpy and tighter when it's calm. That's the difference between a stop that fits the market and one that fights it.
## NATR: comparing risk across instruments
ATR is in price units, which makes it awkward to compare a 1,300-rupee stock against a 1,44,000-point gold contract. The **Normalized ATR (NATR)** fixes that by expressing ATR as a **percentage of price**. Now everything is on one scale: a NATR of 2% means "this thing typically swings about 2% a day," whether it's a penny stock or a commodity. That comparability is exactly what you need for **position sizing** - risk the same _percentage_ of capital on each trade and let NATR translate it into a quantity.
EX 2NATR across a stock and a commodityNSEMCXch13/02_natr_position_size.py
Copy
```
# NATR is ATR as a % of price -- so you can compare risk across very different symbols.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")

# Compare a stock and a commodity on the SAME volatility scale.
for sym, exch in [("RELIANCE", "NSE"), ("GOLDM03JUL26FUT", "MCX")]:
    df = client.history(symbol=sym, exchange=exch, interval="D", start_date=start, end_date=end)
    natr = ta.natr(df["high"], df["low"], df["close"], 14).iloc[-1]
    print(f"{sym:18s} NATR(14) = {natr:5.2f}%  -> price swings ~{natr:.2f}% in a typical day")

# Volatility-based sizing: risk a fixed 1% of capital, let NATR set the quantity.
print("\nIdea: the higher the NATR, the SMALLER the position, so rupee-risk stays steady.")
```

Live output

```
RELIANCE           NATR(14) =  2.11%  -> price swings ~2.11% in a typical day
GOLDM03JUL26FUT    NATR(14) =  1.96%  -> price swings ~1.96% in a typical day

Idea: the higher the NATR, the SMALLER the position, so rupee-risk stays steady.
```

Tip
The sizing rule in one sentence: decide how many rupees you're willing to lose on a trade (say 1% of capital), then set quantity so that an ATR-sized adverse move equals that loss. Higher volatility automatically gives you a _smaller_ position - which is exactly what keeps your rupee-risk steady across wildly different instruments.
## Bollinger Bands: an elastic range
**Bollinger Bands** are the most popular volatility envelope. They draw a 20-period moving average (the middle band) and then place an upper and lower band **two standard deviations** away - a statistical measure of how spread out recent prices have been. The bands breathe: they widen when volatility rises and pinch in when it falls. Price spends most of its time inside them, so tagging a band flags a stretched condition worth a second look.
`ta.bbands(...)` returns a **tuple of three** : upper, middle, lower.
EX 3Bollinger Bands around priceNSEch13/03_bollinger.py
Copy
```
# Bollinger Bands: a moving average with elastic bands set 2 std-devs out.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="TCS", exchange="NSE", interval="D", start_date=start, end_date=end)

# Returns a TUPLE: upper, middle (SMA), lower.
upper, middle, lower = ta.bbands(df["close"], period=20, std_dev=2.0)

price = df["close"].iloc[-1]
print("TCS close   :", round(price, 2))
print(f"Upper band  : {upper.iloc[-1]:8.2f}")
print(f"Middle (SMA): {middle.iloc[-1]:8.2f}")
print(f"Lower band  : {lower.iloc[-1]:8.2f}")

if price >= upper.iloc[-1]:
    print("Read: riding the UPPER band -> strong up move or stretched")
elif price <= lower.iloc[-1]:
    print("Read: tagging the LOWER band -> weak or oversold")
else:
    print("Read: inside the bands -> normal range")
```

Live output

```
TCS close   : 2060.0
Upper band  :  2369.06
Middle (SMA):  2204.93
Lower band  :  2040.80
Read: inside the bands -> normal range
```

### %B and Bandwidth: reading the bands as numbers
Eyeballing a chart is fine, but code needs numbers. Two derived readings turn the bands into single values. **%B** tells you _where price sits within the bands_ on a 0-to-1 scale: 1.0 is right at the upper band, 0.0 at the lower, 0.5 at the middle. **Bandwidth** measures _how wide the bands are_ - and when bandwidth drops near a recent low, the bands have pinched into a **squeeze** , a coiled-spring state that often precedes a sharp breakout.
`ta.bbpercent(...)` and `ta.bbwidth(...)` each return a single Series.
EX 4Bollinger %B and BandwidthNSEch13/04_bb_percent_width.py
Copy
```
# %B (where price sits in the bands) and Bandwidth (how wide the bands are = a squeeze gauge).
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

df["PCTB"] = ta.bbpercent(df["close"])
df["WIDTH"] = ta.bbwidth(df["close"])

pctb = df["PCTB"].iloc[-1]
width = df["WIDTH"].iloc[-1]
width_min = df["WIDTH"].tail(60).min()

print("HDFCBANK close:", round(df["close"].iloc[-1], 2))
print(f"%B       : {pctb:5.2f}   (1.0 = upper band, 0.0 = lower band)")
print(f"Bandwidth: {width:6.4f}  (60-day low was {width_min:.4f})")

# A bandwidth near its recent low is a "squeeze" -- coiled, often before a breakout.
print("Squeeze?", "YES -- bands tight, watch for a breakout" if width <= width_min * 1.1 else "no -- bands are not unusually tight")
```

Live output

```
HDFCBANK close: 772.9
%B       :  0.63   (1.0 = upper band, 0.0 = lower band)
Bandwidth: 0.0984  (60-day low was 0.0590)
Squeeze? no -- bands are not unusually tight
```

## Keltner Channel and the squeeze
The **Keltner Channel** looks like Bollinger Bands but is built differently: it centres on an EMA and sets its width using **ATR** rather than standard deviation. On its own it's a fine trend-and-range tool. But its most celebrated use is _paired with Bollinger Bands_ to detect the **squeeze** precisely: when the Bollinger Bands contract _inside_ the Keltner Channel, volatility has compressed to an extreme, and traders watch for the breakout that tends to follow.
`ta.keltner(...)` returns a **tuple of three** : upper, middle, lower.
EX 5Keltner vs Bollinger squeezeNSEch13/05_keltner_squeeze.py
Copy
```
# Keltner Channel uses ATR, not std-dev. Compared to Bollinger, it spots the "squeeze".
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

# Keltner returns (upper, middle, lower).
kc_up, kc_mid, kc_low = ta.keltner(df["high"], df["low"], df["close"])
# Bollinger for comparison.
bb_up, _, bb_low = ta.bbands(df["close"])

price = df["close"].iloc[-1]
print("SBIN close   :", round(price, 2))
print(f"Keltner upper/lower: {kc_up.iloc[-1]:.2f} / {kc_low.iloc[-1]:.2f}")
print(f"Bollinger upper/lower: {bb_up.iloc[-1]:.2f} / {bb_low.iloc[-1]:.2f}")

# The squeeze: Bollinger bands narrower than the Keltner channel = very low volatility.
squeeze = bb_up.iloc[-1] < kc_up.iloc[-1] and bb_low.iloc[-1] > kc_low.iloc[-1]
print("Squeeze (BB inside KC)?", "YES -- volatility coiled, breakout watch" if squeeze else "no")
```

Live output

```
SBIN close   : 1023.6
Keltner upper/lower: 1048.05 / 972.13
Bollinger upper/lower: 1054.46 / 940.48
Squeeze (BB inside KC)? no
```

## Donchian Channel: the breakout map
The **Donchian Channel** is volatility at its simplest and oldest: the **highest high and lowest low** of the last _N_ bars, with the midpoint between them. There's no averaging or statistics - just the literal range price has covered. That makes it the purest **breakout** tool there is: a close at the upper channel is a new _N_ -bar high (a breakout buy in trend-following systems), and a close at the lower channel is a new _N_ -bar low (a breakdown). The legendary "Turtle" trend-followers built their entire system on this one idea.
`ta.donchian(...)` returns a **tuple of three** : upper, middle, lower.
EX 6Donchian breakout levelsMCXch13/06_donchian.py
Copy
```
# Donchian Channel: the highest high and lowest low of N bars -- a pure breakout map.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")

df = client.history(symbol="CRUDEOIL20JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# Donchian returns (upper, middle, lower).
up, mid, low = ta.donchian(df["high"], df["low"], period=20)

price = df["close"].iloc[-1]
print("CRUDEOIL close:", round(price, 1))
print(f"20-day high (upper): {up.iloc[-1]:.1f}")
print(f"20-day mid         : {mid.iloc[-1]:.1f}")
print(f"20-day low  (lower): {low.iloc[-1]:.1f}")

# Classic rule: a close at the upper channel is a breakout buy; at the lower, a breakdown.
if price >= up.iloc[-1]:
    print("Signal: new 20-day HIGH -> breakout (trend-follow long)")
elif price <= low.iloc[-1]:
    print("Signal: new 20-day LOW -> breakdown (trend-follow short)")
else:
    print("Signal: inside the channel -> no breakout yet")
```

Live output

```
CRUDEOIL close: 6960
20-day high (upper): 8991.0
20-day mid         : 7944.0
20-day low  (lower): 6897.0
Signal: inside the channel -> no breakout yet
```

## Chandelier Exit: a volatility-based trailing stop
Once you're _in_ a winning trade, the hard question is when to get out. The **Chandelier Exit** answers it with volatility. It hangs a stop from the highest high since you entered, a few ATRs below it (like a chandelier from a ceiling), and trails it up as price climbs - but never down. The stop tightens naturally as the trend matures, locking in profit while giving the trade enough room to breathe through normal noise.
`ta.chandelier_exit(...)` returns a **tuple of two** : the long-trade stop (below price) and the short-trade stop (above price).
EX 7Chandelier Exit trailing stopsMCXch13/07_chandelier_exit.py
Copy
```
# Chandelier Exit: an ATR-based trailing stop that hangs from the recent high (or low).
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")

df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# Returns a TUPLE: long-trade exit (below price) and short-trade exit (above price).
long_exit, short_exit = ta.chandelier_exit(df["high"], df["low"], df["close"], period=22, multiplier=3.0)

price = df["close"].iloc[-1]
le = long_exit.iloc[-1]
se = short_exit.iloc[-1]
print("GOLDM close       :", round(price, 1))
print("Long-trade stop   :", round(le, 1), "(exit a long if price closes below this)")
print("Short-trade stop  :", round(se, 1), "(exit a short if price closes above this)")

# Use the stop that matches the current trend: a long's stop sits below price,
# a short's stop sits above it. Either way the cushion (distance to the stop) is positive.
if price > le:
    print("Trade side        : long  -- cushion", round(price - le, 1), "points before the stop triggers")
else:
    print("Trade side        : short -- cushion", round(se - price, 1), "points before the stop triggers")
```

Live output

```
GOLDM close       : 144424
Long-trade stop   : 152857.4 (exit a long if price closes below this)
Short-trade stop  : 151482.6 (exit a short if price closes above this)
Trade side        : short -- cushion 7058.6 points before the stop triggers
```

## Historical Volatility: the regime gauge
Finally, **Historical Volatility (HV)** measures the standard deviation of price returns and **annualises** it into a percentage - the same "vol" number options traders quote. A HV of 25% roughly means the instrument is expected to move within ±25% over a year, judging by its recent behaviour. The trick is to compare a _short_ HV against a _longer_ one: when short-term volatility climbs above its baseline, the market is getting jumpier - a **regime change** that should make you widen stops and trade smaller.
`ta.hv(...)` returns a single Series.
EX 8Historical Volatility regimeNSEch13/08_historical_volatility.py
Copy
```
# Historical Volatility: annualised std-dev of returns -- the "how wild" number in %.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

df["HV20"] = ta.hv(df["close"], length=20)
df["HV60"] = ta.hv(df["close"], length=60)

hv20 = df["HV20"].iloc[-1]
hv60 = df["HV60"].iloc[-1]
print("INFY close:", round(df["close"].iloc[-1], 2))
print(f"HV(20) = {hv20:5.1f}%  (recent, annualised)")
print(f"HV(60) = {hv60:5.1f}%  (longer-run baseline)")

# Rising short-term HV vs the baseline = the market is getting jumpier.
print("Regime:", "volatility EXPANDING (HV20 > HV60)" if hv20 > hv60 else "volatility CALMING (HV20 < HV60)")
```

Live output

```
INFY close: 1029.0
HV(20) =  50.5%  (recent, annualised)
HV(60) =  43.4%  (longer-run baseline)
Regime: volatility EXPANDING (HV20 > HV60)
```

Heads up
Volatility is _mean-reverting_ : calm periods follow storms and storms follow calm. A long, quiet squeeze is not a reason to relax - it's often the warning that a violent move is loading. Size your positions for the volatility you _expect next_ , not the sleepy one you see right now.
## Try it yourself
  * In the ATR example, change the stop multiplier from `2` to `3`. A wider stop survives more noise but risks more per share - see the trade-off in rupees.
  * Run the NATR comparison on three stocks you follow and rank them by volatility. The riskiest is rarely the one you'd guess.
  * In the Donchian example, change the period from 20 to 55 (the classic long-term Turtle setting) and see how much further the breakout levels sit from price.


## Recap
  * **Volatility** measures the _size_ of price swings - not direction - and it's how you size risk and define ranges.
  * **ATR** is the unit of risk in price terms; **NATR** is the same as a percentage, so you can compare any two instruments and size positions consistently.
  * **Bollinger Bands** are an elastic range; **%B** locates price within them and **Bandwidth** flags the **squeeze** before a breakout.
  * **Keltner** (ATR-based) paired with Bollinger pinpoints the squeeze; **Donchian** is the purest breakout map.
  * **Chandelier Exit** is an ATR trailing stop that locks in trend profits; **Historical Volatility** gauges the broader regime.
  * Channels return **3-tuples** , Chandelier returns a **2-tuple** , and the plain readings return a **Series** - unpack accordingly.


That completes the core indicator families - trend, momentum and volatility. Next we add **volume** indicators (OBV, VWAP, Money Flow) to read _participation_ : not just how price is moving, but how much conviction is behind it.
On this page
