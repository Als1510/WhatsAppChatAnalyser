import streamlit as st
import preprocessor, helper
import plost

st.set_page_config(page_title='WhatsApp Chat Analyser', layout = 'centered', page_icon = 'logo.png', initial_sidebar_state = 'expanded')

st.sidebar.title('WhatsApp Chat Analyser')

uploaded_file = st.sidebar.file_uploader('Choose a file')
selected_format = st.sidebar.radio("Time Format of Chat", ('12 Hour', '24 Hour'))

if uploaded_file is not None:
  bytes_data = uploaded_file.getvalue()
  data = bytes_data.decode('utf-8')
  df, Error = preprocessor.preprocess(data, selected_format)
  if(Error):
    if selected_format == '12 Hour':
      helper.showError('Please select the correct time format of your file. It may be 24 Hour format.')
    else:
      helper.showError('Please select the correct time format of your file. It may be 12 Hour format.')
      
  user_list =  df['user'].unique().tolist()
  user_list.remove('group_notification')
  user_list.sort()
  user_list.insert(0, 'Overall')
  selected_user = st.sidebar.selectbox("Show analysis w.r.t.", user_list)

  if st.sidebar.button("Show Analysis"):

    st.dataframe(df)

    # Messages sent per day
    st.header('Message sent per day over time period')
    new_df = helper.countAndGroupMessage(selected_user, df)
    plost.line_chart(
      new_df,
      x = 'date',
      y = 'message_count',
      pan_zoom='zoom'
    )

    # Most common words
    st.header('Most common words')
    new_df = helper.most_common_words(selected_user, df)
    plost.bar_chart(
      new_df,
      bar = 'message',
      value = 'count',
      direction = 'horizontal'
    )

    st.balloons()


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)