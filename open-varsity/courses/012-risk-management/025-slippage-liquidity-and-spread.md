Chapters
Module E · Leverage, Margin and Execution Risk - Chapter 25
# Slippage, Liquidity and Spread
The price you see is not always the price you get. Bid-ask spread, market vs limit orders, liquidity and impact cost - the quiet taxes that turn a winning idea into a losing trade.
Leverage
What you'll learn
  * ·The bid-ask spread
  * ·Market vs limit orders
  * ·What liquidity means
  * ·Impact cost on size
  * ·Slippage in fast markets
  * ·Trading liquid instruments


Meera saw a far out-of-the-money option blinking at Rs 12 on her screen. The move looked ready to go, so she did the fast thing: a market order for a few lots, "just get me in". The order filled at an average of Rs 13.40. More than a rupee above the number she had been staring at, gone in a single click, before the trade had moved an inch. She had not been cheated. The Rs 12 on screen was simply the _last_ trade. The real sellers were sitting much higher, and a market order takes whatever is actually there. To get out later, she would pay that gap a second time.
This chapter is about a cost most beginners never see on any statement: the difference between the price you _see_ and the price you _get_. It is called the spread, and its ugly cousin is slippage. On liquid instruments it is small. On thin ones it quietly bleeds you on every entry and every exit.
## The screen shows one number, the market has two
That single price you see, the Last Traded Price (LTP), is history. It is the price of a trade that already happened. To actually buy right now you must pay the **best ask** (the lowest price a seller is offering). To actually sell right now you receive the **best bid** (the highest price a buyer is bidding). The gap between bid and ask is the **spread** , and it is a real cost you pay on the way in _and_ on the way out.
A market is really a stack of orders at different prices, called the order book. When you send a market order bigger than the orders sitting at the best price, you "walk up the book": you fill some at the best ask, the rest at worse prices above it. Your average fill drifts away from the screen. That drift is **impact cost**.
A thin order book: you pay the sellers, not the screen price resting quantity (lots) SPREAD = Rs 2.00 no orders rest here screen / last trade ~ Rs 12 14.0 5 13.5 8 13.0 10 best ask 11.0 12 best bid 10.5 9 10.0 7 market buy of 23 lots walks 13.0 to 13.5 to 14.0 You saw 12.00 You paid 13.39 avg over 23 lots slippage ~ Rs 1.39 (11%) The screen price is the last trade. A market order fills against whoever is actually resting in the book.
That 11% vanished before the trade was right or wrong, and Meera pays a similar slice again to exit. In a thin instrument the spread and the walk-up can be a bigger enemy than the market itself.
## Market order or limit order
You control which price you accept through your order type. The two basic choices trade speed against price.
  * A **market order** says "fill me now, at whatever price is there." You are guaranteed to trade; you are _not_ guaranteed the price.
  * A **limit order** says "fill me only at this price or better." You are guaranteed the price; you are _not_ guaranteed to trade. If nobody meets your limit, you simply do not get filled.

  
|   | Market order  | Limit order  |  
| --- | --- | --- |  
| You control  | Speed (fills now)  | Price (your number or better)  |  
| The risk  | You accept slippage  | You may never get filled  |  
| Best for  | Liquid instruments, urgent exits  | Thin instruments, calm entries  |  
| In a thin book  | Walks up the book, bleeds  | Sits, waits, no slippage  |  
| In a fast crash exit  | Gets you out (at a price)  | May leave you stuck in  |  
Common mistake
The classic beginner habit is firing **market orders into thin instruments** to feel fast and decisive: far out-of-the-money options, small-caps, illiquid contracts. In a thick book that is harmless. In a thin one it hands away a chunk of your money on every click, in and out, for nothing. The better move is to default to a **limit order** at or near the best bid/ask, and only reach for a market order when you genuinely need out _right now_ and the instrument is liquid enough to absorb it.
## Liquidity decides how much it hurts
**Liquidity** is simply how easily you can trade size without moving the price. A liquid instrument, like a big index future or a large-cap stock, has a deep book: many buyers and sellers stacked close together, a spread of a few paise, and your order fills right where you expected. A thin or illiquid one, like a far OTM option or a tiny small-cap, has a shallow book: few orders, far apart, a wide spread, and your trade itself shoves the price.
Same market order, two very different fills Liquid (index future, large-cap) ask bid screen price spread ~5 paise, fill = what you saw Illiquid (far OTM option, small-cap) ask bid screen wide spread, fill far above screen Same order, same intent. Liquidity is the difference between a clean fill and a painful one.
This is why size matters too. A handful of lots in a deep index future is a drop in the ocean. The same value in a thin small-cap _is_ the ocean, and you move the price against yourself just by trading. Big players measure this carefully and call it impact cost. As a beginner, your defence is simpler: trade liquid things, and use limit orders.
Key idea
The spread and slippage are a tax you pay on entry and on exit, set by liquidity, not by your skill. Liquid instrument plus limit order keeps the tax tiny. Thin instrument plus market order makes it large, certain, and paid every single time you trade.
## Why this matters most for small targets
Slippage is deadly to strategies with small profit targets. Imagine you scalp for a Rs 2 move, but the round-trip spread plus slippage costs you Rs 1.50. You keep half a rupee even when you are _right_ , and you have not yet counted brokerage, STT and other charges. The same Rs 1.50 cost is a rounding error on a Rs 40 swing trade. The thinner your edge, the more brutally the spread eats it. This is the slow bleed that confuses beginners: their calls are often fine, but the costs quietly turn a winning idea into a losing account. (Education only, not advice on what to trade.)
## How each participant feels the spread  
| User type  | How much the spread bites  | What to do  |  
| --- | --- | --- |  
| Long-term investor  | Almost irrelevant, paid once on a multi-year hold in a large-cap  | Use limit orders, ignore a few paise  |  
| Active trader  | Real, paid on every round trip, scales with how often you trade  | Limit orders, liquid names, count it into the target  |  
| F&O / futures trader  | Tight in near-month index futures, wide in far months and weekly tails  | Stick to liquid expiries, avoid thin strikes  |  
| Option seller  | Worst on far OTM strikes you sell, brutal if you must buy back in a panic  | Trade liquid strikes, plan the exit before you enter  |  
## When this fails
A limit order protects your price, but it cannot protect you from _not trading_. In a fast market or an overnight gap, price can leap clean over your limit and never come back. Your buy limit sits patiently while the stock rockets up past it: you miss the move and then chase it at a worse price. Worse, your protective sell limit may never fill as price craters through it, leaving you trapped in a falling position. The very tool that saves you slippage can, at the worst moment, save you out of a fill you badly needed.
A gap jumps over your limit your sell limit gap on news Price never trades at the orange line, so the limit stays unfilled and you are still in the position, lower. Limits protect price, not certainty. In a gap, even a correct limit can be skipped entirely.
The honest takeaway is balance. Default to limit orders so you stop bleeding the spread on routine trades. But know that when speed truly matters, in a liquid instrument, a market order is the right tool, and that no order type defends you from a violent gap. Match the tool to the moment, and never confuse a number on the screen with money in your hand.
## Quick self-check
**1.** What is the bid-ask spread, and when do you pay it?
It is the gap between the best buy price (bid) and the best sell price (ask). You pay it twice: a slice on entry when you buy at the ask, and again on exit when you sell at the bid.
**2.** Why did Meera's option fill at Rs 13.40 when the screen showed Rs 12?
The Rs 12 was the last traded price, just history. Her market order took whatever sellers were actually resting, which started at Rs 13 and walked higher as it filled, so her average was well above the screen number.
**3.** What does a limit order guarantee, and what does it not?
A limit order guarantees the price (your number or better) but not the fill. If nobody trades at your price, your order simply sits unfilled, and you may miss the move entirely.
**4.** Why does slippage hurt small-target strategies the most?
A fixed spread-plus-slippage cost eats a tiny fraction of a large swing but a huge fraction of a small scalp. If your target is Rs 2 and costs are Rs 1.50, you barely profit even when right, and charges make it worse.
**5.** How can a limit order still fail to protect you in a fast market?
Price can gap straight over your limit without trading there. Your protective sell limit may never fill as price crashes through it, leaving you stuck in the position, or your buy limit gets skipped and you end up chasing.
On this page
