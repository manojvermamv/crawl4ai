Chapters
Module F · F&O Risk for Beginners - Chapter 31
# Greeks as Risk Language
Delta, gamma, theta and vega explained only as risk tools, not formulas. What can hurt you today, what builds up by tomorrow, and what explodes during a shock.
Options
What you'll learn
  * ·Greeks as a risk dashboard
  * ·Delta: direction risk
  * ·Theta: time risk
  * ·Vega: volatility risk
  * ·Gamma: acceleration risk
  * ·Reading your position's Greeks


Arjun was sure he had it right. The RBI policy was due, and he believed the market would rally. So two days before, he bought one NIFTY call option, paying Rs 120 a unit. The next morning he was right - NIFTY rose about 80 points, exactly the direction he had bet on. He opened his trading app expecting a fat profit. The call was worth Rs 95. He had guessed direction correctly and _still_ lost money. Nobody cheated him. Two quiet forces he had never heard of had eaten his profit while he was busy being right.
This chapter is about those forces. They carry Greek names - delta, theta, vega and gamma - and they sound like a maths exam. Forget the maths. We will treat the Greeks as nothing more than a **risk dashboard** : four gauges, each one telling you a different way an option can hurt you, and when.
## Your dashboard, not a maths exam
An option's price moves for four different reasons at the same time. Price moving in the underlying is only one of them. Each Greek measures one of these reasons. Think of the dashboard in a car: you do not need to understand the engineering to read the fuel gauge and the speedometer. You just glance and you know. The Greeks work the same way. Each one answers a single beginner question - _what can hurt me, and when?_
You will never need to calculate a Greek by hand. Your broker's option screen shows them, and OpenAlgo can pull them for any contract. The skill that matters is not the maths behind a Greek - it is reading the gauge and knowing what it is warning you about. So we will spend this whole chapter on meaning, never on formulas.
The four Greeks are a risk dashboard DELTA direction risk per 1-point move THETA time risk value lost per day VEGA volatility risk per IV shift GAMMA acceleration risk dangerous near expiry Four gauges, four ways to get hurt. You only have to learn what each one warns about.
## Delta - the direction gauge
Delta answers: _how much does my option move when the underlying moves one point?_ If NIFTY moves up 1 point and your call has a delta of around 0.5, your option gains roughly 50 paise a unit. A delta near 1 means the option behaves almost like the underlying itself; a delta near 0 means it barely reacts.
So delta is your **effective exposure right now**. It is the direction bet, expressed in real money. This is the one gauge every beginner watches, because it is the obvious one: price goes my way, I win. Delta hurts you on a _move_ - when the underlying goes the wrong way, delta is the gauge bleeding red. The trap is that beginners watch this gauge and nothing else, then cannot understand why a correct direction call still lost. The other three gauges are the answer.
## Theta - the time gauge
Here is the gauge Arjun never looked at. Every single day that passes, an option loses a little value, simply because there is less time left for your bet to come good. That daily bleed is **theta**. It ticks down overnight, over the weekend, even on a day when price does not move at all.
Theta hurts the buyer every day. For the option _seller_ , the same bleed arrives as income - the buyer's loss is the seller's slow gain. The closer you get to expiry, the faster this bleed runs. An option is a melting ice cube, and theta is the rate of melt. Part of what emptied Arjun's call was simply two days of time draining out of it.
## Vega - the volatility gauge
Vega answers: _how much does my option move when implied volatility changes?_ Implied volatility, or IV, is the market's expectation of how wildly price might swing. When the crowd expects big moves, IV rises and options get expensive. When the crowd calms down, IV falls and options get cheaper - regardless of where price actually is.
This is the second force that hurt Arjun, and the sneakier one. Before the RBI policy, everyone braced for a big move, so IV was puffed up and his call was pricey. The moment the announcement passed, the uncertainty cleared, IV collapsed - traders call this an "IV crush" - and the option deflated even though NIFTY had gone his way. **Vega can hurt you when price is flat, or even when price moves in your favour.** That is what makes it the gauge beginners never see coming.
## Gamma - the acceleration gauge
Delta is not a fixed number. As the underlying moves, delta itself changes. **Gamma** measures how _fast_ delta changes - it is the acceleration behind your direction risk.
Far from the strike price and far from expiry, gamma is small and gentle: your exposure shifts slowly and predictably. But near the strike on expiry day, gamma turns explosive. Your delta can lurch from near-zero to near-full in minutes, so your effective exposure swings violently on tiny price moves. One small tick and you are suddenly fully exposed; another and you are flat again. That is why expiry day is the least beginner-friendly day on the calendar - we will spend the whole next chapter on it.
What hurts you, and when price moves today DELTA wrong direction a day simply passes THETA every day for the buyer volatility jumps or drops VEGA even if price is flat near the strike at expiry GAMMA sudden acceleration Different gauges fire at different moments. Knowing which is which is half of options risk.
Key idea
The Greeks are not maths to solve - they are a dashboard of four risks. Delta hurts you on a move, theta hurts a buyer every day, vega hurts you on a volatility shift, and gamma hurts you with sudden acceleration near expiry.
## The whole dashboard in one table  
| Greek  | What it measures, in plain words  | Who it hurts most  |  
| --- | --- | --- |  
| Delta  | How much the option moves per 1-point move in the underlying - your real direction exposure now  | Anyone on the wrong side of a move  |  
| Theta  | How much value drains out each day just from time passing  | The option buyer, every single day  |  
| Vega  | How much the option moves when implied volatility rises or falls  | Buyers when IV crashes after an event; sellers when IV spikes  |  
| Gamma  | How fast your delta changes - the acceleration behind direction risk  | Anyone holding near the strike at expiry  |  
Common mistake
The classic beginner trap is watching only delta. You pick a direction, the underlying obliges, and you cannot understand why the option still bled. The answer is almost always theta or vega. Buying options right before a big event - results, policy, expiry - means you are buying when IV is highest and time is about to drain fastest. Even a correct direction call can lose to the IV crush and the daily melt. Read all four gauges, not just the one pointing the way you hope.
## Which Greek each type of trader fears most
The same dashboard reads differently depending on what you hold.  
| User type  | What they usually hold  | The Greek they fear most  |  
| --- | --- | --- |  
| Long-term investor  | Shares, not options  | None directly - Greeks rarely touch a buy-and-hold portfolio  |  
| Active trader  | Buys options for short bursts  | Theta - holding too long quietly bleeds the position dry  |  
| F&O / futures trader  | Leveraged directional positions  | Delta and gamma - leverage magnifies every move and its acceleration  |  
| Option seller  | Sells premium to collect theta  | Vega and gamma - an IV spike or an expiry-day lurch can dwarf the premium collected  |  
The option seller is the mirror image of the buyer. Theta, the buyer's daily enemy, is the seller's daily friend. But the seller takes on vega and gamma in return: a sudden volatility spike or a violent move near the strike can hand back many days of premium in one afternoon. None of this is personalised advice - it is a way to know which gauge to watch for the position you actually hold.
## When this fails
Treating the Greeks as a dashboard is the right starting point, but a dashboard has limits. First, the Greeks are estimates, not promises - they describe how an option _should_ react to a small, smooth change, and the market does not move in small, smooth steps. In a gap or a crash, several gauges move violently and at once, and the neat single-gauge story breaks down. Second, the Greeks interact. A big move changes delta (through gamma), which changes your exposure, while vega and theta are also shifting - so you can rarely blame one gauge cleanly. Third, knowing your Greeks does not size your position for you; a "small" theta on a large, leveraged book is still a large daily loss. The dashboard tells you _which_ risks you are carrying. It does not tell you whether you are carrying too much - that is position sizing, and no Greek will save an oversized bet. Use the gauges to understand your risk, never as a promise of how the option will behave on the worst day.
## Quick self-check
**1.** Arjun guessed direction correctly but still lost. Which two Greeks most likely cost him?
Theta and vega. He held for two days, so time value drained out (theta), and he bought before an event when implied volatility was high; once the event passed, IV crushed and the option deflated (vega) - even though NIFTY moved his way.
**2.** In one line, what does delta tell you?
Roughly how much your option's price moves for each 1-point move in the underlying - in other words, your real direction exposure right now. A higher delta means the option behaves more like the underlying itself.
**3.** Who does theta help and who does it hurt?
Theta hurts the option buyer every single day, because time value drains away whether or not price moves. The same drain is income for the option seller, and it speeds up as expiry approaches.
**4.** How can vega hurt you when the price has not moved at all?
Vega is volatility risk. If implied volatility falls - say after a big event passes - option prices deflate even with the underlying sitting still. A buyer who paid up for high IV before the event watches the option lose value purely from the IV drop.
**5.** Why is gamma the gauge that makes expiry day dangerous?
Gamma measures how fast delta changes. Far from expiry it is gentle, but near the strike on expiry day it turns explosive: your delta can swing from near-zero to near-full on tiny price ticks, so your exposure lurches violently and unpredictably. That is the focus of the next chapter.
On this page
