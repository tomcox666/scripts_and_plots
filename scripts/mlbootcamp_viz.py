import pandas as pd
import plotly.express as px
import streamlit as st

# Kaggle-Specific Data Loading
df = pd.read_csv('mlbootcamp.csv')  # Adjust path if needed

# Streamlit Interface
st.sidebar.header('Select Visualization Options')

# Group By Column Selection
groupby_column = st.sidebar.selectbox(
    'Group by:', 
    options=['State', 'City', 'Category', 'Sub-Category'],  # Adjust as needed
)

# Data Aggregation & Plotting
output_columns = ['Sales', 'Profit']
df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

fig = px.bar(
    df_grouped,
    x=groupby_column,
    y='Sales',
    color='Profit',
    color_continuous_scale=['red', 'yellow', 'green'],  # Customizable color scale
    template='plotly_white',
    title=f'<b>Sales & Profit by {groupby_column}</b>'
)
fig.update_layout(yaxis_title='Sales', xaxis_title=groupby_column)
st.plotly_chart(fig)