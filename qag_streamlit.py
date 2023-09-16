import streamlit as st
import pandas as pd
from qag_preprocess import getQAGDataframe, displayData
from datetime import datetime
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

# Load your DataFrame
# df = pd.read_csv('your_dataframe.csv')  # If you saved your DataFrame to a CSV file
df = getQAGDataframe()

# Create Streamlit app
st.title('Questions Au Gouvernement (QAG) - XVème législature')

# Use st.beta_columns to create two columns for the date inputs
start_date, end_date = st.columns(2)

# Date Range Filter
with start_date:
    start_date = st.date_input('Date min', df['Date'].min())
with end_date:
    end_date = st.date_input('Date max', df['Date'].max())

# Convert the start_date and end_date to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter the DataFrame based on selected date range
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Create a row for the responding ministry filter
with st.expander("Filter by Responding Ministry"):
    selected_ministry = st.selectbox(
        'Select Ministry', df['Responding_Ministry'].unique())


# Group by 'Asking_Group' and count the number of questions per group
group_counts = filtered_df['Asking_Group'].value_counts()

# Create a bar chart to visualize the number of questions
fig, ax = plt.subplots()
group_counts.plot(kind='bar', ax=ax)
ax.set_xlabel('Groupe politique')
ax.set_ylabel('Nombre de questions posées')
ax.set_title('QAG posées par groupe politiques')
st.pyplot(fig)

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
