#!/usr/bin/env python
# coding: utf-8

# ![Alt Text](image/logo_picture.PNG)
# 

# In[40]:


import pandas as pd # Reading the csv data here
df = pd.read_csv(r'D:\Information Technology\Goldman sachs\Goldman Sachs stock data.csv')
df.head() # printing it to see it down there


# In[42]:


df.info() # checking the information about the dataset


# In[44]:


df.isnull().sum() # Checking the null values of the data set


# In[46]:


df.describe() # describing it in term of mean, stander deviation etc.


# In[50]:


# conveting the date column datatype
df['Date'] = pd.to_datetime(df['Date']) # done converting it


# # Time series analysis 

# In[56]:


import matplotlib.pyplot as plt # importing 'matplotlib'
df = df.sort_values('Date') # sort datas
df.set_index('Date', inplace=True) # set date as index


# In[58]:


# Plot closing price over time 

plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price', color='goldenrod')
plt.title('Goldman Sachs Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True)
plt.show() 


# In[60]:


# Calculate daily returns

df['Daily Return'] = df['Adj Close'].pct_change()

# Plot Daily Returns
plt.figure(figsize=(12, 4))
plt.plot(df['Daily Return'], color='purple')
plt.title('Daily Return (%)')
plt.xlabel('Date')
plt.ylabel('Return')
plt.grid(True)
plt.show()


# # Volatility Analysis

# In[67]:


# 30-day rolling volatility
df['30D Volatility'] = df['Daily Return'].rolling(window=30).std() # std dev of 30days rolling

import matplotlib.pyplot as plt # ploting it here as a line plot

plt.figure(figsize=(14, 6))
plt.plot(df['30D Volatility'], color='red', label='30-Day Rolling Volatility')
plt.title('30-Day Rolling Volatility of Daily Returns (Goldman Sachs)')
plt.xlabel('Date')
plt.ylabel('Volatility (Std Dev of Daily Return)')
plt.legend()
plt.grid(True)
plt.show()


# # Volume analysis - stocks traded on that perticular day

# In[74]:


import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot Closing Price
ax1.plot(df.index, df['Close'], color='goldenrod', label='Closing Price')
ax1.set_ylabel('Price ($)', color='goldenrod')
ax1.tick_params(axis='y', labelcolor='goldenrod')
ax1.set_title('Goldman Sachs: Price vs. Volume')

# Create a second y-axis for volume
ax2 = ax1.twinx()
ax2.bar(df.index, df['Volume'], alpha=0.3, color='red', label='Volume')
ax2.set_ylabel('Volume', color='red')
ax2.tick_params(axis='y', labelcolor='red')

fig.tight_layout()
plt.show()


# #  Candlestick Chart Using plotly

# In[81]:


import plotly.graph_objects as go

# Reset index in case Date is the index
df_reset = df.reset_index()

fig = go.Figure(data=[go.Candlestick(
    x=df_reset['Date'],
    open=df_reset['Open'],
    high=df_reset['High'],
    low=df_reset['Low'],
    close=df_reset['Close'],
    increasing_line_color='green',
    decreasing_line_color='red'
)])

fig.update_layout(
    title='Goldman Sachs Candlestick Chart',
    xaxis_title='Date',
    yaxis_title='Price ($)',
    xaxis_rangeslider_visible=False,
    template='plotly_dark'
)

fig.show()


# In[83]:


pip install mplfinance


# In[97]:


# Filter last 100 days
df_recent = df.tail(200)

mpf.plot(
    df_recent,
    type='candle',
    volume=True,
    style='yahoo',
    title='Goldman Sachs - Last 100 Days',
    mav=(20, 50),
    figsize=(14, 6)
)


# In[103]:


# Filter last 100 days
df_recent = df.tail(100)

mpf.plot(
    df_recent,
    type='candle',
    volume=True,
    style='yahoo',
    title='Goldman Sachs - Last 100 Days',
    mav=(20, 50),
    figsize=(14, 6)
)


# In[99]:


# Filter last 50 days
df_recent = df.tail(50)

mpf.plot(
    df_recent,
    type='candle',
    volume=True,
    style='yahoo',
    title='Goldman Sachs - Last 50 Days',
    mav=(20, 50),
    figsize=(14, 6)
)


# In[101]:


# Filter last 10 days
df_recent = df.tail(10)

mpf.plot(
    df_recent,
    type='candle',
    volume=True,
    style='yahoo',
    title='Goldman Sachs - Last 10 Days',
    mav=(20, 50),
    figsize=(14, 6)
)


# In[107]:


corr_df = df[['Daily Return', 'Volume']].dropna()
correlation = corr_df['Daily Return'].corr(corr_df['Volume'])
print(f"Correlation between Daily Return and Volume: {correlation:.4f}")


# In[109]:


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.scatter(corr_df['Volume'], corr_df['Daily Return'], alpha=0.4, color='teal')
plt.title('Volume vs Daily Return')
plt.xlabel('Volume')
plt.ylabel('Daily Return')
plt.grid(True)
plt.show() 


# # Above scatter plot is looking like mostly no relation , because we can not identify the clear and spacific pattern here

# In[111]:


correlation_matrix = df.corr(numeric_only=True) # creating the co-relation matrix
print(correlation_matrix)


# In[117]:


import seaborn as sns # Checking the coorelation here
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title('Correlation Matrix of Goldman Sachs Stock Data')
plt.show()


# # Technical indicators like RSI, MACD, and Bollinger Bands are powerful tools for identifying market trends, momentum, and overbought/oversold conditions.
# # To calculate these indicators easily, we can use the Python library ta (Technical Analysis Library in Python).

# In[123]:


pip install ta


# In[125]:


# Import and apply indecator

from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# Drop NaN values
df = df.dropna()

# RSI
rsi = RSIIndicator(close=df['Close'], window=14)
df['RSI'] = rsi.rsi()

# MACD
macd = MACD(close=df['Close'])
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()

# Bollinger Bands
bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
df['BB_Upper'] = bb.bollinger_hband()
df['BB_Lower'] = bb.bollinger_lband()
df['BB_Middle'] = bb.bollinger_mavg()



# In[127]:


# Visulize each indecator

plt.figure(figsize=(10, 4))
plt.plot(df['RSI'], label='RSI', color='blue')
plt.axhline(70, color='red', linestyle='--', label='Overbought')
plt.axhline(30, color='green', linestyle='--', label='Oversold')
plt.title('Relative Strength Index (RSI)')
plt.legend()
plt.grid(True)
plt.show()


# In[129]:


# MACD Plot

plt.figure(figsize=(10, 4))
plt.plot(df['MACD'], label='MACD', color='purple')
plt.plot(df['MACD_Signal'], label='Signal Line', color='orange')
plt.title('MACD & Signal Line')
plt.legend()
plt.grid(True)
plt.show()


# In[131]:


# Bollinger Bands with Price

plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price', color='black')
plt.plot(df['BB_Upper'], label='Upper Band', color='red', linestyle='--')
plt.plot(df['BB_Lower'], label='Lower Band', color='green', linestyle='--')
plt.plot(df['BB_Middle'], label='Middle Band (20 MA)', color='blue')
plt.fill_between(df.index, df['BB_Lower'], df['BB_Upper'], color='lightgray', alpha=0.3)
plt.title('Bollinger Bands')
plt.legend()
plt.grid(True)
plt.show()


# In[133]:


# Last 100 days Bollinger bands ploting

df_bb = df.tail(100)

plt.figure(figsize=(14, 6))
plt.plot(df_bb['Close'], label='Close Price', color='black')
plt.plot(df_bb['BB_Upper'], label='Upper Band', color='red', linestyle='--')
plt.plot(df_bb['BB_Lower'], label='Lower Band', color='green', linestyle='--')
plt.plot(df_bb['BB_Middle'], label='Middle Band (20 MA)', color='blue')
plt.fill_between(df_bb.index, df_bb['BB_Lower'], df_bb['BB_Upper'], color='lightgray', alpha=0.3)

plt.title('Bollinger Bands (Last 100 Days)')
plt.legend()
plt.grid(True)
plt.show()


# In[ ]:




