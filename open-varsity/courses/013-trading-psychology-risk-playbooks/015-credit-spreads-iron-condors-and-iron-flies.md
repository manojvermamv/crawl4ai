Chapters
Module C · The Option-Seller & Hedger Playbook - Chapter 15
# Credit Spreads, Iron Condors and Iron Flies
How these defined-risk structures reduce risk, where they still fail, and why - for a seller - the maximum loss matters far more than the maximum profit. With clear payoff diagrams.
Options
What you'll learn
  * ·Credit spread basics
  * ·Iron condor and iron fly
  * ·Where structures fail
  * ·Max loss vs max profit
  * ·Probability vs payoff
  * ·Choosing strikes sensibly


Meera started selling iron condors on NIFTY almost every week. The idea felt almost too good. As long as the index stayed inside a wide range, she kept the premium. For four months it worked. Small win, small win, small win - around Rs 4,000 most weeks. Her account climbed steadily and she began to think she had found a machine. Then came a budget-week rally. NIFTY trended hard in one direction for three sessions and ran straight past her call strikes. That single week cost her about Rs 28,000 - nearly every rupee the previous six wins had made. The strategy had not broken. She had simply met the loss it was always capable of.
In the last chapter you saw why a spread is safer than a naked short: it caps your loss up front. This chapter takes the three structures a beginner actually meets - the credit spread, the iron condor and the iron fly - and shows their payoff shapes in plain pictures. No pricing maths. Just where you make money, where you lose it, and the one number that decides everything.
## The credit spread: sell one, buy a cheaper one further out
A credit spread is two options of the same type, sold and bought together. You sell an option that is worth more and buy a cheaper one further away. The difference in their prices lands in your account as a net credit - and that credit is the most you can make. The option you bought is your seatbelt: it caps how much a big move can cost you.
There are two mirror versions. A **bull put spread** is sold below the market: you sell a put and buy a cheaper put lower down. You keep the credit as long as the index stays above your short put. A **bear call spread** is the same idea above the market: you sell a call and buy a cheaper call higher up, and you keep the credit as long as the index stays below your short call. One leans bullish, one leans bearish. Both win if the index simply does not move against you too far.
A credit spread (bull put): capped profit, capped loss 0 Long put (buy, lower) Short put (sell, higher) Max loss (capped) Max profit = the credit Index level → You keep the small credit if the index stays above your short put; the bought put caps the loss if it falls.
## The iron condor: two spreads, one range
Put a bull put spread below the market and a bear call spread above it at the same time, and you have an **iron condor**. You have sold a range. As long as the index finishes between your two short strikes, both spreads expire worthless and you keep both credits. That flat green middle is your profit zone. Step outside it on either side and one spread starts to lose, until your loss is stopped by the wing you bought on that side.
The condor's appeal is obvious: markets spend a lot of time going nowhere, and a condor pays you for exactly that. Its trap is just as real. The profit zone is wide and comfortable, which makes the trade feel safe - but "feels safe" and "is safe" are different things, as the loss tail will remind you.
Iron condor: a flat profit zone in the middle, capped losses on the wings 0 Long put Short put Short call Long call Max profit (both credits) Profit zone: index stays here Max loss Max loss A condor wins if the index simply stays inside the middle range - and loses a capped amount on either wing.
## The iron fly: same idea, tighter
An **iron fly** (iron butterfly) is a condor pulled into the centre. Instead of two separate short strikes with a gap between them, you sell the put and the call at the _same_ strike - usually right near the current price - and buy a wing on each side for protection. Because you are selling at-the-money options, you collect a much larger credit. But the profit zone shrinks to a narrow tent around that one strike. You earn more if the index pins close to where it started, and you give it back if it drifts even moderately. A condor bets on a range; a fly bets on stillness.
## The structures, side by side  
| Structure  | What you sell / buy  | Profit zone  | Max profit vs max loss  |  
| --- | --- | --- | --- |  
| Bull put spread  | Sell a higher put, buy a cheaper lower put  | Index stays **above** the short put  | Small capped credit vs a larger capped loss  |  
| Bear call spread  | Sell a lower call, buy a cheaper higher call  | Index stays **below** the short call  | Small capped credit vs a larger capped loss  |  
| Iron condor  | A bull put spread **plus** a bear call spread  | Index stays **between** the two short strikes  | Two small credits vs a larger capped loss on either side  |  
| Iron fly  | Sell put and call at the **same** strike, buy a wing each side  | Index **pins near** that one strike  | Bigger credit vs a narrow, harder-to-keep zone  |  
Notice the pattern in the last column. In every one of these, the credit you collect is smaller than the loss you can take. That is not a flaw you can shop your way around - it is the price of winning often.
## The one number that matters: max loss, not max profit
Win small, often. Lose big, rarely. Six wins x about Rs 4,000 = +Rs 24,000 One loss: about Rs 28,000 Net result -Rs 4,000 after a winning run A high win rate is not the same as making money: one full loss can wipe out six wins.
Here is the heart of it. These structures are built to win often. The index stays in your range most weeks, so you collect your small credit again and again, and the wins start to feel routine. But look at the _size_ of each result. A typical condor might risk Rs 28,000 to make Rs 4,000. You can be right six or seven times and a single loss erases the lot. A high win rate is not the same as making money. What keeps you solvent is whether the rare loss is survivable - and that is decided entirely by your max loss, a number you know the moment you put the trade on.
Key idea
For a defined-risk seller, the maximum loss matters far more than the maximum profit. These trades usually win, but one full loss can wipe out several wins - so size the position by what you lose when you are wrong, never by what you collect when you are right. (Education, not advice.)
Common mistake
The classic beginner move is to widen the condor's strikes to push the win rate higher - "the index will never get all the way out there." It is true that a wider range wins more often. But widening the short strikes while keeping the same wings makes the _loss_ bigger too, so you are now risking even more to collect the same small credit. Chasing a 90% win rate by quietly growing your max loss is exactly how a string of green weeks ends in one red week that takes it all back. Judge a condor by its worst case, not its hit rate.
## How this differs by who you are  
| User type  | Do these structures fit?  | What to watch  |  
| --- | --- | --- |  
| Long-term investor  | Rarely - this is a trader's tool, not an investing one  | Time and attention; a condor needs managing, an SIP does not  |  
| Active (directional) trader  | Sometimes, to express a "stays in a range" view  | You are now betting on no move - the opposite of a trend trade  |  
| F&O (futures) trader  | A natural step from futures into defined-risk options  | Four legs means four sets of charges and slippage eating the small credit  |  
| Option seller  | The bread-and-butter structures  | Max loss per trade, and total risk across all open condors at once  |  
## When this fails
Two ways, mainly - and it is worth being honest about both.
**A big, fast move blows past your protection.** Your bought wing caps the loss, but it does not erase it - and that cap is several times your credit. A gap on a result day or a budget surprise can take the index clean through both your short and your long strike before you can react. You lose the full, capped amount. That was Meera: one trending week, one max loss, six wins gone.
**The index pins right at your short strike at expiry.** This is the quiet nightmare. Indian index options are cash-settled, so there is no US-style early assignment to worry about - the risk is the expiry settlement itself. If NIFTY closes exactly at or near your short strike, you are caught in "pin risk": you cannot be sure on which side it will settle, your protective long leg may expire worthless while the short is settled against you in cash, and the result can land as a next-session surprise. On stock options and stock futures it is sharper still, because expiry can mean physical delivery of shares. Closing the position before expiry, instead of letting it settle on the strike, avoids most of this.
And then the slow leak. Every condor has four legs. Four legs mean four sets of brokerage, STT and exchange charges, plus slippage on the way in and the way out. On a trade whose whole edge is a Rs 4,000 credit, friction is not a rounding error - it is a real bite out of every win, while the losses stay full size.
Heads up
Defined risk means your loss is _known and capped_ - it does not mean small. "Maximum loss Rs 28,000" is still defined risk. Make sure that capped number is one your account can absorb several times in a row, because over enough trades it will happen.
## Quick self-check
**1.** What is a credit spread, in one line?
Two options of the same type: you sell a dearer one and buy a cheaper one further out, keeping the net credit, with your loss capped by the option you bought.
**2.** How is an iron condor built, and when does it make its maximum profit?
It is a bull put spread below the market plus a bear call spread above it. It makes its full profit when the index finishes between the two short strikes, so both spreads expire worthless and you keep both credits.
**3.** What is the main difference between an iron condor and an iron fly?
A condor sells two separate strikes with a gap, giving a wide profit zone but a smaller credit. A fly sells both options at the same strike, giving a bigger credit but a narrow profit zone - it needs the index to sit almost still.
**4.** Why can a 90% win rate still lose money?
Because the max loss is usually several times the max profit. Many small wins can be erased by one full loss, so the win rate alone tells you nothing about whether the strategy makes money - the size of the loss does.
**5.** Name the two main ways these structures fail.
A big, fast move runs past your protection and hands you the full capped loss; or the index pins right at a short strike at expiry, creating pin and settlement risk. On top of both, charges on four legs quietly erode the small wins.
On this page
