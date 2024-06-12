import streamlit as st
import xml.etree.ElementTree as et
import pandas as pd
import io

st.title('QUEシート作成補助アプリ')
st.caption("動画の編集データを分析し、CUEシートに貼り付けることのできる形式に変換します。")


uploaded_file = st.file_uploader("編集データを選択してください")

data_list = []

if uploaded_file is not None:
	st.info('分析を開始します')
	tree = et.parse(uploaded_file).getroot()

    
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
	st.data_editor(df)
	st.success("分析が完了しました！")


	output = io.BytesIO()
	with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
		df.to_excel(writer, index=False, sheet_name='Updated Data')

	# ダウンロードするファイル名の設定
	st.download_button(
		label="データをダウンロード",
		data=output.getvalue(),
		file_name="QUEシート貼り付け用データ.xlsx",
		mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	)