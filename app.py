import streamlit as st
import xml.etree.ElementTree as et

st.title('QUE sheet maker')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
	st.info('file uploaded!')