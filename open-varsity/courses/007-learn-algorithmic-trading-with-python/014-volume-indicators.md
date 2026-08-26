Chapters
Module C · Technical Indicators - Chapter 14
# Volume Indicators
Read participation with OBV, VWAP, MFI, CMF and relative volume.
NSENFO
What you'll learn
  * ·OBV
  * ·VWAP
  * ·Money Flow Index
  * ·Chaikin Money Flow
  * ·Accumulation/Distribution
  * ·Relative volume


Price tells you _what_ happened. Volume tells you _how much it mattered_. A stock that jumps 2% on a quiet, sleepy day is a very different animal from one that jumps 2% while half the market piles in. The first move can evaporate by lunch; the second has real fuel behind it. That single idea - that **volume is the conviction behind a price move** - is what this chapter is about.
In the previous three chapters you measured trend, momentum and volatility, all from price alone. Volume indicators add the missing dimension: participation. They answer questions price charts can't. Are big players quietly accumulating while the price drifts sideways? Is this breakout backed by a crowd or by a handful of trades? Is the rally running out of buyers? When price and volume agree, you lean into the signal. When they disagree - a **divergence** - you get an early warning that the move is hollow.
A quick reminder before we start: every indicator here lives in `openalgo.ta`, so each script begins with `from openalgo import api, ta`. We confirmed the exact names and return types by testing them against the live server, and you'll see them printed in the output. Most return a pandas **Series** that lines up neatly with your price table.
Note
**What does "volume" actually count?** One unit of volume is one share (or one futures/options contract) that changed hands. If 10,000 shares of a stock trade in a day, the day's volume is 10,000 - regardless of price. Volume is the raw headcount of activity, and these indicators all reshape that headcount into something you can trade on.
## On Balance Volume: the simplest confirmation tool
**On Balance Volume (OBV)** is the gateway volume indicator, and it's beautifully simple. On a day the stock closes up, you _add_ that day's volume to a running total. On a down day, you _subtract_ it. The absolute number is meaningless - what matters is the _direction_ of the line. If OBV is climbing, more volume is flowing in on up days than out on down days: buyers are committed. If it's falling, sellers are.
The real power is comparing OBV's direction to price's direction. When both rise together, the trend is confirmed. When price makes a new high but OBV doesn't, that's a **bearish divergence** - the rally is losing its volume support, and it often precedes a turn.
EX 1On Balance Volume confirms a trendNSEch14/01_obv.py
Copy
```
# On Balance Volume (OBV): does volume confirm the price trend?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

# OBV adds volume on up-close days and subtracts it on down-close days.
df["OBV"] = ta.obv(df["close"], df["volume"])
print("ta.obv returns a", type(df["OBV"]).__name__)

# Is OBV trending the same way as price over the last 10 sessions?
price_chg = df["close"].iloc[-1] - df["close"].iloc[-11]
obv_chg = df["OBV"].iloc[-1] - df["OBV"].iloc[-11]
print(df[["close", "volume", "OBV"]].tail(5).round(2))
print(f"\n10-day price change: {price_chg:+.2f}")
print(f"10-day OBV change  : {obv_chg:+,.0f}")
print("Verdict:", "volume confirms the move" if (price_chg > 0) == (obv_chg > 0)
      else "DIVERGENCE - volume disagrees with price")
```

Live output

```
ta.obv returns a Series
             close    volume          OBV
timestamp                                
2026-06-17  1332.7  10029170 -236282951.0
2026-06-18  1328.1  15494549 -251777500.0
2026-06-19  1309.5  24887034 -276664534.0
2026-06-22  1326.5  12931213 -263733321.0
2026-06-23  1306.0  15277531 -279010852.0

10-day price change: +36.80
10-day OBV change  : +8,541,288
Verdict: volume confirms the move
```

Notice we used `ta.obv(close, volume)` - just two inputs, and it hands back a Series the same length as the price data. We then compared the 10-day change in price with the 10-day change in OBV. When they share a sign, volume confirms; when they don't, we flag a divergence.
## VWAP: the price everyone actually paid
**Volume Weighted Average Price (VWAP)** is the average price of the day, but weighted by how much volume traded at each price. A price level where a million shares changed hands counts for far more than one where a hundred did. The result is a single line that represents the "fair" average cost of the session.
Why traders live by it: large institutions are often judged on whether they bought _below_ VWAP or sold _above_ it, so VWAP acts like a magnet and a battleground. As a rule of thumb, price **above** VWAP means buyers are in control for the day; **below** means sellers are. It's a favourite of intraday traders, so we fetch 5-minute candles for it.
EX 2VWAP, the session's fair priceNSEch14/02_vwap.py
Copy
```
# VWAP: the volume-weighted average price the day's traders actually paid.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# VWAP is an intraday tool, so we pull 5-minute candles for one symbol.
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="5m", start_date=start, end_date=end)

# VWAP needs high, low, close AND volume - price weighted by how much traded there.
df["VWAP"] = ta.vwap(df["high"], df["low"], df["close"], df["volume"])

last = df.iloc[-1]
print(df[["close", "volume", "VWAP"]].tail(5).round(2))
print(f"\nLast close: {last['close']:.2f}   VWAP: {last['VWAP']:.2f}")
print("Bias:", "above VWAP - buyers in control" if last["close"] > last["VWAP"]
      else "below VWAP - sellers in control")
```

Live output

```
close  volume     VWAP
timestamp                                          
2026-06-23 15:05:00+05:30  1024.70  412754  1035.75
2026-06-23 15:10:00+05:30  1024.65  482059  1035.60
2026-06-23 15:15:00+05:30  1023.20  343805  1035.49
2026-06-23 15:20:00+05:30  1023.15  410136  1035.35
2026-06-23 15:25:00+05:30  1023.60  358670  1035.23

Last close: 1023.60   VWAP: 1035.23
Bias: below VWAP - sellers in control
```

Tip
VWAP needs four inputs - `high, low, close, volume` - because it builds a typical price for each bar before weighting it. It resets each session by default (the `anchor="Session"` setting), which is exactly what intraday traders want. Don't expect a meaningful VWAP from daily candles; it's a within-the-day tool.
## Money Flow Index: a volume-aware RSI
If you've met RSI (Chapter 12), the **Money Flow Index (MFI)** will feel familiar. It also runs on a fixed 0-to-100 scale and flags overbought and oversold extremes - but it folds volume into the calculation. So MFI is sometimes called "volume-weighted RSI." A spike to 85 on heavy volume is a louder overbought warning than the same level on thin trade.
The conventional zones: **above 80** is overbought (buyers may be exhausted), **below 20** is oversold (sellers may be exhausted). Like all oscillators, these extremes are most useful in a ranging market and can stay pinned in a strong trend.
EX 3Money Flow Index extremesNSEch14/03_mfi.py
Copy
```
# Money Flow Index (MFI): a volume-weighted RSI for overbought/oversold reads.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

# MFI runs 0-100 like RSI, but weights each move by its volume.
df["MFI"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"], period=14)

mfi = df["MFI"].iloc[-1]
zone = "OVERBOUGHT (>80)" if mfi > 80 else "OVERSOLD (<20)" if mfi < 20 else "neutral (20-80)"
print(df[["close", "volume", "MFI"]].tail(5).round(2))
print(f"\nLatest MFI: {mfi:.1f} -> {zone}")
print("Days overbought in window:", int((df["MFI"] > 80).sum()))
print("Days oversold in window  :", int((df["MFI"] < 20).sum()))
```

Live output

```
close    volume    MFI
timestamp                          
2026-06-17  1157.7   5995119  67.28
2026-06-18  1127.5  16781447  49.17
2026-06-19  1051.4  45665442  34.48
2026-06-22  1065.4  10178505  23.78
2026-06-23  1029.0  19209317  24.06

Latest MFI: 24.1 -> neutral (20-80)
Days overbought in window: 0
Days oversold in window  : 8
```

## Chaikin Money Flow and the A/D Line: tracking accumulation
The next two indicators both ask the same question - _is money flowing in or out?_ - but answer it differently.
**Chaikin Money Flow (CMF)** looks at _where in each bar's range the price closed_. Close near the high and it counts as buying pressure; close near the low, selling pressure. It sums that over a period (default 20) and divides by total volume, giving a value that swings between roughly -1 and +1. **Positive CMF means accumulation** (buyers winning); **negative means distribution** (sellers winning). Readings beyond ±0.20 are considered strong.
EX 4Chaikin Money Flow pressureMCXch14/04_cmf.py
Copy
```
# Chaikin Money Flow (CMF): are buyers or sellers winning over the period?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# CMF sums money-flow volume over 20 days. Positive = accumulation, negative = distribution.
df["CMF"] = ta.cmf(df["high"], df["low"], df["close"], df["volume"], period=20)

cmf = df["CMF"].iloc[-1]
print(df[["close", "CMF"]].tail(5).round(4))
print(f"\nLatest CMF: {cmf:+.4f}")
print("Pressure:", "buying / accumulation" if cmf > 0 else "selling / distribution")
print("Strong reading:", "yes" if abs(cmf) > 0.2 else "no (|CMF| under 0.20 is mild)")
```

Live output

```
close     CMF
timestamp                 
2026-06-17  151747 -0.1027
2026-06-18  147424 -0.1179
2026-06-19  145221 -0.0959
2026-06-22  146125 -0.0951
2026-06-23  144424 -0.0778

Latest CMF: -0.0778
Pressure: selling / distribution
Strong reading: no (|CMF| under 0.20 is mild)
```

The **Accumulation/Distribution Line (ADL)** uses the same close-within-the-range idea but, like OBV, keeps a _running cumulative total_ instead of a bounded average. You read its slope, not its level. A rising ADL says money is steadily being accumulated; a falling ADL says it's leaking out. ADL diverging from price is one of the classic early-warning signals.
EX 5Accumulation/Distribution Line slopeNSEch14/05_adl.py
Copy
```
# Accumulation/Distribution Line (ADL): a running tally of money flow.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
df = client.history(symbol="TCS", exchange="NSE", interval="D", start_date=start, end_date=end)

# ADL is cumulative, like OBV, but weights volume by WHERE the close lands in the bar.
df["ADL"] = ta.adl(df["high"], df["low"], df["close"], df["volume"])

# Rising ADL into a flat/up price = accumulation supporting the move.
adl_slope = df["ADL"].iloc[-1] - df["ADL"].iloc[-6]
print(df[["close", "ADL"]].tail(5).round(0))
print(f"\n5-day ADL change: {adl_slope:+,.0f}")
print("Money flow is", "building (accumulation)" if adl_slope > 0 else "leaking out (distribution)")
```

Live output

```
close         ADL
timestamp                     
2026-06-17  2223.0 -36495923.0
2026-06-18  2203.0 -35258642.0
2026-06-19  2125.0 -26395303.0
2026-06-22  2128.0 -29236433.0
2026-06-23  2060.0 -34513767.0

5-day ADL change: +3,334,290
Money flow is building (accumulation)
```

Key idea
**CMF vs ADL - what's the difference?** Both weight volume by where the close lands in the bar's range. CMF is **bounded and period-based** (a snapshot of the last 20 bars, good for "right now"), while ADL is **cumulative and unbounded** (a running history, good for spotting long divergences). Use CMF for a quick pressure read, ADL to confirm a trend over time.
## Ease of Movement: how hard did volume have to work?
**Ease of Movement (EMV)** combines price change with volume to ask a subtle question: _how much volume did it take to move the price this far?_ When price glides upward on light volume, EMV is strongly positive - the path of least resistance is up. When it takes enormous volume to nudge the price, EMV sits near zero, hinting the move is being fought.
Note its inputs: `high, low, volume` - it doesn't use the close at all, because it measures the _midpoint shift_ of each bar against the volume required to produce it. We run it on a commodity future here.
EX 6Ease of Movement on a commodityMCXch14/06_emv.py
Copy
```
# Ease of Movement (EMV): how little volume it took to move price.
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

# EMV uses high, low and volume (not close). High positive EMV = price rose easily
# on light volume; near zero = it took heavy volume to budge.
df["EMV"] = ta.emv(df["high"], df["low"], df["volume"], length=14)

emv = df["EMV"].iloc[-1]
print(df[["close", "volume", "EMV"]].tail(5).round(2))
print(f"\nLatest EMV: {emv:+.2f}")
print("Reading:", "rising easily (low effort up-move)" if emv > 0
      else "falling easily (low effort down-move)")
```

Live output

```
close  volume       EMV
timestamp                          
2026-06-17   7158   47805 -18176.97
2026-06-18   7054   40641 -13334.72
2026-06-19   7262   44565 -24393.50
2026-06-22   6983   42496 -23474.83
2026-06-23   6957   20948 -33435.57

Latest EMV: -33435.57
Reading: falling easily (low effort down-move)
```

## Force Index: the power behind the move
Elder's **Force Index** is wonderfully direct: it multiplies the day's price change by the day's volume, then smooths the result with an EMA. A big price move on big volume produces a big force reading. The **sign** tells you who's winning - positive means bulls, negative means bears - and a fresh **cross through zero** often marks a momentum shift worth watching.
EX 7Elder Force Index and its zero lineNSEch14/07_force_index.py
Copy
```
# Elder Force Index: price change times volume = the "force" behind a move.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# Force Index multiplies the day's price change by its volume, then EMA-smooths it.
df["FI"] = ta.force_index(df["close"], df["volume"], length=13)

fi = df["FI"].iloc[-1]
print(df[["close", "volume", "FI"]].tail(5).round(0))
print(f"\nLatest Force Index: {fi:+,.0f}")
print("Sign:", "positive - bulls have the force" if fi > 0 else "negative - bears have the force")
# A fresh cross from negative to positive often flags a momentum shift.
crossed_up = df["FI"].iloc[-2] < 0 < df["FI"].iloc[-1]
print("Just crossed up through zero:", crossed_up)
```

Live output

```
close    volume           FI
timestamp                               
2026-06-17  787.0  32405604  115165697.0
2026-06-18  799.0  41492071  169249975.0
2026-06-19  780.0  33798761   52366234.0
2026-06-22  786.0  25194765   68640408.0
2026-06-23  773.0  27503779    5791633.0

Latest Force Index: +5,791,633
Sign: positive - bulls have the force
Just crossed up through zero: False
```

## Relative Volume and Volume ROC: is today unusual?
The last two indicators don't reshape volume into money flow - they simply ask _how busy is it?_ , which is often the most practical question of all.
**Relative Volume (RVOL)** divides the current volume by the average volume over a lookback window. An RVOL of 1.0 is a perfectly average day; 2.0 means twice the usual activity. This is the scanner's favourite filter: a breakout on RVOL above 1.5 is far more trustworthy than one on a quiet day, because the crowd is actually showing up.
EX 8Relative Volume on a Nifty futureNFOch14/08_relative_volume.py
Copy
```
# Relative Volume (RVOL): is today busier than a normal day?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
df = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="D", start_date=start, end_date=end)

# RVOL = today's volume / average volume over the period. 1.0 = average, 2.0 = double.
df["RVOL"] = ta.rvol(df["volume"], period=20)

rvol = df["RVOL"].iloc[-1]
print(df[["close", "volume", "RVOL"]].tail(5).round(2))
print(f"\nLatest RVOL: {rvol:.2f}x the 20-day average")
print("Activity:", "unusually high - breakouts are more trustworthy" if rvol > 1.5
      else "quiet - moves may not stick" if rvol < 0.7 else "roughly normal")
```

Live output

```
close   volume  RVOL
timestamp                         
2026-06-17  24094.0  2506660  0.55
2026-06-18  24192.5  2883270  0.62
2026-06-19  24056.9  3696420  0.78
2026-06-22  24123.8  2096640  0.45
2026-06-23  23810.0  3709225  0.81

Latest RVOL: 0.81x the 20-day average
Activity: roughly normal
```

**Volume Rate of Change (VROC)** measures the _percentage_ change in volume versus N bars ago. It's the acceleration pedal for participation: a sharp positive VROC means a sudden surge of interest, while a deeply negative reading means the crowd is leaving. Pair a price breakout with a positive VROC and you have conviction; a breakout on falling volume is a prime candidate for a fake-out.
EX 9Volume Rate of ChangeNSEch14/09_volume_roc.py
Copy
```
# Volume Rate of Change (VROC): how fast volume itself is changing.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# VROC is a percentage: how much volume changed vs N bars ago.
df["VROC"] = ta.vroc(df["volume"], period=12)

vroc = df["VROC"].iloc[-1]
print(df[["close", "volume", "VROC"]].tail(5).round(2))
print(f"\nLatest VROC(12): {vroc:+.1f}%")
print("Participation is", "surging" if vroc > 50 else "drying up" if vroc < -50 else "steady")
print("A volume surge alongside a breakout adds conviction; a drop warns of a fake move.")
```

Live output

```
close    volume   VROC
timestamp                          
2026-06-17  1336.8   8026424 -19.02
2026-06-18  1342.3  13467985 -24.85
2026-06-19  1346.5   9057322 -35.00
2026-06-22  1352.4   4814845 -75.26
2026-06-23  1335.5  11726416  15.34

Latest VROC(12): +15.3%
Participation is steady
A volume surge alongside a breakout adds conviction; a drop warns of a fake move.
```

Heads up
Volume data quality varies by instrument and exchange. Index _spot_ values (like NIFTY on `NSE_INDEX`) often carry little or no real volume, so volume indicators on an index are unreliable - use the index _future_ (`NFO`) instead. And always sanity-check that the symbol you fetched actually reports volume before trusting any of these readings.
## What volume confirms - putting it together
Step back and the theme is clear. Volume indicators are not standalone buy/sell triggers; they are **confirmation and warning systems** layered on top of price. The workflow most traders follow:
  1. **Spot a price event** - a breakout, a trend, a reversal candle.
  2. **Check participation** - is RVOL elevated? Is VROC positive? A move on heavy volume has fuel.
  3. **Check direction of money flow** - is OBV/ADL rising with price, or diverging? Is CMF positive?
  4. **Act on agreement, fade on divergence** - when price and volume agree, conviction is high; when they split, expect the price move to fail.


That last point - **divergence** - is where volume earns its keep. A new price high on shrinking OBV, or a rally on falling CMF, is the market quietly telling you the move is running on empty.
## Try it yourself
  * Swap `RELIANCE` in the OBV example for a stock you follow, extend the window to 180 days, and look for any 10-day stretch where OBV and price disagree.
  * In the MFI example, change the symbol to a Nifty future (`NIFTY30JUN26FUT`, exchange `"NFO"`) and count how many days hit overbought versus oversold.
  * Combine two indicators: fetch a stock, compute both RVOL and Force Index, and print only the days where RVOL was above 1.5 _and_ Force Index was positive - your first volume-confirmed signal filter.


## Recap
  * **Volume is conviction** - it tells you how much a price move matters, the dimension price alone can't show.
  * **OBV** and the **ADL** are cumulative running tallies; read their _slope_ and watch for divergence from price.
  * **VWAP** is the volume-weighted fair price of a session - an intraday battleground; price above it is bullish, below it bearish.
  * **MFI** is a volume-weighted RSI (0-100, overbought >80, oversold <20); **CMF** is a bounded buying-vs-selling pressure gauge.
  * **EMV** and **Force Index** relate price movement to the volume required to produce it.
  * **RVOL** and **VROC** measure whether participation is unusually high - the scanner's tool for trusting a breakout.
  * The master rule: act when price and volume **agree** , stay cautious when they **diverge**.


Next we open the oscillator toolbox - bounded momentum tools like ROC, TRIX, the Awesome Oscillator and Stochastic RSI - and learn the crucial difference between indicators that thrive in trends and those built for ranges.
On this page
