import streamlit as st
import yfinance as yf
import pandas as pd

# 獲取股票數據的函數
def get_stock_data(ticker, show_average_cost, show_720ma, show_360ma, show_180ma, show_30ma):
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
    
    stock_data = stock_data[columns_to_plot]
    
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
    
    # 用Chart.js 繪製圖表
    chart_data = stock_data.reset_index().to_json(orient='records')
    st.markdown(f'''
        <canvas id="myChart"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            var ctx = document.getElementById('myChart').getContext('2d');
            var chartData = {chart_data};
            
            var labels = chartData.map(function(e) {{
                return e.Date;
            }});
            var datasets = [];
            
            datasets.push({{
                label: 'Close',
                data: chartData.map(function(e) {{
                    return e.Close;
                }}),
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }});
            
            {"datasets.push({label: 'Average Cost', data: chartData.map(function(e) { return e.Average_Cost; }), borderColor: 'rgba(153, 102, 255, 1)', borderWidth: 1, fill: false});" if show_average_cost else ""}
            {"datasets.push({label: '720 MA', data: chartData.map(function(e) { return e['720_MA']; }), borderColor: 'rgba(255, 159, 64, 1)', borderWidth: 1, fill: false});" if show_720ma else ""}
            {"datasets.push({label: '240 MA', data: chartData.map(function(e) { return e['240_MA']; }), borderColor: 'rgba(255, 205, 86, 1)', borderWidth: 1, fill: false});" if show_360ma else ""}
            {"datasets.push({label: '120 MA', data: chartData.map(function(e) { return e['120_MA']; }), borderColor: 'rgba(201, 203, 207, 1)', borderWidth: 1, fill: false});" if show_180ma else ""}
            {"datasets.push({label: '20 MA', data: chartData.map(function(e) { return e['20_MA']; }), borderColor: 'rgba(54, 162, 235, 1)', borderWidth: 1, fill: false});" if show_30ma else ""}
            
            var myChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: datasets
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        x: {{
                            beginAtZero: true
                        }},
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        </script>
    ''')
                            x: {{
                                &#8203;:citation[oaicite:0]{index=0}&#8203;
    ''')
