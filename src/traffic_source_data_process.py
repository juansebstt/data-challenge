import json
import pandas as pd
import plotly.express as px
import os

base_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
base_folder = os.path.abspath(base_folder)

# File paths
file_path = os.path.join(base_folder, "Events.xlsx")
csv_path = os.path.join(base_folder, "traffic_source_analysis.csv")

df = pd.read_excel(file_path)


# Extract the traffic_source column as a JSON object
def extract_traffic_source_data(traffic_source_data):
    try:
        traffic_info = json.loads(traffic_source_data)
        return {
            "name": traffic_info.get("name", None),
            "medium": traffic_info.get("medium", None),
            "source": traffic_info.get("source", None),
        }
    except (json.JSONDecodeError, TypeError):
        return {
            "name": None,
            "medium": None,
            "source": None,
        }


# Apply the extraction to the traffic_source column
traffic_source_data_extracted = df["traffic_source"].apply(extract_traffic_source_data)
traffic_source_df = pd.json_normalize(traffic_source_data_extracted)

# Merge the new data back into the main DataFrame
df_traffic_source_analysis = pd.concat([df, traffic_source_df], axis=1)

# Analyze medium, source, and name
traffic_source_columns = [
    'medium',
    'source',
    'name'
]

# Create funnel charts for each field in the traffic source data
for column in traffic_source_columns:
    traffic_source_counts = df_traffic_source_analysis.groupby(column)["user_pseudo_id"].nunique().reset_index()
    traffic_source_counts.columns = [column, "Unique Users"]

    # Sort by "Unique Users" in descending order
    traffic_source_counts = traffic_source_counts.sort_values(by="Unique Users", ascending=False)

    # Create a funnel chart
    funnel_chart = px.funnel(
        traffic_source_counts,
        x="Unique Users",
        y=column,
        title=f"{column.capitalize()} Traffic Funnel"
    )
    funnel_chart.show()

# Save aggregated data to CSV (summary style)
summary_csv_path = os.path.join(base_folder, "traffic_source_summary.csv")

# Combine all summaries into a single dataframe and save
traffic_source_summary_df = pd.concat([traffic_source_counts for column in traffic_source_columns], axis=0)
traffic_source_summary_df.to_csv(summary_csv_path, index=False)

print(f"Traffic source summary data saved to: {summary_csv_path}")
