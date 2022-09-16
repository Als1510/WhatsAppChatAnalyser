from collections import Counter
import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import base64
from pathlib import Path

def local_css(file_name):
  with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def showError(message):
  st.error(message)
  st.stop()

def img_to_bytes(img_path):
  img_bytes = Path(img_path).read_bytes()
  encoded = base64.b64encode(img_bytes).decode()
  return encoded

def fetch_stats(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  num_messages = df.shape[0]
  diff_days = (df.Date.iloc[len(df)-1] - df.Date.iloc[0]).days
  words = []
  for message in df['Message']:
    words.extend(message.split())

  num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]
  return num_messages, len(words), num_media_messages, diff_days

# Have to work on it
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
  avg_msg = round(user[username]/len(df)*100, 2)
  return username, avg_msg

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
  new_df = new_df.groupby('Date')['Message'].count().reset_index()
  return new_df

def weekly_timeline(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  new_df  = df.groupby(['Year','Month','WeekNum'], sort=False)['Message'].count().reset_index()
  week = []
  for i in range(len(new_df)):
    week.append(str(new_df['WeekNum'][i]) + " - " + new_df['Month'][i] + " - " + str(new_df['Year'][i]))
  new_df['Week'] = week
  new_df['Week'] = new_df[['WeekNum', 'Week']].apply(lambda x: "Week 0"+x['Week'] if x['WeekNum']<10 else "Week "+x['Week'], axis=1)
  new_df.sort_values(['WeekNum', 'Month', 'Year'], inplace=True)
  return new_df

def monthly_timeline(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  new_df  = df.groupby(['Year','Month','MonthNum'], sort=False)['Message'].count().reset_index()
  month = []
  for i in range(new_df.shape[0]):
    month.append(str(new_df['MonthNum'][i]) + " - " + new_df['Month'][i] + " - " + str(new_df['Year'][i]))
  new_df['Months'] = month
  new_df['Months'] = new_df[['MonthNum', 'Months']].apply(lambda x: "Month 0"+x['Months'] if x['MonthNum']<10 else "Month "+x['Months'], axis=1)
  new_df.sort_values(['MonthNum', 'Year'], inplace=True)
  return new_df

def most_busy_day(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  
  new_df = new_df.groupby(['DayName', 'DayOfWeek'], sort=False)['Message'].count().reset_index()
  new_df.sort_values('DayOfWeek', inplace=True)
  new_df['Days'] = new_df['DayOfWeek'].astype(str) + " - " + new_df['DayName']
  return new_df

def most_busy_month(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  
  new_df = new_df.groupby(['MonthNum', 'Month'], sort=False)['Message'].count().reset_index()
  new_df.sort_values('MonthNum', inplace=True)
  new_df['Months'] = new_df['MonthNum'].astype(str) + " - " + new_df['Month']
  new_df['Months'] = new_df[['MonthNum', 'Months']].apply(lambda x: "Month 0"+x['Months'] if x['MonthNum']<10 else "Month "+x['Months'], axis=1)
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

def user_chat_percentage(df):
  df = df[df['User'] != 'group_notification']
  user = df['User'].value_counts()
  new_df = pd.DataFrame ({ 'User': user.index, 'Message': user})
  new_df['Percentage'] = new_df['Message'].apply(lambda x: round(x/len(df)*100, 2))
  new_df['User'] = new_df['Percentage'].astype(str) + "% - " + new_df['User']
  new_df.drop('Message', axis=1, inplace=True)
  new_df.reset_index(drop=True,inplace=True)
  return new_df

def create_wordcloud(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['User'] == selected_user]
  new_df = df[df['User'] != 'group_notification']
  new_df = new_df[new_df['Message'] != '<Media omitted>\n']
  
  f = open('stop_hinglish.txt')
  stop_words = f.read()

  def remove_stop_words(message):
    y = []
    for word in message.lower().split():
      if word not in stop_words:
        y.append(word)
    return " ".join(y)

  wc = WordCloud(width=400, height=400, min_font_size=10)
  new_df['Message'] = new_df['Message'].apply(remove_stop_words)
  df_wc = wc.generate(new_df['Message'].str.cat(sep=" "))
  return df_wc