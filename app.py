import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from pathlib import Path
import plost

st.set_page_config(page_title='WhatsApp Chat Analyser', layout = 'centered', page_icon = 'logo.png', initial_sidebar_state = 'expanded')

helper.local_css("style.css")

st.sidebar.title('WhatsApp Chat Analyser')

uploaded_file = st.sidebar.file_uploader('Choose a file')
selected_format = st.sidebar.radio("Time Format of Chat", ('12 Hour', '24 Hour'))

if uploaded_file is None:
  st.subheader('In order to use our analyzer you need to export your WhatsApp chat to a text file')
  st.write('1. Open the individual or group chat.')
  st.write('2. Tap More options ( : ) > More > Export chat.')
  st.write('3. Choose to export without media.')
  st.write("Check out the [link](https://faq.whatsapp.com/196737011380816/?locale=en_US) for more details")

if uploaded_file is not None:
  # Check File Type
  if Path(uploaded_file.name).suffix != '.txt':
    helper.showError('Please upload a .txt file')

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

    # Chatting From
    year, avg_msg, username = helper.chat_from(selected_user, df)
    st.markdown('<h3 class="center mb-2">'+ username + ' have been chatting since ' + '<span class="primary-color">' + str(year) + '</span>' + ' with an average of ' + '<span class="primary-color">' + str(avg_msg) + '</span> message per day!</h3>',unsafe_allow_html=True)
    
    # Top Statistics
    st.header('Top Statistics')
    num_messages, words, num_media_messages, diff_days = helper.fetch_stats(selected_user, df)
    col1, col2, col3 = st.columns(3)
    with col1:
      st.markdown('<h2 class="primary-color center pb-0">'+str(num_messages)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h3 class="center mb-5">Messages</h3>',unsafe_allow_html=True)
    with col2:
      st.markdown('<h2 class="primary-color center pb-0">'+str(words)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h3 class="center mb-5">Words</h3>',unsafe_allow_html=True)
    with col3:
      st.markdown('<h2 class="primary-color center pb-0">'+str(num_media_messages)+'</h2>',unsafe_allow_html=True)
      st.markdown('<h3 class="center mb-5">Media</h3>',unsafe_allow_html=True)

    # Group Specific
    col1, col2, col3 = st.columns(3)

    removed_left = helper.removed_left(df)
    if selected_user == 'Overall':
      with col1:
        st.markdown('<h2 class="primary-color center pb-0">'+str(len(user_list)-1)+'</h2>',unsafe_allow_html=True)
        st.markdown('<h3 class="center mb-2">Users</h3>',unsafe_allow_html=True)
      with col2:
        st.markdown('<h2 class="primary-color center pb-0">'+str(diff_days)+'</h2>',unsafe_allow_html=True)
        st.markdown('<h3 class="center mb-2">Days</h3>',unsafe_allow_html=True)
      with col3:
        st.markdown('<h2 class="primary-color center pb-0">'+str(removed_left)+'</h2>',unsafe_allow_html=True)
        st.markdown('<h3 class="center mb-2">Removed/Left</h3>',unsafe_allow_html=True)
    
      # Most talkative
      img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("msg_icon.png"))
      img = '<img src="' + img_src + '" style="height: 50px" margin: 0;>'
      username, avg_msg = helper.most_talkative(df)
      st.markdown('<div class="flex flex-col p-1"><div class="flex flex-row">'+img+'<h2 class="p-0 m-0 center"> Most Talkative </h2>'+img+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center">'+ str(avg_msg) +' % of the total messages</h5></div>',unsafe_allow_html=True)

      col1, col2 = st.columns(2)
      with col1:
      # Influencer
        img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("influencer_icon.jpg"))
        img = '<img src="' + img_src + '" style="height: 50px" margin: 0;>'
        st.markdown('<div class="flex flex-col p-1 pr-2"><div class="flex flex-row">'+img+'<h2 class="p-0 m-0 center"> Influencer </h2>'+img+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center"> Media shared (7 photos, videos or voice) 41% </h5></div>',unsafe_allow_html=True)

      # Long Winded
        img_src_left = "data:image/png;base64,{}".format(helper.img_to_bytes("long_letter_icon_left.png"))
        img_src_right = "data:image/png;base64,{}".format(helper.img_to_bytes("long_letter_icon_right.png"))
        img_left = '<img src="' + img_src_left + '" style="height: 50px" margin: 0;>'
        img_right = '<img src="' + img_src_right + '" style="height: 50px" margin: 0;>'
        st.markdown('<div class="flex flex-col p-1 pr-2"><div class="flex flex-row">'+img_left+'<h2 class="p-0 m-0 center"> Long Winded </h2>'+img_right+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center">'+ str(avg_msg) +' of there messages are longer than the others</h5></div>',unsafe_allow_html=True)

        # Early Bird
        img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("early_bird_icon.png"))
        img = '<img src="' + img_src + '" style="height: 50px" margin: 0;>'
        st.markdown('<div class="flex flex-col p-1 pr-2"><div class="flex flex-row">'+img+'<h2 class="p-0 m-0 center"> Early Bird </h2>'+img+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center"> Most of the message are sent in the interval 8 AM - 12 AM '+ str(avg_msg) +'</h5></div>',unsafe_allow_html=True)

      with col2:
        # Professor
        img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("book_icon.jpg"))
        img = '<img src="' + img_src + '" style="height: 50px" margin: 0;>'
        st.markdown('<div class="flex flex-col p-1 pl-2"><div class="flex flex-row">'+img+'<h2 class="p-0 m-0 center"> Professor </h2>'+img+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center"> Used the greatest amount of unique words '+ str(avg_msg) +'</h5></div>',unsafe_allow_html=True)

        # Emoji Lover
        img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("emoji_icon.png"))
        img = '<img src="' + img_src + '" style="height: 50px" margin: 0;>'
        st.markdown('<div class="flex flex-col p-1 pl-2"><div class="flex flex-row">'+img+'<h2 class="p-0 m-0 center"> Emoji Lover </h2>'+img+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center">'+ str(avg_msg) +' of there words are emoticons</h5></div>',unsafe_allow_html=True)
        
        # Night owl      
        img_src = "data:image/png;base64,{}".format(helper.img_to_bytes("night_owl_icon.jpg"))
        img = '<img src="' + img_src + '" style="height: 50px" margin: 0;>'
        st.markdown('<div class="flex flex-col p-1 pl-2"><div class="flex flex-row">'+img+'<h2 class="p-0 m-0 center"> Night Owl </h2>'+img+'</div><h4 class="pt-5 pb-5 center">'+ username +'</h4><h5 class="mb-1 center"> Most of the message are sent in the interval 12 PM - 6 AM '+ str(avg_msg) +'</h5></div>',unsafe_allow_html=True)
      
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
    plost.area_chart(
      new_df,
      x = 'Week',
      y = 'Message',
      pan_zoom='zoom',
    )

    # By Month
    st.subheader('By Month')
    new_df = helper.monthly_timeline(selected_user, df)
    plost.area_chart(
      new_df,
      x = 'Months',
      y = 'Message',
      pan_zoom='zoom',
    )
    
    # Most Busy
    st.header("Most Busy")
    
    # Day of week
    st.subheader('Day')
    new_df = helper.most_busy_day(selected_user, df)
    plost.bar_chart(
      new_df,
      bar = 'Days',
      value = 'Message',
      color='#ff9800',
      use_container_width=True
    )

    # Month of year
    st.subheader('Month')
    new_df = helper.most_busy_month(selected_user, df)
    plost.bar_chart(
      new_df,
      bar = 'Months',
      value = 'Message',
      color='#ff9800',
      use_container_width=True
    )
      

    # By author
    st.subheader('By Author')
    new_df = helper.user_chat_percentage(df)
    plost.donut_chart(
      data=new_df,
      theta='Percentage',
      color='User'
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

    # Create word cloud
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    st.balloons()