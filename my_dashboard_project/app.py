import streamlit as st

st.title("Connection Test")
st.write("I am a data analyst in the making!")
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive Sales Dashboard")

# 1. Load the data
# Use the exact name of the file you downloaded
df = pd.read_csv("Online Sales Data.csv")

# 2. Show a small preview
st.subheader("Data Preview")
st.dataframe(df.head())
# 3. Create a Sidebar for filtering
st.sidebar.header("Filter Data")

# Create a list of unique regions from your data
regions = df['Region'].unique()

# Add a multi-select box to the sidebar
selected_regions = st.sidebar.multiselect("Select Region(s):", options=regions, default=regions)

# 4. Filter the data based on selection
filtered_df = df[df['Region'].isin(selected_regions)]

# 5. Show the filtered table
st.subheader("Filtered Results")
st.dataframe(filtered_df)
# 6. Create a Bar Chart for Sales by Product
st.subheader("Sales by Product Category")

# We use our 'filtered_df' so the chart updates when you use the sidebar!
fig = px.bar(
    filtered_df, 
    x="Product Category", 
    y="Total Revenue", 
    title="Revenue per Product",
    color="Product Category", # This gives each bar a different color
    template="plotly_white"
)

# 7. Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
# 8. Create a Pie Chart for Sales by Region
st.subheader("Sales by Region")

# We group the data by region and sum up the revenue
region_revenue = filtered_df.groupby("Region")["Total Revenue"].sum().reset_index()

fig_pie = px.pie(
    region_revenue, 
    values="Total Revenue", 
    names="Region", 
    title="Revenue Distribution by Region",
    hole=0.4 # This makes it a "Donut" chart, which looks more modern!
)

st.plotly_chart(fig_pie, use_container_width=True)