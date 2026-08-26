Chapters
Module B · Visualisation & Apps - Chapter 10
# Live Dashboards with Streamlit
Build clickable web apps - a quote board, a chart viewer and a mini scanner.
NSEMCX
What you'll learn
  * ·Streamlit basics
  * ·Widgets & inputs
  * ·Live quote dashboard
  * ·Embed a chart
  * ·A simple scanner UI
  * ·Caching SDK calls


Every chart and scanner you've built so far has one thing in common: you run it from the command line, read the output, tweak a number, and run it again. That's fine for you. But the moment you want to _hand it to someone else_ - or even just give yourself a tidy control panel instead of editing code - you need an app. A real one, with a text box to type a symbol, a dropdown to pick an exchange, a button to refresh. Traditionally that meant learning web development: HTML, CSS, JavaScript, a server. For a trader who just wants a dashboard, that's a mountain of work for a molehill of need.
**Streamlit** flattens that mountain. It's a Python library that turns an ordinary script into a web app - no HTML, no JavaScript, no server setup. You write `st.title("My Desk")` and a title appears in a browser. You write `st.text_input("Symbol")` and a text box appears, and whatever the user types comes straight back to your Python code as a string. It is genuinely the fastest way to wrap your OpenAlgo scripts in a clickable interface. In this chapter we'll build a quote board, a chart viewer, and a mini scanner - all in pure Python.
## Installing and running Streamlit
Streamlit isn't run like a normal script. A normal script you'd run with `python file.py`; a Streamlit app you launch with its own command, which starts a little web server and opens your browser:

```
uv add streamlit
uv run streamlit run 01_hello_dashboard.py

```

That `streamlit run` is the key. It executes your script top to bottom, turns every `st.something(...)` call into a piece of the web page, and serves it at `http://localhost:8501`. Edit the file and save - Streamlit notices and offers to re-run instantly. That tight loop is what makes it feel magical.
Heads up
If you run a Streamlit script with plain `python file.py` instead of `streamlit run`, it won't crash, but it also won't show a web page - Streamlit just prints a warning that you should use `streamlit run`. Every example in this chapter is written to detect that situation and print a clean summary instead, so it behaves sensibly either way. But to actually _see_ the app, always use `streamlit run`.
## Your first dashboard
Let's start with the smallest possible app: a title, a line of text, and a **metric** - Streamlit's tidy little tile for showing a single number with a label, the kind you'd use for a price or a P&L figure.
EX 1A hello-world dashboardch10/01_hello_dashboard.py
Copy
```
# Your first Streamlit app: a title, some text, and a metric tile.
# Launch it with:  streamlit run 01_hello_dashboard.py
import logging

import streamlit as st

# Silence the harmless "missing ScriptRunContext" notice when run with plain python.
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None  # True only under `streamlit run`


def app():
    st.title("My Trading Desk")
    st.write("Welcome. This dashboard is built with Streamlit and OpenAlgo.")
    st.metric(label="Watchlist size", value=4)
    st.caption("Quote of the day: plan the trade, trade the plan.")


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 01_hello_dashboard.py")
    print("Dashboard defined: title 'My Trading Desk' with one metric tile.")
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 01_hello_dashboard.py
Dashboard defined: title 'My Trading Desk' with one metric tile.
```

Three calls, three pieces of a web page: `st.title(...)` is the big heading, `st.write(...)` prints text (it's the Swiss-army display call - give it almost anything and it renders sensibly), and `st.metric(label=..., value=...)` draws that clean number tile. Run it with `streamlit run` and you'll see all three in your browser, styled and centred, with zero CSS from you.
Note
You'll notice each example has a small guard near the top: it checks whether it's running under `streamlit run` and, if not, prints a plain-text summary. That's just so the examples behave nicely when tested from the command line - you can ignore the guard and focus on the `app()` function, which is the real Streamlit code. When you write your own apps, you don't need the guard; you can call `st.title(...)` and friends directly.
## Widgets: getting input from the user
A dashboard you can't change is just a chart. **Widgets** are the interactive controls - boxes, dropdowns, sliders - and the beautiful part of Streamlit is how it hands their values back. When you write `symbol = st.text_input("Symbol", "RELIANCE")`, that line both _draws_ a text box (pre-filled with "RELIANCE") and _returns_ whatever the user has typed into the variable `symbol`. No event handlers, no callbacks - just a normal variable assignment. The same goes for `st.selectbox`, which draws a dropdown and returns the chosen option.
EX 2Symbol and exchange widgetsch10/02_widgets_inputs.py
Copy
```
# Widgets: a text box for the symbol and a dropdown for the exchange.
# Launch it with:  streamlit run 02_widgets_inputs.py
import logging

import streamlit as st

logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None


def app():
    st.title("Pick an instrument")
    # text_input returns whatever the user types; the second value is the default.
    symbol = st.text_input("Symbol", value="RELIANCE")
    # selectbox returns the chosen option from the list.
    exchange = st.selectbox("Exchange", ["NSE", "NFO", "MCX"])
    st.write(f"You selected **{symbol}** on **{exchange}**.")


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 02_widgets_inputs.py")
    print("Widgets defined: text_input(Symbol) and selectbox(Exchange).")
    print("Default selection -> RELIANCE on NSE")
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 02_widgets_inputs.py
Widgets defined: text_input(Symbol) and selectbox(Exchange).
Default selection -> RELIANCE on NSE
```

Read it as ordinary Python: `symbol` holds the typed text, `exchange` holds the picked option, and `st.write` shows them back. Here's the mental model that makes Streamlit click: **the whole script re-runs from the top every time a widget changes.** Type a new symbol, and Streamlit runs your file again, top to bottom, with `symbol` now holding the new value. You don't manage state or redraw anything - you just write the script as if it ran once, and Streamlit handles the re-running.
## A live quote board
Now we wire in OpenAlgo. We'll build the board from Chapter 4 - several symbols, their live prices - but as a web page instead of console output. One `multiquotes()` call fetches the whole watchlist in a single request, and `st.table(...)` renders a list of dictionaries as a neat table.
EX 3A live quote boardNSEch10/03_quote_board.py
Copy
```
# A live quote board: one multiquotes() call fills a table of LTPs.
# Launch it with:  streamlit run 03_quote_board.py
import logging
import os

import streamlit as st
from openalgo import api

logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)
WATCHLIST = [{"symbol": s, "exchange": "NSE"} for s in ["RELIANCE", "TCS", "INFY", "HDFCBANK"]]


def fetch_board():
    results = client.multiquotes(symbols=WATCHLIST)["results"]
    return [{"Symbol": r["symbol"], "LTP": r["data"]["ltp"]} for r in results]


def app():
    st.title("Live quote board")
    st.table(fetch_board())


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 03_quote_board.py")
    for row in fetch_board():
        print(f"{row['Symbol']:10s} {row['LTP']:>10.2f}")
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 03_quote_board.py
RELIANCE      1309.50
TCS           2059.60
INFY          1029.30
HDFCBANK       774.65
```

The `fetch_board()` function does exactly what you did in Chapter 4: call `multiquotes`, then build a list of `{"Symbol": ..., "LTP": ...}` rows. The only new thing is the display - `st.table(rows)` turns that list straight into an on-page table. Connecting the SDK is identical to every other chapter: the same `api(...)` client reading the key from the environment. Streamlit just changes how the _result_ is shown.
## Embedding a chart
A quote board answers "where is it now?" A chart answers "how did it get here?" Streamlit ships with built-in charts, and the simplest is `st.line_chart(...)`: hand it a column of numbers and it draws an interactive line. We'll fetch a symbol's closing-price history and plot it.
EX 4A chart viewer with line_chartNSEch10/04_chart_viewer.py
Copy
```
# Embed a chart: st.line_chart draws the closing-price history of any symbol.
# Launch it with:  streamlit run 04_chart_viewer.py
import logging
import os
from datetime import datetime, timedelta

import streamlit as st
from openalgo import api

logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def load(symbol, exchange):
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    return client.history(symbol=symbol, exchange=exchange, interval="D",
                          start_date=start, end_date=end)


def app():
    st.title("Chart viewer")
    symbol = st.text_input("Symbol", "SBIN")
    df = load(symbol, "NSE")
    st.line_chart(df["close"])  # Streamlit draws an interactive line chart from a Series.


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 04_chart_viewer.py")
    df = load("SBIN", "NSE")
    print(f"Loaded {len(df)} closes for SBIN; latest close = {df['close'].iloc[-1]:.2f}")
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 04_chart_viewer.py
Loaded 59 closes for SBIN; latest close = 1023.60
```

`st.line_chart(df["close"])` is the whole charting step - pass it the close column from the history DataFrame and you get a zoomable line chart for free. Combine it with the text-input widget and you've built a tool: type any symbol, see its chart. That's a genuinely useful little app in under twenty lines.
### Bringing in your Plotly charts
`st.line_chart` is quick, but in Chapter 9 you built proper candlestick charts with Plotly. The good news: Streamlit can embed a Plotly figure directly with `st.plotly_chart(fig)`. You build the figure exactly as before, then hand it over - and you get the full interactive candlestick, range tools and all, inside your app.
EX 5Embed a Plotly candlestickNFOch10/05_plotly_candles.py
Copy
```
# Embed a Plotly candlestick chart inside Streamlit with st.plotly_chart.
# Launch it with:  streamlit run 05_plotly_candles.py
import logging
import os
from datetime import datetime, timedelta

import plotly.graph_objects as go
import streamlit as st
from openalgo import api

logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def build_fig(symbol, exchange):
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    df = client.history(symbol=symbol, exchange=exchange, interval="D",
                        start_date=start, end_date=end)
    fig = go.Figure(go.Candlestick(x=df.index, open=df["open"], high=df["high"],
                                   low=df["low"], close=df["close"]))
    fig.update_layout(title=f"{symbol} daily", xaxis_rangeslider_visible=False)
    return fig, len(df)


def app():
    st.title("Plotly candles in Streamlit")
    symbol = st.text_input("NFO future", "NIFTY30JUN26FUT")
    fig, _ = build_fig(symbol, "NFO")
    st.plotly_chart(fig, use_container_width=True)


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 05_plotly_candles.py")
    _, n = build_fig("NIFTY30JUN26FUT", "NFO")
    print(f"Built a Plotly candlestick figure with {n} candles for NIFTY30JUN26FUT")
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 05_plotly_candles.py
Built a Plotly candlestick figure with 56 candles for NIFTY30JUN26FUT
```

`build_fig(...)` is lifted almost verbatim from the previous chapter - fetch history, make a `go.Candlestick` figure. The single new line is `st.plotly_chart(fig, use_container_width=True)`, which drops that figure into the page and stretches it to the full width of the column. Everything you learned about Plotly now lives inside a clickable app.
## A mini scanner UI
This is where it all comes together into something you'd actually use each morning. A **scanner** runs one rule across a list of symbols and reports the hits. We'll scan a small universe for **oversold** names - those whose RSI has dropped below a threshold - and let the user set that threshold with a **slider** , the widget for picking a number in a range.
EX 6A mini RSI scannerNSEch10/06_mini_scanner.py
Copy
```
# A mini scanner UI: pick an RSI threshold, list symbols trading below it (oversold).
# Launch it with:  streamlit run 06_mini_scanner.py
import logging
import os
from datetime import datetime, timedelta

import streamlit as st
from openalgo import api, ta

logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)
UNIVERSE = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN"]


def scan(threshold):
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
    hits = []
    for sym in UNIVERSE:
        df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
        rsi = ta.rsi(df["close"], 14).iloc[-1]
        if rsi < threshold:
            hits.append({"Symbol": sym, "RSI": round(float(rsi), 1)})
    return hits


def app():
    st.title("RSI oversold scanner")
    threshold = st.slider("RSI below", min_value=20, max_value=60, value=45)
    hits = scan(threshold)
    st.write(f"{len(hits)} symbol(s) under RSI {threshold}")
    st.table(hits)


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 06_mini_scanner.py")
    hits = scan(45)
    print(f"{len(hits)} symbol(s) under RSI 45:", [h["Symbol"] for h in hits])
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 06_mini_scanner.py
2 symbol(s) under RSI 45: ['TCS', 'INFY']
```

`st.slider("RSI below", 20, 60, 45)` draws a slider from 20 to 60 starting at 45, and returns the chosen value. The `scan()` function loops the universe, computes each symbol's latest RSI with `ta.rsi(...).iloc[-1]`, and collects the ones below the threshold. Drag the slider and - because the whole script re-runs - the table updates live. You've turned a loop and an indicator into an interactive screening tool.
## Caching SDK calls so the app stays fast
Here's a problem you'll hit immediately: every widget change re-runs the _entire_ script, which means every API call fires again. Move the slider three times and you've re-downloaded the same history three times. That's slow and wasteful. The fix is **caching** - remembering a function's result so an identical call returns instantly without touching the network.
Streamlit makes this a one-line decorator. Put `@st.cache_data` above a function and Streamlit stores its result keyed by the arguments; call it again with the same arguments and you get the stored value back, no API call. Add `ttl=60` and the cache expires after 60 seconds, so live data doesn't go stale.
EX 7Cache SDK calls with st.cache_dataNSEch10/07_caching.py
Copy
```
# st.cache_data remembers a function's result so repeat calls skip the network.
# Launch it with:  streamlit run 07_caching.py
import logging
import os
import time
from datetime import datetime, timedelta

import streamlit as st
from openalgo import api

logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.CRITICAL)
from streamlit.runtime.scriptrunner import get_script_run_ctx

LIVE = get_script_run_ctx() is not None

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


@st.cache_data(ttl=60)  # cache the result for 60 seconds; identical calls reuse it.
def load_history(symbol, exchange):
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    return client.history(symbol=symbol, exchange=exchange, interval="D",
                          start_date=start, end_date=end)


def app():
    st.title("Cached history loader")
    symbol = st.text_input("Symbol", "RELIANCE")
    df = load_history(symbol, "NSE")
    st.write(f"Loaded {len(df)} rows (re-runs are instant thanks to st.cache_data).")
    st.line_chart(df["close"])


if LIVE:
    app()
else:
    print("This is a Streamlit app. Run it with:  streamlit run 07_caching.py")
    t0 = time.time()
    load_history("RELIANCE", "NSE")
    first = time.time() - t0
    t0 = time.time()
    load_history("RELIANCE", "NSE")  # second call hits the cache
    second = time.time() - t0
    print(f"First call: {first:.3f}s | second (cached): {second:.3f}s")
```

Live output

```
This is a Streamlit app. Run it with:  streamlit run 07_caching.py
First call: 0.075s | second (cached): 0.000s
```

The only change to `load_history` is the `@st.cache_data(ttl=60)` line above it - the body is unchanged. The summary output makes the payoff visible: the first call takes real time to hit the server, and the second, identical call returns in effectively zero. In a real app this is the difference between a sluggish dashboard and a snappy one.
Tip
Use `@st.cache_data` for anything that fetches or computes data - history pulls, quote calls, indicator calculations. Pick a `ttl` that matches how fresh you need the data: a few seconds for live quotes, minutes or hours for daily history. Caching is the single biggest speed win in any Streamlit trading app.
## Try it yourself
  * In the quote board, add `SBIN` and `ICICIBANK` to the watchlist and re-run. (Remember: edit, save, and Streamlit offers to re-run.)
  * In the mini scanner, widen the universe with a few more symbols and add a second column showing each hit's latest close.
  * Add `@st.cache_data` to the `scan()` function in the scanner and notice how much snappier the slider feels.


## Recap
  * **Streamlit** turns a Python script into a web app - launch it with `streamlit run file.py`, not plain `python`.
  * `st.title`, `st.write`, `st.metric` and `st.table` are the basic display building blocks.
  * **Widgets** like `st.text_input`, `st.selectbox` and `st.slider` both draw a control and return its value into a variable.
  * The whole script **re-runs top to bottom** on every widget change - write it as if it runs once.
  * Embed charts with `st.line_chart` for a quick line or `st.plotly_chart(fig)` for your full Plotly candlesticks.
  * Wrap data-fetching functions in `@st.cache_data` so repeated runs skip the network and the app stays fast.


You can now build, chart, and wrap your ideas in an interface. From here the series turns to the engine room: the next module dives into the eighty-plus technical indicators in `openalgo.ta`, starting with trend and moving averages - the building blocks of nearly every strategy you'll write.
On this page
