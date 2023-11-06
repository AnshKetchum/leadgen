import streamlit as st
from llms.openai import llm

st.title('🦜🔗 Quickstart App')


def generate_response(input_text):
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)