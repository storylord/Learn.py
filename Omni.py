import datetime
import yfinance as yf
import pandas as pd
import streamlit as st

# Set default parameters
current_date = datetime.datetime.today().strftime('%Y-%m-%d')
default_tickers = "EURUSD=X,VND=X,THB=X,JPY=X"

# User inputs for tickers and dates
tickers_input = st.text_input("Enter up to 5 ticker symbols (comma-separated):", default_tickers)
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')[:5]]

start_date_default = "2024-01-01"
start_date_str = st.text_input("Enter start date (YYYY-MM-DD):", start_date_default)

end_date_str = st.text_input("Enter end date (YYYY-MM-DD):", current_date)

# Validate and parse dates
try:
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    if end_date <= start_date:
        st.error("End date must be greater than start date.")
        st.stop()
except ValueError:
    st.error("Invalid date format. Please use YYYY-MM-DD.")
    st.stop()

# Initialize valid tickers data
valid_tickers = {}

# Fetch data for each ticker
for ticker in tickers:
    try:
        data = yf.download(ticker, start=start_date_str, end=end_date_str, progress=False)
        if data.empty:
            st.warning(f"No data available for ticker '{ticker}'. Skipping.")
        else:
            valid_tickers[ticker] = data
    except Exception as e:
        st.error(f"Error fetching data for ticker '{ticker}': {e}")

# Display each ticker's chart and calculate changes
if valid_tickers:
    st.header("Ticker Data and Visualizations")
    ticker_changes = []

    for ticker, data in valid_tickers.items():
        st.subheader(f"{ticker} - Price Chart")
        st.line_chart(data['Close'])

        # Calculate changes
        changes = {
            'Ticker': ticker,
            '7 Days Change': data['Close'].pct_change(periods=5).iloc[-1].item() * 100 if len(data) > 7 else None,
            '30 Days Change': data['Close'].pct_change(periods=22).iloc[-1].item() * 100 if len(data) > 30 else None,
            '1 Years Change': data['Close'].pct_change(periods=252).iloc[-1].item() * 100 if len(data) > 365 else None
        }
        ticker_changes.append(changes)

    # Display percentage changes in a table
    changes_df = pd.DataFrame(ticker_changes)
    st.subheader("Percentage Changes")
    st.write(changes_df)
else:
    st.error("No valid data to display. Please check your tickers and try again.")
