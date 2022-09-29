
# from distutils.command.upload import upload
# import pandas as pd
import streamlit as st
from datetime import date

import erdem_toolbox

st.set_page_config(page_title='Ad Copy Builder')
st.header('AD Copy Builder')
st.write('V1 - 9.29.2022 created')

### -- Upload File to App ---
uploaded_file_data = st.file_uploader('Please upload Data file')
name = uploaded_file_data.name.split('___')[1].split('__')

new_df = erdem_toolbox.Ad_Copy_Builder(uploaded_file_data)

today_date = date.today().strftime("%m.%d.%y")

### --- Downloading File ---
# Convert DF to a Streamlit excel downloadable version
df_xlsx = erdem_toolbox.to_excel(new_df, 'Data')

st.download_button(
    label = '📥 Press to Download Output File',
    data = df_xlsx,
    file_name = f'Ad Copy Bulk Upload - {today_date} - {name[0]} - {name[1]}.xlsx',
    key = 'download-button'
)
