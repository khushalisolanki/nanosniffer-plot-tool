import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Nanosniffer Data Plot Tool")

uploaded_files = st.file_uploader(
    "Upload *_Data.csv files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:

    for file in uploaded_files:

        df = pd.read_csv(file)

        process_data = df.iloc[:, -5:]
        process_data = process_data.apply(pd.to_numeric, errors='coerce')

        fig, ax = plt.subplots(figsize=(10,5))

        ax.plot(process_data)
        ax.set_title(file.name)
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.legend(["CH1","CH2","CH3","CH4"])
        ax.grid(True)

        st.pyplot(fig)