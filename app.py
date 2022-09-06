import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

st.set_page_config(page_title='WhatsApp Chat Analyser', layout = 'centered', page_icon = 'logo.png', initial_sidebar_state = 'expanded')

st.sidebar.title('WhatsApp Chat Analyser')

uploaded_file = st.sidebar.file_uploader('Choose a file')
selected = st.sidebar.radio("Time Format of Chat", ('12 Hour', '24 Hour'))

if uploaded_file is not None:
  bytes_data = uploaded_file.getvalue()
  data = bytes_data.decode('utf-8')
  df, Error = preprocessor.preprocess(data, selected)
  if(Error):
    helper.showError('Please select the correct time format of your file')
  user_list =  df['user'].unique().tolist()
  user_list.remove('group_notification')
  user_list.sort()
  user_list.insert(0, 'Overall')
  selected_user = st.sidebar.selectbox("Show analysis w.r.t.", user_list)
  
  st.dataframe(df)
  st.balloons()


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)