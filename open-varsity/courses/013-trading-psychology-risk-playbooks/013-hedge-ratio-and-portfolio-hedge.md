Chapters
Module B · Hedging: When, Why and When Not - Chapter 13
# Hedge Ratio and Portfolio Hedge
Beta, notional value, the index hedge, partial vs full hedging, and why over- and under-hedging both cost you. How to size a portfolio hedge without pretending a perfect hedge exists.
Hedging
What you'll learn
  * ·Beta and notional value
  * ·Sizing an index hedge
  * ·Partial vs full hedge
  * ·Over- and under-hedging
  * ·Why perfect hedges are rare
  * ·A worked portfolio hedge


Ravi held about Rs 12,00,000 of stocks - mostly mid-caps he believed in. A big event was coming, so he decided to hedge. He shorted index futures worth roughly the same rupee value as his book: twelve lakh of stock, twelve lakh of NIFTY short. "Rupee for rupee, I'm covered," he told himself. The market fell. NIFTY dropped about 10%, and his short earned him close to Rs 1,20,000. He felt smart - right up until he opened his portfolio and saw it had fallen 14%, a loss of Rs 1,68,000. He was "fully hedged" and still down Rs 48,000. Nothing had gone wrong with his hedge. He had simply ignored the one number that decides how big a hedge needs to be.
That number is beta. This chapter is about sizing a portfolio hedge properly - and about being honest that even a properly sized hedge is never perfect.
## Two numbers that size every hedge
You only need two ideas to size a hedge. Learn them and most of the confusion disappears.
**Beta** is how much your portfolio moves compared with the index. A beta of 1.0 means your stocks move about the same as NIFTY. A beta of 1.2 means they move roughly 20% _more_ - when NIFTY falls 10%, your book tends to fall about 12%. Mid- and small-caps often have a beta well above 1; large, steady names sit closer to 1 or below. Beta is an average from the past, not a promise, but it is the best single guess you have for how hard your portfolio swings with the market.
**Notional value** is the full rupee value a position represents - not the margin you put up, the _whole_ exposure. One NIFTY futures lot is the index level times the lot size. At an index level of around 24,000 and a lot size of around 65 (lot sizes are revised periodically by the exchange - always check the current contract specs), one lot carries a notional of 24,000 x 65 = **Rs 15,60,000**. You may post far less as margin, but you are exposed to about fifteen and a half lakh of index movement. Hedging is about matching notional value, not margin.
Sizing a hedge: value x beta, then convert to lots Portfolio value Rs 10,00,000 x Beta 1.2 = Hedge notional to short Rs 12,00,000 Hedge notional Rs 12,00,000 / One NIFTY lot 24,000 x 65 = Rs 15,60,000 = About 0.77 lot Your real market exposure is value x beta. That, not your portfolio value, is what you hedge.
## Sizing an index hedge, step by step
Here is the whole calculation in plain rupees. Say you hold a Rs 10,00,000 portfolio and you have worked out its beta is about 1.2.
  1. **Find your real exposure.** Portfolio value x beta = 10,00,000 x 1.2 = **Rs 12,00,000**. Your twelve-lakh book behaves, in the market's eyes, like twelve lakh of index. That is why Ravi's rupee-for-rupee hedge fell short - his real exposure was bigger than his cash value.
  2. **Match that with index notional.** You want to be short about Rs 12,00,000 of NIFTY to offset the fall.
  3. **Convert to lots.** Divide by one lot's notional: 12,00,000 / 15,60,000 = **0.77 lot**. You cannot trade three-quarters of a lot, so you round to one lot (a small over-hedge) or skip it.


Key idea
The size of an index hedge is your portfolio value multiplied by its beta - not the rupee value of the portfolio. Hedge your _exposure_ , then divide by one lot's notional to get the number of lots. This is not advice on whether to hedge; it is only how to size one if you choose to.
## Full, partial, over and under
You do not have to take off all the risk. Hedging is a dial, not a switch.
A **partial hedge** removes only part of the risk on purpose. If you want to keep some upside and only soften a fall, hedge half: take your hedge notional and multiply by 0.5. For the book above, a 50% hedge is six lakh of index, not twelve. You will feel half the drop and keep half the bounce. This is often the sensible middle: you are nervous but not certain, so you take some risk off rather than all of it. A full hedge protects the most but gives up the most upside; a partial hedge is a deliberate "I want to stay a little in the game" choice.
The two ways to get it wrong are quieter. **Under-hedging** means your short is smaller than your real exposure - you are still partly exposed, and a fall still hurts (this was Ravi). **Over-hedging** means your short is _larger_ than your exposure - and now you have flipped. You are net short the market. If it keeps falling you profit, but if it rises you lose money even though your stocks went up. An over-hedge stops being insurance and becomes a fresh bet in the other direction.
Under, right, and over: matching the hedge to your exposure Under-hedged Long stocks (exposure) Short hedge Hedge too small. A fall still hurts you. Right-sized Long stocks (exposure) Short hedge Hedge = value x beta. The fall is mostly offset. Over-hedged Long stocks (exposure) Short hedge Now you are net short. A rise loses you money. The blue bar is your real exposure. The hedge should match it, not your cash value.
Common mistake
Two beginner traps sit here. The first is hedging **rupee-for-rupee** - shorting index equal to your portfolio's cash value while ignoring beta. A high-beta book stays under-hedged and still falls hard, exactly like Ravi. The second is **over-hedging** "to be safe" - buying so much protection that you are now net short, so a recovery rally costs you money on the very day your stocks finally bounce. Size to value x beta, then stop.
## A worked portfolio-hedge sizing table
Same method, different books. Index level around 24,000, lot around 65, so one lot is about Rs 15,60,000 of notional. Watch how the lots rarely come out whole.  
| Portfolio  | Beta  | Protect  | Hedge notional (value x beta x %)  | Lots (notional / 15,60,000)  | Practical choice  |  
| --- | --- | --- | --- | --- | --- |  
| Rs 10,00,000  | 1.2  | All (100%)  | 12,00,000  | 0.77  | 1 lot - slightly over-hedged  |  
| Rs 30,00,000  | 1.2  | All (100%)  | 36,00,000  | 2.31  | 2 lots - slight under-hedge  |  
| Rs 30,00,000  | 1.2  | Half (50%)  | 18,00,000  | 1.15  | 1 lot - slight under-hedge  |  
| Rs 50,00,000  | 0.9  | All (100%)  | 45,00,000  | 2.88  | 3 lots - small over-hedge  |  
The lesson in the last column: small books and odd betas almost never divide into whole lots. You are forced to round, and rounding is a tiny over- or under-hedge every time. That is normal. The goal is _close enough_ , not perfect.
## How this differs by who you are
The same maths applies to everyone, but how much it matters changes with your seat.  
| User type  | Does a portfolio hedge fit?  | What to watch  |  
| --- | --- | --- |  
| Long-term investor  | Rarely needed; one lot may dwarf a small SIP book  | A NIFTY lot is ~15.6 lakh notional - too big to hedge a few-lakh portfolio cleanly  |  
| Active trader  | Sometimes, into a known event  | Beta of your actual holdings, not a guess; round lots carefully  |  
| F&O (futures) trader  | Yes, this is the native tool  | Margin on the short lot, and not drifting into a net-short bet by over-hedging  |  
| Option seller  | Often hedges with index options, not futures  | A short put already adds market exposure; size the hedge to net beta, not gross  |  
## When this fails
Even sized perfectly, a portfolio hedge is an approximation. Be honest about why.
**Basis and tracking risk - your stocks are not the index.** You hedge with NIFTY, but you do not own NIFTY. You own a specific basket. If your stocks fall while the index holds up (a sector problem, a single bad result), your hedge barely moves and you lose anyway. The index can only protect against the part of your fall that is _market-wide_. The stock-specific part is uncovered.
**Beta drifts.** The 1.2 you calculated is a backward-looking average. In a sharp crash, correlations jump and many stocks fall together harder than their calm-day beta suggested - so a hedge sized for normal times can under-cover exactly when you needed it most. Beta is a guide, not a guarantee.
**Lots do not divide evenly.** As the table showed, you are almost always forced to round to a whole lot, leaving a small over- or under-hedge baked in from the start.
A perfect hedge - one that cancels your loss to the rupee - is a textbook idea, not a market reality. The honest aim is to take _most_ of the market risk off the table at a known cost, and to know which risks you are still carrying.
Note
This closes Module B. You now have the full honest picture of hedging: what it really does, when it is worth it, when it is not, what it costs, the simple tools, and how to size one with beta and notional value. None of it is free, and none of it is perfect - but used with clear eyes, a hedge buys you the calm to hold through a storm instead of panic-selling the bottom. Next the course turns to protecting capital directly.
## Quick self-check
**1.** Your portfolio is worth Rs 20,00,000 with a beta of 1.3. How much index notional should a full hedge be?
Value times beta: 20,00,000 x 1.3 = Rs 26,00,000 of index notional. You hedge your real exposure, not the cash value of the portfolio.
**2.** Why did Ravi still lose money even though he was "fully hedged" rupee-for-rupee?
He ignored beta. His mid-cap book had a beta around 1.4, so it fell 14% when NIFTY fell 10%. A rupee-for-rupee short only covered the 10% market move, leaving the extra fall uncovered. He was under-hedged without realising it.
**3.** What does it mean to be over-hedged, and why is it risky?
Your short is larger than your real exposure, so you are now net short the market. You make money if it falls further, but you lose money if it rises - even though your stocks went up. The hedge has turned into a fresh directional bet.
**4.** One NIFTY lot is about Rs 15,60,000 of notional. Why is that a problem for a Rs 5,00,000 portfolio?
A single lot is far bigger than the whole book, so even one lot massively over-hedges it. Small portfolios usually cannot hedge cleanly with index futures - reducing position size or holding cash is often the simpler move.
**5.** Why is a perfect hedge rare even when you size it correctly?
Your stocks are not the index (basis and tracking risk), beta drifts and often rises in a crash, and lot sizes force you to round. A hedge takes off most of the market risk at a cost - it does not cancel your loss to the rupee.
On this page
