import streamlit as st

def showError(message):
  st.error(message)
  st.stop()