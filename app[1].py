
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("NUTMD_Prebook_logs.csv")

# Extract and normalize the response message
df["StatusMessage"] = df["RESPONSE"].str.extract(r'"StatusMessage":"(.*?)"')
df["Agency"] = df["PAXNAME"].str.extract(r'(\d+)', expand=False)
df["Provider"] = df["rateDetailCode"].str.extract(r'^(\d+)', expand=False)
df["HotelID"] = df["rateDetailCode"].str.extract(r'\|(\d+)\|')
df["Hour"] = pd.to_datetime(df["DATE"]).dt.hour
df["Date"] = pd.to_datetime(df["DATE"]).dt.date

# Sidebar filters
st.sidebar.header("Filters")
selected_agency = st.sidebar.selectbox("Select Agency", df["Agency"].dropna().unique())
filtered_df = df[df["Agency"] == selected_agency]

# Display full error table
st.title("Valuation Error Dashboard")
st.subheader("Full Error Log")
st.dataframe(filtered_df[["Date", "Agency", "Provider", "HotelID", "StatusMessage"]])

# Error count by provider
st.subheader("📊 Error Count by Provider")
provider_error_count = filtered_df.groupby("Provider").size().reset_index(name="Error Count")
fig_provider = px.bar(provider_error_count, x="Provider", y="Error Count", color="Error Count")
st.plotly_chart(fig_provider)

# Error count by hotel
st.subheader("🏨 Error Count by Hotel")
hotel_error_count = filtered_df.groupby("HotelID").size().reset_index(name="Error Count")
fig_hotel = px.bar(hotel_error_count, x="HotelID", y="Error Count", color="Error Count")
st.plotly_chart(fig_hotel)

# Error count by StatusMessage
st.subheader("📬 Error Type Frequency")
error_type_count = filtered_df.groupby("StatusMessage").size().reset_index(name="Count")
fig_message = px.bar(error_type_count, x="StatusMessage", y="Count", color="Count")
st.plotly_chart(fig_message)
