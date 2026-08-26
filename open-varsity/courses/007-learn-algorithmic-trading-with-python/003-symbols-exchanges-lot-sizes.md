Chapters
Module A · Foundations - Chapter 03
# Symbols, Exchanges & Lot Sizes
Master the OpenAlgo symbol format across NSE equity, NFO F&O and MCX commodities.
NSENFOMCXINDEX
What you'll learn
  * ·Equity / future / option symbols
  * ·search() & symbol()
  * ·Index symbols
  * ·expiry() for F&O
  * ·instruments() master list
  * ·Lot sizes for sizing


Every order you ever place, every quote you ever pull, every chart you ever draw begins with one small piece of text: a **symbol**. It's the name the system uses to know exactly _which_ instrument you mean. Get it right and everything works. Get it wrong and, at best, you get an error - at worst, you trade the wrong thing entirely.
Here's the good news. Different brokers each have their own messy way of naming instruments, but OpenAlgo hides all of that behind **one consistent format**. Learn it once here and it works everywhere - for stocks on NSE, futures and options on NFO, and commodities on MCX. This chapter is your map.
Note
A "symbol" is just a string (text in quotes) like `"RELIANCE"` or `"NIFTY30JUN26FUT"`. Every symbol travels with an **exchange code** that says _where_ it trades. The two always go together - symbol plus exchange.
## Equity symbols: just the name
For a stock, the symbol _is_ its short name - `RELIANCE`, `SBIN`, `INFY`. No date, no suffix, nothing fancy. The exchange is `NSE` (or `BSE`). The `client.symbol()` call asks OpenAlgo for the details it stores about any instrument: its official name, lot size, and tick size (the smallest price step it can move in).
EX 1Look up an equity symbolNSEch03/01_equity_symbol.py
Copy
```
# Equity symbols are just the base name: RELIANCE, SBIN, INFY.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

info = client.symbol(symbol="RELIANCE", exchange="NSE")["data"]
print("Symbol    :", info["symbol"])
print("Name      :", info["name"])
print("Lot size  :", info["lotsize"])
print("Tick size :", info["tick_size"])
```

Live output

```
Symbol    : RELIANCE
Name      : RELIANCE INDUSTRIES
Lot size  : 1
Tick size : 0.1
```

## When you don't know the exact name: search()
You won't always remember the precise symbol - especially for futures and options, where dates are baked into the name. `client.search()` solves this: give it a few words and an exchange, and it hands back every match, each with its expiry date and lot size. Think of it as the market's autocomplete.
EX 2Search for matching symbolsNFOch03/02_search.py
Copy
```
# search() finds tradable symbols when you do not know the exact name.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

result = client.search(query="NIFTY FUT", exchange="NFO")
print("Matches found:", result.get("message"))
for item in result["data"][:5]:
    print(f"{item['symbol']:22s} expiry {item['expiry']}  lot {item['lotsize']}")
```

Live output

```
Matches found: Found 15 matching symbols
NIFTY30JUN26FUT        expiry 30-JUN-26  lot 65
NIFTY28JUL26FUT        expiry 28-JUL-26  lot 65
NIFTY25AUG26FUT        expiry 25-AUG-26  lot 65
BANKNIFTY30JUN26FUT    expiry 30-JUN-26  lot 30
BANKNIFTY28JUL26FUT    expiry 28-JUL-26  lot 30
```

Tip
`search()` is the fastest way to find the _exact_ string you need before placing an order. When a symbol you typed gets rejected, search for it first - you'll usually spot a wrong date or a missing `FUT` immediately.
## Futures: base + expiry + FUT
A **future** is a contract to buy or sell something on a fixed future date (its **expiry**). Its OpenAlgo symbol is built as `[Base][Expiry]FUT`. So the NIFTY future expiring on 30 June 2026 is `NIFTY30JUN26FUT`, and Reliance's is `RELIANCE30JUN26FUT`. The date is written as `DDMMMYY` - day, three-letter month, two-digit year.
EX 3Inspect a futures contractNFOch03/03_future_symbol.py
Copy
```
# Future format: [Base][Expiry]FUT  e.g. NIFTY30JUN26FUT
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

info = client.symbol(symbol="NIFTY30JUN26FUT", exchange="NFO")["data"]
print("Symbol   :", info["symbol"])
print("Type     :", info["instrumenttype"])
print("Expiry   :", info["expiry"])
print("Lot size :", info["lotsize"])
print("Tick size:", info["tick_size"])
```

Live output

```
Symbol   : NIFTY30JUN26FUT
Type     : FUT
Expiry   : 30-JUN-26
Lot size : 65
Tick size: 0.1
```

## Options: base + expiry + strike + type
**Options** add two more pieces: the **strike price** (the price level the option is tied to) and the **type** - `CE` for a Call (a bet up) or `PE` for a Put (a bet down). The format is `[Base][Expiry][Strike][CE/PE]`. So a NIFTY 24000 Call expiring 30 June 2026 is `NIFTY30JUN2624000CE`. The search below shows the same strike across several expiries.
EX 4List option contractsNFOch03/04_option_symbol.py
Copy
```
# Option format: [Base][Expiry][Strike][CE/PE]  e.g. NIFTY30JUN2624000CE
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

result = client.search(query="NIFTY 24000 CE", exchange="NFO")
for item in result["data"][:5]:
    print(f"{item['symbol']:24s} strike {item['strike']:>7}  expiry {item['expiry']}")
```

Live output

```
NIFTY23JUN2624000CE      strike 24000.0  expiry 23-JUN-26
NIFTY30JUN2624000CE      strike 24000.0  expiry 30-JUN-26
NIFTY07JUL2624000CE      strike 24000.0  expiry 07-JUL-26
NIFTY14JUL2624000CE      strike 24000.0  expiry 14-JUL-26
NIFTY21JUL2624000CE      strike 24000.0  expiry 21-JUL-26
```

Tip
NSE index options expire _weekly_ , so you'll see many expiries for one strike. The nearest expiry is usually the most actively traded. We'll use friendlier helpers - `optionsymbol()` and `optionchain()` - in Chapter 24. For now, just learn to read the format so it stops looking like alphabet soup.
## Indices: the NSE_INDEX exchange
An **index** like NIFTY or BANKNIFTY is a number that summarises a basket of stocks - you can _watch_ it but not buy it directly (you trade its futures and options instead). Indices live on a special exchange code, `NSE_INDEX`, and are quote-only.
EX 5Read index levelsINDEXch03/05_index_symbols.py
Copy
```
# Indices live on the NSE_INDEX exchange and are quote-only (you cannot trade them directly).
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

for idx in ["NIFTY", "BANKNIFTY", "FINNIFTY", "INDIAVIX"]:
    q = client.quotes(symbol=idx, exchange="NSE_INDEX")["data"]
    print(f"{idx:12s} {q['ltp']:>10.2f}")
```

Live output

```
NIFTY          23824.10
BANKNIFTY      57183.75
FINNIFTY       26329.30
INDIAVIX          13.94
```

Heads up
The most common beginner error in the whole SDK: asking for `NIFTY` on exchange `NSE`. That fails, because the index lives on `NSE_INDEX` - `NSE` is only for stocks. Whenever a request mysteriously errors, check that the symbol and exchange match.
## Expiry dates
Before you can build a valid futures or options symbol, you need a real expiry date - and they change over time. `client.expiry()` lists the currently available ones, separately for futures and options.
EX 6Get expiry datesNFOch03/06_expiry_dates.py
Copy
```
# expiry() lists the available expiry dates for futures and options.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

fut = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="futures")
opt = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")
print("Future expiries:", fut["data"][:5])
print("Option expiries:", opt["data"][:5])
```

Live output

```
Future expiries: ['30-JUN-26', '28-JUL-26', '25-AUG-26']
Option expiries: ['23-JUN-26', '30-JUN-26', '07-JUL-26', '14-JUL-26', '21-JUL-26']
```

## Commodities on MCX
Commodities - gold, crude oil, silver and more - trade on the `MCX` exchange, using the same `[Base][Expiry]FUT` format as other futures. A bonus for us: MCX trades late into the evening, long after stock markets close, so it's perfect for testing live data after hours. A quick search confirms the exact tradable symbol and its lot size.
EX 7Discover MCX commoditiesMCXch03/07_mcx_commodities.py
Copy
```
# MCX hosts commodity futures: gold, crude oil, silver and more.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

for query in ["GOLDM", "CRUDEOIL", "SILVERM"]:
    result = client.search(query=query, exchange="MCX")
    if result["data"]:
        first = result["data"][0]
        print(f"{query:10s} -> {first['symbol']:22s} lot {first['lotsize']}")
```

Live output

```
GOLDM      -> GOLDM03JUL26FUT        lot 1
CRUDEOIL   -> CRUDEOIL20JUL26FUT     lot 1
SILVERM    -> SILVERM30JUN26FUT      lot 1
```

## The full instrument list
Sometimes you want _every_ instrument on an exchange at once - to build your own scanner universe, say. `client.instruments()` returns the entire master list as a **DataFrame** (a spreadsheet-like table from the pandas library, which we'll properly meet in Chapter 7). It's thousands of rows you can filter and search.
EX 8The full instrument listNSEch03/08_instruments_master.py
Copy
```
# instruments() returns the full master contract list as a pandas DataFrame.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

df = client.instruments(exchange="NSE")
print("Total NSE instruments:", len(df))
print("Columns:", df.columns.tolist())
print(df[["symbol", "name", "lotsize"]].head())
```

Live output

```
Total NSE instruments: 9717
Columns: ['brexchange', 'brsymbol', 'exchange', 'expiry', 'instrumenttype', 'lotsize', 'name', 'strike', 'symbol', 'tick_size', 'token']
        symbol                       name  lotsize
0  GOLDSTAR-SM             GOLDSTAR POWER    11250
1   21STCENMGM  21ST CENTURY MGMT SERVICE        1
2     AARTIIND           AARTI INDUSTRIES        1
3          ABB                  ABB INDIA        1
4   656KA30-SG          SDL KA 6.56% 2030      100
```

## Lot sizes and contract value
Here's something that surprises new derivatives traders: in F&O and commodities you don't trade single units - you trade **lots**. One NIFTY lot is 65 units; one Reliance future lot is 500 shares. So a single contract can be worth lakhs of rupees. Multiplying lot size by price gives the **contract value** , which tells you how much exposure one lot really carries - essential for sizing your trades, as we'll formalise in the strategy and risk chapters.
EX 9Lot size and contract valueNFOMCXch03/09_lot_sizes.py
Copy
```
# Lot size decides how many units one F&O contract controls -- key for sizing.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def contract_value(symbol, exchange):
    info = client.symbol(symbol=symbol, exchange=exchange)["data"]
    ltp = client.quotes(symbol=symbol, exchange=exchange)["data"]["ltp"]
    return info["lotsize"], ltp, info["lotsize"] * ltp


for sym, exch in [("NIFTY30JUN26FUT", "NFO"), ("GOLDM03JUL26FUT", "MCX")]:
    lot, ltp, value = contract_value(sym, exch)
    print(f"{sym:18s} lot {lot:>4} x {ltp:>10.2f} = {value:>14,.0f}")
```

Live output

```
NIFTY30JUN26FUT    lot   65 x   23810.00 =      1,547,650
GOLDM03JUL26FUT    lot    1 x  144335.00 =        144,335
```

Heads up
Always _look up_ the lot size with `symbol()` rather than assuming it - exchanges revise lot sizes periodically. Hard-coding `65` for NIFTY today could quietly break your sizing math after the next revision.
Finally, here's a single helper that describes any instrument on any exchange - a small utility you'll reuse whenever you need an instrument's lot or tick size.
EX 10A universal symbol describerNSENFOMCXch03/10_symbol_resolver.py
Copy
```
# One helper to describe any instrument across NSE, NFO and MCX.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def describe(symbol, exchange):
    d = client.symbol(symbol=symbol, exchange=exchange)["data"]
    return f"{d['symbol']:22s} {exchange:4s} lot={d['lotsize']:<5} tick={d['tick_size']}"


print(describe("SBIN", "NSE"))
print(describe("BANKNIFTY30JUN26FUT", "NFO"))
print(describe("CRUDEOIL20JUL26FUT", "MCX"))
```

Live output

```
SBIN                   NSE  lot=1     tick=0.05
BANKNIFTY30JUN26FUT    NFO  lot=30    tick=0.2
CRUDEOIL20JUL26FUT     MCX  lot=1     tick=1.0
```

## Try it yourself
  * Run the search example with your own query, like `"BANKNIFTY FUT"` or `"SBIN"`.
  * Build a NIFTY _Put_ symbol for the 23000 strike, nearest expiry, and look it up with `symbol()`.
  * Search MCX for `"NATURALGAS"` and note its lot size - commodities vary widely.


## Recap
  * OpenAlgo uses **one symbol format** across every broker - learn it once.
  * **Equity** = base name (`SBIN`); **Future** = `[Base][Expiry]FUT`; **Option** = `[Base][Expiry][Strike][CE/PE]`.
  * Exchange codes: `NSE`/`BSE` (stocks), `NFO`/`BFO` (F&O), `MCX` (commodities), `NSE_INDEX` (indices, quote-only).
  * `search()` finds symbols, `symbol()` returns details, `expiry()` lists expiries, `instruments()` dumps the whole list.
  * **Lot size** drives sizing in F&O and commodities - always look it up, never guess.


You can now name anything the market trades and find its key facts. Next we put that to work pulling richer live data - full quotes, fast multi-symbol snapshots, and the order book - across all three exchanges.
On this page
