Chapters
Module I · Production, Compliance & Career - Chapter 77
# SEBI Algo Compliance and Ethics
Trading inside the rules - the SEBI algo framework, system audit and governance duties, market-conduct rules, and the ethics of automated trading.
NSE
What you'll learn
  * ·The SEBI algo framework
  * ·System audit and governance
  * ·Cyber resilience duties
  * ·Market-conduct rules
  * ·Manipulation red lines
  * ·Ethics and responsibility


You've learned the craft - market structure, the mathematics, the models, the strategies, the rigor. This chapter steps back from the screen to the career: how to actually _become_ a working quant in India. The Indian quant scene, once tiny, is now genuinely growing - prop desks, asset managers launching systematic funds, fintechs, and global firms with India offices. The path in is demanding but learnable, and it rewards exactly the disciplined, honest thinking this course has tried to build.
## Where quants work in India
There are broadly four homes, echoing Chapter 1 but now as employers:
  * **Sell-side** (banks, large brokers) - building pricing models, risk engines and execution tools for clients.
  * **Buy-side** (AMCs, hedge funds, PMS, family offices) - the alpha hunters, running systematic and quant funds. India's mutual funds and PMS houses are increasingly launching factor and quant strategies.
  * **Proprietary trading firms** - trading the firm's own capital, often intraday and options-heavy, where India has a vibrant and growing scene.
  * **HFT shops** - the colocated, microsecond players (Chapter 31), a small but elite world.


## The roles
Within these, three distinct jobs - and you should know which fits you. The **quant researcher** hunts for and validates edges (this course's centre of gravity). The **quant developer** builds the fast, reliable systems that data and strategies run on. The **quant trader** runs and risk-manages strategies in the live market. Big firms separate them; smaller ones expect you to wear all three hats - which, conveniently, is exactly what building your own systematic strategy teaches.
## The interview
Quant interviews are famously rigorous, testing four pillars:
Probability & brainteasers expected value, conditional prob, puzzles Coding & data structures clean, fast Python; algorithms Statistics & ML regression, hypothesis tests, overfitting Markets & products options, microstructure, the real market The four pillars every quant interview tests
The brainteasers are the famous part - and there's a quant secret to them: when the closed-form maths is hard, _simulate_. Here's a classic, solved in seconds with the Monte Carlo of Chapter 10:
EX 1A quant-interview brainteaser, simulatedch77/01_interview_brainteaser.py
Copy
```
# A classic quant-interview puzzle, cracked the quant way - by simulation.
# Break a stick at two random points. What's the chance the 3 pieces form a triangle?
import numpy as np

rng = np.random.default_rng(0)
N = 500_000

cuts = np.sort(rng.random((N, 2)), axis=1)          # two random break points in [0,1]
a = cuts[:, 0]
b = cuts[:, 1] - cuts[:, 0]
c = 1 - cuts[:, 1]

# Three lengths form a triangle only if NO piece is longer than half the stick.
forms_triangle = (a < 0.5) & (b < 0.5) & (c < 0.5)
prob = forms_triangle.mean()

print(f"Simulated {N:,} broken sticks.")
print(f"P(three pieces form a triangle) ~ {prob:.4f}")
print(f"Exact answer                     = {1 / 4:.4f}  (1/4)")
print("\nWhen the maths is hard, a quant simulates - the same Monte Carlo tool from Chapter 12.")
```

Live output

```
Simulated 500,000 broken sticks.
P(three pieces form a triangle) ~ 0.2497
Exact answer                     = 0.2500  (1/4)

When the maths is hard, a quant simulates - the same Monte Carlo tool from Chapter 12.
```

The simulation nails the elegant answer of exactly **1/4**. And you can watch the estimate converge, a demonstration of the very law of large numbers you'd be expected to explain:
EX 2Monte Carlo converging on the answerch77/02_mc_convergence.py
Copy
```
# Watch the Monte Carlo estimate home in on the true answer as samples pile up.
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

rng = np.random.default_rng(0)
N = 50_000
cuts = np.sort(rng.random((N, 2)), axis=1)
a, b, c = cuts[:, 0], cuts[:, 1] - cuts[:, 0], 1 - cuts[:, 1]
hits = ((a < 0.5) & (b < 0.5) & (c < 0.5)).astype(float)

running = np.cumsum(hits) / np.arange(1, N + 1)        # running probability estimate

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(np.arange(1, N + 1), running, color="#7c83ff", lw=1)
ax.axhline(0.25, color="#16a34a", ls="--", lw=1.6, label="true answer = 1/4")
ax.set_xscale("log")
ax.set_ylim(0.1, 0.4)
ax.set_title("Monte Carlo convergence - the estimate settles onto 1/4")
ax.set_xlabel("Number of simulations (log scale)")
ax.set_ylabel("Estimated probability")
ax.legend()

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"After {N:,} sims the estimate is {running[-1]:.4f} (true 0.2500). Saved {out.name}")
```

Live output

```
After 50,000 sims the estimate is 0.2501 (true 0.2500). Saved 02_mc_convergence.png
```

![Monte Carlo converging on the answer chart](https://openalgo.in/quant/charts/ch77_02_mc_convergence.png)
Knowing _both_ the exact reasoning (no piece can exceed half the stick) _and_ the simulation is precisely the dual fluency interviewers look for - rigorous theory backed by practical computation.
## SEBI algo-trading compliance
A working quant in India trades inside a regulatory framework, and you must know it. **SEBI** governs algorithmic trading - algos route through registered brokers, with approvals, unique strategy IDs, and mandatory risk controls (price and quantity limits, kill switches). SEBI has been actively building a **framework for retail algo trading** , formalising how individuals deploy automated strategies through their brokers. Compliance isn't optional bureaucracy - trading outside the rules can cost you your access and more. Know the current circulars before you deploy.
## Ethics and responsibility
Automation amplifies everything, including the capacity to do harm. **Market manipulation** (spoofing, layering, pump-and-dump), **front-running** , and reckless strategies that destabilise a thinly-traded stock are not clever edges - they're illegal and unethical, and regulators increasingly detect them. With the power to place thousands of orders a second comes real responsibility: to trade fairly, to test exhaustively before risking real money (always start in analyze mode), and to never confuse "I can" with "I should". The best quants are also the most careful citizens of the market.
## How to break in
You don't need permission to start building a track record - which is the single most persuasive thing you can show:
  * **Build something real and honest.** A well-researched strategy with a clean, out-of-sample backtest and a sandbox-trading record - OpenAlgo's analyzer mode, using everything in this course - beats any certificate.
  * **Contribute to open source.** Projects like OpenAlgo are a way to learn the full stack _and_ be visible - real code others use.
  * **Master the foundations cold.** The probability, statistics and coding that interviews drill - practise them until they're reflexive.
  * **Be honest about edges.** The discipline of _not_ fooling yourself (Chapters 13, 27, 32) is, ironically, the rarest and most valued quant trait of all.


Key idea
Becoming a quant in India is a craft you can largely teach yourself: master the four interview pillars, build a real and _honest_ track record (sandbox-trade everything first in analyzer mode), respect SEBI's rules and the ethics of automation, and let your demonstrated rigor - the willingness to kill your own bad ideas - be your strongest credential.
## Try it yourself
  * Solve another classic by simulation: the expected number of fair-coin flips to first see two heads in a row. (Then verify it's 6.)
  * Take one strategy from this course, run it honestly out-of-sample with costs, and write a one-page research note. That note is the start of a track record.
  * Read SEBI's latest circular on retail algorithmic trading. What controls would your strategy need to comply?


## Recap
  * Indian quants work across **sell-side, buy-side, prop and HFT** , in three role types: **researcher, developer, trader**.
  * Interviews test four pillars - **probability/brainteasers, coding, statistics/ML, and markets** - and the quant trick for hard puzzles is to **simulate** (the broken-stick answer is exactly 1/4).
  * **SEBI** governs algo trading - registered brokers, risk controls, and an evolving **retail algo framework** ; know the rules before you deploy.
  * Automation demands **ethics** - no manipulation or front-running, exhaustive testing, and analyze mode first.
  * Break in by building a **real, honest track record** , contributing to **open source** , mastering the foundations, and making your **intellectual honesty** your credential.


You now have the knowledge and the path. The final chapter ties it all together into a single, end-to-end research project - the capstone that turns this course from theory into a thing you have actually built.
On this page
