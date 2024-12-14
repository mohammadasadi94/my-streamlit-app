
# app.py
import pandas as pd

import streamlit as st


st.title("Beijing Multi-Site Air Quality data analysis ")
combined_dataFrame = None
csv_files = st.file_uploader("Please Upload at least 6 of the CSV files to start the analysis", accept_multiple_files=True, type='csv')
if csv_files is not None:
  if len(csv_files) >= 6:
    dataframes = []
    for file in csv_files:
      df = pd.read_csv(file)
      dataframes.append(df)
    combined_dataFrame=pd.concat(dataframes,ignore_index=True)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Data Overview", "Exploratory Data Analysis (EDA)", "Modelling and Prediction"])
    if page == "Data Overview":
      if combined_dataFrame is not None:
        main.ma(combined_dataFrame)
    elif page=="Exploratory Data Analysis (EDA)":
      if combined_dataFrame is not None:
        preprocessing.m(combined_dataFrame)
    else:
        st.warning("Please upload at least 6 CSV files first.")
  else:
    st.warning("Please upload at least 6 CSV files to start the analysis")
