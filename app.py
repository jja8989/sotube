import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from PIL import Image

icon = Image.open("./sotube.png")
st.set_page_config(
     page_title="SoTube",
     page_icon=icon
 )

st.image("./sotube.png", width = 200)

st.title("Welcome to SoTube!")

@st.cache_data
def load_data():
    with open("./test.pickle", "rb") as f:
        df = pickle.load(f)
    return df

df = load_data()

st.subheader("Search the youtuber name")


channel_name = st.selectbox("", df['data.channel.title'].unique())

if channel_name:
    st.markdown("---")

    filtered_df = df[df['data.channel.title']==channel_name].reset_index(drop=True)
    

    try:
        st.image(filtered_df['data.channel.banner'][0], use_column_width=True)
    except:
        pass

    try:
        st.image(filtered_df['data.channel.thumbnails'][0], width=200)
    except:
        pass
    
    try:
        st.write(filtered_df['data.channel.description'][0])
    except:
        pass
    
    trend_sub_df = pd.json_normalize(filtered_df['data.channel.stat'][0])

    st.markdown("---")
    st.subheader("Subscriber Number Trend")
    fig = px.line(trend_sub_df, x='searchDate', y='subscriberCount')
    fig.update_layout(xaxis_title='', yaxis_title='구독자 수')
    st.plotly_chart(fig)

    view_count = trend_sub_df[trend_sub_df['dailyViewCount']>0]
    st.markdown("---")
    st.subheader("Daily View Count Trend")
    fig = px.line(view_count, x='searchDate', y='dailyViewCount')
    fig.update_layout(xaxis_title='', yaxis_title='일일 조회수')
    st.plotly_chart(fig)

    
