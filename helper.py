from collections import Counter
import streamlit as st
import pandas as pd

def showError(message):
  st.error(message)
  st.stop()

def countAndGroupMessage(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]
  new_df = df[df['user'] != 'group_notification']
  
  new_df['message_count'] = [1] * new_df.shape[0]
  new_df = new_df.groupby('date').sum().reset_index()
  return new_df

def most_common_words(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]
  new_df = df[df['user'] != 'group_notification']
  new_df = new_df[new_df['message'] != '<Media omitted>\n']

  f = open('stop_hinglish.txt')
  stop_words = f.read()

  words = []

  for message in new_df['message']:
    for word in message.lower().split():
      if word not in stop_words:
        words.append(word)
  
  most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['message', 'count'])
  return most_common_df