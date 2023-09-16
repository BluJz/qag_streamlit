import streamlit as st
import pandas as pd
from qag_preprocess import getQAGDataframe, displayData
from datetime import datetime

# Load your DataFrame
# df = pd.read_csv('your_dataframe.csv')  # If you saved your DataFrame to a CSV file
df = getQAGDataframe()

# Create Streamlit app
st.title('Questions Au Gouvernement (QAG) - XVème législature')

st.markdown("<hr>", unsafe_allow_html=True)

st.header('Questions Au Gouvernement en détail')

# Add filters for Asking_Group and Responding_Ministry
asking_group_filter = st.selectbox(
    'Sélectionnez le groupe politique de la QAG:', df['Asking_Group'].unique())
ministry_filter = st.selectbox(
    'Sélectionnez le ministère cible de la QAG:', df['Responding_Ministry'].unique())

# Apply filters to the DataFrame
filtered_df = df[(df['Asking_Group'] == asking_group_filter)
                 & (df['Responding_Ministry'] == ministry_filter)]

displayed_df = displayData(filtered_df)

# List of expandable questions
expanders = []
for index, row in displayed_df.iterrows():
    expander = st.expander(
        f"{row['Displayed_Date']} - {row['Asking_Person_ID']}", expanded=False)
    expander.markdown(row['Discussion_Content'], unsafe_allow_html=True)
#    expander.write(row['Discussion_Content'])
    expanders.append(expander)
