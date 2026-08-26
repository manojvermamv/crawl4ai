Chapters
Module 5 · Python for the Markets - Chapter 34
# Symbols, Tickers & Lot Sizes
RELIANCE, RELIANCE.NS or AAPL? Learn the symbol systems across India and the US, plus lot sizes and what a ticker really is.
NSEUS
What you'll learn
  * ·NSE symbols
  * ·Yahoo .NS / .BO suffixes
  * ·US tickers
  * ·Index symbols
  * ·Lot size basics
  * ·Mapping symbols across sources


You'd think a stock would have _one_ name. It doesn't. Reliance is `RELIANCE` to the NSE, `RELIANCE.NS` to Yahoo, `RELIANCE.BO` if you mean its BSE listing, and `INE002A01018` to the settlement system. Apple is simply `AAPL`. Getting the symbol right is the difference between fetching real data and getting an empty result, so this short chapter makes symbols - and the F&O "lot" - second nature.
## One company, many tickers
The same company carries different identifiers across systems, and you need to translate between them:
EX 1Mapping a symbol across NSE, BSE and YahooPYch34/01_symbol_mapping.py
Copy
```
import yfinance as yf

# The same company wears different "names" on different systems.
def to_yahoo(symbol, exchange="NSE"):
    """Turn a plain NSE/BSE symbol into its Yahoo Finance ticker."""
    suffix = {"NSE": ".NS", "BSE": ".BO"}.get(exchange, "")
    return symbol + suffix

print("RELIANCE on NSE ->", to_yahoo("RELIANCE", "NSE"))   # RELIANCE.NS
print("RELIANCE on BSE ->", to_yahoo("RELIANCE", "BSE"))   # RELIANCE.BO
print("AAPL (US)       ->", to_yahoo("AAPL", "US"))        # AAPL (no suffix)
print()

# Fetch the latest close for each, proving the mapped symbols really work.
for label, ysym in [("RELIANCE (NSE)", "RELIANCE.NS"), ("Apple (US)", "AAPL")]:
    close = yf.Ticker(ysym).history(period="5d")["Close"].dropna()
    print(f"{label:16} last close: {round(float(close.iloc[-1]), 2)}")
```

Live output

```
RELIANCE on NSE -> RELIANCE.NS
RELIANCE on BSE -> RELIANCE.BO
AAPL (US)       -> AAPL

RELIANCE (NSE)   last close: 1313.6
Apple (US)       last close: 293.08
```

Reliance Industries NSE: RELIANCE BSE: RELIANCE Yahoo: RELIANCE.NS Yahoo: RELIANCE.BO One company, four tickers. Its ISIN (INE002A01018) is the single id every system agrees on.
The rules are simple once you know them: Yahoo wants **`.NS`**for an NSE listing and**`.BO`**for a BSE one;**US tickers** (`AAPL`, `MSFT`) take no suffix; and an **index** starts with **`^`**(Chapter 33). A tiny mapping function like`to_yahoo` saves you from ever guessing - write it once, reuse it everywhere.
Key idea
The same stock has different symbols per system. For **Yahoo** : NSE adds **`.NS`**, BSE adds**`.BO`**, US tickers take**no suffix** , indices start with **`^`**. Behind them all, the**ISIN** is a single global id. A small mapping function keeps your code source-agnostic.
## Lot sizes: trading in bundles
In the cash market you can buy a single share. But in **futures and options** , you trade fixed bundles called **lots** - you can't buy "one Nifty," only one _lot_ of Nifty. The money at stake is the **contract value** : price times lot size:
EX 2Contract value = price x lot sizePYch34/02_lot_sizes.py
Copy
```
# In F&O you trade fixed LOTS, not single shares. Contract value = price x lot size.
# (Lot sizes are illustrative - exchanges revise them periodically.)
lots = {"NIFTY": 65, "BANKNIFTY": 30, "RELIANCE": 500, "TCS": 175}
prices = {"NIFTY": 24021.65, "BANKNIFTY": 52000.00, "RELIANCE": 1313.60, "TCS": 2109.00}

print(f"{'Symbol':<12}{'Lot':>6}{'Price':>12}{'Contract value':>18}")
print("-" * 48)
for sym, lot in lots.items():
    value = lot * prices[sym]
    print(f"{sym:<12}{lot:>6}{prices[sym]:>12,.2f}{value:>18,.2f}")
```

Live output

```
Symbol         Lot       Price    Contract value
------------------------------------------------
NIFTY           75   24,021.65      1,801,623.75
BANKNIFTY       35   52,000.00      1,820,000.00
RELIANCE       500    1,313.60        656,800.00
TCS            175    2,109.00        369,075.00
```

A single Nifty lot controls over ₹18 lakh of index; a Reliance lot, around ₹6.5 lakh. That's no accident:
Note
**Lot sizes are set deliberately - and they change.** Exchanges (under SEBI's rules) size each lot so that one contract is worth a _meaningful_ sum - typically several lakh rupees - large enough to discourage reckless punting, small enough to stay accessible. Because the lot flexes to keep that value in range, a cheap index has a big lot and a pricey stock a small one. The exact numbers are revised periodically, so for live trading always pull the current lot size from the exchange or your broker, never a hard-coded guess.
Did you know?
**The word "ticker" comes from a sound.** In 1867 the stock ticker was invented - a machine that printed a running stream of stock symbols and prices onto a narrow paper "ticker tape," making the _tick-tick-tick_ noise that gave it its name. It was the world's first real-time market data feed, and traders would watch the tape spool out to follow prices. The tape is long gone, but we still call a stock's code its "ticker symbol" - a hundred-and-fifty-year-old echo of that little clicking machine.
## Mapping symbols in code
The practical takeaway is a habit: keep a small function (or dictionary) that converts between your symbol and whatever a data source expects. Your strategy code then speaks plain symbols - `RELIANCE`, `AAPL` - and the mapper handles the `.NS`, the `.BO`, the `^`, or the format OpenAlgo wants. It's a five-line investment that pays off the moment you pull data from more than one place.
## Try it yourself
  * Extend `to_yahoo` to handle an index: if `exchange == "INDEX"`, return the symbol unchanged (you'd pass `^NSEI` directly).
  * Use it to fetch TCS from the NSE (`to_yahoo("TCS")`) and confirm you get a real price back.
  * In the lot-size table, add `INFY` with a lot of 400 at its current price, and read off its contract value.


## Recap
  * The same stock has **different symbols** per system; for Yahoo, **`.NS`**(NSE),**`.BO`**(BSE), no suffix (US),**`^`**(index).
  * The **ISIN** is a single global identifier behind all the ticker variants.
  * In **F &O** you trade **lots** ; **contract value = price x lot size** , and lots are sized to a meaningful rupee value (and change over time).
  * Keep a small **mapping function** so your code speaks plain symbols and adapts to any data source.


You can now name any instrument and find its data. Two more everyday practicalities separate a confident Indian-market coder from a confused one: the _units_ (lakhs and crores, not millions) and the _clock_ (9:15 IST, holidays and all). The next chapter handles **money, timings and holidays**.
On this page
