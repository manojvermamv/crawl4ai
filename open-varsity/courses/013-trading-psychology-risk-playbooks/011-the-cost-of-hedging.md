Chapters
Module B · Hedging: When, Why and When Not - Chapter 11
# The Cost of Hedging
Option premium, time decay, the bid-ask spread, taxes, brokerage, slippage, basis risk, margin and the upside you give up. Every hedge has a bill - here is how to read it before you pay it.
Hedging
What you'll learn
  * ·Premium and time decay
  * ·Spread, brokerage, taxes
  * ·Basis and tracking risk
  * ·Margin on the hedge
  * ·Giving up upside
  * ·Total cost of protection


Meera holds a calm, long-term portfolio of Rs 5,00,000. Early last year a scary headline rattled her, so she did the responsible-sounding thing: she started buying a one-month NIFTY put every month to "sleep better". The market drifted sideways and slightly up the whole year - no crash, no drama. At year-end she totted up every premium she had paid and went pale. She had spent close to Rs 90,000 protecting a portfolio that was never seriously in danger. The insurance was real. So was the bill - and it had quietly eaten most of her gains.
That is the lesson of this chapter. A hedge is not free safety. It is a product you buy, with a price tag, and you should read that price tag before you pay it.
## A hedge is a product, and it has a price
In the last two chapters you saw what hedging does and when you might want it. Now the honest part: every hedge costs money, and the cost shows up in more places than the beginner expects. Insurance on your scooter has a premium you can see. A market hedge has a premium too, plus a handful of smaller charges that hide in the corners. Add them up and a "cheap" hedge is often not cheap at all. The point is not to scare you off hedging - it is to make you a buyer who knows the total bill, so you only pay it when the risk is genuinely large and genuinely real.
## The eight costs hiding in every hedge
A protective put - the simplest hedge, an option that pays you if the market falls - carries roughly eight separate costs. Some are obvious. Most beginners only notice the first one.
**1. Option premium.** The upfront price of the put. This is the big one. A one-month put that protects close to today's level typically costs somewhere around 1.5% to 2% of the value you are protecting. On Rs 5,00,000 that is roughly Rs 7,500 to Rs 10,000 - gone the moment you buy, whether or not the market ever falls.
**2. Time decay (theta).** A long option loses a little value every single day, just from time passing. That premium you paid melts away as expiry approaches. If the crash never comes, the put expires worthless and the entire premium becomes a realised loss. Theta is simply the daily drip of that same premium draining out.
**3. The bid-ask spread.** You buy at the higher "ask" price and, when you exit, you sell at the lower "bid" price. The gap between them is a cost you pay twice - once getting in, once getting out - and it is wider on far-dated or less-traded strikes.
**4. Brokerage, STT and other charges.** Every hedge leg is an order, and orders carry brokerage, exchange fees, GST and Securities Transaction Tax. Individually small, but real, and they repeat every time you roll the hedge to a new month.
**5. Slippage.** The price you see and the price you actually get are not the same, especially in a fast or thin market - which is exactly when you tend to buy protection. The difference is slippage, an invisible tax on top of the spread.
**6. Basis and tracking risk.** If you hedge a basket of specific stocks with a NIFTY index put, the index and your stocks do not move in lockstep. The index can hold up while your stocks fall - so your hedge pays little while your portfolio bleeds. That mismatch is basis risk, and it means the protection you paid for may not fully fire when you need it.
**7. Margin tied up in a futures hedge.** If you hedge by shorting a futures contract instead of buying a put, you do not pay a premium - but you must park margin money with the exchange, and that capital is blocked and cannot work elsewhere. A sharp move against the short can also trigger a margin call mid-hedge.
**8. Missed upside.** Some hedges, like a collar or a covered call, lower your cost by capping your gains. You give up the big up-move in exchange for cheaper protection. If the market rallies hard, the "saving" can cost you far more than the premium you avoided.
The hedge bill stacks up - one month, Rs 5,00,000 protected Option premium Rs 7,500 Bid-ask spread ~Rs 400 Brokerage + STT ~Rs 200 Slippage ~Rs 200
Cost stacks All-in ~Rs 8,300 about 1.6% / month
The premium is only the headline. The small charges stack on top - and repeat every roll.
The premium and theta are two views of the same money: theta is the speed at which the premium you paid quietly disappears.
Time decay: the premium melts if the crash never comes Premium paid: Rs 7,500 Expiry: Rs 0 Buy Expiry day decay speeds up near the end If the market sits still, a long-option hedge bleeds to zero - faster in its final days.
## A worked example: insuring Rs 5,00,000 for a month
Say you want to protect a Rs 5,00,000 equity portfolio for one month using an index put. Here is the full bill, with round, illustrative numbers - your real figures will vary with the market and your strike.  
| Cost item  | What it is  | One-month rupee cost  |  
| --- | --- | --- |  
| Option premium (~1.5%)  | The put itself - the protection you buy  | Rs 7,500  |  
| Bid-ask spread  | Paid on entry and again on exit  | ~Rs 400  |  
| Brokerage + exchange + GST  | Charges on the hedge order legs  | ~Rs 150  |  
| STT and other statutory fees  | Tax on the option transaction  | ~Rs 100  |  
| Slippage  | The gap between screen price and fill  | ~Rs 200  |  
| **All-in for one month**  | **Total cost of protection**  | **~Rs 8,350 (about 1.7%)**  |  
So the true price of one month of cover is closer to 1.7% than the 1.5% the premium alone suggested. Pay it once before a known, scary event and that is reasonable insurance. But watch what happens if you do it every month, like Meera: roughly 1.7% a month, rolled twelve times, is on the order of 18% to 20% a year - even in a year where nothing bad happens. You can spend a fifth of your portfolio's value insuring against a fall that never arrives.
Key idea
Every hedge has a bill, and the premium is only the top line. The all-in cost - premium, time decay, spread, charges, slippage, basis risk, blocked margin and capped upside - is what you actually pay. Read the whole bill before you buy the protection.
## Protection versus cost: when the bill is worth paying
A hedge is worth its cost only when the risk you are removing is both real and large relative to that cost. Paying 1.7% to protect against a genuine, near-term threat to a big portfolio can be smart. Paying the same 1.7% every month out of vague worry, when no specific danger is in sight, is just slowly handing your gains away.
When the hedge is worth its price Worth it cost large, real risk small bill buys away a big, near-term danger Not worth it cost vague worry same bill, paid again and again, for no real danger Same price tag. The risk on the other side of the scale is what decides if it is worth paying.
Common mistake
The two classic errors are rolling hedges forever and ignoring the all-in cost. Rolling a put month after month "just in case" bleeds theta and charges every cycle, so a calm, rising year still ends with a big hole - exactly Meera's Rs 90,000. And quoting only the premium ("it's just 1.5%") hides the spread, slippage, taxes and capped upside that push the real cost higher. The better move: name the specific risk and its window, price the whole bill, and only hedge when the danger is real and large - otherwise consider simply trimming the position instead.
This is education, not advice on a specific trade. The numbers here are illustrations to teach the shape of the cost, not a recommendation to buy or skip any particular hedge.
## How the cost of hedging differs by seat
The same costs land differently depending on the seat you sit in.  
| User type  | Where the cost bites most  | The honest call  |  
| --- | --- | --- |  
| Long-term investor  | Premium and repeated rolls drain steady SIP gains  | Usually do not hedge a long horizon; ride out falls, or hedge only around a known big event  |  
| Active (cash) trader  | Spread, slippage and brokerage on every protective leg  | Often cheaper to cut or size down the position than to buy a put  |  
| F&O (futures) trader  | Margin blocked on the hedge leg and basis risk  | Weigh tying up capital against the move you fear; a tight stop may be cheaper  |  
| Option seller  | Buying protection eats the premium they collected  | A protective wing lowers income but caps the tail loss - price both sides before selling  |  
## When this fails
Reading the cost of a hedge is essential, but cost-counting alone can mislead you.
It fails when you let the bill talk you out of protection you truly need. A real, large, near-term risk to a big portfolio can justify paying up. Skipping a worthwhile hedge just because "1.7% feels like a lot" is how a small premium turns into a catastrophic loss.
It fails when the numbers are guesses. Real premiums move with volatility - protection gets dramatically more expensive precisely when fear is high and a crash looks likely. The 1.5% in calm times can be 4% or 5% in a panic, so price the hedge for the conditions you are actually in.
It fails when basis risk is bigger than you assumed. An index hedge on a portfolio of small or mid-cap stocks can pay almost nothing while your holdings fall hard. A cheap hedge that does not fire is not a saving - it is money lost twice.
And it fails as a substitute for sizing. If a position is so large that the only way to sleep is to hedge it every month, the deeper problem is the position size, not the missing hedge - and the cheapest, cleanest protection is often owning less in the first place.
## Quick self-check
**1.** Besides the option premium, name three other costs hidden in a protective put.
Any three of: time decay (theta), the bid-ask spread on entry and exit, brokerage and exchange charges, STT and statutory fees, slippage, basis or tracking risk, margin blocked on a futures hedge, and missed upside from a cap. The premium is only the headline cost.
**2.** Meera's portfolio rose slightly all year, yet hedging cost her about Rs 90,000. How?
She bought a fresh one-month put every month at roughly 1.5% to 1.7% of a Rs 5,00,000 portfolio. Rolled twelve times with no crash to pay off, the premiums and charges added up to nearly a fifth of the portfolio's value - theta bleed with nothing to show for it.
**3.** What is basis risk, and why does it make a hedge cost more than it looks?
Basis risk is the mismatch between your hedge and what you actually hold - for example, a NIFTY index put against a basket of specific stocks. The index can hold up while your stocks fall, so the hedge pays little when you need it most. You paid for protection that did not fully fire.
**4.** When is paying around 1.7% for a month of protection a reasonable cost?
When the risk being removed is both real and large relative to that cost - for instance, a known, near-term event that could badly hurt a sizeable portfolio. Paying the same amount every month out of vague worry, with no specific danger in sight, slowly hands your gains away.
**5.** A beginner says "the hedge is cheap, it's only the 1.5% premium." What is wrong with that?
The premium is just the top line. The all-in cost also includes the bid-ask spread, brokerage, STT, slippage, any basis risk, blocked margin and capped upside. Counting only the premium understates the real bill - and that bill repeats every time the hedge is rolled.
On this page
