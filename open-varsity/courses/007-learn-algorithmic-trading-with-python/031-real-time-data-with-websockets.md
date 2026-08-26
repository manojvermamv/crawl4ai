Chapters
Module I · Going Live - Chapter 31
# Real-Time Data with WebSockets
Stream live ticks over a WebSocket and manage a position in real time - computing stop-loss, target and trailing stop as each price arrives.
NSENFOMCX
What you'll learn
  * ·Polling (REST) vs streaming (WebSocket)
  * ·When to use the API vs the feed
  * ·connect() & subscribe_ltp/quote/depth
  * ·Compute a live stop-loss & target
  * ·Trailing stop-loss on every tick
  * ·A complete live trade manager


You've built strategies, backtested them, even wired up a complete bot. But notice something about every example so far: _you_ asked for the data. You called `quotes()`, you called `history()` - you reached out and **pulled** a value each time you wanted one. That's perfect for analysis and for placing orders. It's the wrong tool the moment you have a live position and need to react the _instant_ price moves.
This final chapter adds the missing piece: data that is **pushed** to you, tick by tick, the moment it changes - and the live trade-management logic that rides on top of it. By the end you'll compute a stop-loss, a target and a trailing stop straight from a real-time stream.
## What exactly is a WebSocket?
A normal API call is a quick conversation that ends immediately. You knock on the door, ask _"what's the price of Reliance?"_ , get one answer, and the door shuts. Want a fresh price a second later? Knock again. This request-response pattern is called **polling** , and it's how every chapter up to now has worked.
A **WebSocket** is different. You knock once, the door opens, and it _stays_ open - a single, persistent, two-way line between your script and OpenAlgo. You tell it which symbols you care about, and from then on the exchange **streams** prices to you the instant a trade happens. No more knocking. The data simply arrives.
Key idea
Polling = _you pull_ data, again and again. A WebSocket = _the market pushes_ data to you over one always-on connection. For anything that must react in real time, push beats pull every single time.
That "push" model is why a WebSocket is fast and light. Polling fifty symbols once a second is fifty separate requests every second hammering your broker connection. A single WebSocket subscription delivers all fifty over **one** connection, only when something actually changes.
## API or feed - which should you use?
Both have their place, and a good trading system uses each for what it's best at. The rule is simple: **pull with the REST API for actions and history; stream over the feed for live monitoring.**  
| Use the REST API when...  | Use the WebSocket feed when...  |  
| --- | --- |  
| You need a one-off snapshot, or a value once a minute  | You need every price change the instant it happens  |  
| Placing, modifying or cancelling orders  | Watching an open position for its exit  |  
| Downloading historical candles for a backtest  | Running a live dashboard or a scalping screen  |  
| Scanning a universe every few minutes  | Trailing a stop or reacting to the order book  |  
Tip
A live bot almost always uses **both at once** : it _places_ the entry order through the REST API (Chapter 25), then _monitors_ that position over the WebSocket feed and fires the exit order - again through the REST API - when the stream tells it to. Orders go out by pull; price comes in by push.
## Open your first stream
Three method calls run every stream: `connect()` opens the line, `subscribe_ltp()` registers the symbols you want plus a **callback** function, and `disconnect()` closes it cleanly at the end. The callback is the heart of it - OpenAlgo calls _your_ function automatically every time a new tick arrives, handing it the latest data.
EX 1Your first live LTP streamNSEch31/01_ltp_stream.py
Copy
```
# Your first live stream: open one connection and let prices come to you.
import os
import time

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
    ws_url=os.getenv("OPENALGO_WS_URL", "ws://127.0.0.1:8765"),
)

instruments = [
    {"exchange": "NSE", "symbol": "RELIANCE"},
    {"exchange": "NSE", "symbol": "INFY"},
]


# This callback fires every time the exchange pushes a fresh tick.
def on_ltp(message):
    tick = message["data"]
    print(f"{tick['symbol']:10s} LTP: {tick['ltp']}")


client.connect()                       # open the persistent connection once
client.subscribe_ltp(instruments, on_data_received=on_ltp)

time.sleep(10)                         # let ticks stream in for ten seconds

client.unsubscribe_ltp(instruments)
client.disconnect()                    # always close the line when you are done
```

Each message your callback receives is a small dictionary. The fields you'll use live under `message["data"]` - `message["data"]["ltp"]` is the last traded price. That nesting matters, so keep it in mind for every callback below.
## The three modes: LTP, quote and depth
Just like the snapshot calls back in Chapter 4, the stream comes in three depths of detail. You pick one by calling the matching `subscribe_` method:
  * **LTP** (`subscribe_ltp`) - just the last traded price and a timestamp. The lightest, fastest stream.
  * **Quote** (`subscribe_quote`) - the full snapshot: LTP plus open, high, low, close and volume.
  * **Depth** (`subscribe_depth`) - the live order book, the stacked bids and asks from Chapter 4, updating in real time.


Here's quote mode, giving you enough to show price, the day's change and its range as they move:
EX 2Streaming the full quoteNSEch31/02_quote_stream.py
Copy
```
# Quote mode streams the full snapshot - price, volume and the day's range.
import os
import time

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
    ws_url=os.getenv("OPENALGO_WS_URL", "ws://127.0.0.1:8765"),
)

instruments = [{"exchange": "NSE", "symbol": "SBIN"}]


def on_quote(message):
    q = message["data"]
    change = q["ltp"] - q["close"]          # close here is yesterday's close
    print(
        f"{q['symbol']}  LTP {q['ltp']:.2f}  "
        f"({change:+.2f})  vol {q['volume']}  "
        f"range {q['low']:.2f}-{q['high']:.2f}"
    )


client.connect()
client.subscribe_quote(instruments, on_data_received=on_quote)

time.sleep(10)

client.unsubscribe_quote(instruments)
client.disconnect()
```

Note
Your callback runs on a **background thread** while your main script keeps going - that's how prices arrive without you waiting for them. So keep the callback quick: read the tick, update a couple of variables, decide whether to exit. Never run a slow download or a long calculation inside it, or you'll fall behind the stream.
## Computing a stop-loss and a target
Now the part that actually protects your money. Two numbers turn a raw position into a managed trade:
  * A **stop-loss** - the price at which you admit the trade is wrong and exit, capping the loss to an amount you decided _before_ entering.
  * A **target** - the price at which you're happy to take profit and walk away.


For a long (buy) position you set them around your entry price: the stop sits _below_ , the target _above_. The gap between them is your **risk-reward** : risk 30 points to make 60 and you have a 1:2 trade. Then you let the live stream watch price for you - the moment LTP touches either line, you're out.
EX 3Live stop-loss and target monitorMCXch31/03_stop_and_target.py
Copy
```
# Watch a live position and exit the moment price hits the stop-loss or target.
import os
import time

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
    ws_url=os.getenv("OPENALGO_WS_URL", "ws://127.0.0.1:8765"),
)

SYMBOL, EXCHANGE = "CRUDEOIL20JUL26FUT", "MCX"
entry = 6000.0           # the price you bought at (from your fill - see Chapter 25)
stop_loss = entry - 30   # cap the loss 30 points below entry
target = entry + 60      # take profit 60 points above (a 1:2 risk-reward)
position_open = True


def on_ltp(message):
    global position_open
    if not position_open:
        return
    ltp = float(message["data"]["ltp"])
    if ltp <= stop_loss:
        print(f"\nSTOP-LOSS hit at {ltp:.2f} - exit for a small, planned loss")
        position_open = False
    elif ltp >= target:
        print(f"\nTARGET hit at {ltp:.2f} - exit in profit")
        position_open = False
    else:
        print(f"holding  LTP {ltp:.2f}  SL {stop_loss:.2f}  TGT {target:.2f}", end="\r")


client.connect()
client.subscribe_ltp([{"exchange": EXCHANGE, "symbol": SYMBOL}], on_data_received=on_ltp)

while position_open:      # the feed, not a polling loop, drives the exit
    time.sleep(0.2)

client.unsubscribe_ltp([{"exchange": EXCHANGE, "symbol": SYMBOL}])
client.disconnect()
```

Read the callback closely: on every tick it asks two questions - _have we fallen to the stop?_ and _have we risen to the target?_ - and flips `position_open` to `False` the instant either is true. The `while position_open` loop in the main script does nothing but wait; the **feed** drives the decision, not a timer.
Heads up
In a real bot, the `exit` would place a market SELL order through the REST API, exactly as in the order chapter - here we just print, so you can study the logic safely in analyze mode. And `entry` would come from your actual fill price, not a hard-coded number.
## Trailing the stop (TSL)
A fixed stop-loss is good; a **trailing stop-loss** is smarter when a trade runs in your favour. The idea: as price climbs, you drag the stop up behind it - never letting it slip back down. The trade is given room to breathe, but every new high _locks in_ a little more profit. If price then reverses, you exit having kept most of the gain instead of riding it all the way back to your original stop.
The mechanics are just two lines of bookkeeping per tick: remember the highest price seen (`high_water`), and set the stop a fixed distance under it. The stop only ever moves **up**.
EX 4A trailing stop-loss on every tickMCXch31/04_trailing_stop.py
Copy
```
# A trailing stop follows price up to lock in profit - it never moves back down.
import os
import time

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
    ws_url=os.getenv("OPENALGO_WS_URL", "ws://127.0.0.1:8765"),
)

SYMBOL, EXCHANGE = "CRUDEOIL20JUL26FUT", "MCX"
TRAIL = 25.0             # keep the stop 25 points under the best price seen
entry = 6000.0
high_water = entry       # highest price reached since entry
stop_loss = entry - TRAIL
position_open = True


def on_ltp(message):
    global high_water, stop_loss, position_open
    if not position_open:
        return
    ltp = float(message["data"]["ltp"])
    if ltp > high_water:             # new high -> drag the stop up behind it
        high_water = ltp
        stop_loss = high_water - TRAIL
    if ltp <= stop_loss:             # price slipped back to the trailing stop
        print(f"\nTRAILING STOP hit at {ltp:.2f}  (stop had locked to {stop_loss:.2f})")
        position_open = False
    else:
        print(f"LTP {ltp:.2f}  peak {high_water:.2f}  stop {stop_loss:.2f}", end="\r")


client.connect()
client.subscribe_ltp([{"exchange": EXCHANGE, "symbol": SYMBOL}], on_data_received=on_ltp)

while position_open:
    time.sleep(0.2)

client.unsubscribe_ltp([{"exchange": EXCHANGE, "symbol": SYMBOL}])
client.disconnect()
```

Key idea
The whole secret of a trailing stop is the one-way ratchet: `stop = max(stop, new_high - trail)`. Because of that `max`, the stop can rise but can _never_ fall. Profit, once locked, stays locked.
## A complete live trade manager
Let's put it together the way you actually would in production - a small class that holds the trade's state and exposes a single `on_tick` method as the callback. It carries a fixed target _and_ a trailing stop at the same time, exiting on whichever comes first. This is the pattern your real bot would wrap around a freshly filled order.
EX 5A complete SL + target + TSL managerMCXch31/05_trade_manager.py
Copy
```
# A complete live trade manager: a fixed target plus a trailing stop, in one class.
import os
import time

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
    ws_url=os.getenv("OPENALGO_WS_URL", "ws://127.0.0.1:8765"),
)


class TradeManager:
    def __init__(self, entry, trail, target):
        self.entry = entry
        self.trail = trail
        self.target = entry + target
        self.high_water = entry
        self.stop = entry - trail
        self.open = True

    def on_tick(self, message):
        if not self.open:
            return
        ltp = float(message["data"]["ltp"])
        if ltp > self.high_water:               # trail the stop upward only
            self.high_water = ltp
            self.stop = max(self.stop, ltp - self.trail)
        if ltp >= self.target:
            self.close(ltp, "TARGET")
        elif ltp <= self.stop:
            self.close(ltp, "TRAILING STOP")
        else:
            print(f"LTP {ltp:.2f}  stop {self.stop:.2f}  tgt {self.target:.2f}", end="\r")

    def close(self, ltp, reason):
        print(f"\n{reason} hit at {ltp:.2f} - closing the position")
        self.open = False


mgr = TradeManager(entry=6000.0, trail=25.0, target=60.0)
inst = [{"exchange": "MCX", "symbol": "CRUDEOIL20JUL26FUT"}]

client.connect()
client.subscribe_ltp(inst, on_data_received=mgr.on_tick)
while mgr.open:
    time.sleep(0.2)
client.unsubscribe_ltp(inst)
client.disconnect()
```

Wrapping the logic in a class keeps every moving part - entry, high-water mark, stop, target - tidily together, and makes it trivial to run _several_ managers at once, one per open position, all fed by the same connection.
## Reconnects and heartbeats
A live connection has to survive a flaky network. OpenAlgo sends a **ping** roughly every 30 seconds; the client answers with a **pong** automatically to prove it's still alive. If the line does drop, the client reconnects and re-subscribes to your symbols for you. The one rule for your code: keep your state (entry, stop, target) in variables that outlive a single message - as we've done throughout - so a brief blip never loses track of your trade.
Note
On a local setup the feed lives at `ws://127.0.0.1:8765`. Behind a domain in production it's served over TLS at `wss://yourdomain.com/ws`. Set `OPENALGO_WS_URL` in your `.env` and the same code works in both places.
## Try it yourself
  * Point the LTP stream at an MCX symbol like `CRUDEOIL20JUL26FUT` and run it in the evening - the commodity session keeps ticking long after stocks close.
  * Change the trailing example's `TRAIL` from 25 to 10 points and watch how a tighter stop exits sooner but locks in less.
  * Add a **time stop** to the trade manager: store the start time and close the position if it hasn't hit target or stop within, say, 15 minutes.
  * Swap `subscribe_ltp` for `subscribe_depth` and print the best bid and ask from `message["data"]["depth"]` as they move.


## Recap
  * A WebSocket is one persistent, two-way connection: the market **pushes** prices to you, instead of you **pulling** them with repeated API calls.
  * **Pull** with the REST API for snapshots, history and placing orders; **stream** over the feed for live position monitoring. Real bots use both together.
  * Every stream is `connect()` -> `subscribe_ltp/quote/depth(instruments, on_data_received=...)` -> `disconnect()`, and your **callback** receives each tick with the price under `message["data"]["ltp"]`.
  * A **stop-loss** caps your loss and a **target** books profit; the live feed exits the instant price touches either.
  * A **trailing stop** ratchets up behind a rising price - `stop = max(stop, high - trail)` - locking in gains while never giving them back.
  * Keep callbacks fast and your trade state in long-lived variables, so reconnects and heartbeats never trip you up.


That's the loop a real trading desk runs on: pull to act, stream to watch, and let well-defined stops and targets do the deciding. You now have every piece - from your first `quotes()` call to a live, self-managing position. Go build something, and trade it in analyze mode first.
On this page
