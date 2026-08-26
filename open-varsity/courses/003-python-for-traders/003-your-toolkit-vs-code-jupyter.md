Chapters
Module 1 · Getting Started with Python - Chapter 03
# Your Toolkit: VS Code & Jupyter
Set up a clean, friendly place to write code - and meet Jupyter, the notebook traders love for poking at data.
PY
What you'll learn
  * ·Installing VS Code
  * ·Running your first .py file
  * ·What a Jupyter notebook is
  * ·Cells & interactive output
  * ·Editor vs notebook
  * ·A comfortable setup


You've got Python installed and you've run a file from the terminal. That works, but typing into a bare black window gets old fast - no colours, no help, no easy way to fix a typo on line 3. A carpenter doesn't work on the floor; they set up a workbench. Let's set up yours. By the end of this chapter you'll have a proper, friendly place to write code - and you'll meet the interactive notebook that data people practically live in.
## A proper home for your code: VS Code
To write code comfortably you want a **code editor** - a text editor that understands code, colours it in, spots your typos, and runs it at the click of a button. There are several good ones, but for a beginner the easy pick is **Visual Studio Code** , usually just called **VS Code**. It's free, it's made by Microsoft, and it's far and away the most widely used editor in the world.
Getting set up takes three steps:
  1. Download it from **[code.visualstudio.com](https://code.visualstudio.com/)** and install it.
  2. Open VS Code, click the **Extensions** icon in the left bar, search for **"Python"** , and install the official one by Microsoft. This is what gives you colours, autocomplete, and a green **Run** button.
  3. Use **File - Open Folder** to open a folder for your course work. Everything you write lives there.


Tip
Always open a **folder** , not a single file. VS Code is happiest when it can see your whole project - it makes running files, finding things, and later installing libraries far smoother. Make one folder called something like `python-for-traders` and keep all your practice files in it.
## Running your first file in VS Code
Inside that folder, create a new file called `average.py`, paste in the code below, and press the **Run** button (the triangle in the top-right). The output appears in a panel at the bottom.
EX 1A week of closes, averaged - run it with the Run buttonPYch03/01_watchlist_average.py
Copy
```
# A taste of things to come - run this in VS Code by pressing the Run button.
# We take a week of closing prices and work out the average.
prices = [101.2, 103.5, 102.8, 104.1, 105.6]   # five daily closes

average = sum(prices) / len(prices)             # add them up, divide by how many

print("Five closing prices:", prices)
print(f"Average close this week: {average:.2f}")
```

Live output

```
Five closing prices: [101.2, 103.5, 102.8, 104.1, 105.6]
Average close this week: 103.44
```

That's a genuine little piece of analysis: five days of closing prices, averaged to `103.44`. We're using a **list** (`[...]`) and two built-in helpers, `sum()` and `len()` - all of which get their own chapters soon. For now, notice how much nicer this is than the terminal: colours, a click to run, and a tidy output panel.
## Notebooks: the data explorer's playground
There's a second way to run Python that data analysts and quants adore: the **Jupyter notebook**. Instead of one file that runs top to bottom, a notebook is a stack of **cells** - little blocks of code you run one at a time, with the output appearing right underneath each one. You can run a cell, look at the result, tweak it, run it again, and build up an analysis step by step - all while keeping notes in between.
Jupyter notebook In [1]: prices = [101.2, 103.5, 102.8, 104.1, 105.6] In [2]: sum(prices) / len(prices) Out[2]: 103.44 In [3]: plt.plot(prices) # a chart appears right here Out[3]: [ a little price chart ] Run a cell, see its output right below - then build up your analysis one step at a time.
Two small things make notebooks feel magical when you're exploring data:
  * **Output appears inline.** Run a cell that draws a chart, and the chart shows up right there in the page - no separate window.
  * **The last line auto-displays.** In a notebook you don't even need `print()` - just put `sum(prices) / len(prices)` on the last line of a cell and the answer pops out below it (that's the `Out[2]: 103.44` above).


The easiest way in is VS Code itself: install the **Jupyter** extension, create a file ending in **`.ipynb`**, and you've got a notebook. (Or run`pip install jupyter` and type `jupyter notebook` in your terminal for the classic browser version.)
Did you know?
**The name "Jupyter" is a nod to three open-source languages it was built for: Julia, Python, and R.** Project Jupyter went on to win the 2017 ACM Software System Award - the same prestigious prize previously given to Unix, the World Wide Web, and TeX. Not bad for a tool you'll use to doodle with stock prices.
## Editor or notebook - which should I use?
Both, eventually - they're good at different jobs:
  * A **script** (`.py`) is best for code you'll _reuse or automate_ - a program you run again and again, start to finish.
  * A **notebook** (`.ipynb`) is best for _exploring and learning_ - trying ideas, inspecting data, sketching charts, keeping notes.


Note
For this course, **use whichever you enjoy**. Following along in a notebook is lovely because you can run each snippet and immediately poke at it. Writing the same code in a `.py` file and pressing Run is just as valid. There's no wrong choice - the Python inside is identical.
## Try it yourself
  * Open the bottom panel in VS Code (View - Terminal) and run `python average.py` from there too. Same result, second way to run it.
  * In `average.py`, add a sixth price to the list, save, and re-run. Watch the average change on its own.
  * If you set up a notebook, paste the three lines into separate cells and run them one by one. Notice you only needed `print()` in the script, not in the notebook.


## Recap
  * **VS Code** is a free, hugely popular editor; add the official **Python extension** and you get colours, autocomplete, and a one-click **Run** button.
  * Always **open a folder** , not a lone file, and keep your practice work together.
  * A **Jupyter notebook** runs code in **cells** with output shown inline - perfect for exploring data, and the last line auto-displays without `print()`.
  * Use **scripts** for reusable programs and **notebooks** for exploring; for this course, either is great.


Your workbench is ready and the tools are laid out. From here on it's all Python. In the next chapter we start with the most fundamental building block of every program there is - the **variable** - and we'll use it to store prices, symbols, and quantities.
On this page
