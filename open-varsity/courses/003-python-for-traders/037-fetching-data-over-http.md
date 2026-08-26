Chapters
Module 5 · Python for the Markets - Chapter 37
# Fetching Data over HTTP
How programs talk to markets. Use the requests library to hit OpenAlgo's REST API and read the JSON that comes back - live, from India.
NSELIVE
What you'll learn
  * ·What an API is
  * ·Request & response
  * ·The requests library
  * ·Calling OpenAlgo REST
  * ·Reading the JSON
  * ·Handling errors


Until now, every price came from a file or from yfinance's delayed feed. To actually _trade_ , you need data straight from the source - live, from a broker. Programs get that data by talking to an **API** over the internet, and in this chapter you make your first real calls: first to a generic web service to learn the mechanics, then to **OpenAlgo** , fetching live Indian market data into Python. This is the moment your code plugs into the real market.
## What is an API?
An **API** (Application Programming Interface) is simply a way for one program to ask another for data or action. Your code sends a **request** to a server; the server sends back a **response**. On the web this happens over **HTTP** - the same protocol your browser uses - and the answer almost always comes back as **JSON** (Chapter 22). That's the whole model:
Your programrequests API server(OpenAlgo) 1. request (URL + JSON) 2. response (200 OK + JSON) An API call is a round trip: your program asks, the server answers in JSON.
## The requests library
Python's **`requests`**library makes that round trip a one-liner. Let's hit a free public testing service to see the mechanics, with nothing to set up:
EX 1A first HTTP request with requestsPYch37/01_requests_basics.py
Copy
```
import requests

# A GET request fetches data from a URL. httpbin.org is a free testing service.
resp = requests.get("https://httpbin.org/json", timeout=10)

print("Status code  :", resp.status_code)             # 200 means OK
print("Content type :", resp.headers["Content-Type"])  # tells us it's JSON
data = resp.json()                                     # parse the JSON body -> a dict
print("Top-level keys:", list(data.keys()))
```

Live output

```
Status code  : 200
Content type : application/json
Top-level keys: ['slideshow']
```

Three things to learn here, and they're the same for _every_ API: `requests.get(url)` sends the request; `resp.status_code` tells you if it worked (**200** means OK); and `resp.json()` parses the JSON body into a Python dict you can index. Master these three and you can talk to any web API on earth.
Key idea
**`requests.get(url)`**(or`.post(url, json=...)`) makes an HTTP call. Check **`resp.status_code`**(200 = OK), then**`resp.json()`**to turn the response into a Python dict. That's the universal pattern for every web API.
## Calling OpenAlgo's REST API
OpenAlgo exposes the market through exactly this kind of REST API. You **POST** a small JSON body - your key, the symbol, the exchange - to an endpoint, and get a JSON quote back:
EX 2Fetching a live quote from OpenAlgo's REST APIPYch37/02_openalgo_rest.py
Copy
```
import os

import requests

host = os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000")
api_key = os.getenv("OPENALGO_API_KEY", "your_api_key_here")

# OpenAlgo's REST API: POST a small JSON body, get a JSON response back.
resp = requests.post(
    f"{host}/api/v1/quotes",
    json={"apikey": api_key, "symbol": "RELIANCE", "exchange": "NSE"},
    timeout=10,
)

print("Status code :", resp.status_code)          # 200 = the request succeeded
quote = resp.json()
print("Status      :", quote["status"])           # "success"
print("Fields      :", list(quote["data"].keys()))
print("LTP (live)  :", quote["data"]["ltp"])       # fills with the live price in market hours
```

Live output

```
Status code : 200
Status      : success
Fields      : ['ask', 'bid', 'high', 'low', 'ltp', 'oi', 'open', 'prev_close', 'volume']
LTP (live)  : 1313.6
```

There it is - a live LTP for Reliance, straight from the market into Python, using nothing but `requests`. The response is a dict with a `status` and a `data` block holding the price fields. Notice we read the key with **`os.getenv`**, never pasting it into the code.
Tip
**Keep your API key out of your code.** Store it in an environment variable - `OPENALGO_API_KEY` - and read it with `os.getenv("OPENALGO_API_KEY")`. A key is like a password to your trading account; a key hard-coded into a file you share (or push to GitHub) is a key you've given away. Every example in this course uses the `os.getenv` pattern for exactly this reason.
## The cleaner way: the SDK
Raw `requests` works, but for a service you use a lot, a **library** (an "SDK") wraps the calls so you skip the JSON plumbing. OpenAlgo's Python SDK turns a history request straight into a pandas DataFrame:
EX 3Real OHLCV from the OpenAlgo SDKPYch37/03_openalgo_history.py
Copy
```
import os

from openalgo import api

# The OpenAlgo SDK wraps the REST calls for you - cleaner than raw requests.
client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# history() hands back a ready-made pandas DataFrame - no JSON to unpack.
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                    start_date="2026-06-10", end_date="2026-06-24")

print("Rows:", len(df))
print(df[["open", "high", "low", "close", "volume"]].tail(3).round(2))
```

Live output

```
Rows: 11
              open    high     low   close    volume
timestamp                                           
2026-06-22  1316.7  1344.9  1314.1  1326.5  12931213
2026-06-23  1328.9  1333.0  1304.0  1309.5  15400184
2026-06-24  1305.7  1322.0  1297.5  1313.6  11030917
```

One call, and you have a clean DataFrame of real Reliance OHLCV - ready for every Module 4 skill. Under the hood it's making the same HTTP requests you just made by hand; the SDK simply does the boilerplate for you. (This SDK is the foundation of OpenAlgo's full **Algo Trading** course - a natural next step after this one.)
Did you know?
**The style of API you just used began as a student's thesis.** "REST" - the conventions behind almost every web API, including OpenAlgo's - was defined by **Roy Fielding** in his year-2000 PhD dissertation. He described a simple, durable way for programs to talk over HTTP: plain URLs, standard verbs like GET and POST, and data in and out as JSON. Two decades later, that academic framework quietly underpins how nearly every app, website and trading system on the internet exchanges data.
## Handling errors
The network is unreliable, so real API code is defensive - and you already have the tools from Chapter 20. Always check the status code, wrap risky calls in `try/except`, and pass a `timeout` so a dead server can't hang your program forever:

```
try:
    resp = requests.post(url, json=body, timeout=10)
    resp.raise_for_status()          # raises if status_code isn't 2xx
    data = resp.json()
except requests.RequestException as e:
    print("Request failed:", e)

```

A **200** means success; a **404** means the endpoint wasn't found; a **500** means the server itself errored. Checking, not assuming, is the difference between a robust tool and one that crashes on the first hiccup.
## Try it yourself
  * Change the OpenAlgo REST example to fetch `TCS` instead of `RELIANCE`, and print its LTP.
  * Use the SDK's `client.history(...)` to pull a different date range, then run `.describe()` on the `close` column.
  * Add a `try/except` around the REST call that prints a friendly message if the server is unreachable (try a wrong port to test it).


## Recap
  * An **API** lets programs exchange data over HTTP: your code sends a **request** , the server returns a **response** (usually **JSON**).
  * **`requests`**:`.get` /`.post`, check **`status_code`**(200 = OK), parse with**`.json()`**.
  * **OpenAlgo's REST API** takes a POST with your key, symbol and exchange and returns a live quote; the **SDK** wraps it into clean Python (a DataFrame from `history`).
  * Keep your **API key in an environment variable** (`os.getenv`), and **handle errors** with status checks, `try/except` and `timeout`.


You've now pulled both delayed data (yfinance) and live data (OpenAlgo). The difference between them - and _when each one matters_ - is worth a chapter of its own. Next we put a **live quote and a delayed quote side by side** and see exactly what "real-time" buys you.
On this page
