import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# 獲取股票數據的函數
def get_stock_data(ticker, show_average_cost, show_720ma, show_360ma, show_180ma, show_30ma):
    stock_data = yf.download(ticker, period="max", progress=False)
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

    return stock_data

# 輸入股票代號
ticker = st.text_input("輸入股票代號 (例如: 'VWRA.L')", value="VWRA.L")

# 添加checkbox
show_average_cost = st.checkbox('顯示平均成本', value=True)
show_30ma = st.checkbox('顯示20日移動平均線', value=False)
show_180ma = st.checkbox('顯示120日移動平均線', value=False)
show_360ma = st.checkbox('顯示240日移動平均線', value=False)
show_720ma = st.checkbox('顯示720日移動平均線', value=True)

if st.button("顯示圖表"):
    stock_data = get_stock_data(ticker, show_average_cost, show_720ma, show_360ma, show_180ma, show_30ma)
    columns_to_plot = ['Date', 'Close']
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
    
    stock_data = stock_data.reset_index()[columns_to_plot]

    st.write('每日均價:', stock_data['Average_Cost'].iloc[-1] if show_average_cost else 'N/A')
    st.write('最新收盤:', stock_data['Close'].iloc[-1])
    if show_30ma:
        st.write('月均價:', stock_data['20_MA'].iloc[-1])
    if show_180ma:
        st.write('半年均價:', stock_data['120_MA'].iloc[-1])
    if show_360ma:
        st.write('年均價:', stock_data['240_MA'].iloc[-1])
    if show_720ma:
        st.write('3年均價:', stock_data['720_MA'].iloc[-1])
    
    # 用Altair繪製圖表
    base = alt.Chart(stock_data).encode(x='Date:T')
    
    lines = base.mark_line().encode(
        y=alt.Y('Close', title='收盤價'),
        color=alt.value('blue')
    )
    
    if show_average_cost:
        average_cost_line = base.mark_line().encode(
            y='Average_Cost',
            color=alt.value('orange')
        )
        lines += average_cost_line
    
    if show_720ma:
        ma720_line = base.mark_line().encode(
            y='720_MA',
            color=alt.value('green')
        )
        lines += ma720_line
    
    if show_360ma:
        ma360_line = base.mark_line().encode(
            y='240_MA',
            color=alt.value('red')
        )
        lines += ma360_line
    
    if show_180ma:
        ma180_line = base.mark_line().encode(
            y='120_MA',
            color=alt.value('purple')
        )
        lines += ma180_line
    
    if show_30ma:
        ma30_line = base.mark_line().encode(
            y='20_MA',
            color=alt.value('brown')
        )
        lines += ma30_line

    st.altair_chart(lines, use_container_width=True)
