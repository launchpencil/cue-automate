import streamlit as st
import xml.etree.ElementTree as et
import pandas as pd
import io

st.title('QUE sheet maker')

uploaded_file = st.file_uploader("Choose a file")

data_list = []
data_list2 = []

if uploaded_file is not None:
	st.info('file uploaded!')
	tree = et.parse(uploaded_file).getroot()

	tree[1][0][0][0][0]

    
	for child in tree[1][0][0][0][0]:
		time = child.attrib["offset"]
		if time != "0s":
			parts = child.attrib["offset"].split('/')
			result = int(parts[0]) // int(parts[1][:-1])
			time = result
		else:
			time = 0

		try:
			status = child.attrib["name"]
		except:
			status = 'unknown'
		data_list.append({"分": time//60, "秒": time%60, "トラック名": status})

df = pd.DataFrame(data_list)
df


output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Updated Data')

# ダウンロードするファイル名の設定
download_file_name = "QUEシート貼り付け用データ.xlsx"
st.download_button(
    label="データをダウンロード",
    data=output.getvalue(),
    file_name=download_file_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)