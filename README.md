# Concepted By: Noah Moore
## Question: Is there a correlation between price fluctuations and momentum based indicators?

## Project Sponsors:
### Atlas Capital

Task:
Create a model to classify and identify asset prices rising and lowering utilizing Bollinger bands and Moving Average convergence divergence

ML Model:
Decision Tree: Sci-Learn library
Graphics via Matplotlib

Input and Target:
Input: BB and MACD
Output: Bullish or Bearish

Data Sampling
Obtain data samples via quantconnect API add to dictionary and use Pandas to format into DataFrames
Training Data:
Data{
“PriceChange”: []
“Bollinger Band”:[]
“MACD”:[]
}
Use PriceChange to test if bullish or bearish
Real Data (model will be filled with live data):
Data{
“Bollinger Band”:[]
“MACD”:[]
}
Data:
*all data will be defined by pre-established periods (i.e. month, day, hour, minute, tick)*
Price Change-Price change within defined period of time
Bollinger Band- STDEV (distribution value)
MACD- First degree derivative of slope of Moving Average Convergence Divergence


Data Periods:
Start with daily PriceChange
BB and MACD obtained at noon (can tweak times later)
And transition to hourly to every minute (as long as logical correlations exist and there’s accuracy)

Project targets
50+% Model accuracy (enough accuracy to establish correspondence to have a gaining purchasing effect)
