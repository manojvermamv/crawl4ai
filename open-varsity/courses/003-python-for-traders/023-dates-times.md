Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 23
# Dates & Times
Markets run on a clock and a calendar. Parse, format and do arithmetic with dates - sessions, expiries and gaps.
PY
What you'll learn
  * ·date & datetime
  * ·Parsing & formatting
  * ·strftime & strptime
  * ·timedelta maths
  * ·Market session times
  * ·Weekday & holidays


Every price, every trade, every candle carries a timestamp - and timestamps are where tidy data gets messy. Different formats, time zones, weekends, market hours, holidays: dates and times have more quirks than any other kind of data. The good news is Python's `datetime` module handles the hard parts, and once you know a few moves, working with dates becomes routine. This chapter gives the timestamp the respect it deserves.
## date and datetime
There are two everyday types. A **`date`**is a calendar day (no time); a**`datetime`**is a day _and_ a time. You build them by passing the parts, and read the parts back as attributes:
EX 1Building dates and reading their partsPYch23/01_date_datetime.py
Copy
```
from datetime import date, datetime

d = date(2026, 6, 25)                     # a calendar date
dt = datetime(2026, 6, 25, 15, 30, 0)     # a date AND a time (3:30 PM, market close)

print("Date     :", d)
print("Datetime :", dt)
print("Parts    : year", d.year, "month", d.month, "day", d.day)
print("Time     : hour", dt.hour, "minute", dt.minute)
print("Weekday  :", d.strftime("%A"))     # the day name
```

Live output

```
Date     : 2026-06-25
Datetime : 2026-06-25 15:30:00
Parts    : year 2026 month 6 day 25
Time     : hour 15 minute 30
Weekday  : Thursday
```

`date(2026, 6, 25)` is the 25th of June; add `15, 30` and you've got `datetime(2026, 6, 25, 15, 30)` - half past three in the afternoon, the moment the NSE cash market closes. Every part - `.year`, `.month`, `.day`, `.hour`, `.minute` - is right there to read.
## Formatting and parsing: strftime and strptime
Timestamps constantly need to move between `datetime` objects (which you can do maths on) and **text** (which humans and files use). Two methods, with a handy mnemonic, do the conversion:
EX 2strftime to format, strptime to parsePYch23/02_format_parse.py
Copy
```
from datetime import datetime

dt = datetime(2026, 6, 25, 15, 30)

# strftime: a datetime -> formatted TEXT   (f = format)
print("ISO date  :", dt.strftime("%Y-%m-%d"))
print("Readable  :", dt.strftime("%d %b %Y, %I:%M %p"))
print("Day & time:", dt.strftime("%A %H:%M"))

# strptime: TEXT -> a datetime   (p = parse)
text = "2026-06-25 09:15"
parsed = datetime.strptime(text, "%Y-%m-%d %H:%M")
print("Parsed    :", parsed, "| type:", type(parsed).__name__)
```

Live output

```
ISO date  : 2026-06-25
Readable  : 25 Jun 2026, 03:30 PM
Day & time: Thursday 15:30
Parsed    : 2026-06-25 09:15:00 | type: datetime
```

Both use the same little **format codes** - `%Y` for year, `%H` for hour, and so on. Here's a cheat-sheet of the ones you'll reach for most:
Common strftime / strptime codes %Yfour-digit year %mmonth number %dday of month %Hhour (24-hour) %Mminute %Aweekday name %bmonth, short %pAM / PM "%Y-%m-%d %H:%M" -> 2026-06-25 15:30 Mix the codes to build any layout you need.
Key idea
**`strftime`**turns a datetime into text (**f** = _format_); **`strptime`**turns text into a datetime (**p** = _parse_). Both use `%` codes like `%Y-%m-%d %H:%M`. The mnemonic: **f** ormat out, **p** arse in.
## Date arithmetic with timedelta
To add or subtract time, use a **`timedelta`**- a _duration_. Adding one to a datetime gives you another datetime:
EX 3timedelta maths and a market-hours checkPYch23/03_timedelta_session.py
Copy
```
from datetime import datetime, timedelta, time

# timedelta does date and time arithmetic.
close = datetime(2026, 6, 25, 15, 30)
print("Close         :", close)
print("One week later:", close + timedelta(weeks=1))
print("90 min before :", close - timedelta(minutes=90))

# Is a given moment within NSE cash hours (09:15 to 15:30, weekdays only)?
def is_market_open(dt):
    return dt.weekday() < 5 and time(9, 15) <= dt.time() <= time(15, 30)

print("11:00 Thu open?", is_market_open(datetime(2026, 6, 25, 11, 0)))   # True
print("16:00 Thu open?", is_market_open(datetime(2026, 6, 25, 16, 0)))   # False (after close)
print("11:00 Sun open?", is_market_open(datetime(2026, 6, 28, 11, 0)))   # False (weekend)
```

Live output

```
Close         : 2026-06-25 15:30:00
One week later: 2026-07-02 15:30:00
90 min before : 2026-06-25 14:00:00
11:00 Thu open? True
16:00 Thu open? False
11:00 Sun open? False
```

`timedelta(weeks=1)` jumps a week ahead; `timedelta(minutes=90)` steps back 90 minutes. And the `is_market_open` function shows the real payoff: combining **`.weekday()`**(where Monday is 0 and Saturday/Sunday are 5 and 6) with a**`time`**range to ask "is this moment inside NSE trading hours, on a weekday?" That single idea - filtering data to market hours, excluding weekends - is something you'll do constantly with real price data.
Note
Indian markets run on a single time zone, **IST** - and the NSE cash session is **09:15 to 15:30**. Real holiday calendars (Diwali, Republic Day, and the rest) are a separate list you'd check against; weekends you can catch with `.weekday()` as we did here. We'll lean on pandas for heavier time-series work in Module 4, but the building blocks are exactly these.
Did you know?
**To a computer, all time is just a count of seconds since 1970.** Most systems track time as the number of seconds elapsed since midnight on 1 January 1970 UTC - a moment programmers call the "Unix epoch." It works beautifully, with one catch: the classic 32-bit version of that counter runs out of room on 19 January 2038, an echo of the Y2K scare known as the "Year 2038 problem." Modern Python uses bigger numbers and sidesteps it - but somewhere under your timestamps, a very large second-counter is quietly ticking.
## Try it yourself
  * Format `datetime(2026, 6, 25, 9, 15)` as `"09:15 AM on Thursday"` using the right `%` codes.
  * Parse the text `"25-12-2026"` into a date with `strptime` and the format `"%d-%m-%Y"`. What weekday is Christmas 2026?
  * Use `timedelta(days=...)` to find the date 45 days after `date(2026, 6, 25)` - a rough options-expiry horizon.


## Recap
  * **`date`**is a calendar day;**`datetime`**adds a time. Read parts via`.year` , `.month`, `.hour`, etc.
  * **`strftime`**formats a datetime to text,**`strptime`**parses text to a datetime - both use`%` codes (f = format out, p = parse in).
  * **`timedelta`**represents a duration; add or subtract it to do date arithmetic.
  * **`.weekday()`**(Mon = 0) plus a**`time`**range filters data to weekday market hours - a constant need with price data.


That's nearly all of Module 3. You can import libraries, install packages, read and write files and JSON, handle errors, and work with dates. The final piece is a _meta_ -skill - the one that makes you self-sufficient for everything still ahead: knowing how to **get unstuck** on your own. It's the next, and last, chapter of Module 3.
On this page
