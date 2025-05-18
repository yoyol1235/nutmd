
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("NUTMD_Prebook_Logs.csv")

# Extract JSON error message (if any)
df['StatusMessage'] = df['RESPONSE'].str.extract(r'"StatusMessage":"([^"]+)"')
df['Provider'] = df['rateDetailCode'].str.extract(r"(\d+)-")
df['Agency'] = df['rateDetailCode'].str.extract(r"-(\d+)")

# Convert datetime if needed
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])

st.title("Prebook Error Monitoring Dashboard")

# General metrics
st.metric("Total Errors", len(df))
st.metric("Unique Providers", df['Provider'].nunique())
st.metric("Unique Agencies", df['Agency'].nunique())

# Grouped error counts by provider
provider_error_count = df.groupby('Provider').size().reset_index(name='Error Count')
fig1 = px.bar(provider_error_count, x='Provider', y='Error Count', title="Errors by Provider")
st.plotly_chart(fig1)

# Grouped error counts by StatusMessage
status_count = df.groupby('StatusMessage').size().reset_index(name='Count')
fig2 = px.bar(status_count, x='StatusMessage', y='Count', title="Status Message Distribution")
st.plotly_chart(fig2)

# Grouped errors by Hotel ID and Hotel Name (if fields exist)
if 'hotelId' in df.columns and 'hotelName' in df.columns:
    hotel_errors = df.groupby(['hotelId', 'hotelName']).size().reset_index(name='Errors')
    fig3 = px.bar(hotel_errors, x='hotelName', y='Errors', title="Errors by Hotel", hover_data=['hotelId'])
    st.plotly_chart(fig3)

# Optional table view
st.subheader("Raw Data")
st.dataframe(df[['TIMESTAMP', 'Agency', 'Provider', 'StatusMessage']])
