import streamlit as st
import pandas as pd
from qag_preprocess import getQAGDataframe, displayData
from datetime import datetime

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

displayed_df = displayData(filtered_df)
# st.write('Displayed Data:')
# table = st.table(displayed_df.drop(columns=['Discussion_Content']))

# Display the filtered DataFrame
# st.write('Filtered Data:')
# table = st.table(filtered_df.drop(columns=['Discussion_Content']))

# Add expander for discussion content
# st.write('Discussion Content:')
# selected_row = st.expander(
#     'Click a row to view Discussion Content:', expanded=False)
# if selected_row:
#     row_index = selected_row.radio('Select a Row:', filtered_df.index)
#     selected_content = filtered_df.at[row_index, 'Discussion_Content']
#     st.write(selected_content)

expanders = []
for index, row in displayed_df.iterrows():
    expander = st.expander(
        f"{row['Displayed_Date']} - {row['Asking_Person_ID']}", expanded=False)
    expander.write(row['Discussion_Content'])
    expanders.append(expander)

# Listen for row selection
# selected_expander = st.selectbox(
#     'Select a Row:', expanders, format_func=lambda expander: expander.title)
