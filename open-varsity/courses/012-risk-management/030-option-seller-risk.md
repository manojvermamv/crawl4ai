Chapters
Module F · F&O Risk for Beginners - Chapter 30
# Option Seller Risk
Small frequent profits and rare, large losses. Why 'high probability' is not the same as 'low risk', what the loss tail really looks like, and the respect option selling demands.
Options
What you'll learn
  * ·The seller's payoff shape
  * ·High probability vs low risk
  * ·The fat loss tail
  * ·Margin and assignment
  * ·Why sellers blow up
  * ·Selling with defined risk


Arjun found option selling in his fourth month of trading, and for a while it felt like he had found a cheat code. Every week he sold a far-away option, collected a small premium, and watched it quietly expire worthless. Win. Win. Win. Eleven weeks, around Rs 2,000 a week, and not a single loss. So he did the natural thing: he doubled his size, then doubled it again, because this clearly _worked_. On the twelfth week the index gapped hard at the open, his sold option exploded in value, and a single morning erased every rupee of those eleven wins and a big chunk of his capital on top. Nothing about his method had changed. The market had simply shown up for the one day his method had no answer for.
This chapter is about that trade: the one where selling options feels like collecting free money right up until the bill arrives all at once.
## The seller sits on the other side
When you _buy_ an option, you pay a premium for the right to a big move. When you _sell_ (or "write") an option, you are the other side of that bet. You collect the premium up front, and in exchange you take on the obligation. Most of the time the big move does not come, the option you sold loses its value, and you keep the premium. That is the whole appeal: you get paid for the moves that _do not_ happen, and most moves do not happen.
But look at the shape of what you signed up for. Your best case is fixed and small - the premium, nothing more. Your worst case is far larger - theoretically unlimited for a short call, and very large for a short put. If the market runs against you, the option you sold keeps getting more expensive, and your loss keeps growing with it. You collected, say, Rs 80 a share. You can never make more than that Rs 80. You can lose Rs 200, Rs 400, far more, with very little to stop it.
What you sign up for when you sell an option price of the index at expiry profit loss strike you sold breakeven max profit = premium (capped) loss has no floor A small flat win on one side, an open-ended loss on the other. That trade-off never changes.
## High probability is not low risk
Here is the trap that catches almost every beginner. A sold option that is far from the current price will _probably_ expire worthless. You might win nine times out of ten. That high win rate feels like safety. It is not. Winning often and losing rarely tells you nothing about _how much_ you lose on the rare day.
Think in plain rupees. Say you win Rs 2,000 about nine times for every one time you lose, but the loss, when it lands, is Rs 40,000. Your win rate is a glorious 90%. Your average outcome per trade is still negative: nine wins of Rs 2,000 is Rs 18,000, wiped out by a single Rs 40,000 loss, leaving you Rs 22,000 _poorer_ over ten trades. The scoreboard says you win almost always. The bank balance says you are bleeding.
A 90% win rate that loses money win Rs 2,000 - 90% of the time 10% lose - Rs 40,000 Average per trade: 0.9 × (+2,000) + 0.1 × (−40,000) = +1,800 − 4,000 = − Rs 2,200 per trade example numbers Being right often is not the same as making money. The size of the rare loss decides everything.
Key idea
High probability is not the same as low risk. A trade that wins nine times out of ten can still ruin you if the one loss is many times bigger than the nine wins. Sellers get paid often and small, and pay rarely and large - so the rare day is the only one that matters.
## The loss tail
That rare, oversized loss has a name worth remembering: the _tail_. Most of your results cluster in a happy little pile of small wins. Then, far out on the edge, sits a single result so large it swallows the whole pile. Your equity curve as a seller does not look like a smooth climb. It looks like a gentle staircase up, followed by a cliff.
Ten small wins, then one cliff starting capital ten wins, +Rs 2,000 each one loss −Rs 40,000 ends below where it began The staircase feels like skill. The cliff is the real risk you were carrying the whole time.
## Margin and settlement
Selling options is not free to hold. Because your loss can run very large, your broker demands _margin_ - a large block of your capital frozen as security against the position. A single sold index option can lock up far more capital than the premium you collected, and that requirement can _rise_ during the day if the market turns volatile, squeezing you exactly when things are going wrong.
There is also _settlement_. As a seller you carry an obligation you cannot simply walk away from. For Indian index options, expiry is cash-settled - the in-the-money value is paid in cash. For stock options and stock futures, expiry can mean physical settlement: actual delivery of shares, which ties up far more money. The real beginner risk here is not US-style early assignment - it is expiry settlement: a physical-delivery obligation in stock F&O, margin pressure as expiry nears, and simply not knowing what happens if you leave a position open at expiry. The rule is simple: if you do not fully understand settlement, close the position before expiry. The premium was the easy part; the obligation is the part that bites.
Common mistake
The classic blow-up has two stages. First, **selling naked** - an unhedged sold option with nothing capping the loss - because the premium looks like easy income. Second, **sizing up after a winning streak** , doubling lots because it "keeps working", which simply guarantees that you are carrying your largest position on the day the tail finally arrives. The better move: never sell naked as a beginner, and keep your size _constant_ through a winning streak, not growing. A streak of wins is not proof of safety; it is just the part of the cycle before the cliff.
## Buyer versus seller: the shape is flipped
A seller is, in almost every way, the mirror image of a buyer. The buyer pays small and rarely wins big. The seller collects small and rarely loses big. Neither is "safer" - they are opposite risk shapes, and you must respect whichever one you are holding.  
| Aspect  | Option buyer  | Option seller  |  
| --- | --- | --- |  
| Cash up front  | Pays the premium  | Collects the premium  |  
| Best case  | Large, open-ended gain  | Small, capped (the premium)  |  
| Worst case  | Limited - you lose the premium  | Large - unlimited for a call, very large for a put  |  
| How often you win  | Often loses small  | Often wins small  |  
| Margin needed  | None beyond the premium  | Large block frozen, can rise  |  
| Where the danger lives  | Slow bleed from many small losses  | One rare, giant loss (the tail)  |  
| Feels like  | Buying lottery tickets  | Collecting free money  |  
## How each participant meets tail risk
Tail risk - the rare giant loss - is not only a seller's problem. It lands differently on each kind of participant, but the seller is the one most exposed to it by design.  
| User type  | Usual risk shape  | Hidden danger  | First defence  |  
| --- | --- | --- | --- |  
| Long-term investor  | Many small gains over years  | A crash drawing down the whole portfolio  | Diversify, hold quality, never use borrowed money  |  
| Active trader  | Mix of wins and losses with stops  | A gap that jumps the stop  | Cut size into events, do not trust stops on gaps  |  
| F&O / futures trader  | Leveraged, linear up and down  | Leverage turning a normal move into a wipeout  | Tiny lots, real margin buffer, no overnight leverage into events  |  
| Option seller  | Frequent small wins, rare huge loss  | The tail - one move that erases months  | Define the loss in advance; never sell naked  |  
## Start with defined risk, never naked
The honest beginner version of option selling is the _defined-risk_ version. Instead of selling an option alone with an open-ended loss, you also buy a cheaper, further-away option that caps how bad the loss can get. This pairing - a spread - turns the bottomless drop into a known, fixed worst case. You collect a little less premium, and in return your worst case is a known, fixed loss instead of a bottomless one - as long as you size that defined loss so that even a run of them is survivable. The full mechanics of spreads belong to a later options course; for now, the rule is simply: if you are going to sell, sell with a defined loss, not a naked one.
Before any sold position, run a short check:
  * Is my loss _defined_ (a spread) or open-ended (naked)? Beginners pick defined.
  * Do I know the exact rupee worst case before I enter?
  * Have I kept size the same as last week, not bigger after wins?
  * Can I survive this worst case landing on a gap-down or gap-up morning?
  * Is the margin frozen here money I can genuinely spare?


This is education, not advice: it is a framework for thinking about seller risk, not a recommendation to sell options or a personalised position size.
## When this fails
Everything above assumes the market gives you orderly conditions to manage your position. The day it does not is the day this whole game changes - and that day is the gap and the volatility explosion from Chapter 24. When the index gaps far overnight, a sold option does not drift to a worse price you can react to; it _reopens_ deep in-the-money, and your loss is already booked before you can touch it. Worse, a shock makes options themselves more expensive across the board (volatility spikes), so the option you sold for Rs 80 can be worth Rs 500 not only because price moved but because fear repriced every option at once. The two punches land together. A defined-risk spread survives this because its loss was capped from the start. A naked short does not - it is the single position most likely to convert a quiet, winning quarter into a margin call and a blown account on one bad morning. That is the whole reason a beginner should never sell naked: not because the move is likely, but because when it comes, you have already lost the chance to do anything about it.
## Quick self-check
**1.** Why is a 90% win rate not the same as low risk for an option seller?
Because win rate ignores the size of the loss. If nine wins of Rs 2,000 are wiped out by one loss of Rs 40,000, you win almost every time and still go backwards. The rare loss is large enough to swallow many small wins, so being right often does not mean making money.
**2.** What does the payoff of a sold option look like?
A small, flat, capped profit (the premium) on the safe side, and an open-ended loss that keeps growing if price runs against you. Your best case is fixed and modest; your worst case can run far larger than the premium. It is the mirror image of buying an option.
**3.** What is the "loss tail" and why does it matter?
The tail is the rare, oversized loss sitting far out at the edge of your results. Most outcomes are small wins, but the single giant loss can erase all of them. A seller's equity curve climbs in small steps and then drops off a cliff - the cliff is the tail, and it is the real risk being carried the whole time.
**4.** Why do option sellers blow up after a winning streak?
Because the streak feels like proof the method is safe, so they size up - doubling lots right before the bad day. That guarantees the largest position is on when the tail finally lands. Keeping size constant through a streak, and never selling naked, is what prevents it.
**5.** What does "defined risk" mean, and why should a beginner start there?
It means capping the worst case in advance, usually by also buying a cheaper far-away option so the loss can never exceed a known amount (a spread). A beginner should start there because it removes the open-ended tail - the one outcome, often a gap or volatility spike, that ends accounts.
On this page
