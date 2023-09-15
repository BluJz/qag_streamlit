import streamlit as st
import pandas as pd
from qag_preprocess import getQAGDataframe

# Load your DataFrame
# df = pd.read_csv('your_dataframe.csv')  # If you saved your DataFrame to a CSV file
df = getQAGDataframe()

# Create Streamlit app
st.title('Question Files Viewer')

# Add filters for Asking_Group and Responding_Ministry
asking_group_filter = st.selectbox(
    'Select Asking Group:', df['Asking_Group'].unique())
ministry_filter = st.selectbox(
    'Select Responding Ministry:', df['Responding_Ministry'].unique())

# Apply filters to the DataFrame
filtered_df = df[(df['Asking_Group'] == asking_group_filter)
                 & (df['Responding_Ministry'] == ministry_filter)]

# Display the filtered DataFrame
st.write('Filtered Data:')
st.write(filtered_df)

# Optionally, you can display the Question_File values as a list
# st.write('Question Files:')
# st.write(filtered_df['Question_File'].tolist())
