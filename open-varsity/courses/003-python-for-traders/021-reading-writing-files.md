Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 21
# Reading & Writing Files
Save your results and load data from disk - open files safely, read lines, and write a small report.
PY
What you'll learn
  * ·Opening a file
  * ·Reading text
  * ·The with block
  * ·Writing & appending
  * ·File paths
  * ·Saving a small report


Everything your programs have done so far vanishes the moment they finish - the variables are forgotten, the results gone. To do anything useful with data, a program needs to **read** information from disk and **write** its results back. Saving a watchlist, loading yesterday's prices, exporting a report: all of it is file handling, and Python makes it refreshingly simple. This is the bridge between a throwaway script and a real tool.
## Writing a file
To write to a file you **`open`**it in`"w"` (write) mode and call `write`. The modern way always wraps this in a **`with`**block, for a reason we'll see in a moment:
EX 1Writing lines to a text filePYch21/01_write.py
Copy
```
# Writing a file: open it in "w" (write) mode, inside a with-block.
lines = ["RELIANCE,1313.60", "TCS,2109.00", "INFY,1056.60"]

with open("watchlist.txt", "w") as f:     # "w" creates the file (or overwrites it)
    for line in lines:
        f.write(line + "\n")              # write() does NOT add newlines for you

print("Wrote", len(lines), "lines to watchlist.txt")
```

Live output

```
Wrote 3 lines to watchlist.txt
```

`open("watchlist.txt", "w")` creates the file (in the current folder), and `f.write(...)` puts text into it. Two things to note: `write` does **not** add line breaks for you, so we tack on `"\n"` ourselves; and `"w"` mode starts the file fresh.
The mode letter you pass to `open` decides what happens:
"r"readload what's there "w"writecreate or OVERWRITE "a"appendadd to the end Three modes: read, write (overwrite), and append.
Heads up
**`"w"`mode erases the file's existing contents** the instant you open it. Open `watchlist.txt` in `"w"` and whatever was there is gone, replaced by what you write. If you mean to _add_ to a file rather than replace it, you want `"a"` - more on that below. This is a genuinely common way to lose data, so register it now.
## The with block, and why it matters
You'll notice every example uses `with open(...) as f:`. The **`with`**block automatically**closes** the file when you're done - even if an error happens partway through. An open file that's never closed can lose data that's still sitting in a buffer, or lock the file from other programs.
Key idea
Always open files with **`with open(name, mode) as f:`**. The`with` block guarantees the file is properly closed afterwards, no matter what. Modes: **`"r"`**read,**`"w"`**write (overwrite),**`"a"`**append.
## Reading a file back
Reading is the mirror image - open in `"r"` mode (or omit the mode, since read is the default). You can grab the whole file at once with `read()`, or, more usefully for data, loop over it line by line:
EX 2Reading a file whole, then line by linePYch21/02_read.py
Copy
```
# Reading a file back: open it in "r" (read) mode - the default.
with open("watchlist.txt", "r") as f:
    content = f.read()                # the whole file as one big string
print("--- whole file ---")
print(content)

# More often you loop line by line, parsing as you go.
print("--- parsed ---")
with open("watchlist.txt") as f:      # "r" is assumed if you omit the mode
    for line in f:
        symbol, price = line.strip().split(",")
        print(f"{symbol:10} {float(price):>9.2f}")
```

Live output

```
--- whole file ---
RELIANCE,1313.60
TCS,2109.00
INFY,1056.60

--- parsed ---
RELIANCE     1313.60
TCS          2109.00
INFY         1056.60
```

Looping over the file object hands you one line at a time, including its trailing newline - which is why we `strip()` it before `split(",")`. That two-step (`strip` then `split`) is the bread-and-butter of reading simple data files by hand.
## Appending
To add to a file without destroying what's there, open it in **`"a"`**(append) mode. New writes land at the end:
EX 3Appending a line to an existing filePYch21/03_append.py
Copy
```
# "a" (append) mode adds to the end without erasing what is already there.
with open("watchlist.txt", "a") as f:
    f.write("HDFCBANK,1642.40\n")

# Read it back to confirm the new line joined the others.
with open("watchlist.txt") as f:
    print(f.read())
```

Live output

```
RELIANCE,1313.60
TCS,2109.00
INFY,1056.60
HDFCBANK,1642.40
```

`HDFCBANK` joins the three names already in the file, instead of replacing them. Append mode is perfect for logs - a running record you keep adding lines to, like a journal of trades or signals.
Did you know?
**Dropbox is built on Python - and so was its creator's career.** The file-syncing service used by hundreds of millions of people runs huge amounts of Python, and from 2013 to 2019 its team even included Guido van Rossum, the person who _invented_ Python. A product whose entire job is reading and writing files, powered by - and partly steered by the maker of - the very language you're using to read and write files right now.
## A note on file paths
`"watchlist.txt"` is a **relative** path - it points to a file in the folder your program is running from. You can also give an **absolute** path like `"C:/data/watchlist.txt"` (forward slashes work fine on Windows in Python, and avoid the backslash headaches). For anything beyond the basics, Python's `pathlib` module - with its handy `Path` object - is the modern, tidy way to build and join paths; keep the name in mind for when your projects grow.
Tip
Plain text files are great for simple notes and logs, but real market data is almost always tabular - rows and columns of numbers. You _could_ parse that by hand with `split(",")` as we did here, but in Module 4 you'll meet **pandas** , which reads an entire CSV into a table with a single line. Hand-parsing is good to understand once; after that, let pandas do it.
## Try it yourself
  * Write your three favourite stock symbols to a file `mylist.txt`, one per line, then read it back and print each in uppercase.
  * Open the same file in `"a"` mode and add a fourth symbol. Read it again to confirm all four are there.
  * Now open it in `"w"` mode and write a single symbol. Read it back - notice the other three are gone. (That's the overwrite warning, made real.)


## Recap
  * Open files with **`with open(name, mode) as f:`**- the`with` block always closes them safely.
  * Modes: **`"r"`**read,**`"w"`**write (which**overwrites**), **`"a"`**append (adds to the end).
  * **Write** with `f.write(text)` (add your own `"\n"`); **read** with `f.read()` or by looping line by line (then `strip()` and `split()`).
  * Paths can be **relative** (to the current folder) or **absolute** ; use forward slashes, and `pathlib` for bigger projects.


You just hand-parsed comma-separated text with `split(",")`. There's a more structured cousin of that format used everywhere in trading - **JSON** , the language market APIs speak. We've glimpsed it twice already; in the next chapter we give it the full treatment.
On this page
