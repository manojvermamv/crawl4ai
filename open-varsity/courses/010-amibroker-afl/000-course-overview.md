Chapters
36 chapters · indicators to live automation · beginner to intermediate
# AmiBroker AFL
Learn to code in AFL - the language behind one of the fastest backtesting engines a trader or investor can own. Built for traders and investors alike, it starts from your very first plotted line and builds up to scanners, complete trading systems, backtests and live order automation. No heavy programming - if you can read a chart, you can do this.
[Start Chapter 1 ](001-what-is-amibroker-afl.md)[Browse all chapters](000-course-overview.md#modules)
36
Chapters
8
Modules
AFL
From scratch
India
Market focus
## Why learn AmiBroker?
AmiBroker is a native C++ analysis platform built for speed. It was the world's first 64-bit technical-analysis program for Windows, its formula engine runs across every core of your CPU, and its charting renders up to forty times faster than before. In practice that means you can scan thousands of symbols or backtest a system over years of history and a basket of stocks in seconds - and that fast feedback is exactly what lets you iterate on an idea. AFL is the small, friendly language that drives all of it: one formula can be an indicator, a market-wide scan, or a full backtested system.
MODULE A
## Meet AmiBroker
What AmiBroker is, how the Formula Editor works, and the one idea - arrays - that makes AFL click.
[Chapter 01 What is AmiBroker & AFL The big picture - charts, the Analysis window, and the four things AFL can do: indicate, explore, scan and backtest. Basics](001-what-is-amibroker-afl.md)[Chapter 02 The Formula Editor & Your First Indicator Write, apply and save your first AFL - a one-line RSI plot - and learn the editor habits that save hours. BasicsAFL ](002-the-formula-editor-your-first-indicator.md)[Chapter 03 How AFL Thinks: Arrays & Bars The single most important idea in AFL - every variable is a whole array of values, one per bar. Get this and everything else is easy. BasicsAFL ](003-how-afl-thinks-arrays-bars.md)[Chapter 04 Price Arrays, Variables & Operators Meet O, H, L, C, V and Volume, store results in variables, and do maths across an entire chart at once. BasicsAFL ](004-price-arrays-variables-operators.md)
MODULE B
## The AFL Language
The grammar of AFL - plotting, parameters, built-in functions, logic, looking back, and writing your own functions.
[Chapter 05 Plotting & Chart Styles Draw lines, candles, histograms and bands - and control colour, thickness and style like a pro. ChartAFL ](005-plotting-chart-styles.md)[Chapter 06 Parameters: Interactive Controls Turn hard-coded numbers into sliders, colour pickers and dropdowns with Param, ParamColor, ParamList and friends. ChartAFL ](006-parameters-interactive-controls.md)[Chapter 07 Built-in Functions & Indicators A guided tour of the functions you will use every day - MA, EMA, RSI, MACD, ATR, BBands and how to read the function reference. IndicatorAFL ](007-built-in-functions-indicators.md)[Chapter 08 Conditions, Logic & IIf Build true/false arrays with comparisons and AND/OR, then choose values bar-by-bar with the all-important IIf. AFL](008-conditions-logic-iif.md)[Chapter 09 Looking Back: Ref, Cross & BarsSince Reach into earlier (and later) bars with Ref, detect crossovers with Cross, and count bars since an event. AFL](009-looking-back-ref-cross-barssince.md)[Chapter 10 Dates, Times & the Trading Session Read the calendar and the clock - Day, Month, time-of-day - and answer the question every intraday system asks: has a new day started? AFLRealtime ](010-dates-times-the-trading-session.md)[Chapter 11 Arrays vs Loops: the for-loop Most AFL needs no loops - but some logic (like a trailing stop) does. Learn when and how to write a clean for-loop. AFL](011-arrays-vs-loops-the-for-loop.md)[Chapter 12 Custom Functions & Procedures Package logic you reuse into your own functions and procedures, with local and global scope. AFL](012-custom-functions-procedures.md)
MODULE C
## Charting & Visualisation
Make charts that communicate - arrows, colour-coded candles, dynamic titles, multi-pane layouts and GFX dashboards.
[Chapter 13 Arrows, Shapes & Text Mark signals on the chart with PlotShapes and PlotText - up arrows, down arrows, stars and labels. Chart](013-arrows-shapes-text.md)[Chapter 14 Colours, Ribbons & Conditional Candles Colour candles by trend, paint background ribbons and build at-a-glance visual context. Chart](014-colours-ribbons-conditional-candles.md)[Chapter 15 The Title Bar & StrFormat Build a rich, dynamic chart header - name, OHLC, percent change - with Title, StrFormat and WriteIf. Chart](015-the-title-bar-strformat.md)[Chapter 16 Multiple Panes & Comparing Symbols Stack indicator panes, and pull in another symbol's data with Foreign and PlotForeign for relative strength. Chart](016-multiple-panes-comparing-symbols.md)[Chapter 17 GFX Dashboards Draw your own panels - boxes, gradients and text - with the low-level GFX functions for a polished dashboard. Chart](017-gfx-dashboards.md)
MODULE D
## Exploration & Scanning
Screen the whole market at once - the Analysis window, AddColumn, filters and ranking.
[Chapter 18 Exploration: the Analysis Window Turn AFL into a spreadsheet over your whole watchlist with Filter and AddColumn. Exploration](018-exploration-the-analysis-window.md)[Chapter 19 Building a Signal Scanner Scan dozens of symbols for a real setup - MACD crosses, RSI extremes and breakouts - and list only the hits. Exploration](019-building-a-signal-scanner.md)[Chapter 20 Filtering, Sorting & Ranking Sort the results, colour the cells, and rank your universe by strength or volume. Exploration](020-filtering-sorting-ranking.md)
MODULE E
## Building Trading Systems
The mechanics of a tradable system - signals, clean entries and exits, stops, targets and sizing.
[Chapter 21 Buy, Sell, Short & Cover The four reserved arrays that turn an idea into a system - and how AmiBroker reads them. Strategy](021-buy-sell-short-cover.md)[Chapter 22 Clean Signals: ExRem, Flip & No Repainting Remove duplicate signals with ExRem, hold state with Flip, and delay one bar so your system never repaints. Strategy](022-clean-signals-exrem-flip-no-repainting.md)[Chapter 23 Stops, Targets & ApplyStop Add a stop-loss and profit target - both as visual chart levels and as real backtest exits with ApplyStop. Strategy](023-stops-targets-applystop.md)[Chapter 24 Position Sizing & Trade Delays Control how much you trade with SetPositionSize, and when fills happen with SetTradeDelays and SetOption. Strategy](024-position-sizing-trade-delays.md)
MODULE F
## Backtesting & Optimisation
Prove an edge before risking capital - run a backtest, read the report, and optimise without fooling yourself.
[Chapter 25 Your First Backtest Run a full backtest in the Analysis window, set the date range and settings, and see your equity curve. Backtest](025-your-first-backtest.md)[Chapter 26 Reading the Backtest Report Make sense of the numbers - net profit, CAR, drawdown, win rate, payoff and the risk-adjusted ratios. Backtest](026-reading-the-backtest-report.md)[Chapter 27 Optimisation & Robustness Sweep parameters with Optimize(), read the results, and choose robust settings - not just the curve-fit peak. Backtest](027-optimisation-robustness.md)
MODULE G
## Strategy Playbook
Five complete, explained systems - each one ready for you to backtest and drop your own report images into.
[Chapter 28 Strategy: EMA Crossover System The classic trend system, built end-to-end - signals, arrows, delays and a backtest you can run yourself. StrategyBacktest ](028-strategy-ema-crossover-system.md)[Chapter 29 Strategy: Supertrend System Build the popular ATR-based Supertrend from scratch with a for-loop, plot the trailing stop, and trade it. StrategyBacktest ](029-strategy-supertrend-system.md)[Chapter 30 Strategy: VWAP Intraday System An intraday mean-reversion / trend system around VWAP, with time-based entries and a session reset. StrategyBacktest ](030-strategy-vwap-intraday-system.md)[Chapter 31 Strategy: Donchian / Opening-Range Breakout Two breakout classics - the Donchian channel and the opening-range breakout - coded and ready to test. StrategyBacktest ](031-strategy-donchian-opening-range-breakout.md)[Chapter 32 Strategy: RSI Pullback & Mean Reversion A counter-trend pullback system using RSI with a trend filter - buying dips in an uptrend. StrategyBacktest ](032-strategy-rsi-pullback-mean-reversion.md)
MODULE H
## Real-Time, Alerts & Automation
Take a system live - multiple time frames, alerts to your phone, and order automation through OpenAlgo.
[Chapter 33 Multiple Time Frames Read a higher time frame on a lower-time-frame chart with TimeFrameSet, TimeFrameGetPrice and friends. Realtime](033-multiple-time-frames.md)[Chapter 34 Alerts: Telegram & Voice Fire alerts the moment a signal triggers - on-chart AlertIf, a Telegram message, and a spoken voice alert. Realtime](034-alerts-telegram-voice.md)[Chapter 35 Automating Orders with OpenAlgo Send your AFL signals to OpenAlgo to place real orders - button and signal-based automation, in sandbox first. RealtimeOpenAlgo ](035-automating-orders-with-openalgo.md)[Chapter 36 Where to Go Next A map of what you have learned, the parts of AFL still to explore, and how to keep getting better. Basics](036-where-to-go-next.md)
For education only - not investment advice. Practise in sandbox trading (analyzer mode in OpenAlgo). 36 chapters of AFL, beginner to intermediate.
