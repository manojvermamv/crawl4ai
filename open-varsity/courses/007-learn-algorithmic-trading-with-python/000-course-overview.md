Chapters
32 chapters · 200+ runnable examples · NSE · NFO · MCX
# Learn algorithmic trading with Python
Built for traders new to Python. Start from zero - variables, NumPy, Pandas - and finish with backtested, optimised strategies and a live trading bot. Every example is real, runnable code, powered by the OpenAlgo Python SDK.
[Start Chapter 1 ](001-getting-started-with-openalgo.md)[Browse all chapters](000-course-overview.md#modules)
32
Chapters
9
Modules
80+
Indicators
100%
OpenAlgo SDK
MODULE A
## Foundations
Set up, talk to the market, and learn just enough Python, NumPy and Pandas.
[Chapter 01 Getting Started with OpenAlgo Connect the OpenAlgo Python SDK, check funds, and understand analyze vs live mode. NSE](001-getting-started-with-openalgo.md)[Chapter 02 Python Essentials for Traders The Python you actually need - variables, lists, dicts, loops and functions, in a trading context. NSE](002-python-essentials-for-traders.md)[Chapter 03 Symbols, Exchanges & Lot Sizes Master the OpenAlgo symbol format across NSE equity, NFO F&O and MCX commodities. NSENFOMCXINDEX ](003-symbols-exchanges-lot-sizes.md)[Chapter 04 Quotes, Depth & LTP Pull live snapshots - single quotes, batched multiquotes and full order-book depth. NSENFOMCX ](004-quotes-depth-ltp.md)[Chapter 05 Historical Data & Timeframes Fetch OHLCV history at any interval and reshape it for analysis. NSENFOMCX ](005-historical-data-timeframes.md)[Chapter 06 NumPy for Traders NumPy fundamentals for traders - creating arrays, indexing, vectorised math and the everyday functions, on simple price data. NSEINDEX ](006-numpy-for-traders.md)[Chapter 07 Pandas for Traders DataFrames, rolling windows, resampling and group-bys - the workhorse of market analysis. NSEMCX ](007-pandas-for-traders.md)
MODULE B
## Visualisation & Apps
Turn data into charts and interactive dashboards.
[Chapter 08 Charting with Matplotlib Static charts: price lines, return distributions, subplots and indicator overlays. NSEMCXINDEX ](008-charting-with-matplotlib.md)[Chapter 09 Interactive Charts with Plotly Zoomable candlestick charts with volume and multi-pane indicators. NSENFO ](009-interactive-charts-with-plotly.md)[Chapter 10 Live Dashboards with Streamlit Build clickable web apps - a quote board, a chart viewer and a mini scanner. NSEMCX ](010-live-dashboards-with-streamlit.md)
MODULE C
## Technical Indicators
Eighty-plus indicators from the openalgo.ta library, by category.
[Chapter 11 Trend & Moving Averages From SMA and EMA to Supertrend, Ichimoku and Parabolic SAR. NSENFOMCX ](011-trend-moving-averages.md)[Chapter 12 Momentum Indicators Measure speed and strength: RSI, MACD, Stochastic, CCI and more. NSENFO ](012-momentum-indicators.md)[Chapter 13 Volatility Indicators ATR, Bollinger Bands, Keltner and Donchian channels for range and risk. NSEMCX ](013-volatility-indicators.md)[Chapter 14 Volume Indicators Read participation with OBV, VWAP, MFI, CMF and relative volume. NSENFO ](014-volume-indicators.md)[Chapter 15 Oscillators Bounded momentum tools: ROC, TRIX, Awesome Oscillator, StochRSI, Vortex and friends. NSEMCX ](015-oscillators.md)[Chapter 16 Statistical, Hybrid & Utility Functions Regression, correlation, ADX, pivots - plus the signal helpers you'll use everywhere. NSENFO ](016-statistical-hybrid-utility-functions.md)
MODULE D
## Signals & Scanning
Convert indicators into clean signals and screen the whole market.
[Chapter 17 From Indicators to Trading Signals Build precise, de-duplicated entry and exit signals you can trust in a backtest. NSE](017-from-indicators-to-trading-signals.md)[Chapter 18 Scanning & Screeners Run a signal across dozens of symbols and rank the results. NSENFOMCX ](018-scanning-screeners.md)
MODULE E
## Strategy Playbook
Real strategy styles - each one fetched, signalled and explained.
[Chapter 19 Cash & Equity Strategies Delivery-style trend following and momentum ranking on equities. NSE](019-cash-equity-strategies.md)[Chapter 20 Intraday Strategies Opening-range breakout, VWAP reversion and intraday EMA systems. NSENFO ](020-intraday-strategies.md)[Chapter 21 Pair Trading & Statistical Arbitrage Trade the spread: ratio, z-score, correlation and beta-neutral pairs. NSE](021-pair-trading-statistical-arbitrage.md)[Chapter 22 Momentum & Volatility Trading Cross-sectional momentum plus ATR / Bollinger volatility-driven entries and sizing. NSEMCX ](022-momentum-volatility-trading.md)[Chapter 23 Seasonal & Calendar Strategies Day-of-week, month and expiry-week effects measured straight from history. NSENFO ](023-seasonal-calendar-strategies.md)[Chapter 24 Options Strategies From the option chain to buying, spreads, straddles and hedging - all by symbol. NFOINDEX ](024-options-strategies.md)
MODULE F
## Execution
Place and manage real orders through the SDK (in analyze mode).
[Chapter 25 Placing & Managing Orders Every order type - market, limit, SL, smart, basket, split - plus modify and cancel. NSENFOMCX ](025-placing-managing-orders.md)
MODULE G
## Backtesting & Optimisation
Prove an edge before risking capital - with VectorBT.
[Chapter 26 Backtesting from Scratch & with VectorBT Build a vectorised backtest by hand, then reproduce it with VectorBT and realistic costs. NSEMCX ](026-backtesting-from-scratch-with-vectorbt.md)[Chapter 27 Performance Metrics & Reporting Sharpe, Sortino, CAGR, drawdown and win-rate - plus a full QuantStats report. NSE](027-performance-metrics-reporting.md)[Chapter 28 Parameter Optimisation Sweep parameter grids, draw heatmaps and pick robust settings - not just the best. NSEMCX ](028-parameter-optimisation.md)[Chapter 29 Walk-Forward Testing & Robustness Split in- and out-of-sample, roll the window forward, and avoid fooling yourself. NSE](029-walk-forward-testing-robustness.md)
MODULE H
## Machine Learning
Teach a model to read the market, then ship a complete bot.
[Chapter 30 Machine Learning, Neural Nets & a Complete Bot Engineer features, train a classifier and a neural network, then wire it into a live OpenAlgo loop. NSENFO ](030-machine-learning-neural-nets-a-complete-bot.md)
MODULE I
## Going Live
Stream live ticks over WebSockets and manage real positions in real time.
[Chapter 31 Real-Time Data with WebSockets Stream live ticks over a WebSocket and manage a position in real time - computing stop-loss, target and trailing stop as each price arrives. NSENFOMCX ](031-real-time-data-with-websockets.md)[Chapter 32 Risk & Position Sizing Turn a signal into the right quantity - sizing by fixed-fractional risk, the stop distance, ATR and portfolio heat, with a reusable lot-aware sizer. NSENFOMCX ](032-risk-position-sizing.md)
For education only - not investment advice. Practise in analyze mode. 32 chapters built on the OpenAlgo Python SDK.
