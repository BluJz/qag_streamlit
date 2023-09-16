import streamlit as st
import pandas as pd
from qag_preprocess import getQAGDataframe, displayData
from datetime import datetime
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
# with st.expander('Filtre'):
ministries = df['Responding_Ministry'].unique()
ministries = ['Tous'] + list(ministries)  # Add "All" option
selected_ministry = st.selectbox('Ministère adressé', ministries)

# Adjust filtering based on the selected ministry
if selected_ministry == 'Tous':
    ministry_filtered_df = filtered_df  # No filter applied
else:
    ministry_filtered_df = filtered_df[filtered_df['Responding_Ministry']
                                       == selected_ministry]

# Calculate the number of questions per group
group_counts = ministry_filtered_df['Asking_Group'].value_counts()

# Convert the group_counts to a dictionary
group_counts_dict = group_counts.to_dict()

# Create a bar chart using Stream Echarts
options = {
    "title": {"text": "Nombre de QAG par groupe politique"},
    # Rotate the x-axis labels
    "xAxis": {"type": "category", "data": list(group_counts_dict.keys()), "axisLabel": {"rotate": 45}},
    "yAxis": {"type": "value"},
    "series": [{"data": list(group_counts_dict.values()), "type": "bar"}],
}

st_echarts(options=options, height=300, key="bar_chart")

####################################
st.markdown("<hr>", unsafe_allow_html=True)

# Create a row for the asking group filter
asking_groups = df['Asking_Group'].unique()
asking_groups = ['Tous'] + list(asking_groups)  # Add "All" option
asking_group_filter = st.selectbox(
    'Sélectionnez le groupe politique de la QAG :', asking_groups)

# Create a pie chart for the proportion of responding ministries for the selected group
group_filtered_df = df[(df['Asking_Group'] == asking_group_filter)
                       & (df['Date'] >= start_date) & (df['Date'] <= end_date)]
ministries = group_filtered_df['Responding_Ministry'].value_counts()

# Create a pie chart using Stream Echarts
pie_options = {
    "title": {"text": f"Proportion des ministères pour le groupe {asking_group_filter}"},
    "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b}: {c} ({d}%)"},
    "series": [
        {
            "name": "Proportion",
            "type": "pie",
            "radius": ["50%", "70%"],
            "avoidLabelOverlap": False,
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "30", "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data": [{"value": v, "name": k} for k, v in ministries.items()],
        }
    ],
}

st_echarts(options=pie_options, height=300, key="pie_chart")

####################################
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
