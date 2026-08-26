Chapters
Module 5 · Python for the Markets - Chapter 35
# Money, Timings & Holidays
Lakhs vs millions, 9:15 IST vs 9:30 ET - the everyday units and clocks of Indian and US markets, expressed in code.
NSEUS
What you'll learn
  * ·Lakh & crore vs million
  * ·Formatting Indian money
  * ·Market hours IST vs ET
  * ·Time zones in Python
  * ·Trading holidays
  * ·Sessions & pre-open


Two small things trip up almost everyone writing code for Indian markets, and neither is hard - they're just _different_ from the US defaults most software assumes. The first is **units** : India counts in lakhs and crores, grouped 2-2-3, not in millions grouped in threes. The second is the **clock** : the market runs 9:15 to 3:30 on its own time zone, skips weekends, and closes on a long list of holidays. Get these right and your numbers and timestamps will always make sense to an Indian trader.
## Lakhs and crores
Indian numbering groups digits **2-2-3 from the right** - so 656800 is written `6,56,800` (six lakh, fifty-six thousand, eight hundred), not the Western `656,800`. A lakh is 1,00,000 and a crore is 1,00,00,000. Python's built-in `:,` gives Western grouping, so for Indian style you write a small helper:
EX 1Formatting numbers the Indian wayPYch35/01_indian_money.py
Copy
```
def indian_format(n):
    """Format a whole number with Indian 2-2-3 digit grouping (lakh/crore style)."""
    s = f"{int(round(n)):d}"
    if len(s) <= 3:
        return s
    last3, rest = s[-3:], s[:-3]
    parts = []
    while len(rest) > 2:                 # group the rest in twos, from the right
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return ",".join(parts) + "," + last3

# The same numbers, Western grouping vs Indian grouping.
for n in [1313, 656800, 18016237, 1500000000]:
    print(f"Western {n:>14,}   ->   Indian Rs {indian_format(n)}")
```

Live output

```
Western          1,313   ->   Indian Rs 1,313
Western        656,800   ->   Indian Rs 6,56,800
Western     18,016,237   ->   Indian Rs 1,80,16,237
Western  1,500,000,000   ->   Indian Rs 1,50,00,00,000
```

The function peels off the last three digits, then groups the rest in twos. The difference is stark on big numbers: a Reliance lot's value is `6,56,800` to an Indian reader, and a billion rupees is `1,50,00,00,000` - 150 crore. Whenever you display rupee figures to Indian users, reach for this grouping; the Western commas look subtly wrong to a local eye.
Key idea
Indian numbers group **2-2-3** from the right: **lakh** = `1,00,000` (10^5), **crore** = `1,00,00,000` (10^7). Python's `:,` does Western grouping, so use a small helper for Indian style. One crore = 100 lakh = 10 million.
## Market hours across time zones
The NSE cash session runs **09:15 to 15:30 IST** , weekdays only; the US runs **09:30 to 16:00 ET**. To reason about both safely, attach a real time zone to your datetimes with Python's **`zoneinfo`**, and convert with**`astimezone`**:
EX 2Market hours across IST and ETPYch35/02_market_hours.py
Copy
```
from datetime import datetime, time
from zoneinfo import ZoneInfo

ist = ZoneInfo("Asia/Kolkata")
et = ZoneInfo("America/New_York")

# One fixed moment - 11:00 on a Thursday in Mumbai - shown in two time zones.
moment = datetime(2026, 6, 25, 11, 0, tzinfo=ist)
print("Mumbai   (IST):", moment.strftime("%a %H:%M %Z"))
print("New York (ET) :", moment.astimezone(et).strftime("%a %H:%M %Z"))
print()

# NSE cash session is 09:15 to 15:30 IST, on weekdays only.
def nse_open(dt):
    dt = dt.astimezone(ist)
    return dt.weekday() < 5 and time(9, 15) <= dt.time() <= time(15, 30)

for label, m in [("Thu 11:00 IST", datetime(2026, 6, 25, 11, 0, tzinfo=ist)),
                 ("Thu 16:00 IST", datetime(2026, 6, 25, 16, 0, tzinfo=ist)),
                 ("Sun 11:00 IST", datetime(2026, 6, 28, 11, 0, tzinfo=ist))]:
    print(f"{label}: NSE open? {nse_open(m)}")
```

Live output

```
Mumbai   (IST): Thu 11:00 IST
New York (ET) : Thu 01:30 EDT

Thu 11:00 IST: NSE open? True
Thu 16:00 IST: NSE open? False
Sun 11:00 IST: NSE open? False
```

12am9am12pm3:307pm12am NSE 9:15 - 15:30 IST (pre-open 9:00) US market in IST: 7:00pm to 1:30am next day On an IST clock: the NSE trades by day, the US by night - the two barely overlap.
The output makes the gap concrete: 11:00 in Mumbai is 01:30 the _previous night_ in New York. That's why, on an IST clock, the US market only comes alive in your evening. The `nse_open` check combines the weekday test from Chapter 23 with a time-zone-aware conversion, so it's correct no matter where the code runs.
Note
**IST is UTC+5:30 - one of the world's few half-hour time zones.** Most zones are whole hours off UTC; India (with Sri Lanka) sits on a thirty-minute offset, and the entire country uses this _single_ zone despite spanning nearly two hours of real sunrise difference. The lesson for code: never assume whole-hour offsets or that "local time" means one thing - always attach a real zone with `zoneinfo` and let it do the arithmetic.
## Holidays and special sessions
Weekends are easy (`weekday() >= 5`), but markets also close on a long list of **trading holidays** - Republic Day, Holi, Diwali, Independence Day and more - that don't follow any simple rule. There's no formula; you check the date against the exchange's published holiday list for the year. The day also has structure beyond the bell: a **pre-open** auction from 09:00 to 09:15 sets the opening price before continuous trading begins.
Did you know?
**Once a year, the Indian market opens at night - on Diwali.** On Diwali evening the NSE and BSE hold a special one-hour session called **Muhurat Trading** , considered an auspicious moment to begin the new Samvat (the traditional accounting year). It's the only scheduled trading on what is otherwise a holiday, and many traders place a small symbolic buy for good fortune. A centuries-old ritual, conducted on a modern electronic exchange - a very Indian blend of the ancient and the algorithmic.
## Try it yourself
  * Format `12345678` and `99000` with `indian_format`. Read them aloud in lakhs and crores.
  * Convert `datetime(2026, 6, 25, 9, 30, tzinfo=et)` (US open) into IST - what evening time does the US market open for an Indian trader?
  * Add a check to `nse_open` that also rejects a hard-coded holiday date of your choice (e.g. `dt.date() == date(2026, 1, 26)`).


## Recap
  * Indian numbers group **2-2-3** (**lakh** 10^5, **crore** 10^7); use a small helper since `:,` is Western.
  * NSE trades **09:15-15:30 IST** (pre-open from 09:00); the US trades **09:30-16:00 ET** - barely overlapping on an IST clock.
  * Attach real time zones with **`zoneinfo`**and convert with**`astimezone`**;**IST is UTC+5:30**.
  * Markets close on **weekends and holidays** (no simple rule - check the published list).


You can now speak the market's language of money and time. It's finally time to look closely at the unit of market data itself - the bar that every chart is built from. The next chapter dissects **OHLCV data** : open, high, low, close and volume, and the candle they form.
On this page
