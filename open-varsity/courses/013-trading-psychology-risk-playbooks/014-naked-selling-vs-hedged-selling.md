Chapters
Module C · The Option-Seller & Hedger Playbook - Chapter 14
# Naked Selling vs Hedged Selling
Why a naked short option carries open-ended risk, how a spread defines your maximum loss up front, and why defined-risk selling is the only sensible starting point for a beginner.
Options
What you'll learn
  * ·The naked-short danger
  * ·How a spread caps loss
  * ·Defined vs undefined risk
  * ·Margin difference
  * ·Why beginners start hedged
  * ·Reading max loss first


Meera found something that felt like free money. Every week she sold a NIFTY call option a little above the market and pocketed the premium - small, steady, easy. Rs 5,200 here, Rs 5,000 there. For five months it worked, and she started thinking of it as income. Then came an election result morning. NIFTY gapped up about 1,200 points before she could touch her screen. The call she had sold for Rs 5,200 was suddenly worth around Rs 78,000. One gap erased five months of premium and then some. Arjun, sitting two desks away, had the exact same view that week - but he had sold a _spread_. He lost Rs 15,600 that morning and not one rupee more, because his loss had a floor built in before he entered.
That single difference - a floor or a cliff - is what this chapter is about. It opens the Option-Seller playbook with the one rule a beginner seller cannot skip: only sell with defined risk.
## The two trades, in one minute
Selling an option means you collect a premium today and take on an obligation. If the market moves against you, you pay. There are two ways to carry that obligation.
A **naked short** is selling a call or a put with nothing behind it. You collect the premium and stand exposed to whatever the market does. Sell a call, and a rally costs you. Sell a put, and a crash costs you. There is no second leg protecting you - "naked" means exactly that.
A **hedged short** , usually called a **spread** , is selling one option and _buying_ a further-away option as insurance. You sell the 24,000 call and buy the 24,300 call. The option you buy costs you a little premium, so you collect less. In return, that bought option caps your loss. No matter how far the market runs, the long leg pays you back above its strike. Your worst case is fixed the moment you enter.
Same view of the market. Two completely different risk shapes.
## The cliff: why a naked short is open-ended
Picture the payoff of Meera's naked short call. As long as NIFTY stays below her strike, she keeps the full premium - a small, flat profit. Above the strike, every point the market rises is a point she loses, and there is nothing to stop it. The line just falls, and falls, off the bottom of the chart.
Naked short call: a small premium, then a cliff profit loss 0 Strike 24,000 break-even premium kept: Rs 5,200 loss keeps growing no floor below The most you can make is the premium. The most you can lose has no limit.
Run the numbers on Meera's morning. She sold a 24,000 call for Rs 80 a unit. One NIFTY lot is around 65 units, so she collected 80 x 65 = **Rs 5,200**. NIFTY gapped to about 25,200 - up 1,200 points. Her call was now worth at least its intrinsic value: 1,200 x 65 = **Rs 78,000**. She owed roughly seventy-eight thousand on a trade that paid her about five thousand. That is a loss of about **Rs 72,800** - fourteen times the premium she collected - and if the gap had been bigger, so would the loss. That is the cliff: tiny reward, unbounded risk.
## The floor: how a spread caps your loss
Now Arjun's version. He sold the same 24,000 call for Rs 80, but he also _bought_ the 24,300 call for Rs 20. He collected less - 80 minus 20 = Rs 60 a unit, or **Rs 3,900** for the lot. The trade-off is everything that matters: above 24,300, his bought call rises point-for-point with the call he sold, so the two cancel. His loss stops dead.
Hedged short (spread): a smaller premium, but a floor profit loss 0 Sell 24,000 Buy 24,300 break-even premium kept: Rs 3,900 max loss: Rs 15,600 floor - loss stops here The bought option turns the bottomless cliff into a flat, known floor.
Here is the worst case, fixed in advance. The gap between his two strikes is 300 points. He collected 60. So his maximum loss is (300 - 60) x 65 = 240 x 65 = **Rs 15,600**. NIFTY could gap to 25,200, to 26,000, to anywhere - Arjun still loses exactly Rs 15,600 and not one rupee more. That is the floor. He gave up about Rs 1,300 of premium to convert an unknown, possibly catastrophic loss into a number he wrote down before he clicked buy.
Key idea
For a beginner, only sell options with **defined risk** - a spread, where you have already bought the protection that caps your loss. A naked short hands you a small premium and an open-ended loss. The premium you give up for the hedge is the cheapest insurance you will ever buy. This is education, not advice on any specific trade.
## Naked vs spread, side by side  
| What matters  | Naked short  | Hedged short (spread)  |  
| --- | --- | --- |  
| Premium collected  | Larger - Rs 5,200  | Smaller - Rs 3,900  |  
| Maximum loss  | Open-ended, undefined  | Defined - Rs 15,600  |  
| Worst case on a gap  | Whatever the market does (Rs 72,800+)  | Still Rs 15,600  |  
| Margin blocked  | Large and can balloon as it moves against you  | Much smaller - the long leg earns a margin benefit  |  
| Can you size it sanely?  | No - the worst case is unknown  | Yes - you know the worst case up front  |  
| Sleep on a result night?  | Not really  | Yes  |  
The row that quietly decides everything is the margin one. A naked short blocks a large margin, and when the trade moves against you, your broker demands _more_ - exactly when you can least afford it. A spread blocks far less because the exchange can see your loss is capped, so it does not need a cushion for a disaster that cannot happen.
Common mistake
The classic beginner trap is selling naked "for the extra premium." Yes, the naked short collects Rs 5,200 versus the spread's Rs 3,900 - about 33% more. It feels like leaving money on the table to buy the hedge. But you are not collecting extra premium; you are getting paid a tiny sum to underwrite an unlimited loss. One gap and the "extra" Rs 1,300 you saved across many weeks vanishes under a single Rs 72,800 hit. The hedge is not a cost - it is the only thing that keeps one bad day from ending your account.
## Why defined risk lets you size - and sleep
This is the deeper reason the floor matters. **You cannot size a position whose worst case you do not know.** Position sizing is just one question: "If this goes maximally wrong, how much do I lose, and can I survive it?" For a spread, the answer is a number - Rs 15,600 - so you can decide how many lots fit your risk budget. If your rule is to risk no more than 2% of a Rs 5,00,000 account, that is Rs 10,000, so this spread is already a touch too big and you trade a narrower one. The maths _works_.
For a naked short, the worst case is "unknown, possibly ruinous," and you cannot size against infinity. So sellers do the dangerous thing instead: they size off the _margin_ or off how safe it feels, both of which say nothing about the tail. That is how a quiet income strategy ends in a single wipe-out.
A worked checklist before you ever sell:
  * Write down the maximum loss in rupees. If you cannot, the trade is naked - do not place it.
  * Check that max loss against your risk-per-trade limit (e.g. 1-2% of capital).
  * Confirm there is a bought leg, with a real strike, actually filled.
  * Note the margin, and that it is the smaller hedged margin, not the naked one.
  * Only then, size the number of lots so the defined loss fits your budget.

Worst case you are underwriting runs off the chart Naked: unknown capped Spread: Rs 15,600 You can only size a number. The naked bar has no top edge to size against.
## How this differs by who you are  
| User type  | Naked or hedged?  | What this means for you  |  
| --- | --- | --- |  
| Long-term investor  | Neither - selling naked is not investing  | If you sell at all, only a covered call against shares you own  |  
| Active trader  | Hedged only  | Define the max loss in rupees before entry; spreads, never naked  |  
| F&O trader  | Hedged as the default  | Smaller margin, capped tail; treat naked selling as an advanced, rare exception  |  
| Option seller (income)  | Defined-risk structures  | Your premium edge only survives if no single tail event can wipe months of it  |  
## When this fails
Defined risk solves one problem completely - the open-ended tail - but it is not a magic shield. Be honest about its limits.
**A spread can still lose its full defined amount, and that is real money.** Rs 15,600 is capped, not small. Lose it on three trades in a row and you are down Rs 46,800. Defined does not mean safe; it means survivable and sizeable.
**The protection has its own costs.** Two legs mean two sets of brokerage and charges, and a wider bid-ask to cross. On small premiums those frictions eat a real slice of an already thin edge. Sell tiny spreads often enough and costs alone can turn a winning idea into a losing one.
**Settlement and gaps still bite inside the spread.** For Indian index options, expiry is cash-settled, so there is no US-style early assignment to fear - the real risk is what happens at expiry settlement. A violent gap near expiry can park you at the worst point of the payoff, and stock options or stock futures can carry a physical-delivery obligation if you hold them into expiry. The loss is still capped - but you can hit the cap fast and without warning. If you do not fully understand how a position settles, close it before expiry.
**The premium edge is genuinely thin.** Most weeks the seller collects a little. The whole game is making sure the rare bad week cannot erase the many good ones. That is precisely what the hedge buys you - and precisely why skipping it is so tempting and so dangerous.
Note
This is the same fat loss tail you met in the Risk Management course's Option Seller Risk chapter: an option seller's return curve is many small wins and a few rare, very large losses. A naked short leaves that tail fully exposed - one event can be larger than every win combined. A spread cuts the tail off at a known point. The defined-risk seller still loses sometimes, but never more than the number they wrote down first.
This chapter is education, not investment advice, and the strikes and rupee figures are illustrative examples - not a recommendation to sell any particular option.
## Quick self-check
**1.** What is the single biggest danger of a naked short option?
The loss is open-ended. You collect a small premium, but if the market moves hard against you there is no floor - one gap can lose many times what you collected, as Meera's roughly Rs 72,800 loss on Rs 5,200 of premium shows.
**2.** How does a spread cap your loss?
You buy a further-away option as protection. Beyond its strike, that bought leg gains point-for-point with the option you sold, so the two cancel and your loss stops. Your maximum loss is the gap between strikes minus the premium collected - a fixed number known before you enter.
**3.** Arjun sold a 24,000 call and bought a 24,300 call for a net Rs 60 credit, lot size 65. What is his maximum loss?
The strikes are 300 points apart, and he collected 60, so the most he can lose is (300 - 60) x 65 = 240 x 65 = Rs 15,600 - no matter how far NIFTY runs.
**4.** Why does defined risk let you size a position when naked risk does not?
Sizing asks "if this goes maximally wrong, can I survive it?" A spread has a known worst case in rupees, so you can fit it to a risk budget. A naked short's worst case is unknown and possibly ruinous, so there is no number to size against - sellers end up sizing off margin or gut feel instead.
**5.** If a spread caps your loss, why isn't it simply "safe"?
You can still lose the full defined amount, several times over. Two legs cost more in brokerage and spread, settlement and gaps can hit you near expiry, and the seller's edge is thin. Defined risk makes the loss survivable and sizeable - it does not make it small or guaranteed.
On this page
