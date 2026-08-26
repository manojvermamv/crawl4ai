Chapters
Module E · Leverage, Margin and Execution Risk - Chapter 26
# Gap Risk and Event Risk
Results, RBI policy, elections, global shocks and overnight news move price while the market is shut. Why a stop-loss cannot protect you against a gap, and how to size for the surprises.
Leverage
What you'll learn
  * ·What a gap is
  * ·Why stops fail on gaps
  * ·Overnight and event risk
  * ·Results and policy days
  * ·Global shock examples
  * ·Sizing for surprises


Meera bought a stock at Rs 105 the day before its quarterly results. She did everything she thought was safe. She set a stop-loss at Rs 100, telling herself, "Worst case, I lose five rupees a share." She slept well. The next morning the results were poor, and the stock did not drift down to Rs 100 and stop her out. It simply _opened_ at Rs 85. Her stop turned into a market exit at 85, and her "Rs 5 risk" became a Rs 20 loss before she had even finished her chai. Nothing was broken. The stop worked exactly as designed. It just could not do the one thing she had trusted it to do.
This chapter is about the risk that lives in the spaces where you cannot act: overnight, over a weekend, during a halt, or in the half-second a shock hits. Price keeps moving even when you cannot. That is gap risk and event risk, and it is the one risk a stop-loss cannot save you from.
## What a gap actually is
A gap is when a stock or index opens at a price far from where it last closed. The market shut at one level; news arrived while it was closed; it reopened somewhere else entirely. There were no trades in between, so price did not _travel_ from the old level to the new one. It teleported.
Gaps happen because the world does not stop when the exchange does. Overnight, a company can post bad results, the RBI can change rates, the US market can crash, a war can start, or an election can surprise everyone. By 9:15 the next morning, the first trade simply reflects all of it at once.
A gap jumps straight over your stop stop Rs 100 105 85 market closes here opens Rs 85 no trades happened between 100 and 85 fill = 85, not 100 Price did not pass through your stop. It skipped over it while the market was shut.
## Why a stop-loss cannot save you from a gap
A stop-loss is not a guarantee to exit at your price. It is an _instruction_ : "once price reaches Rs 100, turn my order into a sell and get me out at whatever the next available price is." It needs trades happening near Rs 100 to fill you near Rs 100. In a gap, there are no trades near 100. The first available price is 85, so that is where you exit. The stop did fire. It just fired into thin air.
This is the single most misunderstood idea for beginners. A stop controls your risk _while the market is open and orderly_. It does nothing about the distance price can travel while you are asleep, or in the instant a shock lands. Your real overnight risk is not the gap to your stop. It is the gap to wherever the news decides to open the stock.
Key idea
A stop-loss caps the price you _trigger_ at, never the price you _fill_ at. Against an overnight gap or a sudden event, your true risk is the size of the surprise, not the distance to your stop.
## Scheduled events and unscheduled shocks
Event risk is the reason gaps happen, and events come in two flavours. Some are on the calendar. You know the date in advance, even if you cannot know the outcome: company results, RBI and US Fed rate decisions, the Union Budget on 1 February, monthly and weekly expiry, and election counting days. The 4 June 2024 election results are a clean example. Everyone knew the date for weeks. The exit polls said one thing, the actual count said another, and the NIFTY fell sharply that single morning. A known event, an unknown outcome.
The other flavour gives no warning at all. Demonetisation was announced one evening in November 2016, after the market had closed. The COVID crash in March 2020 brought repeated gap-downs and even lower-circuit halts as the NIFTY fell roughly 38 to 40% in weeks. Wars, a foreign bank collapsing overnight, a sudden regulatory order. You cannot put these on a calendar because nobody sent you the date.
Two kinds of event risk, one result Scheduled - on the calendar Company results / earnings RBI and US Fed rate decisions Union Budget (1 February) Weekly and monthly expiry Election counting days known date, unknown outcome Unscheduled - no warning Global selloff overnight War and geopolitics Pandemic shock (COVID, 2020) Sudden regulatory order Demonetisation (Nov 2016) no date, no preparation time GAP at the open You can prepare for the dates you know. You can only size for the ones you do not.
## How to manage gap and event risk
You cannot stop gaps. You can only decide how much of your account is exposed when one arrives. Three habits do most of the work.
First, **size smaller into known events.** If results, a budget, or an election count is tomorrow and you still want a position, cut your normal size. A half-size position that gaps badly hurts half as much. Second, **avoid holding leveraged positions overnight before a big event.** Leverage and gaps are the worst pair in trading: a gap that is a bruise on an unleveraged holding can be a wipeout on a margined one, because you owe the full move on borrowed money. If you must hold through an event with leverage, that is the time to be smallest. Third, **size for the surprise, not for the stop.** Ask the honest question before you hold overnight: "if this opens 10% against me tomorrow, can I take that loss and keep trading?" If the answer is no, the position is too big, stop or no stop.
Same gap, your choice of damage a 15% overnight gap against you, on Rs 1,00,000 capital - Rs 15,000 full size - Rs 7,500 half size into the event you cannot pick the gap, only the bar height The gap is the market's decision. The size of the position is yours.
Common mistake
Two errors stack into disaster here. The first is **holding full leveraged size overnight into a known event** because "the trade is working" - then the event gaps it against you and the leverage turns a bad morning into a blown account. The second is **trusting a stop to cap your gap loss** : setting a stop at Rs 100 and believing Rs 100 is the worst case. It is not. The better move is to treat any overnight hold as if the stop does not exist, and size so the _surprise_ is survivable.
## A checklist for event days
Run this before you carry any position past the close, especially on or before a known event date.
  * Is there a scheduled event (results, RBI or Fed, budget, expiry, election count) before the next session I will be holding through?
  * If I am holding through it, have I cut my size from normal?
  * Am I using leverage overnight? If yes, can I reduce or close it before the close?
  * If this opens 10% against me tomorrow, is the rupee loss one I can take and move on?
  * Am I treating my stop as a real floor? (It is not - assume it can be skipped.)
  * Am I an option seller? If so, is my loss defined, or open-ended into a gap?


## Gap risk for each type of participant
The same gap lands differently depending on what you hold.  
| User type  | How a gap hits  | Main defence  |  
| --- | --- | --- |  
| Long-term investor  | A gap-down is a paper loss in a position you meant to hold for years; you can wait it out  | Own quality, stay diversified, never over-concentrate in one name into results  |  
| Active trader  | Overnight or pre-event gaps blow past stops; intraday-only trading sidesteps most of it  | Reduce or close size before known events; do not assume the stop holds overnight  |  
| F&O / futures trader  | Leverage magnifies the gap; a margined future can lose multiples of a cash position on one open  | Smaller lots into events, avoid carrying leverage overnight before big dates  |  
| Option seller  | Most exposed of all - a gap can turn a small premium into a loss many times larger, with no cap  | Define the risk: buy a protective option, keep size tiny, never sell naked into events  |  
The option seller deserves the warning. Selling an option collects a small, capped premium but accepts an open-ended loss if price runs. A gap is exactly the move that runs furthest fastest, so the rare gap is where naked sellers do most of their lifetime damage. None of this is personalised advice - it is a framework to size against.
## When this fails
You cannot avoid all gap risk, and any honest chapter has to say so. If you hold anything overnight, you are exposed, full stop. Even hedges are not free protection. Buying a protective put or a downside option does cap your loss, but it costs premium every time, and most of those events never come - so the insurance quietly bleeds your returns while you wait for the rare day it pays. Going fully to cash before every event avoids the gap but also means missing the moves, the costs of trading in and out, and the simple fact that you cannot be in cash for every uncertainty, because there is always another uncertainty. The realistic goal is not zero gap risk. It is to never let a single gap, on a single oversized or over-leveraged position, end your participation in the market. Survive the surprise, and you get to trade the next thousand days.
## Quick self-check
**1.** Why can a stop-loss at Rs 100 still exit you at Rs 85?
A stop is an instruction to sell once price reaches Rs 100, at the next available price. If the stock gaps and opens at Rs 85 with no trades in between, the next available price is 85. The stop fires but fills at 85, because price skipped over 100 while the market was shut.
**2.** What exactly is a gap, and why do gaps happen?
A gap is when a stock or index opens far from its previous close, with no trades in between - price teleports rather than travels. It happens because news arrives while the market is closed: results, RBI or Fed decisions, the US market, elections, or a sudden shock all land at once at the open.
**3.** What is the difference between scheduled and unscheduled event risk?
Scheduled events are on the calendar - results, RBI and Fed decisions, the Budget, expiry, election counts - so you know the date even if not the outcome. Unscheduled shocks give no warning, like demonetisation in 2016 or the COVID crash in 2020. You can prepare for the dates you know and only size for the ones you cannot.
**4.** Why are option sellers especially exposed to gap risk?
Selling an option collects a small capped premium but accepts an open-ended loss if price runs hard. A gap is the move that runs furthest fastest, so a single overnight gap can turn a tiny premium into a loss many times larger - the rare event where naked sellers do most of their damage.
**5.** If you cannot avoid all gaps, what is the realistic goal?
Not zero gap risk - that is impossible if you hold anything overnight, and even hedges cost money. The goal is to size and limit leverage so no single gap on one oversized position can end your trading. Survive the surprise and keep your capital in the game.
On this page
