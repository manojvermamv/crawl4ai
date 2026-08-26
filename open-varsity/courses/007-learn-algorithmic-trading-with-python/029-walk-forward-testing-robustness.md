Chapters
Module G · Backtesting & Optimisation - Chapter 29
# Walk-Forward Testing & Robustness
Split in- and out-of-sample, roll the window forward, and avoid fooling yourself.
NSE
What you'll learn
  * ·Train/test split
  * ·In- vs out-of-sample
  * ·Rolling walk-forward
  * ·Parameter stability
  * ·Overfitting red flags
  * ·Deflated expectations


Here is the uncomfortable truth that ends most trading systems before they begin: any strategy can be made to look brilliant _on the past_. Give me enough parameters to tune and a fixed slice of history, and I'll hand you a gorgeous equity curve that means absolutely nothing. The market never repeats that exact history, so a strategy fitted to it has learned a story that will never be told again.
Last chapter we found "best" parameters by sweeping a grid. But best _on what_? On the very data we tuned them on - which is like grading your own exam after seeing the answer key. This chapter introduces the single most important discipline in quantitative trading: **walk-forward testing**. The idea is simple and almost old-fashioned in its honesty - tune on one slice of history, then judge the result on a _different_ slice the strategy has never seen. If the edge survives that, you might have something. If it doesn't, you've been fooling yourself, and it's far better to learn that on a screen than with real money.
## In-sample and out-of-sample
Two terms you'll use forever:
  * **In-sample** (or _training_) data is the history you're allowed to tune on. You can optimise, fit, and fiddle here as much as you like.
  * **Out-of-sample** (or _test_) data is held back, sealed in an envelope. The strategy never sees it during tuning. It's the exam.


The split is brutally simple: cut the timeline in two. Everything _before_ the cut is in-sample; everything _after_ is out-of-sample. The order is sacred - the future must stay in the future. You never shuffle market data the way you might shuffle a deck, because that would let tomorrow's information leak into yesterday's decisions.
EX 1Split into in- and out-of-sampleNSEch29/01_train_test_split.py
Copy
```
# Split history into IN-SAMPLE (train) and OUT-OF-SAMPLE (test) -- never shuffle time.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]

# Cut the timeline once. The FIRST chunk is for tuning; the LAST is held back,
# untouched, to judge the result. Order matters -- the future must stay future.
cut = int(len(close) * 0.7)
in_sample = close.iloc[:cut]
out_sample = close.iloc[cut:]

print(f"Total daily bars : {len(close)}")
print(f"In-sample (train): {len(in_sample)} bars  {in_sample.index[0].date()} -> {in_sample.index[-1].date()}")
print(f"Out-of-sample    : {len(out_sample)} bars  {out_sample.index[0].date()} -> {out_sample.index[-1].date()}")
print("\nWe tune ONLY on the in-sample. The out-of-sample is a sealed exam paper.")
```

Live output

```
Total daily bars : 610
In-sample (train): 427 bars  2024-01-05 -> 2025-09-23
Out-of-sample    : 183 bars  2025-09-24 -> 2026-06-23

We tune ONLY on the in-sample. The out-of-sample is a sealed exam paper.
```

Heads up
This is why, when we reach machine learning in Chapter 30, we always pass `train_test_split(..., shuffle=False)`. The default shuffles rows randomly - fine for photos of cats, catastrophic for time series. Shuffling lets the model peek at the future, and a model that has seen the future always looks like a genius.
## Step one: optimise on the training slice
Walk-forward is a two-step dance, and step one is exactly the optimisation you already know - but performed _only_ on the in-sample data. We sweep the EMA grid on the training slice and pick the combo with the best Sharpe. Notice we never even touch the test data here.
EX 2Tune the parameter in-sampleNSEch29/02_optimise_in_sample.py
Copy
```
# Step 1 of walk-forward: find the best parameter ON THE TRAINING DATA ONLY.
import os
from datetime import datetime, timedelta

import pandas as pd
import vectorbt as vbt
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]
train = close.iloc[:int(len(close) * 0.7)]            # tune only on this slice

combos = [(f, s) for f in (10, 20, 30) for s in (40, 50, 60) if f < s]
ent, ext = {}, {}
for f, s in combos:
    fe, se = ta.ema(train, f), ta.ema(train, s)
    ent[(f, s)] = (fe > se) & (fe.shift(1) <= se.shift(1))
    ext[(f, s)] = (fe < se) & (fe.shift(1) >= se.shift(1))
cols = pd.MultiIndex.from_tuples(combos, names=["fast", "slow"])
pf = vbt.Portfolio.from_signals(train, pd.DataFrame(ent).set_axis(cols, axis=1),
                                pd.DataFrame(ext).set_axis(cols, axis=1),
                                init_cash=100000, fees=0.001, freq="1D")

best = tuple(int(x) for x in pf.sharpe_ratio().idxmax())
print(f"Tuned on {len(train)} in-sample bars.")
print(f"Best combo by Sharpe: EMA {best[0]}/{best[1]}")
print(f"In-sample Sharpe    : {pf.sharpe_ratio()[best]:.2f}  (looks great -- but it SHOULD)")
```

Live output

```
Tuned on 427 in-sample bars.
Best combo by Sharpe: EMA 30/60
In-sample Sharpe    : 0.71  (looks great -- but it SHOULD)
```

The in-sample Sharpe will usually look good. It _should_ - we hand-picked the combo that scored highest on exactly this data. That number is not evidence of skill; it's evidence that we optimised. The real question comes next.
## Step two: grade it out-of-sample
Now the moment of truth. We take the winner from training - and only the winner - and run it on the held-back test data. Then we put the two returns side by side.
EX 3Evaluate it out-of-sampleNSEch29/03_evaluate_out_of_sample.py
Copy
```
# Step 2: take the winner from training and grade it on UNSEEN out-of-sample data.
import os
from datetime import datetime, timedelta

import pandas as pd
import vectorbt as vbt
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def run(c, f, s):                                     # backtest one combo on a slice
    fe, se = ta.ema(c, f), ta.ema(c, s)
    e = (fe > se) & (fe.shift(1) <= se.shift(1))
    x = (fe < se) & (fe.shift(1) >= se.shift(1))
    return vbt.Portfolio.from_signals(c, e, x, init_cash=100000, fees=0.001, freq="1D")


def best_on(c, combos):                               # pick best Sharpe combo on a slice
    ent = {cb: ((ta.ema(c, cb[0]) > ta.ema(c, cb[1])) &
                (ta.ema(c, cb[0]).shift(1) <= ta.ema(c, cb[1]).shift(1))) for cb in combos}
    ext = {cb: ((ta.ema(c, cb[0]) < ta.ema(c, cb[1])) &
                (ta.ema(c, cb[0]).shift(1) >= ta.ema(c, cb[1]).shift(1))) for cb in combos}
    cols = pd.MultiIndex.from_tuples(combos, names=["fast", "slow"])
    pf = vbt.Portfolio.from_signals(c, pd.DataFrame(ent).set_axis(cols, axis=1),
                                    pd.DataFrame(ext).set_axis(cols, axis=1),
                                    init_cash=100000, fees=0.001, freq="1D")
    return tuple(int(x) for x in pf.sharpe_ratio().idxmax())


end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]
cut = int(len(close) * 0.7)
combos = [(f, s) for f in (10, 20, 30) for s in (40, 50, 60) if f < s]

best = best_on(close.iloc[:cut], combos)              # learn on train
in_s = run(close.iloc[:cut], *best).total_return() * 100
out_s = run(close.iloc[cut:], *best).total_return() * 100
print(f"Chosen on training: EMA {best[0]}/{best[1]}")
print(f"In-sample return  : {in_s:6.2f} %  (what we tuned for)")
print(f"Out-of-sample     : {out_s:6.2f} %  (the only number that counts)")
```

Live output

```
Chosen on training: EMA 30/60
In-sample return  :  15.90 %  (what we tuned for)
Out-of-sample     :  -4.57 %  (the only number that counts)
```

Key idea
The in-sample number is what you _tuned for_ ; the out-of-sample number is the only one that counts. A strategy that earned a great in-sample return but stumbles out-of-sample hasn't found an edge - it has memorised noise. When the two are close, you've found something that might generalise. When the out-of-sample badly trails the in-sample, that gap is the cost of your overfitting, paid back to you as a warning instead of a loss.
A note on what you'll see: a simple EMA crossover on a single stock won't print heroic returns, and an out-of-sample slice of a few months can easily come back negative. That's realistic - most simple ideas are mediocre, and walk-forward is the tool that _tells you so_ before you bet on them.
## Rolling the window forward
One split is a snapshot; real trading is a film. In practice you'd re-tune your strategy periodically - say every quarter - using recent history, then trade those settings until the next re-tune. **Walk-forward testing** mimics exactly that: tune on a window, test on the window immediately after, then _slide_ both windows forward and repeat.
Stitch all those out-of-sample test results together and you get something precious: a track record built entirely from data the strategy had never seen at the moment of each decision. It's the closest thing to live trading you can get without risking capital.
EX 4Roll the window forwardNSEch29/04_rolling_walk_forward.py
Copy
```
# Roll the window forward: tune, test, slide, repeat -- mimicking real re-tuning.
import os
from datetime import datetime, timedelta

import pandas as pd
import vectorbt as vbt
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

COMBOS = [(f, s) for f in (10, 20, 30) for s in (40, 50, 60) if f < s]


def signals(c, f, s):
    fe, se = ta.ema(c, f), ta.ema(c, s)
    return ((fe > se) & (fe.shift(1) <= se.shift(1)),
            (fe < se) & (fe.shift(1) >= se.shift(1)))


def best_on(c):
    ent = {cb: signals(c, *cb)[0] for cb in COMBOS}
    ext = {cb: signals(c, *cb)[1] for cb in COMBOS}
    cols = pd.MultiIndex.from_tuples(COMBOS, names=["fast", "slow"])
    pf = vbt.Portfolio.from_signals(c, pd.DataFrame(ent).set_axis(cols, axis=1),
                                    pd.DataFrame(ext).set_axis(cols, axis=1),
                                    init_cash=100000, fees=0.001, freq="1D")
    return tuple(int(x) for x in pf.sharpe_ratio().idxmax())


end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]

train_len, test_len = 250, 100                        # window sizes in bars
print(f"{'window':7}{'tuned EMA':12}{'OOS return %':>13}")
i = 0
while i + train_len + test_len <= len(close):
    tr = close.iloc[i:i + train_len]
    te = close.iloc[i + train_len:i + train_len + test_len]
    f, s = best_on(tr)                                # tune on train window
    e, x = signals(te, f, s)
    oos = vbt.Portfolio.from_signals(te, e, x, init_cash=100000, fees=0.001,
                                     freq="1D").total_return() * 100
    print(f"{i // test_len + 1:<7}{f'{f}/{s}':12}{oos:13.2f}")  # test on next window
    i += test_len                                     # slide forward
```

Live output

```
window tuned EMA    OOS return %
1      30/60               -3.30
2      30/60               -6.07
3      30/60               -4.15
```

Each row here is an independent little experiment: tune on 250 bars, trade the next 100, slide on. No single window gets to cherry-pick its own answer key.
## Parameter stability: the quiet truth-teller
Here's a test that catches overfitting before you even look at returns. Across all those rolling windows, _did the optimiser keep picking the same settings?_ If window after window lands on roughly the same EMA lengths, your strategy is **stable** - it's responding to a persistent feature of the market. If the "best" combo ricochets wildly from one window to the next, the optimiser is just chasing random noise, and whatever it picks next is anyone's guess.
EX 5Check parameter stabilityNSEch29/05_parameter_stability.py
Copy
```
# Parameter STABILITY: does the optimiser pick the same settings each window?
import os
from datetime import datetime, timedelta

import pandas as pd
import vectorbt as vbt
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

COMBOS = [(f, s) for f in (10, 20, 30) for s in (40, 50, 60) if f < s]


def best_on(c):
    ent, ext = {}, {}
    for f, s in COMBOS:
        fe, se = ta.ema(c, f), ta.ema(c, s)
        ent[(f, s)] = (fe > se) & (fe.shift(1) <= se.shift(1))
        ext[(f, s)] = (fe < se) & (fe.shift(1) >= se.shift(1))
    cols = pd.MultiIndex.from_tuples(COMBOS, names=["fast", "slow"])
    pf = vbt.Portfolio.from_signals(c, pd.DataFrame(ent).set_axis(cols, axis=1),
                                    pd.DataFrame(ext).set_axis(cols, axis=1),
                                    init_cash=100000, fees=0.001, freq="1D")
    return tuple(int(x) for x in pf.sharpe_ratio().idxmax())


end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]

picks = []
train_len, step = 250, 100
i = 0
while i + train_len <= len(close):
    picks.append(best_on(close.iloc[i:i + train_len]))
    i += step

print("Best combo chosen in each rolling training window:")
for n, (f, s) in enumerate(picks, 1):
    print(f"  window {n}: EMA {f}/{s}")
unique = len(set(picks))
print(f"\nDistinct picks across {len(picks)} windows: {unique}")
print("Few distinct picks -> STABLE and trustworthy. Jumping around -> noise-fitting.")
```

Live output

```
Best combo chosen in each rolling training window:
  window 1: EMA 30/60
  window 2: EMA 30/60
  window 3: EMA 30/60
  window 4: EMA 10/40

Distinct picks across 4 windows: 2
Few distinct picks -> STABLE and trustworthy. Jumping around -> noise-fitting.
```

Tip
Stability is more reassuring than any single backtest number. A strategy whose ideal parameters barely move through time is one you can actually trust to re-tune and keep trading. A strategy whose parameters won't sit still is telling you, loudly, that it has no real edge - listen to it.
## Reading the overfitting red flags
Let's make the warning signs concrete. When you lay in-sample and out-of-sample returns side by side for several combos, the **gap** between them is the overfitting tell. A combo that looks spectacular in training and falls apart in testing has fitted the past's noise. The combo whose two columns stay closest - even if neither is the absolute highest - is the more honest bet.
EX 6Spot the overfitting gapNSEch29/06_overfit_red_flag.py
Copy
```
# The overfitting tell: a big gap between in-sample glory and out-of-sample reality.
import os
from datetime import datetime, timedelta

import pandas as pd
import vectorbt as vbt
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

COMBOS = [(f, s) for f in (5, 10, 20) for s in (30, 50) if f < s]


def run(c, f, s):
    fe, se = ta.ema(c, f), ta.ema(c, s)
    e = (fe > se) & (fe.shift(1) <= se.shift(1))
    x = (fe < se) & (fe.shift(1) >= se.shift(1))
    return vbt.Portfolio.from_signals(c, e, x, init_cash=100000, fees=0.001, freq="1D")


end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]
cut = int(len(close) * 0.6)
train, test = close.iloc[:cut], close.iloc[cut:]

print(f"{'EMA':9}{'in-sample %':>13}{'out-sample %':>14}{'  gap':>8}")
for f, s in COMBOS:
    ins = run(train, f, s).total_return() * 100
    oos = run(test, f, s).total_return() * 100
    print(f"{f'{f}/{s}':9}{ins:13.2f}{oos:14.2f}{ins - oos:8.1f}")
print("\nA combo that shines in-sample but collapses out-of-sample is OVERFIT.")
print("Trust the setting whose two columns stay closest together.")
```

Live output

```
EMA        in-sample %  out-sample %     gap
5/30            -11.89         -6.86    -5.0
5/50             -3.03         -7.06     4.0
10/30           -17.24         -7.40    -9.8
10/50            -7.06         -9.18     2.1
20/30            -5.75        -10.88     5.1
20/50            -5.26         -8.11     2.8

A combo that shines in-sample but collapses out-of-sample is OVERFIT.
Trust the setting whose two columns stay closest together.
```

The classic red flags, gathered in one place:
  * **A large in-sample / out-of-sample gap** - the bigger the drop-off, the more you overfit.
  * **Unstable parameters** - the best settings jump around from window to window.
  * **Too few trades** - a curve built on a handful of trades is luck wearing a costume.
  * **Fragility** - a tiny change in a parameter flips the result from wonderful to dreadful.


Note
Even a genuinely good in-sample result deserves suspicion. If you test 50 combos, one will look great by pure chance - the same way one of 50 coin-flippers will get ten heads in a row. Professionals "deflate" their expectations for exactly this reason: the more things you tried, the luckier your apparent winner probably is. Walk-forward is the antidote, because luck rarely survives on data the strategy never saw.
## Walk-forward by hand
To be sure the mechanics aren't VectorBT magic, here's the same walk-forward written in plain pandas - positions from an EMA comparison, returns from `pct_change`, equity from a running product. Every moving part is visible, and the conclusion is the same: the stitched-together out-of-sample record is your honest expectation, not the flattering in-sample dream.
EX 7Walk-forward with plain returnsNSEch29/07_manual_walk_forward.py
Copy
```
# Walk-forward without VectorBT: plain pandas returns, so you see every moving part.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def strat_return(c, f, s):
    # Hold long while fast EMA is above slow; earn the bar's return when in.
    pos = (ta.ema(c, f) > ta.ema(c, s)).astype(int).shift(1).fillna(0)
    daily = c.pct_change().fillna(0)
    equity = (1 + pos * daily).prod()                 # gross growth multiple
    return (equity - 1) * 100


end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=900)).strftime("%Y-%m-%d")
close = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                       start_date=start, end_date=end)["close"]

combos = [(f, s) for f in (10, 20) for s in (40, 50, 60) if f < s]
train_len, test_len, i, oos_total = 250, 100, 0, []
while i + train_len + test_len <= len(close):
    tr = close.iloc[i:i + train_len]
    te = close.iloc[i + train_len:i + train_len + test_len]
    best = max(combos, key=lambda cb: strat_return(tr, *cb))     # tune on train
    oos_total.append(strat_return(te, *best))                    # score on test
    print(f"window {i // test_len + 1}: tuned EMA {best[0]}/{best[1]} -> OOS {oos_total[-1]:6.2f} %")
    i += test_len

print(f"\nAverage out-of-sample return per window: {sum(oos_total) / len(oos_total):.2f} %")
print("This stitched out-of-sample record is the honest expectation -- not the in-sample dream.")
```

Live output

```
window 1: tuned EMA 20/60 -> OOS  -9.08 %
window 2: tuned EMA 10/60 -> OOS  -1.94 %
window 3: tuned EMA 20/60 -> OOS  -4.38 %

Average out-of-sample return per window: -5.13 %
This stitched out-of-sample record is the honest expectation -- not the in-sample dream.
```

When this honest number is good, you have real reason to proceed to live trading. When it's poor, you've just saved yourself a costly lesson - and that's a win too.
## Try it yourself
  * In `04_rolling_walk_forward.py`, shrink `train_len` to 150 and `test_len` to 60. Do more, smaller windows make the picks more or less stable?
  * Run the stability check on a different stock. Count the distinct picks - would you trust this strategy on that name?
  * In the red-flag example, change the split from 0.6 to 0.5. Do the in-sample/out-of-sample gaps widen or narrow, and why might that be?


## Recap
  * Tuning and judging on the same data is self-deception; **walk-forward** tunes **in-sample** and grades **out-of-sample**.
  * Never shuffle time-series data - the future must stay future (hence `shuffle=False` for ML splits).
  * **Rolling** the window forward builds an honest track record from data the strategy never saw at decision time.
  * **Parameter stability** across windows is a powerful, return-free sign of a real edge; jumpy parameters signal noise-fitting.
  * The **in-sample / out-of-sample gap** , unstable parameters, too few trades, and fragility are the classic overfitting red flags.
  * The more combos you test, the luckier your apparent winner - deflate your expectations and trust the out-of-sample record.


You've now proven an edge the honest way. In the final chapter we make a different leap: instead of hand-coding rules, we let a machine _learn_ the rules from data - training a classifier and a neural network to read the market, then wiring the whole thing into a complete, runnable trading bot.
On this page
