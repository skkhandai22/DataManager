import streamlit as st
import pandas as pd
from utils.data_cleaning import DataClean
from utils.data_processing import DataProcessing
from utils.data_vizualization import DataVisuals
from io import BytesIO
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title='Data Manager', page_icon="images/png-transparent-product-lifecycle-aras-corp-product-data-management-computer-software-china-cloud-miscellaneous-logo-engineering.png", layout="wide", initial_sidebar_state='expanded')

st.sidebar.title('''**Data Manager**''')

# Create a download button for the processed data
def convert_df_to_excel(dataframe, table_chart_path, pie_chart_path):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, sheet_name='Processed Data', index=False)
        
        workbook = writer.book
        
        # Create a new sheet for Data Insights
        insights_sheet = workbook.create_sheet('Data Insights')

        # Add table chart to Data Insights sheet
        table_img = Image(table_chart_path)
        table_img.width = 590  # Adjust the width as needed
        table_img.height = 600  # Adjust the height as needed
        insights_sheet.add_image(table_img, 'A1')
        
        # Add pie chart to Data Insights sheet
        pie_img = Image(pie_chart_path)
        pie_img.width = 600  # Adjust the width as needed
        pie_img.height = 400  # Adjust the height as needed
        insights_sheet.add_image(pie_img, 'J1')  # Adjust the position as needed
        
        # Remove default sheet if it exists
        if 'Sheet' in writer.book.sheetnames:
            default_sheet = writer.book['Sheet']
            writer.book.remove(default_sheet)
        
    processed_data = output.getvalue()
    return processed_data

# Sidebar for file upload
st.sidebar.header('Upload your Excel file')
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    # Read and display the dataframe
    df = pd.read_excel(uploaded_file)
    st.subheader('Preview of Uploaded Data')
    st.dataframe(df.head())

    # Create an instance of DataClean and process the data
    cleaned_data = DataClean(df).process_clean()
    processed_data = DataProcessing(cleaned_data).process_data()
    visualizations = DataVisuals(data=df, processed_data=processed_data)
    visualizations.process_visuals()

    st.subheader('Preview of Processed Data')
    st.dataframe(processed_data)
    
    excel_data = convert_df_to_excel(processed_data, "table_chart.png", "pie_chart.png")
    
    st.download_button(
        label="Download Processed Data",
        data=excel_data,
        file_name="processed_data_with_visualizations.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
