import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Use the current calendar date as the default end date
current_date = datetime.datetime.today().strftime('%Y-%m-%d')

# Ask the user for up to 5 ticker symbols
#tickers = input("Enter up to 5 ticker symbols, separated by commas (e.g., AAPL, MSFT, BZ=F): ").strip().split(',')
tickers = "EURUSD=x,VND=x,THB=x,JPY=x"

# Limit to 5 tickers
tickers = [ticker.strip().upper() for ticker in tickers[:5]]

# Ask the user for the start date
#start_date_str = input("Enter the start date (YYYY-MM-DD): ")
start_date_str = "2024-01-01"
st.write("Enter the end date (YYYY-MM-DD) (leave blank for today): ")
end_date_str = current_date

# Set the end date to today if left blank
#if not end_date_str:
#    end_date_str = current_date

# Validate and parse dates
try:
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
except ValueError:
    print(f"Invalid start date format. Please use YYYY-MM-DD.")
    exit()

try:
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
except ValueError:
    print(f"Invalid end date format. Please use YYYY-MM-DD.")
    exit()

# Check if end date is greater than start date
if end_date <= start_date:
    print("End date must be greater than start date.")
    exit()

# Initialize a dictionary to store data for valid tickers
valid_tickers = {}

# Process each ticker
for ticker in tickers:
    try:
        data = yf.download(ticker, start=start_date_str, end=end_date_str, progress=False)
        if data.empty:
            print(f"No data available for the ticker '{ticker}'. Skipping.")
        else:
            valid_tickers[ticker] = data
    except Exception as e:
        print(f"An error occurred while fetching data for ticker '{ticker}': {e}")

# Check if there are valid tickers to plot
if not valid_tickers:
    print("No valid tickers were provided. Exiting.")
    exit()

# Plot the closing prices for each ticker separately
for ticker, data in valid_tickers.items():
    st.write(ticker)
    st.line_chart(data.Close)