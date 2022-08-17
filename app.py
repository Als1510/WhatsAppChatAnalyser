import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader('Choose a file')

st.sidebar.radio("Time Format of Chat", ('12 Hour', '24 Hour'))

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 