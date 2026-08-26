Chapters
Module A · Foundations - Chapter 01
# Getting Started with OpenAlgo
Connect the OpenAlgo Python SDK, check funds, and understand analyze vs live mode.
NSE
What you'll learn
  * ·Set up a workspace with uv
  * ·Create an api client
  * ·Keep secrets in .env
  * ·Read funds & version
  * ·Analyze mode vs live mode
  * ·Your first data pull


Let me guess why you're here. You've placed trades by hand - watched a level, hesitated, clicked too late. You've wondered whether that setup you keep seeing actually _works_ , or whether you just remember the wins. And somewhere along the way you realised that the traders who answer those questions don't do it by staring harder at charts. They do it with code.
That's what this series is about. Over 32 chapters you'll go from _"I can open a Python file"_ to _"I have a strategy I've backtested, optimised, and wired into a bot."_ We won't skip steps and we won't hand-wave. And every single code example here is **real, runnable code that was executed against a live OpenAlgo server before it reached this page** - the outputs you see are genuine market responses, not made up.
This first chapter is about getting comfortable. By the end you'll have set up a clean Python workspace, connected to the market, checked your account, pulled a live price, and downloaded historical data. Small steps - but they're the foundation everything else stands on.
## Why bother automating?
A human trader can watch maybe five charts at once, gets tired, gets emotional, and can't remember exactly what happened the last forty times a pattern appeared. Code has none of those limits. It can scan 200 stocks in a second, never panics, and - crucially - lets you _test an idea on years of history before risking a rupee._ You're not trying to replace your judgement. You're trying to give it a microscope and a calculator.
## Why Python, and why the professionals use it
If you learn one language for markets, make it Python. It has quietly become the common tongue of quantitative finance, and not by accident.
Look at who relies on it. **JP Morgan** built its internal analytics and trading platform, _Athena_ , on Python. **Goldman Sachs** has steadily moved analytics onto Python and even open-sourced Python tooling. Quant powerhouses and proprietary trading desks - the people who trade for a living at the highest level - use it daily for research, signal generation, and data analytics; even **Jane Street** , famous for its OCaml core, reaches for Python for data work and machine learning. The point isn't to copy any one firm. It's that the entire industry, from bulge-bracket banks to two-person prop shops, has converged on the same toolkit you're about to learn.
Why did that happen?
  * **It reads like English.** You spend your time thinking about the _trade_ , not fighting the language.
  * **Batteries included for finance.** NumPy and Pandas for data, Matplotlib and Seaborn for charts, scikit-learn for machine learning, VectorBT for backtesting - all free, all mature.
  * **It glues everything together.** One script can pull broker data, compute indicators, run a backtest, place an order, and ping your phone. That is exactly what we'll build.
  * **A huge community.** Almost any question you'll hit has already been answered somewhere.


Note
A quick word on vocabulary, since we'll use it immediately. A **library** (or "package") is a bundle of ready-made code someone else wrote that you can pull into your own program - `openalgo`, `pandas` and `numpy` are all libraries. You install a library once, then `import` it to use it. We unpack libraries, modules and functions properly in Chapter 2; for now, just know that `uv add openalgo` _installs_ a library and `from openalgo import api` _uses_ it.
## Install Python and an editor
Before any trading code, get two free tools onto your machine.
  1. **Python itself** - the language. Download the latest version from [python.org](https://www.python.org/downloads/) and run the installer. On Windows, tick **"Add Python to PATH"** on the first screen (it saves a lot of pain later). Check it worked by opening a terminal and running `python --version`.
  2. **VS Code** - a free, friendly code editor from Microsoft ([code.visualstudio.com](https://code.visualstudio.com/)). After installing, open the Extensions panel, search for **"Python"** , and install the official Microsoft extension. That gives you colour-coded code, a Run button, and a built-in terminal so you never leave the window.


You also need the trading platform itself running, and a key to talk to it:
  * **Install and start OpenAlgo** by following its official setup guide. Once it's running on your computer it lives at `http://127.0.0.1:5000`.
  * Open that address in your browser, log in, go to the **API Key** page in the dashboard, and **copy your API key**. That single key is what lets your Python scripts place orders and pull data. You'll paste it into a `.env` file in a moment - and we'll treat it like a password.


Tip
Keep the OpenAlgo dashboard open in a browser tab while you work through this series. It's where you confirm orders fired, flip between analyze and live mode, and regenerate your API key if it ever leaks.
## Set up your workspace with uv
Before any code, one habit that will save you endless pain: give this project its **own isolated Python environment**. Think of it like a separate trading account for a new strategy - you don't want it tangled up with everything else on your machine. If two projects need different versions of a library, isolation is what stops them breaking each other.
We'll use **uv** , a fast, modern tool that manages both Python and your packages. Install it once:

```
pip install uv

```

Then create a project folder and add the SDK. `uv` builds the isolated environment for you automatically - no manual "activate" dance required.

```
uv init my-trading
cd my-trading
uv add openalgo            # the trading SDK - indicators are built in

```

That single package gives you everything: the trading API _and_ the 80+ technical indicators we'll use from Chapter 11. There's no separate add-on to install - `from openalgo import ta` just works.
From now on you run any script with `uv run` and it uses that isolated environment every time:

```
uv run python my_script.py

```

Note
The indicator library has a **Rust-powered core**. You write plain Python, but the heavy number-crunching runs in compiled Rust under the hood - so the maths is markedly faster than hand-rolled Python loops, especially across large histories of thousands of candles. You get readable code and real speed at the same time.
Tip
`uv add <package>` is how you install anything - `uv add pandas matplotlib vectorbt`. It records the package in your `pyproject.toml` so the project is reproducible: a friend can clone it and get the exact same setup with one command. That reproducibility is gold when a strategy behaves differently on two machines.
If you'd rather not use uv, plain `pip install openalgo` works too - you just lose the automatic isolation.
Now run your very first script, end to end. Save the snippet below as `check.py` in your project folder, then run it from the terminal with `uv run` - which quietly uses the isolated environment you just built:

```
uv run python check.py

```

If it prints a version number with no error, your workspace is ready and `uv run` is working. This is the exact loop you'll repeat for every example in the series: save a `.py` file, then `uv run python <file>.py`.
EX 1Confirm the SDK is installedch01/01_version.py
Copy
```
# Confirm the OpenAlgo Python SDK is installed and check its version.
from importlib.metadata import version

import openalgo  # the OpenAlgo trading SDK

print("OpenAlgo SDK version:", version("openalgo"))
print("Imported from       :", openalgo.__file__)
```

Live output

```
OpenAlgo SDK version: 2.0.2
Imported from       : D:\Quantflow4\Day14\.venv\Lib\site-packages\openalgo\__init__.py
```

## What is OpenAlgo, really?
Here's the mental model. Your **broker** is where your money and orders live, but every broker speaks its own technical dialect. **OpenAlgo** is a free platform you run on your own computer that sits in the middle and translates: you speak to it in one clean, standard language, and it speaks to whichever broker you use. Switch brokers later and your code doesn't change.
For us, the star of the show is the **OpenAlgo Python SDK** - a small library that turns the whole platform into ordinary Python function calls:

```
from openalgo import api
client = api(api_key="...", host="http://127.0.0.1:5000")
client.quotes(symbol="RELIANCE", exchange="NSE")

```

That `client` object is your remote control for the market. Throughout this series, whenever you see `client`, that's what it is.
Note
You need a running OpenAlgo instance to follow along. Once it's running on your machine it lives at `http://127.0.0.1:5000`, and you generate an **API key** from its web dashboard. The official OpenAlgo setup guide walks through installation; this series assumes your server is already up and you have a key in hand.
## Connecting to the server
To do anything we create an `api` client. It needs two things: your **API key** (which proves it's really you) and the **host** (where your OpenAlgo server is running). Look closely at how we supply the key - we _don't_ paste it into the code. We read it from an environment variable with `os.getenv`.
EX 2Connect and confirmch01/02_connect.py
Copy
```
# Create an API client and prove we are connected to the OpenAlgo server.
import os

from openalgo import api

# Best practice: read the key from an environment variable instead of hard-coding it.
client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

status = client.analyzerstatus()  # a tiny call that confirms the connection works
print("Connected:", status["status"] == "success")
print("Current mode:", status["data"]["mode"])
```

Live output

```
Connected: True
Current mode: analyze
```

## Managing secrets: the .env file
Why the fuss about not typing your key into the code? Because that key can place real orders. If it's sitting in a script, it ends up in screenshots, in shared files, in version control - and now anyone who sees it can trade your account. Treat it like your ATM PIN.
The clean, professional solution is a **`.env`file** : a little text file that holds your secrets, sits next to your code, and is _never shared_. The `python-dotenv` library loads it into your environment automatically. Create a file called `.env`:

```
OPENALGO_API_KEY=your_real_key_here
OPENALGO_HOST=http://127.0.0.1:5000

```

Then load it at the top of any script with `load_dotenv()`:
EX 3Load secrets from a .env filech01/09_dotenv.py
Copy
```
# Best practice: keep secrets in a .env file and load them with python-dotenv.
import os

from dotenv import load_dotenv

from openalgo import api

load_dotenv()  # reads a .env file in this folder into the environment

api_key = os.getenv("OPENALGO_API_KEY", "your_api_key_here")
client = api(api_key=api_key, host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"))

print("Loaded key ending in:", api_key[-4:])
print("Connected:", client.analyzerstatus()["status"] == "success")
```

Live output

```
Loaded key ending in: 7751
Connected: True
```

Key idea
Two rules that matter more than they look:
  1. Add `.env` to your `.gitignore` so it can never be committed. Ship a `.env.example` with blank values instead, so others know which keys to set.
  2. This project includes both files already - copy `.env.example` to `.env`, drop in your key, and every example in the series just works. No editing scripts, no leaked secrets.


## Know your firepower: funds
You wouldn't start a trading day without knowing your balance. `client.funds()` returns exactly that - available cash, what's already committed, and your running profit and loss. Notice the shape of the response: a dictionary with a `"status"` and a `"data"` payload. Almost every SDK call looks like this, so get used to reaching into `["data"]`.
EX 4Check funds and marginsch01/03_funds.py
Copy
```
# Read your trading account balance (funds and margins).
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

funds = client.funds()
data = funds["data"]
print("Available cash :", data["availablecash"])
print("Utilised       :", data["utiliseddebits"])
print("Realised P&L   :", data.get("m2mrealized"))
print("Unrealised P&L :", data.get("m2munrealized"))
```

Live output

```
Available cash : 9965741.58
Utilised       : 14448.5
Realised P&L   : -7496.81
Unrealised P&L : 0.0
```

## Analyze mode: your flight simulator
This is the single most important idea in the chapter, so slow down here. OpenAlgo has two modes:
  * **Live mode** - orders go to the real exchange, with real money. Mistakes cost you.
  * **Analyze mode** - orders are _simulated_. They look real, behave realistically, give you realistic responses - but nothing actually trades.


Analyze mode is a flight simulator. A pilot doesn't learn to fly by taking a packed jet up on day one; they crash a simulator a hundred times first, for free. You'll do the same: every order-placing example in this series was run in analyze mode, and you should keep it on while you learn. Check which mode you're in before you ever send an order:
EX 5Check which mode you're inch01/04_analyze_mode.py
Copy
```
# Understand analyze mode vs live mode before sending any order.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

status = client.analyzerstatus()["data"]
print("analyze_mode:", status["analyze_mode"])

if status["analyze_mode"]:
    print("SAFE: orders are simulated, nothing reaches the exchange.")
else:
    print("LIVE: real orders would be sent. Practise in analyze mode first.")
# To switch on simulation from code:  client.analyzertoggle(mode=True)
```

Live output

```
analyze_mode: True
SAFE: orders are simulated, nothing reaches the exchange.
```

Heads up
Before any chapter that places orders (especially 24 and 25), confirm `analyze_mode` is `True`. You can switch it from code with `client.analyzertoggle(mode=True)` or from the dashboard. Going live should always be a deliberate, conscious decision - never an accident.
## Your first look at the market
Now the part you came for. `client.quotes()` fetches a live snapshot for one symbol. Let's answer a question every trader asks each morning - _where is Reliance trading, and how's its day going?_
EX 6Pull a live quoteNSEch01/05_first_quote.py
Copy
```
# Your first live data pull: a price quote for one stock.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="RELIANCE", exchange="NSE")["data"]
print("RELIANCE last traded price:", q["ltp"])
print("Open / High / Low:", q["open"], q["high"], q["low"])
print("Previous close   :", q["prev_close"])
```

Live output

```
RELIANCE last traded price: 1309.5
Open / High / Low: 1328.9 1333 1304
Previous close   : 1326.5
```

A quote is a single moment. To study how a stock _behaves_ - its trends, its swings, its character - you need its past. `client.history()` downloads **OHLCV** candles (Open, High, Low, Close, Volume) and hands them back as a pandas `DataFrame`, the table-like structure we'll master in Chapters 6 and 7. This is the raw material of every backtest you'll ever run.
EX 7Download historical candlesNSEch01/06_first_history.py
Copy
```
# Download historical daily candles into a pandas DataFrame.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)
print(df.tail())          # last few OHLCV rows
print("Rows downloaded:", len(df))
```

Live output

```
close    high      low  oi    open    volume
timestamp                                                 
2026-06-17  1026.50  1028.1  1013.45   0  1017.0   8190062
2026-06-18  1042.70  1045.7  1024.45   0  1027.9  11048009
2026-06-19  1035.10  1042.0  1029.30   0  1042.0   9099878
2026-06-22  1040.75  1043.0  1033.60   0  1038.0   6209440
2026-06-23  1023.60  1045.5  1022.35   0  1041.0  10392214
Rows downloaded: 12
```

We asked for the `"D"` (daily) interval. Different brokers offer different candle sizes - you can always ask which are available:
EX 8List supported intervalsch01/07_available_intervals.py
Copy
```
# Ask the server which candle intervals your broker supports.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

intervals = client.intervals()["data"]
print("Minutes:", intervals["minutes"])
print("Hours  :", intervals["hours"])
print("Daily  :", intervals["days"])
```

Live output

```
Minutes: ['1m', '3m', '5m', '10m', '15m', '30m', '60m']
Hours  : ['1h']
Daily  : ['D']
```

## Putting it together: your morning watchlist
Let's build something that actually feels useful - a tiny watchlist that prints each stock's price and how much it's moved today. This is your first taste of looping over symbols, the pattern behind every scanner in this series. Imagine running this each morning to see your universe at a glance.
EX 9A four-stock watchlistNSEch01/08_market_hello.py
Copy
```
# Put it together: a tiny "market dashboard" for a list of stocks.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

watchlist = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
print(f"{'SYMBOL':10s} {'LTP':>10s} {'CHANGE%':>9s}")
for sym in watchlist:
    q = client.quotes(symbol=sym, exchange="NSE")["data"]
    pct = (q["ltp"] - q["prev_close"]) / q["prev_close"] * 100
    print(f"{sym:10s} {q['ltp']:>10.2f} {pct:>8.2f}%")
```

Live output

```
SYMBOL            LTP   CHANGE%
RELIANCE      1309.50    -1.28%
TCS           2059.60    -3.21%
INFY          1029.30    -3.39%
HDFCBANK       774.65    -1.49%
```

A working market dashboard in a dozen lines. That's the leverage code gives you - and we've barely started.
## Try it yourself
The best way to learn is to change something and see what happens:
  * Swap `RELIANCE` for a stock you actually follow and re-run the quote example.
  * Add three more symbols to the watchlist in the last example.
  * Change the history window from 15 days to 60 and see how many rows come back.


## Recap
  * **Isolate your workspace** with `uv` - it's like a separate account for this project, and it keeps your setup reproducible.
  * The **OpenAlgo Python SDK** (`client`) is your remote control for any broker.
  * Keep your API key in a **`.env`file** , load it with `python-dotenv`, and never commit it.
  * Most SDK calls return `{"status": ..., "data": ...}` - you'll reach into `["data"]` constantly.
  * **Analyze mode** is a flight simulator: practise orders with zero risk, and keep it on while learning.
  * `client.quotes()` gives a live snapshot; `client.history()` gives a DataFrame of candles to study.


Next we slow right down and cover just enough core Python - variables, lists, dictionaries, loops and functions - to make every later chapter feel easy. If you already know Python, skim it. If you don't, it's the most valuable hour you'll spend in this whole series.
On this page
