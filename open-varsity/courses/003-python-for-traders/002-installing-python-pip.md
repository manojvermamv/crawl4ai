Chapters
Module 1 · Getting Started with Python - Chapter 02
# Installing Python & pip
Get Python onto your computer the painless way, and meet pip - the tool that installs everything else you'll use.
PY
What you'll learn
  * ·Download & install Python
  * ·Windows vs Mac notes
  * ·Checking your version
  * ·What pip is
  * ·Your first terminal command
  * ·Avoiding common setup traps


In the last chapter we made the case for Python. Now let's actually get it running on _your_ computer - because everything that follows, every example and every chart, you'll want to run yourself. This is the one chapter that's mostly setup rather than ideas, so we'll keep it short, practical, and trap-free. Twenty minutes from now you'll have written and run your very first program.
## Step 1: Get Python onto your computer
There are a few ways to install Python, but for an absolute beginner there's a clear winner: the **official installer from[python.org](https://www.python.org/downloads/)**. It's free, it's maintained by the people who make Python, and it works the same on Windows and Mac.
Head to the downloads page and click the big button that says **Download Python** (it offers you the latest version automatically). Then run the file you downloaded.
Heads up
**Windows users - read this or you'll hit a wall.** On the very first screen of the installer there's a small checkbox at the bottom: **"Add python.exe to PATH"**. Tick it before clicking Install. That one box is the difference between typing `python` and having it just work, versus a confusing "not recognized" error later. If you miss it, no harm done - just run the installer again and tick it.
On a **Mac** , the installer just walks you through Next - Next - Done. (macOS does ship with an ancient Python under the name `python3`, but installing the latest from python.org is cleaner and avoids surprises.)
## Step 2: Check it actually worked
Installing software and _confirming_ it installed are two different things. Let's confirm.
First, open a **terminal** - the plain text window where you type commands:
  * **Windows:** press Start, type `cmd`, and open **Command Prompt** (or **PowerShell**).
  * **Mac:** press Cmd+Space, type `terminal`, and open **Terminal**.


Now type this and press Enter:

```
python --version

```

You should see something like:

```
Python 3.14.4

```

The exact numbers will differ - any `3.x` is perfect. If you see a version, congratulations: Python is installed and on your PATH.
Tip
On some Macs and Linux machines the command is `python3` instead of `python` (and the installer there keeps an old `python` pointing elsewhere). If `python` gives you an error or shows version 2-something, just use **`python3`**everywhere in this course. Same language, longer name.
## Step 3: Your first program
Time for the rite of passage. Open a plain text editor, paste in the lines below, and save the file as **`hello.py`**. Then, in your terminal, run`python hello.py`.
EX 1Your first Python program - run it yourselfPYch02/01_hello.py
Copy
```
# Your very first Python program.
# Save it as hello.py, then run it from a terminal with:  python hello.py
import sys

print("Hello, markets! Python is working.")
print("You are running Python version", sys.version.split()[0])

# Python is also a calculator. A quick profit check on one share:
buy_price = 100.0
sell_price = 105.5
profit = sell_price - buy_price
print(f"Bought at {buy_price}, sold at {sell_price}, profit of {profit} per share.")
```

Live output

```
Hello, markets! Python is working.
You are running Python version 3.14.4
Bought at 100.0, sold at 105.5, profit of 5.5 per share.
```

Three small ideas are hiding in there, and we'll spend whole chapters on each soon: **`print()`**shows text on screen,**`import`**borrows a ready-made tool (here`sys` , to read the version), and the last line does a little **arithmetic** and slots the answers into a sentence. Don't worry about the details yet - the point is simply that _you ran code, and the computer answered._
## Step 4: Meet pip, Python's gateway to half a million tools
Python by itself is powerful, but its real superpower is the enormous library of free add-on tools other people have written - including NumPy and pandas, which we'll use constantly. The program that fetches and installs those tools is called **pip** , and it came bundled with your Python install.
Check it's there:

```
pip --version

```

When the time comes, installing a library is gloriously simple - one line, like this (we'll do it for real in Chapter 19):

```
pip install pandas

```

That command reaches out to a giant online warehouse called **PyPI** - the Python Package Index - finds the tool, downloads it, and installs it for you.
Your computer pip install pandas PyPI 500,000+ free packages asks for a tool downloads & installs it One line - pip fetches a tool from PyPI and sets it up for you.
Did you know?
**PyPI hosts more than half a million packages** - over 500,000 free, ready-to-use Python tools, from stock-charting libraries to whole machine-learning frameworks. Each `pip install` is one short command away from any of them. Very few languages have a free toolbox even close to this size, and it's a big part of _why_ finance fell in love with Python.
## Five common traps (and the one-line fix)
Almost every beginner hits one of these. Here's the cheat sheet so you don't lose an evening to it:
  * **"'python' is not recognized"** (Windows) - PATH wasn't set. Re-run the installer and tick **"Add python.exe to PATH"**.
  * **`python`opens version 2 or errors** (Mac/Linux) - use **`python3`**instead.
  * **`pip`not found** - try **`pip3`**, or`python -m pip` which always works.
  * **You installed Python twice** - stick to one version to avoid confusion; uninstall the spare.
  * **"Permission denied" when installing** - don't fight it with admin rights; we'll use a clean **virtual environment** in Chapter 19, which sidesteps the whole problem.


Note
You do **not** need to memorise any of this. Bookmark the chapter, get `python --version` and `python hello.py` working once, and move on. Setup is a one-time tax; the fun part starts the moment it's paid.
## Try it yourself
  * Run `python --version` and note your version number. Anything starting with `3` is good to go.
  * Change the `sell_price` in `hello.py` to a number _below_ the buy price, save, and re-run. What does the profit line say now? (You just made Python report a loss.)
  * Add one more line: `print(2026 - 1991)`. Run it. You've just asked Python how old it is - we'll see why that number matters in a moment.


## Recap
  * Install Python from the **official python.org installer** - and on Windows, **tick "Add python.exe to PATH"**.
  * Confirm it with **`python --version`**in a terminal (use**`python3`**if`python` doesn't behave).
  * You wrote and ran your **first program** , `hello.py` - `print`, `import`, and a dash of arithmetic.
  * **pip** installs free libraries from **PyPI** , a warehouse of over half a million tools - the engine behind Python's reputation.
  * Setup traps are common and each has a one-line fix; pay the one-time tax and you're done.


You've got Python running and you've run code from a file. But typing into a bare terminal gets old fast. In the next chapter we'll set up a proper, friendly home for your code - **VS Code** - and meet **Jupyter** , the interactive notebook that traders love for poking at data.
On this page
