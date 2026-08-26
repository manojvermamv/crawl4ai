Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 19
# Installing Libraries: pip & venv
Reach beyond the standard library. Install pandas and friends with pip, and keep projects clean with virtual environments.
PY
What you'll learn
  * ·pip install
  * ·Finding packages
  * ·Virtual environments
  * ·Why venv matters
  * ·requirements.txt
  * ·Installing pandas & yfinance


The standard library is generous, but the tools that make Python a _trading_ powerhouse - NumPy, pandas, yfinance, matplotlib - don't come built in. You install them. You met the installer, **pip** , back in Chapter 2; now we'll actually use it, and learn the one habit that keeps a Python setup from descending into chaos: the **virtual environment**. This chapter is light on Python and heavy on a few terminal commands - the small bit of housekeeping that makes everything in Module 4 possible.
## pip: installing a library
To install a package, you run **`pip install`**followed by its name, in your terminal (not inside Python):

```
pip install pandas

```

That's genuinely all it takes - pip reaches out to PyPI, downloads pandas and everything it depends on, and sets it up. Installing the libraries this whole course builds towards is just:

```
pip install numpy pandas matplotlib seaborn yfinance

```

A couple of companion commands are handy:

```
pip list              # show everything installed
pip show pandas       # details about one package: version, location, dependencies

```

Tip
If `pip` isn't recognised, use **`python -m pip install ...`**instead - it runs pip through the exact Python you're using, which sidesteps the most common "which pip?" confusion on machines with more than one Python. On a Mac you may also need`pip3`.
## Did the install work?
The honest test of an install is simple: can you import it? If this script runs without an error, you're in business:
EX 1Confirming the key libraries are installedPYch19/01_check_installed.py
Copy
```
# If these import without an error, the libraries installed correctly.
# Every one of them was added with a single "pip install" command.
import numpy
import pandas
import yfinance

print("numpy   :", numpy.__version__)
print("pandas  :", pandas.__version__)
print("yfinance:", yfinance.__version__)
```

Live output

```
numpy   : 2.4.2
pandas  : 2.3.3
yfinance: 1.4.1
```

Each of those imports would fail with a `ModuleNotFoundError` if the library weren't installed - so a clean run, printing versions, is your green light for Module 4.
## Virtual environments: a clean room per project
Here's a problem that bites everyone eventually. One project needs an old version of a library; another needs the newest. Install them globally and they fight - upgrading for one project silently breaks the other. The fix is a **virtual environment** (`venv`): a private, isolated set of libraries that belongs to _one_ project.
Project A - backtester .venv - its own libraries pandas 1.5numpy 1.26matplotlib 3.7 Project B - live data .venv - its own libraries pandas 2.3numpy 2.4yfinance 1.4 Each project gets its own isolated libraries - upgrade one without ever breaking the other.
You create and switch on a virtual environment with two commands, run once per project:

```
python -m venv .venv        # create an environment in a folder named .venv

# then "activate" it:
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac / Linux

```

Once it's active (your prompt shows `(.venv)`), every `pip install` lands _inside_ that environment, touching nothing else on your machine. Type `deactivate` to step back out.
Key idea
A **virtual environment** is a private library set for one project. Create it with **`python -m venv .venv`**, activate it, then`pip install` freely - isolated from every other project. It's the single best habit for keeping Python tidy.
## requirements.txt: a shopping list
To record exactly what your project uses - so a teammate (or future you on a new laptop) can recreate it - freeze your installed packages into a file:

```
pip freeze > requirements.txt          # save the exact versions
pip install -r requirements.txt        # later, reinstall them all at once

```

`requirements.txt` is just a plain text list of packages and versions. It turns "it works on my machine" into "it works on any machine."
Did you know?
**"pip" is a joke that installs itself.** The name is widely explained as a recursive acronym - "Pip Installs Packages" - a programmer's wink where the name refers to itself. Through that little tool, the Python community pulls an astonishing volume from PyPI: well over a _billion_ package downloads every single day, with pandas alone fetched hundreds of millions of times a month. You're tapping into one of the largest shared toolboxes ever built.
## A practical recipe
Put together, the standard opening move for any new Python project is just five lines:

```
mkdir my-analysis && cd my-analysis      # a folder for the project
python -m venv .venv                      # create its environment
.venv\Scripts\activate                    # activate it (Windows)
pip install pandas yfinance matplotlib    # install what you need
pip freeze > requirements.txt             # record it

```

Do that once and you've got a clean, reproducible workspace - exactly the setup we'll use for the data work ahead.
## Try it yourself
  * Run `pip show pandas` and read the output. What version do you have, and what other packages does it depend on?
  * Create a virtual environment in a fresh folder, activate it, and run `pip list`. Notice how short the list is - a clean slate.
  * Inside that environment, `pip install yfinance`, then run the version-check script from this chapter.


## Recap
  * **`pip install <name>`**downloads and installs a library from PyPI;`pip list` and `pip show` inspect what you have.
  * Confirm an install by **importing** it - a clean run means success.
  * A **virtual environment** (`python -m venv .venv`, then activate) gives each project its **own isolated** libraries, preventing version clashes.
  * **`requirements.txt`**(`pip freeze`) records exact versions so any machine can reproduce your setup.


You're now fully equipped: standard library plus any package you can install. But the moment you lean on more code, you'll hit more errors - that's normal, and not scary once you can read them. The next chapter turns the dreaded red error text into something you handle calmly: **errors and debugging**.
On this page
