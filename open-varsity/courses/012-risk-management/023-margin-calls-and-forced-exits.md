Chapters
Module E · Leverage, Margin and Execution Risk - Chapter 23
# Margin Calls and Forced Exits
What margin means, why your broker squares you off, why forced exits happen at the worst prices, and why 'available margin' is not the same as usable capital.
Leverage
What you'll learn
  * ·What margin really is
  * ·Why brokers force-close
  * ·Forced exits at bad prices
  * ·Available vs usable margin
  * ·Peak-margin rules
  * ·Avoiding the square-off


Meera had Rs 1,00,000 in her account and her broker app showed "available margin" of about Rs 5,00,000 for intraday trades. To her, that number read like spending money. So one morning she used almost all of it, building a large position in a single index future. For an hour it drifted her way. Then a news headline hit, the index dropped sharply in minutes, and a red box appeared: _position squared off_. The broker had force-closed her trade automatically, near the bottom of the fall, at a price far worse than she would ever have chosen. She had not pressed sell. The system did it for her, and the loss was much bigger than the small wobble she thought she was risking.
Meera's mistake was not the trade idea. It was treating the big "available margin" number as capital, leaving no room for a normal swing. This chapter is about that exact trap: what margin really is, what a margin call is, why your broker can and will close your position, and how to keep the decision in your own hands instead of the system's.
## What margin really is
When you buy a stock for delivery, you pay the full price. When you take a leveraged position, an intraday trade or a futures contract, you do not pay the full value. You put down a deposit, and the broker lets you control a much larger position with it. That deposit is **margin**.
Margin is not the cost of the trade. It is a security deposit, like the advance you leave with a landlord. It sits there to cover losses if the trade goes against you. A NIFTY futures contract might control several lakh rupees of index value, but the margin to hold it could be roughly Rs 1,00,000 or so (exchanges revise the exact figure). That gap between the position's size and your deposit is leverage, and it is exactly why a small price move can swing your account hard.
## A margin call, in plain words
Your position's value moves every second. At the end of each day, and often through the day, the exchange marks your position to the latest price, this is called **mark-to-market** or M2M. If the trade is losing, that loss is deducted from your deposit. Your margin shrinks.
A **margin call** , or **margin shortfall** , happens when your remaining margin falls below the minimum the position needs. The broker asks you, in effect: _add money now, or reduce the position._ If you do neither in time, the broker acts for you. Think of your free margin as fuel in a tank. Trading losses burn it. When the gauge hits the red line, the engine cuts out, not when you decide, but when the fuel runs low.
Margin is a fuel tank - losses burn the buffer Margin blocked by the position free margin your buffer square-off line As the trade loses, M2M eats the green buffer from the right... buffer nearly gone - margin call If you do not add funds or cut the position, the engine cuts out for you. The buffer is small to start with. A normal swing can drain it fast.
## Why the broker squares you off, and at a bad price
The broker is not your enemy here. They lent you buying power, and they are legally and financially on the hook if your position loses more than your deposit can cover. So when the buffer runs out, they protect themselves by force-closing, or **squaring off** , your position. This is automatic. No phone call, no permission.
The cruel part is the timing. Margin runs low precisely when price is moving hard against you, in a fast, one-sided market. That is the worst moment to be a forced seller. Your own exit, a stop-loss you placed calmly in advance, would have triggered higher up. The broker's forced exit fires later and lower, into thin, panicky prices, so you take a bigger loss than your plan ever called for.
Your exit vs the broker's forced exit price time -> your planned stop - controlled exit broker's forced square-off - worse price extra loss The gap between a chosen stop and a forced exit is loss you never agreed to.
## "Available margin" is not spending money
This is the heart of Meera's error. The "available margin" your app displays is the most the broker will _let_ you deploy. It is a ceiling, not a target. Using all of it means your position is as large as the rules allow, with almost no buffer left to absorb the ordinary up-and-down that every position has. The first normal swing eats your tiny buffer and triggers a margin call.
Usable capital is smaller, and quieter. It is the size you can hold while still keeping a comfortable cushion of free margin, enough that a routine 1% or 2% wiggle does not put you anywhere near the square-off line. If a position can only survive when price moves your way immediately, it is too big.
Common mistake
Two linked mistakes sink beginners here. First, **treating "available margin" as capital** and deploying nearly all of it. Second, **ignoring the buffer** , forgetting that free margin is what absorbs normal swings, not idle money to be used up. The better move is to decide position size from your own risk rule first, then check that a comfortable slice of margin stays free afterward. The displayed maximum is a limit you stay well under, never a goal you fill to the brim.
## The India rules that matter
Three SEBI and exchange rules shape how this plays out on Indian markets, and beginners get caught by all three.
  * **Peak-margin rules.** SEBI requires the full margin to be collected upfront, and brokers must check your margin at random snapshots through the day, not just at entry. The deep intraday leverage of the old days is gone. If you are short of margin even briefly, a penalty can apply, and the broker tightens up fast.
  * **Intraday auto square-off near the close.** An intraday product (the high-leverage one) is meant to be closed the same day. If you do not exit, the broker's system auto-squares it off in a window before the closing bell, around mid-afternoon. You do not pick the price; the system sells into whatever the market is at that moment.
  * **M2M shortfall.** Through the day, mark-to-market losses are checked against your margin. If a sharp move opens an M2M shortfall, the broker can square you off immediately, well before any closing-time window. A fast adverse move does not wait for the afternoon.


Key idea
"Available margin" is a ceiling set by the broker, not capital you own. Use it all and you have no buffer, so a normal swing becomes a margin call and the broker force-closes your trade, at the worst possible price, on its schedule instead of yours.
## A checklist to avoid the forced exit
The whole game is keeping the exit decision in your hands. That means never running the buffer down to the red line. Before and during any leveraged trade:
  * I sized this position from my own risk rule, not from the "available margin" figure.
  * After entering, a comfortable slice of my margin is still free as a buffer.
  * I know roughly how far price can move before I get a margin call, and it is a long way off.
  * My own stop-loss sits well above any forced square-off level.
  * If margin runs low, I will add funds or cut the position myself, early, on my terms.
  * For intraday trades, I will exit before the broker's auto square-off window, not wait for it.
  * I never hold a position so large that an ordinary 1-2% swing threatens it.


This is education, not personalised advice. The right buffer depends on your capital, your instrument and how much movement it normally shows.
## Who actually faces margin calls
Margin calls are not equal across user types. Some people barely meet them; others live one fast move away from one.  
| User type  | Margin-call exposure  | Why  |  
| --- | --- | --- |  
| Long-term investor (delivery)  | Almost none  | Pays full price, no borrowed money, so there is nothing to be squared off  |  
| Active intraday trader  | Real, daily  | Uses leveraged products; a sharp move plus a thin buffer triggers M2M square-off, and the auto square-off window looms each afternoon  |  
| Futures / F&O trader  | High  | Leverage and daily mark-to-market mean losses hit the deposit fast; margin must be topped up or the position is cut  |  
| Option seller  | Highest  | Sells for a small premium but blocks large margin and faces rare, violent moves; a volatility spike can demand far more margin at the worst time, forcing an exit into a panic  |  
The pattern is clear: the more leverage you use and the more you sell rather than buy, the closer you live to a margin call. Option sellers especially should assume a buffer that looks "too big" on a calm day is exactly right for the day that is not calm.
## When this fails
Keeping a buffer reduces forced exits; it does not abolish them. A large overnight gap, a result, a policy surprise, can open the next session far below your buffer, so the M2M shortfall and the square-off both arrive before you can react, that is gap risk, and a buffer alone cannot fully cover it. In a violently fast market, even a forced exit can slip to a worse price than the square-off level suggests, because there may be few buyers there at all.
There is also a quieter failure: a buffer so large that you trade tiny and your costs and effort stop being worth it. The cure is not to abandon the buffer but to right-size the position to your real capital and the instrument's normal movement, loose enough to live, never so tight that ordinary noise calls your margin. And none of the example figures here are advice; they are a way of thinking. Your numbers depend on what you trade and what you can genuinely sit through.
## Quick self-check
**1.** What is margin, and how is it different from the cost of the trade?
Margin is a security deposit that backs a leveraged position, like an advance left with a landlord. It is not the price of the trade; it sits there to cover losses if the trade goes against you, while letting you control a much larger position than the deposit alone.
**2.** What is a margin call, and what happens if you ignore it?
A margin call, or margin shortfall, is when your remaining margin falls below what the position needs, usually because mark-to-market losses have eaten your buffer. You must add funds or reduce the position. If you do neither in time, the broker force-closes the trade for you.
**3.** Why does a forced square-off usually happen at a worse price than your own exit?
Margin runs low exactly when price is moving hard against you in a fast, one-sided market. Your own stop would have triggered higher up; the broker's forced exit fires later and lower, into thin panicky prices, so the loss is bigger than your plan called for.
**4.** Why is "available margin" not the same as usable capital?
Available margin is the ceiling the broker will let you deploy, not money you own. Using all of it leaves almost no free-margin buffer, so the first normal swing triggers a margin call. Usable capital is the smaller size you can hold while keeping a comfortable cushion.
**5.** Which type of trader faces margin calls most, and how should they respond?
Option sellers, because they block large margin for a small premium and face rare, violent moves and volatility spikes that suddenly demand more margin. They should keep a buffer that looks oversized on a calm day, since that is exactly the size needed on the day that is not calm.
On this page
