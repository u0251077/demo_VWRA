import streamlit as st
import yfinance as yf
import pandas as pd

# 函數來計算和顯示結果
def calculate_average_cost(current_shares, current_avg_price, new_price, target_avg_price):
    current_total_cost = current_shares * current_avg_price

    additional_shares = 0
    new_avg_price = current_avg_price

    while new_avg_price <= target_avg_price:
        additional_shares += 1
        total_cost = current_total_cost + (additional_shares * new_price)
        new_avg_price = total_cost / (current_shares + additional_shares)

    return additional_shares - 1, new_avg_price

# Streamlit界面
st.title("平均成本計算器")
st.write("計算從上市開始到今天，每天都買進的平均成本，以及當前條件下買入更多股票以控制平均成本的最大股數。")

# 輸入欄位
current_shares = st.number_input("現有股數", value=10)
current_avg_price = st.number_input("現有均價", value=100)
new_price = st.number_input("當前每股價格", value=130.0)
target_avg_price = st.number_input("目標均價", value=108)

if st.button("計算"):
    max_additional_shares, new_avg_price = calculate_average_cost(current_shares, current_avg_price, new_price, target_avg_price)
    st.write(f"在目前條件下，最多可以再買入 {max_additional_shares} 股，新的平均成本為 {new_avg_price:.3f}")

# 繪製圖表的函數
def plot_stock_with_average_cost(ticker):
    stock_data = yf.download(ticker, period="max")
    stock_data = stock_data.sort_index()
    stock_data['Cumulative_Cost'] = stock_data['Close'].cumsum()
    stock_data['Cumulative_Shares'] = range(1, len(stock_data) + 1)
    stock_data['Average_Cost'] = stock_data['Cumulative_Cost'] / stock_data['Cumulative_Shares']
    stock_data['720_MA'] = stock_data['Close'].rolling(window=720).mean()
    stock_data['360_MA'] = stock_data['Close'].rolling(window=360).mean()
    
    st.line_chart(stock_data[['Close', 'Average_Cost', '720_MA','360_MA']])


# 輸入股票代號
ticker = st.text_input("輸入股票代號 (例如: 'VWRA.L')", value="VWRA.L")

if st.button("顯示圖表"):
    plot_stock_with_average_cost(ticker)
