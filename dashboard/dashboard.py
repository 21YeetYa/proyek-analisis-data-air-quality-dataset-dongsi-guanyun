import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Apply seaborn styling
sns.set_style("whitegrid")

# Load the data
merged_df = pd.read_csv('main_data.csv')

# Set page configuration
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Sidebar for user input
st.sidebar.header("Filter Options")
selected_station = st.sidebar.multiselect(
    'Select Station(s)',
    options=merged_df['station'].unique(),
    default=merged_df['station'].unique()
)

selected_year = st.sidebar.slider(
    'Select Year Range',
    int(merged_df['year'].min()), 
    int(merged_df['year'].max()), 
    (int(merged_df['year'].min()), int(merged_df['year'].max()))
)

# Filter the data based on user input
filtered_df = merged_df[(merged_df['station'].isin(selected_station)) & 
                        (merged_df['year'].between(*selected_year))]

# Main Title
st.title("Air Quality Analysis Dashboard 🌤️")
st.markdown("""
This dashboard provides insights into air pollution trends between 2013 and 2017 for Dongsi and Guanyuan stations. 
You can explore the yearly concentration of **PM2.5** and **PM10**, compare stations, and identify trends in air quality.
""")

# Layout: Divide into two columns for better organization
col1, col2 = st.columns(2)

# First plot: PM2.5 concentration
with col1:
    st.subheader("Yearly Average PM2.5 Concentration")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='year', y='PM2.5', hue='station', data=filtered_df, palette='viridis')
    plt.title('Rata-rata Tahunan Konsentrasi PM2.5 (2013-2017)', fontsize=14)
    plt.xlabel('Tahun')
    plt.ylabel('Konsentrasi PM2.5 (μg/m³)')
    st.pyplot(plt.gcf())

# Second plot: PM10 concentration
with col2:
    st.subheader("Yearly Average PM10 Concentration")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='year', y='PM10', hue='station', data=filtered_df, palette='rocket')
    plt.title('Rata-rata Tahunan Konsentrasi PM10 (2013-2017)', fontsize=14)
    plt.xlabel('Tahun')
    plt.ylabel('Konsentrasi PM10 (μg/m³)')
    st.pyplot(plt.gcf())

# Group data by year and station, then calculate the mean PM2.5 and PM10
yearly_avg = filtered_df.groupby(['year', 'station'])[['PM2.5', 'PM10']].mean().reset_index()

# Third plot: PM2.5 (average by year and station)
st.subheader("Average PM2.5 Concentration by Year and Station")
plt.figure(figsize=(12, 6))
sns.lineplot(x='year', y='PM2.5', hue='station', data=yearly_avg, palette='coolwarm')
plt.title('Rata-rata Tahunan Konsentrasi PM2.5 di Dongsi dan Guanyuan (2013-2017)', fontsize=14)
plt.xlabel('Tahun')
plt.ylabel('Konsentrasi PM2.5 (μg/m³)')
st.pyplot(plt.gcf())

# Fourth plot: PM10 (average by year and station)
st.subheader("Average PM10 Concentration by Year and Station")
plt.figure(figsize=(12, 6))
sns.lineplot(x='year', y='PM10', hue='station', data=yearly_avg, palette='magma')
plt.title('Rata-rata Tahunan Konsentrasi PM10 di Dongsi dan Guanyuan (2013-2017)', fontsize=14)
plt.xlabel('Tahun')
plt.ylabel('Konsentrasi PM10 (μg/m³)')
st.pyplot(plt.gcf())

# Calculate percentage change in PM2.5 and PM10 from previous year
yearly_avg['PM2.5_change'] = yearly_avg.groupby('station')['PM2.5'].pct_change()
yearly_avg['PM10_change'] = yearly_avg.groupby('station')['PM10'].pct_change()

# Display most significant decrease in PM2.5 and PM10
st.subheader("Most Significant Decrease in PM2.5 and PM10")

pm25_decrease_year = yearly_avg.loc[yearly_avg.groupby('station')['PM2.5_change'].idxmin()]
pm10_decrease_year = yearly_avg.loc[yearly_avg.groupby('station')['PM10_change'].idxmin()]

st.write("**Tahun dengan penurunan paling signifikan dalam konsentrasi PM2.5:**")
st.write(pm25_decrease_year[['station', 'year', 'PM2.5_change']])

st.write("**Tahun dengan penurunan paling signifikan dalam konsentrasi PM10:**")
st.write(pm10_decrease_year[['station', 'year', 'PM10_change']])

# Footer
st.markdown("""
---
**Note**: Data shows historical trends and does not represent real-time monitoring. The data is sourced from air quality measurements collected between 2013 and 2017.
""")
