import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# --- DATA LOADING LOGIC ---
# This part automatically finds your file regardless of the folder structure
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, "Online Sales Data.csv")

try:
    df = pd.read_csv(csv_path)
    
    st.title("📊 Interactive Sales Dashboard")
    st.markdown("---")

    # --- SIDEBAR FILTER ---
    st.sidebar.header("Filter Options")
    regions = df['Region'].unique()
    selected_regions = st.sidebar.multiselect(
        "Select Region(s):", 
        options=regions, 
        default=regions
    )

    # Filter the data based on selection
    filtered_df = df[df['Region'].isin(selected_regions)]

    # --- KPI SECTION ---
    total_revenue = filtered_df['Total Revenue'].sum()
    avg_sales = filtered_df['Total Revenue'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Average Sale", f"${avg_sales:,.2f}")

    st.markdown("---")

    # --- CHARTS SECTION ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Sales by Product Category")
        fig_bar = px.bar(
            filtered_df, 
            x="Product Category", 
            y="Total Revenue", 
            color="Product Category",
            template="plotly_white"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.subheader("Revenue Distribution by Region")
        region_revenue = filtered_df.groupby("Region")["Total Revenue"].sum().reset_index()
        fig_pie = px.pie(
            region_revenue, 
            values="Total Revenue", 
            names="Region", 
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- DATA PREVIEW ---
    with st.expander("View Raw Filtered Data"):
        st.dataframe(filtered_df)

except FileNotFoundError:
    st.error(f"Error: Could not find 'Online Sales Data.csv'. Please ensure it is in the same folder as app.py on GitHub.")
    st.info(f"Current looking in: {csv_path}")