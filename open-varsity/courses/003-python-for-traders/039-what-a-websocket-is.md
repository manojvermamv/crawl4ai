Chapters
Module 5 · Python for the Markets - Chapter 39
# What a WebSocket Is
Why live trading data streams to you instead of being asked for. A plain-words look at WebSockets - the concept, no setup required.
LIVE
What you'll learn
  * ·Request/response vs streaming
  * ·What a WebSocket is
  * ·Why ticks stream
  * ·A subscribe message
  * ·When you'd need one
  * ·SDK vs raw socket


The last two chapters had one thing in common: _you_ did the asking. Every quote meant sending a request and waiting for a reply. That's fine for an occasional check, but imagine wanting the price the _instant_ it changes - you'd have to ask again and again, thousands of times a minute. There's a better way, and it's the opposite idea: open a connection once and let the market **push** prices to you as they happen. That's a **WebSocket**. This chapter is concept-only - no code to run - because you rarely need one as a beginner, but understanding it completes your picture of how market data flows.
## Two ways to get live data: pull vs push
The APIs in Chapter 37 work by **polling** - request, response, repeat. A WebSocket works by **streaming** - one open pipe, prices pushed to you. The difference is stark:
POLLING - ask over and over WEBSOCKET - one open stream your code server your code server update? no update? 1313.60 update? no ...again and again (wasteful) subscribe (once) tick 1313.60 tick 1313.80 tick 1313.50 ...pushed the instant they happen Polling asks again and again; a WebSocket opens once and the server pushes every tick.
Key idea
**Polling** = your code repeatedly _asks_ "any update?" (request/response, over and over). **Streaming** (a WebSocket) = your code _subscribes once_ , and the server **pushes** every price change down a single open connection. Polling pulls; a WebSocket pushes.
## What a WebSocket is
A **WebSocket** is a single, long-lived, two-way connection between your program and the server. Unlike an HTTP request - which is one question and one answer, then done - a WebSocket stays **open** , and either side can send a message at any time. That's why ticks can arrive the moment a trade happens, with no asking.
Did you know?
**The WebSocket was standardised in 2011 to end an era of clever hacks.** Before it (RFC 6455), "live" web data meant either hammering the server with constant requests (**polling**) or holding a request open and praying (**long-polling**) - awkward workarounds for a web built on one-shot requests. A WebSocket replaced them with a proper two-way pipe that stays open: **full-duplex** , like a phone call where both people can talk at once, versus HTTP's exchange of sealed letters. Today the same protocol streams chat messages, multiplayer games, and live market ticks alike.
## Subscribing to a stream
The flow is simple in principle: connect, send a **subscribe** message listing what you want, then receive ticks. That subscribe message is just a small piece of JSON - the shape you already understand:
EX 1The shape of a subscribe message (no socket opened)PYch39/01_subscribe_message.py
Copy
```
import json

# A WebSocket subscription is just a small message you send ONCE to start a stream.
# (This only builds and prints the message - it does not open a real connection.)
subscribe = {
    "action": "subscribe",
    "mode": "ltp",
    "symbols": [
        {"symbol": "RELIANCE", "exchange": "NSE"},
        {"symbol": "TCS", "exchange": "NSE"},
    ],
}

print(json.dumps(subscribe, indent=2))
```

Live output

```
{
  "action": "subscribe",
  "mode": "ltp",
  "symbols": [
    {
      "symbol": "RELIANCE",
      "exchange": "NSE"
    },
    {
      "symbol": "TCS",
      "exchange": "NSE"
    }
  ]
}
```

Once subscribed, every price update arrives as a message, and you handle each one with a **callback** - a function the stream calls for you, automatically, on every tick:

```
def on_tick(tick):
    print(tick["symbol"], "is now", tick["ltp"])

# (illustrative, not run here) connect, attach the callback, subscribe, and listen:
# feed.on_message = on_tick
# feed.subscribe(["RELIANCE", "TCS"])
# feed.run_forever()      # stays open, calling on_tick for every update

```

Notice the inversion: with polling, _you_ call the server in a loop; with a stream, the server effectively calls _you_ , running `on_tick` each time a price moves. That's the whole mental shift.
## When do you actually need one?
Be honest with yourself about this:
  * **You don't need a WebSocket** to glance at prices, study history, or test ideas - a periodic `quotes` call (Chapter 38) is simpler and plenty.
  * **You do need one** when you must react _tick by tick_ - a live dashboard that updates instantly, or a fast strategy that can't afford to miss a move.


For where you are now, polling is the right tool. File the WebSocket away as the thing you'll reach for _when_ you build something genuinely real-time.
Tip
**Don't write raw WebSocket code by hand.** A bare socket means managing the connection, the handshake, reconnections when it drops, and parsing every message - fiddly and easy to get wrong. Libraries like the **OpenAlgo SDK** wrap all of that: you provide a callback and a list of symbols, and it handles the plumbing. When the day comes, use the SDK, not a raw socket.
## Try it yourself
No code to run today - just reason it through:
  * A strategy checks the price once a minute. Does it need a WebSocket, or is polling fine? Why?
  * Roughly how many requests would polling every second for 8 hours make? (That's the waste a WebSocket avoids.)
  * In your own words, what's the difference between _your code asking_ and _the server telling_?


## Recap
  * **Polling** repeatedly _asks_ for updates (request/response); a **WebSocket** opens once and the server **pushes** ticks down a single, long-lived connection.
  * A WebSocket is **full-duplex** - both sides can send at any time - which is why live ticks arrive instantly.
  * You **subscribe** with a small JSON message, then handle each tick in a **callback** function.
  * Beginners rarely need one; reach for a WebSocket (via an **SDK** , never a raw socket) only for genuinely **real-time** tools.


You've now seen every way market data reaches Python - hard-coded, files, delayed feeds, live quotes, and streams. It's time to bring the whole course together. In the final chapter, we take real prices and, step by step, turn them into **returns, a trading signal, and a performance scorecard** - and point you to where your Python-for-trading journey goes next.
On this page
