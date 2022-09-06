import re
import pandas as pd
import streamlit as st

def seperate_date_time(x):
  date = pd.to_datetime(x.split(', ')[0], format="%m/%d/%y")
  time = x.split(', ')[1].split(' - ')[0]
  return date, time

def preprocess(data, format):
  pattern = {
    '12 Hour':'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
    '24 Hour':'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
  }

  user_message = re.split(pattern[format], data)[1:]
  date_time = re.findall(pattern[format], data)

  if (len(user_message) and len(date_time)) == 0:
    return pd.DataFrame(), True

  df = pd.DataFrame({'user_message': user_message, 'date_time': date_time})
  df[['date','time']] = df['date_time'].apply(lambda x: seperate_date_time(x)).to_list()
  
  users = []
  messages = []
  for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]:
      users.append(entry[1])
      messages.append(entry[2])
    else:
      users.append('group_notification')
      messages.append(entry[0])

  df['user'] = users
  df['message'] = messages
  df['year'] = df['date'].dt.year
  df['month'] = df['date'].dt.month_name()
  df['month_num'] = df['date'].dt.month
  df['day'] = df['date'].dt.day
  df['day_name'] = df['date'].dt.day_name()
  df['date'] = df['date'].dt.date
  df['hour'] = df['time'].apply(lambda x: x.split(':')[0])
  df['minute'] = df['time'].apply(lambda x: (x.split(':')[1]).split(' ')[0])
  if format == '12 Hour':
    df['meridian'] = df['time'].apply(lambda x: (x.split(':')[1]).split(' ')[1])
    
  df.drop(columns=['user_message', 'date_time'], inplace=True)
  return df, False
