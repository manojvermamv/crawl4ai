Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 24
# Getting Unstuck
The real superpower: helping yourself. Use help(), read the docs, search well, and never be truly stuck again.
PY
What you'll learn
  * ·help() & dir()
  * ·Reading documentation
  * ·Searching effectively
  * ·Reading error messages
  * ·Minimal examples
  * ·Asking good questions


Here's a truth no course usually admits: nobody remembers all of this. Professional developers look things up dozens of times a day - syntax, method names, what some function returns. The skill that actually separates people who thrive from people who give up isn't memory; it's **knowing how to get unstuck**. This short chapter - the last of Module 3 - hands you that skill. Master it and you'll never be truly stuck again, which means you're ready for the bigger libraries ahead.
## Ask Python itself: type() and dir()
Your first move when confused about a value isn't to search the web - it's to ask Python directly. **`type()`**tells you _what_ something is; **`dir()`**lists _what it can do_ :
EX 1type() and dir() - interrogating an objectPYch24/01_type_dir.py
Copy
```
# Stuck on a mystery value? Ask Python what it is and what it can do.
prices = [101.2, 103.5, 102.8]

print("What is it?  ", type(prices).__name__)      # list

# dir() lists the methods - the verbs you can use on it.
# We hide the __dunder__ names to see just the useful ones.
methods = [m for m in dir(prices) if not m.startswith("__")]
print("What can it do?", methods)
```

Live output

```
What is it?   list
What can it do? ['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```

In two lines you've learned that `prices` is a `list` and discovered every method it offers - `append`, `sort`, `count`, and the rest - without looking anything up. When some value surprises you, `type()` and `dir()` are the fastest way to understand it. (We hid the `__dunder__` names - the double-underscore ones Python uses internally - to keep the list readable.)
## Read the manual: help()
Once `dir()` shows you a method exists, **`help()`**tells you how to use it - it prints the official documentation, right in your terminal:
EX 2help() prints the built-in docsPYch24/02_help.py
Copy
```
# help() prints the built-in documentation for almost anything.
# Here we ask what str.strip actually does, instead of guessing.
help(str.strip)
```

Live output

```
Help on method descriptor strip:

strip(self, chars=None, /) unbound builtins.str method
    Return a copy of the string with leading and trailing whitespace removed.

    If chars is given and not None, remove characters in chars instead.
```

There it is, straight from the source: `strip` removes leading and trailing whitespace, and takes an optional `chars` argument. No guessing, no web search - the manual was built into Python all along. In a notebook you can also type `str.strip?` for the same thing.
Key idea
Three built-ins make Python self-documenting: **`type(x)`**(what is it?),**`dir(x)`**(what can it do?), and**`help(x)`**(how do I use it?). Reach for these _before_ searching the web - they're faster and always match your exact version.
## Capture and inspect
When you're unsure what a line of code _produces_ , don't squint at it - **capture the result in a variable and inspect it** :
EX 3Capturing a result to examine itPYch24/03_capture_inspect.py
Copy
```
# When you are unsure what a function gives back, capture it and inspect it.
text = "RELIANCE,TCS,INFY"
result = text.split(",")

print("Result     :", result)
print("Type        :", type(result).__name__)
print("How many    :", len(result))
print("First item  :", result[0], "->", type(result[0]).__name__)
```

Live output

```
Result     : ['RELIANCE', 'TCS', 'INFY']
Type        : list
How many    : 3
First item  : RELIANCE -> str
```

Printing the value, its `type`, its `len`, and a sample item turns a mystery into facts. This habit - run a small piece, look at exactly what came out - is the single most useful debugging move there is, and it works at every level, all the way up to pandas DataFrames in the next module.
## The unstuck ladder
When the quick checks don't crack it, escalate calmly through these steps - most problems fall before you reach the bottom:
1Read the error - its last line names the problem 2Ask Python - type(), dir(), help() 3Search the exact error message, in quotes 4Boil it down to a tiny, minimal example 5Ask a clear question - show what you tried Work down only as far as you need - most problems are solved by step 1 or 2.
## Searching and asking well
Two of those rungs deserve a tip each. When you **search** , paste the **exact error message** (the bottom line of the traceback), in quotes - someone has almost certainly hit it before. Trust the official docs and reputable Q&A sites; be wary of code you don't understand.
And a **minimal example** - the smallest snippet that still shows the problem - is magic. Half the time, the act of stripping your code down to the essentials reveals the bug yourself, before you ever ask anyone.
Did you know?
**Programmers debug by talking to a rubber duck.** It sounds absurd, but "rubber duck debugging" is a real, beloved technique from the classic book _The Pragmatic Programmer_ : you keep a toy duck on your desk and, when stuck, explain your code to it line by line, out loud. Astonishingly often, the act of articulating the problem clearly makes the bug obvious before you finish your sentence. Writing a good question - or a minimal example - works for exactly the same reason. No duck required, but it helps.
## Try it yourself
  * Run `dir("RELIANCE")` (a string) and find three methods you recognise from Chapter 8. Then `help()` one of them.
  * Make a dictionary and use `type()` and `dir()` to confirm it's a `dict` and discover its `.keys()` and `.values()` methods.
  * Next time you hit an error, explain the failing line out loud (to a duck, a pet, or the wall) before searching. Notice how often it clicks.


## Recap
  * The skill that matters most is **getting unstuck** , not memorising - even experts look things up constantly.
  * Ask Python first: **`type()`**(what),**`dir()`**(what it can do),**`help()`**(how to use it).
  * **Capture and inspect** a result - print its value, type and length - to turn confusion into facts.
  * When stuck, escalate the **unstuck ladder** : read the error, ask Python, search the exact message, make a minimal example, ask a clear question.
  * A **minimal example** often reveals the bug on its own - the secret behind rubber-duck debugging.


That completes **Module 3** - you can now use the whole Python ecosystem and stand on your own feet when something breaks. You're ready for the part traders have been waiting for. In **Module 4** , we meet the libraries that make Python a data powerhouse - **NumPy** and **pandas** - starting with the fast arrays that deliver the speed you saw all the way back in Chapter 1.
On this page
