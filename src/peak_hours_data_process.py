import pandas as pd
import plotly.express as px
import os

# Define file paths
base_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
base_folder = os.path.abspath(base_folder)

# File paths for the Excel and output files
file_path = os.path.join(base_folder, "Events.xlsx")
csv_path = os.path.join(base_folder, "peak_usage_hours.csv")

# Load data from the Excel file
df = pd.read_excel(file_path)

# Convert 'user_first_touch_timestamp' to datetime format (adjust unit='s' if it's UNIX timestamp)
df['user_first_touch_timestamp'] = pd.to_datetime(df['user_first_touch_timestamp'], unit='s')

# Extract the hour from the 'user_first_touch_timestamp'
df['hour'] = df['user_first_touch_timestamp'].dt.hour

# Group by hour and count unique users
hourly_activity = df.groupby('hour')['user_pseudo_id'].nunique().reset_index()
hourly_activity.columns = ['Hour', 'Unique Users']

# Ensure all 24 hours are included (even if there are no users in some hours)
all_hours = pd.DataFrame({'Hour': range(24)})
hourly_activity = pd.merge(all_hours, hourly_activity, on='Hour', how='left').fillna(0)

# Sort the data by hour to display in order
hourly_activity = hourly_activity.sort_values('Hour')

# Create a bar chart to visualize peak usage hours
fig = px.bar(hourly_activity, x='Hour', y='Unique Users', title="Peak Use Hours",
             labels={'Hour': 'Hour of the Day', 'Unique Users': 'Number of Unique Users'},
             text='Unique Users')

# Show exact values on top of bars for clarity
fig.update_traces(texttemplate='%{text}', textposition='outside', showlegend=False)

# Customize x-axis to show every hour from 0 to 23
fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    yaxis_title='Unique Users'
)

fig.show()

# Save the aggregated data to CSV
hourly_activity.to_csv(csv_path, index=False)

print(f"Peak usage hours data saved to: {csv_path}")
