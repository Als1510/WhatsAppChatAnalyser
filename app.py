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
      
  user_list =  df['User'].unique().tolist()
  user_list.remove('group_notification')
  user_list.sort()
  user_list.insert(0, 'Overall')
  selected_user = st.sidebar.selectbox("Show analysis w.r.t.", user_list)

  if st.sidebar.button("Show Analysis"):
    # Top Statistics
    st.header('Top Statistics')
    num_messages, words, num_media_messages = helper.fetch_stats(selected_user, df)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.markdown('<h2 style="color:Blue; text-align:center; padding-bottom: 0;">'+str(num_messages)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h4 style="color:Blue; text-align:center;">Message</h4>',unsafe_allow_html=True)
    with col2:
      st.markdown('<h2 style="color:Blue; text-align:center; padding-bottom: 0">'+str(len(user_list)-1)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h4 style="color:Blue; text-align:center;">Users</h4>',unsafe_allow_html=True)
    with col3:
      st.markdown('<h2 style="color:Blue; text-align:center; padding-bottom: 0">'+str(words)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h4 style="color:Blue; text-align:center;">Words</h4>',unsafe_allow_html=True)
    with col4:
      st.markdown('<h2 style="color:Blue; text-align:center; padding-bottom: 0">'+str(num_media_messages)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h4 style="color:Blue; text-align:center;">Media</h4>',unsafe_allow_html=True)

    # Chatting From
    year, avg_msg, username = helper.chat_from(selected_user, df)
    st.markdown('<h3 style="text-align:center; margin-top: 0.5rem">'+ username + ' have been chatting since ' + '<span style="color: #7dc580">' + str(year) + '</span>' + ' with an average of ' + '<span style="color: #7dc580">' + str(avg_msg) + '</span> message per day!</h3>',unsafe_allow_html=True)

    # Most talkative
    img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("msg_icon.png"))
    img = '<img src="' + img_src + '" style="height: 30px" margin: 0;>'
    st.markdown('<div style="text-align:center; margin: 1.5rem 0 0.3rem 0; display: flex; flex-direction: row; align-items:center; justify-content:center;">' + img + '<h2 style=" padding: 0;"> Most Talkative </h2>' + img + '</div>', unsafe_allow_html=True)
    
    username, avg_msg = helper.most_talkative(df)
    st.markdown('<h4 style="text-align:center; padding: 0.4rem 0;">' + username + '</h4>', unsafe_allow_html=True)
    st.markdown('<h5 style="text-align:center;">' + str(avg_msg) + '% of the total messages</h5>', unsafe_allow_html=True)

    # Messages sent by
    st.header('Message Sent')

    # By Hour
    st.subheader('By Hour')
    new_df = helper.hourly_timeline(selected_user, df, selected_format)
    plost.area_chart(
      new_df,
      x = 'Hour',
      y = 'Message',
      pan_zoom='zoom',
    )

    # By Day
    st.subheader('By Day')
    new_df = helper.daily_timeline(selected_user, df)
    plost.area_chart(
      new_df,
      x = 'Date',
      y = 'Message',
      pan_zoom='zoom'
    )

    # By Week
    st.subheader('By Week')
    new_df = helper.weekly_timeline(selected_user, df)
    plost.line_chart(
      new_df,
      x = 'Days',
      y = 'Message',
      pan_zoom='zoom'
    )

    # By Month
    st.subheader('By Month')
    new_df = helper.monthly_timeline(selected_user, df)
    plost.line_chart(
      new_df,
      x = 'Month',
      y = 'Message',
      pan_zoom='zoom',
    )
    

    # Most common words
    st.header('Most common words')
    new_df = helper.most_common_words(selected_user, df)
    plost.bar_chart(
      new_df,
      bar = 'Message',
      value = 'Count',
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