Chapters
Module F · F&O Risk for Beginners - Chapter 29
# Option Buyer Risk
Limited loss, but a low probability of winning. Premium decay, being right on direction but wrong on timing, IV crush, and the overtrading of cheap options that quietly drains an account.
Options
What you'll learn
  * ·Limited loss, low odds
  * ·Premium time decay
  * ·Right direction, wrong timing
  * ·IV crush after events
  * ·The cheap-option trap
  * ·Buying options with discipline


Every Thursday morning, Arjun did the same thing. He opened his trading app, looked at the NIFTY weekly options, and bought a far out-of-the-money call for Rs 6. "It's only Rs 6," he told himself. "One lot is about 65, so that's Rs 390. If NIFTY runs today, this Rs 6 becomes Rs 60 and I make ten times my money." Most Thursdays it expired worthless. A few times it did pop, and those wins felt amazing. But at the end of three months, Arjun added it all up. He had won four times and lost nine. The four wins were nice. The nine quiet losses had eaten more than the wins paid. He had not blown up in one bad trade. He had bled out, Rs 390 at a time.
This chapter is about the trap Arjun fell into. Buying an option feels like the safe corner of F&O, because your loss is capped. And it is capped. But "limited loss" hides a low chance of winning, and three quiet killers that drain buyers slowly: time decay, bad timing, and IV crush.
## The good news first: your loss is limited
When you _buy_ an option, you pay a premium up front, and that premium is the most you can ever lose. A call option is a bet that price rises; a put option is a bet that price falls. Pay Rs 390 for one NIFTY lot (the lot size is around 65 units and is revised periodically by the exchange - always check the current contract specs), and Rs 390 is the floor. The market can crash or rip, and you still lose only what you paid. No margin calls, no owing more than you put in. That makes it one of the most loss-limited beginner structures in F&O, and it is why beginners are told to start here.
Buying a call: loss is capped, but the floor is the whole premium profit loss strike breakeven = strike + premium max loss = the premium you paid profit only out here price has to clear the strike AND the premium Your loss is limited to the premium. But price must travel past the strike and past the premium just to break even.
Look at where profit actually starts. Price does not just have to move your way. It has to clear the strike _and_ the premium you paid, before expiry. That gap between "I was right about direction" and "I made money" is where most buyers get trapped and lose.
## Killer one: time decay (theta)
An option's premium has two parts. One part is real, in-the-money value. The other is _time value_ - what you pay for the hope that price moves your way before expiry. That hope has an expiry date, and it leaks away a little every single day, even if the stock does nothing at all. This daily leak is called **theta** , or time decay.
Here is the cruel part: decay is not steady. It speeds up as expiry approaches. A weekly option held over a quiet week does not lose value in a straight line - it holds up early, then falls off a cliff in the last two or three days. The cheap out-of-the-money weeklies Arjun loved are almost _all_ time value, so they are almost all decay. Every hour NIFTY sits still, his Rs 6 melts toward zero.
Time decay is not steady - it accelerates near expiry premium 30 days left 7 days left expiry decay fastest here slow leak early The same option loses far more value in its final three days than in its first three weeks.
Key idea
When you buy an option, time is your enemy. Every day price stays still, you lose money - and the loss speeds up as expiry nears. To win, you do not just need to be right. You need to be right _soon enough_ and _big enough_ to beat the decay.
## Killer two: right on direction, wrong on timing
This one stings the most, because you were _right_. You buy a NIFTY call because you think the index will rise. You are correct - it does rise. But it rises next week, after your weekly option already expired worthless this Thursday. Or it dips first, bleeds your premium to near zero, _then_ rallies. Your view came true. Your option was dead before it could pay you.
A stock can rise 4% over a month and still hand a string of weekly call buyers nothing but losses, because each week the move was too small, too slow, or arrived after that week's option expired. Direction is only half the bet. With a bought option you are also betting on _timing_ , and timing is far harder to get right than direction.
## Killer three: IV crush after an event
This is the one beginners never see coming. **Implied volatility** (IV) is the market's expectation of how much price will swing. When a big event is near - company results, the Union Budget, an RBI decision - everyone expects a large move, so option premiums get pumped up with extra IV. The option is _expensive_ precisely because the crowd is bracing for fireworks.
You buy a call before the results, expecting a big jump. The results come out. The stock does move up a little - you were right on direction. But the _uncertainty is now gone_ , so IV collapses, and that inflated premium deflates with it. Your option can lose value even though price moved your way, because the air came out of the premium. This is **IV crush** , and it is why buying options right before a known event so often loses even when your view is correct.
IV crush: right on direction, premium still drops Rs 90 before result Rs 55 after result (price up a bit) premium falls volatility / time value (vanishes) real in-the-money value The orange volatility value is what you overpay for before an event. When the event passes, it deflates.
Common mistake
Two classic buyer mistakes. The first is **buying cheap far-out-of-the-money "lottery" options** - "it's only Rs 5" - again and again. They expire worthless far more often than they pay, and the steady stream of small losses quietly outweighs the rare wins. The second is **buying right before a big event for the "obvious" big move** - results, Budget, RBI day - when IV is already pumped. Even if you are right on direction, IV crush can shrink your premium. The better move: buy fewer, closer-to-the-money options, give yourself more time to expiry, and avoid paying inflated pre-event premiums.
## A checklist for sane option buying
Before you buy any option, walk through this. If you cannot tick most boxes, skip the trade.
  * Do I know the _exact_ premium in rupees I am risking, and am I fine losing all of it?
  * Is this a small, sane part of my account - not a position I would repeat ten times a week?
  * Am I buying something close to the money with real value, not a cheap far-OTM lottery ticket?
  * Have I given myself enough _time to expiry_ for my view to play out, instead of a 1-2 day weekly?
  * Is IV unusually high because an event is near? If so, am I knowingly overpaying?
  * Do I have a price or time exit - "I sell if it halves, or by Wednesday" - not just "hope till expiry"?


## How an option buyer's risk compares
The same market move means very different things depending on what you are.  
| User type  | What they hold  | Main risk  | Worst case  |  
| --- | --- | --- | --- |  
| Long-term investor  | Shares, owned outright  | Price falls, but you can wait years  | Paper loss until you sell; company can sink  |  
| Stock trader  | Shares, short-term  | Price moves against the trade  | Loss to your stop (gaps aside)  |  
| F&O futures trader  | A leveraged futures position  | Leverage magnifies every move, both ways  | Large loss, margin calls, can exceed deposit  |  
| Option **buyer**  | A paid-for premium  | Time decay, bad timing, IV crush; low win rate  | The full premium, but no more  |  
| Option **seller**  | Premium collected up front  | Rare, large, open-ended loss  | Many times the premium received  |  
Notice the buyer and the seller are mirror images. The buyer has a _capped_ loss but loses _often_ (decay works against them). The seller wins _often_ but carries a _rare, large_ loss (decay works for them). Neither is "safe" - they just fail in opposite ways. This is education, not advice; size every position so that being wrong is survivable.
## When this fails
The honest limit of this chapter: doing everything right can still lose, because time and volatility are working against a buyer by design. You can pick the right direction, buy a sensible at-the-money option, avoid the event, give yourself weeks - and still lose if the move is too small or too slow to beat the decay you are paying. That is not a mistake you made; it is the structural cost of being a buyer. Buying options is best thought of as paying for a defined, limited bet with a real chance of total loss on that bet - useful for cheap, capped exposure to a sharp move you genuinely expect soon, and poison when it becomes a weekly habit. Most option buyers do not blow up in one trade. They lose slowly, one Rs 390 ticket at a time, to decay and IV - exactly the way Arjun did. The defence is fewer, better-chosen buys, not more of them.
## Quick self-check
**1.** When you buy an option, what is the most you can lose?
The premium you paid, and no more. Buy one NIFTY lot for Rs 390 and Rs 390 is the floor - no margin calls, no owing extra. That capped loss is the real advantage of being a buyer.
**2.** What is theta, and why does it hurt buyers?
Theta is time decay - the daily leak of an option's time value, even if price does nothing. It hurts buyers because it speeds up near expiry, so a held option loses far more in its final days than at the start. To win you must be right soon enough to beat the decay.
**3.** You bought a call, the stock did rise, but you still lost. How?
Two common reasons. Your timing was off - it rose after your option expired, or too slowly to clear the strike plus premium. Or IV crush hit: you bought before an event with inflated premium, and when the event passed, volatility value collapsed even though price moved your way.
**4.** Why are cheap far-out-of-the-money weekly options a trap?
They are almost entirely time value, so they are almost entirely decay, and they expire worthless far more often than they pay. "It's only Rs 5" feels harmless, but repeated week after week the small losses quietly outweigh the rare big wins - a slow bleed, not a blow-up.
**5.** How do an option buyer and an option seller fail differently?
They are mirror images. The buyer has a capped loss but a low win rate, because decay and IV work against them and they lose often. The seller wins often but carries a rare, large, open-ended loss. Neither is truly safe - they fail in opposite ways, so size both so being wrong is survivable.
On this page
