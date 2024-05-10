import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Public Health Campaign", layout='wide')

# Load data
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/your-repo/sample_data.csv"  # Replace with your data source
    data = pd.read_csv(url)
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
disease_filter = st.sidebar.multiselect(
    "Select Diseases", options=df["Disease"].unique(), default=df["Disease"].unique()
)
region_filter = st.sidebar.multiselect(
    "Select Regions", options=df["Region"].unique(), default=df["Region"].unique()
)
year_filter = st.sidebar.slider(
    "Select Year Range", min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()), value=(int(df["Year"].min()), int(df["Year"].max()))
)

# Apply filters
filtered_data = df[
    (df["Disease"].isin(disease_filter)) &
    (df["Region"].isin(region_filter)) &
    (df["Year"].between(year_filter[0], year_filter[1]))
]

# Page Title
st.title("Public Health Campaign - Regional Disparities Visualization")

# Storytelling: Introduction
st.markdown("""
### Introduction
Public health campaigns require a deep understanding of regional disparities to allocate resources effectively. This app provides visual insights into such disparities, focusing on selected diseases across different regions.
""")

# Visualization: Regional Disease Cases Over Time
st.markdown("### Disease Cases Over Time")
fig1 = px.line(
    filtered_data,
    x="Year",
    y="Cases",
    color="Region",
    line_group="Disease",
    hover_name="Disease",
    title="Regional Disease Cases Over Time",
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization: Heatmap to Highlight Regional Disparities
st.markdown("### Regional Disease Cases Heatmap")
heatmap_data = filtered_data.pivot_table(
    index="Region", columns="Disease", values="Cases", aggfunc="sum"
).fillna(0)
fig2 = px.imshow(
    heatmap_data,
    labels=dict(x="Disease", y="Region", color="Cases"),
    title="Regional Disease Cases Heatmap",
)
st.plotly_chart(fig2, use_container_width=True)

# Visualization: Bar Chart for Yearly Disease Cases
st.markdown("### Yearly Disease Cases by Region")
fig3 = px.bar(
    filtered_data,
    x="Year",
    y="Cases",
    color="Disease",
    barmode="group",
    facet_row="Region",
    title="Yearly Disease Cases by Region",
)
st.plotly_chart(fig3, use_container_width=True)

# Storytelling: Conclusion
st.markdown("""
### Conclusion
The visualizations above provide a clear understanding of regional disparities in disease cases. By leveraging these insights, public health officials can prioritize interventions and allocate resources more effectively.
""")
