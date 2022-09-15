from collections import Counter
import streamlit as st
import pandas as pd
import base64
from pathlib import Path

def showError(message):
  st.error(message)
  st.stop()

def img_to_bytes(img_path):
  img_bytes = Path(img_path).read_bytes()
  encoded = base64.b64encode(img_bytes).decode()
  return encoded

def chat_from(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  else:
    selected_user = 'You'
  unique_years = df['Year'].unique()
  start_year = unique_years[0]
  msg_count = df.groupby(['Date']).count()['Message']
  avg_msg = round(msg_count.mean(),2)
  return start_year, avg_msg, selected_user

def most_talkative(df):
  df = df[df['User'] != 'group_notification']
  user = df['User'].value_counts()
  username = user.index[0]
  avg_msg = round(len(df)/user[username], 2)
  return username, avg_msg
  
def fetch_stats(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  num_messages = df.shape[0]
  words = []
  for message in df['Message']:
    words.extend(message.split())

  num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]
  return num_messages, len(words), num_media_messages

def hourly_timeline(selected_user, df, format):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  
  new_df['Message'] = [1] * new_df.shape[0]
  if format == '12 Hour':
    new_df['Hour'] = new_df['Hour'].astype(str) + ' ' + new_df['Meridian'].astype(str)
    new_df = new_df.groupby('Hour').sum().reset_index()
  else:
    new_df = new_df.groupby('Hour').sum().reset_index()
  return new_df

def daily_timeline(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  
  new_df['Message'] = [1] * new_df.shape[0]
  new_df = new_df.groupby('Date').sum().reset_index()
  return new_df

def weekly_timeline(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  
  new_df['Message'] = [1] * new_df.shape[0]
  days = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  new_df = new_df.groupby('DayName').sum().reindex(days)
  new_df['Days'] = ['1 - Monday', '2 - Tuesday', '3 - Wednesday', '4 - Thursday', '5 - Friday', '6 - Saturday', '8 - Sunday']
  return new_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
      df = df[df['User'] == selected_user]
    new_df = df[df['User'] != 'group_notification']
    new_df  = df.groupby(['Year','Month','MonthNum']).count()
    new_df.reset_index(inplace=True)
    time = []
    for i in range(new_df.shape[0]):
        time.append(str(new_df['MonthNum'][i]) + " - " + str(new_df['Year'][i]) + " - " + new_df['Month'][i])
    new_df['Month'] = time
    return new_df

def most_common_words(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  new_df = new_df[new_df['Message'] != '<Media omitted>\n']
  new_df = new_df[new_df['Message'] != 'This message was deleted\n']

  f = open('stop_hinglish.txt')
  stop_words = f.read()

  words = []

  for message in new_df['Message']:
    for word in message.lower().split():
      if word not in stop_words:
        words.append(word)
  
  most_common_df = pd.DataFrame(Counter(words).most_common(50), columns=['Message', 'Count'])
  most_common_df.sort_values('Count')
  return most_common_df