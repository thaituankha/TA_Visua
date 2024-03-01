import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


st.header('Phần trăm các chỉ số phân tích kỹ thuật theo ngành')
st.write('Chỉ số được tính bằng cách lấy số mã cổ phiếu trong ngành đó có giá vượt qua hay thủng xuống giá trị ngưỡng tương ứng chia cho số mã cổ phiếu trong ngành đó. Âm 1 thể hiện ngưỡng dưới, 1 thể hiện ngưỡng trên. Ví dụ: RSI_am1 là tỷ lệ giữa số cổ phiếu trong ngành đó có giá dưới RSI30 chia cho số cổ phiếu trong ngành đó.')

#Vẽ biểu đồ các tỷ lệ
data_streamlit = pd.read_csv('data_ta_industry.csv')
data_streamlit['time'] = pd.to_datetime(data_streamlit['time'])

#chọn 30 ngày cuối cùng
data_streamlit['time'] = pd.to_datetime(data_streamlit['time'])
unique_dates = data_streamlit['time'].unique() 
train_size = len(unique_dates) - 30
test_dates = unique_dates[train_size:]
data_plot = data_streamlit[data_streamlit['time'].isin(test_dates)]

#plot
def plot_selected_columns(selected_columns):
    fig = make_subplots(rows=len(selected_columns), cols=1, shared_xaxes=True, subplot_titles=selected_columns)

    for i, col in enumerate(selected_columns):
        for industry, group in data_plot.groupby('industry'):
            fig.add_trace(go.Scatter(x=group['time'], y=group[col], mode='lines', name=industry), row=i+1, col=1)
            fig.update_yaxes(title_text="%", row=i+1, col=1)
    fig.update_layout(height=600, title_text="", showlegend=True)
    st.plotly_chart(fig)

selectable_columns = [col for col in data_plot.columns if col != 'time' and col != 'industry']
dropdown_widget = st.selectbox('Chọn biến', options=selectable_columns)

plot_selected_columns([dropdown_widget])


#vẽ các biểu đồ khác
data_mvsi_highlow_vnis200 = pd.read_csv('data_mvsi_highlow_vnis200.csv') 

#biểu đồ MVSI
st.header(' McClellon Volume Summation Index')
fig_MVSI = px.line(data_mvsi_highlow_vnis200, x='time', y='MVSI', title='',
              color_discrete_sequence=['blue'])
st.plotly_chart(fig_MVSI)

#biểu đồ high_low
st.header('Chêch lệch vượt đỉnh và thủng đáy')
st.write('Biểu đồ được tính toán dựa trên hiệu số giữa mã có giá vượt đỉnh 200 ngày và số mã có giá thủng đáy 200 ngày.')
fig_high_low = px.line(data_mvsi_highlow_vnis200, x='time', y='high_low', title='',
              color_discrete_sequence=['blue'])
st.plotly_chart(fig_high_low)

#biểu đồ VNI_SMA200
st.header('Chêch lệch VNINDEX và SMA200')
st.write('Biểu đồ được tính toán dựa trên hiệu số giữa VNINDEX và chỉ báo kỹ thuật SMA200.')
fig_vni_sma200 = px.line(data_mvsi_highlow_vnis200, x='time', y='VNI_Sma200', title='',
              color_discrete_sequence=['blue'])
st.plotly_chart(fig_vni_sma200)
