import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 繪製圖表的函數
def plot_stock_with_average_cost(ticker, show_average_cost, show_720ma, show_360ma, show_180ma, show_30ma):
    stock_data = yf.download(ticker, period="max")
    stock_data = stock_data.sort_index()
    
    if show_average_cost:
        stock_data['Cumulative_Cost'] = stock_data['Close'].cumsum()
        stock_data['Cumulative_Shares'] = range(1, len(stock_data) + 1)
        stock_data['Average_Cost'] = stock_data['Cumulative_Cost'] / stock_data['Cumulative_Shares']
    
    if show_720ma:
        stock_data['720_MA'] = stock_data['Close'].rolling(window=720).mean()
    
    if show_360ma:
        stock_data['240_MA'] = stock_data['Close'].rolling(window=240).mean()
    
    if show_180ma:
        stock_data['120_MA'] = stock_data['Close'].rolling(window=120).mean()
    
    if show_30ma:
        stock_data['20_MA'] = stock_data['Close'].rolling(window=20).mean()

    columns_to_plot = ['Close']
    if show_average_cost:
        columns_to_plot.append('Average_Cost')
    if show_720ma:
        columns_to_plot.append('720_MA')
    if show_360ma:
        columns_to_plot.append('240_MA')
    if show_180ma:
        columns_to_plot.append('120_MA')
    if show_30ma:
        columns_to_plot.append('20_MA')

    st.write('每日均價')
    st.write(stock_data['Average_Cost'][-1])    
    st.write('最新收盤')
    st.write(stock_data['Close'][-1])
    if show_30ma:
        st.write('月均價')
        st.write(stock_data['20_MA'][-1])
    if show_180ma:
        st.write('半年均價')
        st.write(stock_data['120_MA'][-1])      
    if show_360ma:
        st.write('年均價')
        st.write(stock_data['240_MA'][-1])       
    if show_720ma:
        st.write('3年均價')
        st.write(stock_data['720_MA'][-1])
                
    st.line_chart(stock_data[columns_to_plot])
   

# 輸入股票代號
ticker = st.text_input("輸入股票代號 (例如: 'VWRA.L')", value="VWRA.L")

# 添加checkbox
show_average_cost = st.checkbox('顯示平均成本', value=True)
show_30ma = st.checkbox('顯示20日移動平均線', value=False)
show_180ma = st.checkbox('顯示120日移動平均線', value=False)
show_360ma = st.checkbox('顯示240日移動平均線', value=False)
show_720ma = st.checkbox('顯示720日移動平均線', value=True)




if st.button("顯示圖表"):
    plot_stock_with_average_cost(ticker, show_average_cost, show_720ma, show_360ma, show_180ma, show_30ma)
