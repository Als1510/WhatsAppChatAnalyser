from collections import Counter
import streamlit as st
import pandas as pd

def showError(message):
  st.error(message)
  st.stop()

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