import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os
import glob
import tempfile

st.title("Nanosniffer ETD Data Plot Generator")

uploaded_zip = st.file_uploader("Upload ETD Folder (ZIP)", type="zip")

if uploaded_zip:

    # Create temporary folder
    temp_dir = tempfile.mkdtemp()

    # Extract ZIP
    zip_path = os.path.join(temp_dir, "data.zip")

    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.getbuffer())

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Find CSV files
    files = glob.glob(os.path.join(temp_dir, "**", "*_Data.csv"), recursive=True)

    st.write("Total files found:", len(files))

    plots_folder = os.path.join(temp_dir, "Plots")
    os.makedirs(plots_folder, exist_ok=True)

    for file_path in files:

        try:
            df = pd.read_csv(file_path)

            process_data = df.iloc[1:, -5:]
            process_data = process_data.apply(pd.to_numeric, errors='coerce')

            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(process_data)

            ax.set_title(os.path.basename(file_path))
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")
            ax.legend(["CH1","CH2","CH3","CH4"])
            ax.grid(True)

            st.pyplot(fig)

            file_name = os.path.basename(file_path).replace(".csv",".png")
            save_path = os.path.join(plots_folder, file_name)

            fig.savefig(save_path, dpi=100)
            plt.close()

        except Exception as e:
            st.error(f"Error in {file_path}")
            st.write(e)

    st.success("All plots generated successfully.")