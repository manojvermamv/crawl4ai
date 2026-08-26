Chapters
Module D · Trader Risk Management - Chapter 21
# Portfolio Heat: Your Total Open Risk
One percent per trade still adds up. With several positions open at once - especially correlated ones - your total risk can quietly reach eight percent or more. How to measure portfolio heat, why correlation and sector overlap hide it, and how to cap it.
Trader
What you'll learn
  * ·What portfolio heat is
  * ·Per-trade risk vs total risk
  * ·Correlation and hidden concentration
  * ·Sector overlap
  * ·Gross vs net exposure
  * ·Setting a total-heat limit


Priya had read every beginner rule and followed them all. "Never risk more than 1% on a trade," the books said, so she did exactly that. On her Rs 2,00,000 account, 1% was Rs 2,000, and she set every stop-loss so a single trade could only cost her about that much. The day she felt most disciplined, she had eight positions open at once, each risking a tidy 1%. They were all good companies she liked: a few private banks, a housing finance name, an insurer, a public-sector bank. Then came a single ugly day for financials. Rates wobbled, a results miss spooked the sector, and every one of her eight stops got hit on the same afternoon. Eight times 1% is 8%. Priya lost Rs 16,000 in a day while believing she had only ever risked "1% at a time".
Priya did nothing wrong on any single trade. Her mistake lived in the space _between_ the trades, in a number she never added up. That number has a name.
## What portfolio heat is
Portfolio heat is the total amount of your capital that is at risk across **all** your open positions at the same time. Not the risk on your worst trade. Not the average. The sum.
If one trade risks 1% and you have one trade open, your heat is 1%. Open a second 1% trade and your heat is 2%. Open eight and, on paper, your heat is 8%. Per-trade risk asks "how much can _this_ trade lose me?" Portfolio heat asks the scarier and more honest question: "if everything I am holding goes wrong together, how much of my account disappears?"
Eight "tiny" 1% risks stack into one big one Per-trade view (what you feel) 8 positions, 1% (Rs 2,000) each each one looks harmless add them up Portfolio-heat view (what is true) 6% heat cap Total open heat = 8% Rs 16,000 at risk at once Each trade obeyed the 1% rule. Together they broke the account's real limit.
Key idea
Per-trade risk and total risk are not the same thing. One trade at 1% is safe. Eight trades at 1% each is 8% of your account on the line at once - and if those trades are related, the true danger is worse than 8%. Cap the total, not just the slice.
## Correlation: why "diversified" can be a lie
Here is the part that caught Priya, and it catches almost everyone. Adding up the per-trade risks assumes each trade is its own separate bet that can win or lose on its own. Eight independent coin flips rarely all land tails. But Priya's eight trades were not independent. They were all financials. When the sector turned, they did not behave like eight separate bets - they behaved like **one** bet she had taken eight times.
This is correlation. Two positions are correlated when they tend to move together. Five private banks, or five stocks in the same sector, share the same news, the same interest-rate sensitivity, the same crowd of buyers and sellers. On a calm day they drift apart a little and the diversification feels real. In a fall, that comfort vanishes. Stress makes correlations rush toward 1, the number that means "perfectly in step". Everyone sells everything at once, and your "eight different stocks" all gap down on the same candle.
Diversification works on calm days, not in the crash Calm days: paths drift apart losses offset wins - net move is small Crash day: all paths plunge as one correlations go to 1 - no offset left Five "different" positions in the same theme are really one position wearing five hats.
The cleanest Indian reminder is March 2020. As the COVID panic hit, NIFTY fell roughly 38-40% from its January high to the late-March low, and it did not fall politely one stock at a time. Almost everything dropped together - banks, autos, metals, pharma, the lot. Anyone who thought they were diversified because they held "ten different stocks" found out those were ten lines on the same falling rope. Correlation did not care about their stock-picking.
## Sector overlap and the hidden concentration
Correlation hides best inside what looks like variety. You can hold positions with five different company names and still own one bet. A loan from a bank, a housing-finance lender, a microfinance name and an NBFC are all the same trade on interest rates and credit. Three IT services exporters are one trade on the rupee and US tech spending. The screen shows you five tickers; your risk sees one theme. This is **sector overlap** , and it is the quiet reason a portfolio that feels spread out is actually stacked on a single point.
The fix is to count your bets by _theme_ , not by _ticker_. Before you add a position, ask: do I already own this story? If three of your open trades rise and fall on the same driver, treat them as roughly one position for heat purposes, and size them as if they were one.
## Gross versus net exposure
There are two ways to total up how much market you are holding, and beginners often confuse them.
  * **Gross exposure** is the size of everything added together, longs and shorts, ignoring direction. If you are long Rs 60,000 of stocks and short Rs 20,000 of an index future, your gross is Rs 80,000. Gross tells you how much is _in play_ , which is what costs, slippage and surprises act on.
  * **Net exposure** is longs minus shorts: Rs 60,000 long minus Rs 20,000 short is Rs 40,000 net long. Net tells you which way you lean and by how much.

Gross adds, net cancels Long Rs 60,000 Short Rs 20,000 same book, two ways to total it Gross = 60 + 20 = Rs 80,000 how much is in play Net = 60 - 20 = Rs 40,000 long which way you lean A small net can hide a large gross. Both numbers deserve a limit.
Why it matters: a hedged-looking book with a small net can still carry a huge gross, and gross is what bleeds you through charges and what bites you when a hedge fails to behave. Watch both. Heat is built from your _risk_ , but exposure is the raw size that risk sits on.
## The portfolio-heat calculator
Here is the whole job on one sheet. For each open position, your risk is simply how far price has to travel to hit your stop, times your quantity. Add a column for the theme so you can spot overlap. Then total it.  
| Position  | Theme  | Position value  | Stop distance  | Rupee at risk  | % of Rs 2,00,000  |  
| --- | --- | --- | --- | --- | --- |  
| Bank A (long)  | Financials  | Rs 40,000  | 5%  | Rs 2,000  | 1.0%  |  
| Bank B (long)  | Financials  | Rs 40,000  | 5%  | Rs 2,000  | 1.0%  |  
| Housing-fin (long)  | Financials  | Rs 40,000  | 5%  | Rs 2,000  | 1.0%  |  
| Insurer (long)  | Financials  | Rs 40,000  | 5%  | Rs 2,000  | 1.0%  |  
| Auto stock (long)  | Autos  | Rs 40,000  | 5%  | Rs 2,000  | 1.0%  |  
| **Raw total heat**  |   |   |   | **Rs 10,000**  | **5.0%**  |  
| **Correlation-adjusted**  | 4 financials count as ~1.5  |   |   | **~Rs 7,000**  | **~3.5% true**  |  
Read the last two rows carefully. The raw heat is 5%, which looks within a 6% cap. But four of the five positions share one theme, so the _real_ concentrated risk on a bad financials day is closer to the four moving as one - far more than the 1% the spreadsheet shows for any single name. The honest number is somewhere worse than the raw total suggests for that sector, and only the lone auto position offers any genuine offset.
A pre-trade checklist before you click buy:
  * What is my heat right now, totalled across every open position?
  * Will this new trade push my total heat above my cap (say 6%)?
  * Do I already own this theme - is this really a fresh bet or my fifth helping of one?
  * Counting correlated names as one, how many _independent_ bets do I actually have?
  * What is my gross exposure, and am I comfortable with that much in play?


## How much heat for each type of participant
Heat means something different depending on what you trade and how leveraged you are. Lot sizes shown are for the April-June 2026 cycle (lot sizes are revised periodically by the exchange - check current contract specs).  
| User type  | What "heat" means for you  | A sensible cap (example)  | The main trap  |  
| --- | --- | --- | --- |  
| Long-term investor  | Weight in any one stock or sector, not stops  | No single sector above ~20-25% of the portfolio  | Owning ten stocks that are really one sector bet  |  
| Active trader  | Sum of per-trade risk across open positions  | ~5-6% total open heat, fewer correlated names  | Eight 1% trades in the same theme = one 8% trade  |  
| F&O / futures trader  | Risk per lot times lots, magnified by leverage  | Tighter, ~3-5%, because moves hit margin fast  | One NIFTY lot (65) plus a BANKNIFTY lot (30) are nearly the same India-financials bet  |  
| Option seller  | Worst-case loss if the move goes against you, not premium  | Cap combined max-loss, stress-test a gap  | Several short strikes that all blow out together in one big move  |  
Common mistake
The classic error is grading yourself on per-trade risk alone. You proudly "never risk more than 1%", open as many 1% trades as you like, and never add them up - so your true open risk creeps to 7%, 8%, 10% without a single rule being broken on paper. Worse, you count five bank stocks as five positions when the market counts them as one. The better move: track total heat as one number, set a hard cap on it (many cap around 5-6%), and treat positions in the same theme as a single bet when you size and when you total.
## When this fails
The heat number is a model, and like every model it has a soft spot. The neat "1% plus 1% plus 1%" arithmetic quietly assumes your positions are independent. They almost never are. So the raw total tends to _understate_ your real danger, because on the day it matters, correlations climb toward 1 and your separate bets become one. A 6% raw cap on a book that is secretly all one theme can lose far more than 6% in a single session. The fix is not a fancier formula - it is judgement: count correlated names as one, and keep genuine variety in _what drives_ your positions, not just in their tickers.
Heat also says nothing about _gaps_. Your stops define your risk only if they fill near your price. An overnight gap, a circuit, or a frozen, illiquid name can blow straight through every stop at once, so your "controlled" 5% becomes something larger before you can act. And none of the example caps here are personalised advice - they are a framework. Your real heat limit depends on your capital, your strategy and how much of a bad day you can genuinely sit through. Set the number when you are calm, total it honestly, and respect it when the screen turns red.
## Quick self-check
**1.** What is portfolio heat, and how is it different from per-trade risk?
Portfolio heat is the total capital at risk across all your open positions added together. Per-trade risk is just one position's slice. Eight trades risking 1% each is 1% per trade but 8% of total heat.
**2.** Why did Priya lose about 8% when every trade obeyed the 1% rule?
Her eight positions were all financials, so they were correlated - effectively one bet taken eight times. When the sector fell, all eight stops were hit on the same day, and 8 times 1% is 8%.
**3.** What happens to correlation between similar stocks during a crash?
It rushes toward 1, meaning they move in lockstep. The diversification you felt on calm days vanishes, and "different" positions all plunge together - as nearly everything did in March 2020.
**4.** What is the difference between gross and net exposure?
Gross adds all positions ignoring direction (longs plus shorts) and tells you how much is in play. Net is longs minus shorts and tells you which way and how strongly you lean. A small net can hide a large gross.
**5.** Why can the raw heat total understate your true risk, and what is the fix?
The simple sum assumes positions are independent, but correlated names fall together, so real risk is worse than the arithmetic. The fix is to count same-theme positions as one bet and keep genuine variety in what drives your trades.
On this page
