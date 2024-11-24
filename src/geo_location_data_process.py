import json
import pandas as pd
import plotly.express as px
import os

base_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
base_folder = os.path.abspath(base_folder)

# File paths
file_path = os.path.join(base_folder, "Events.xlsx")
csv_path = os.path.join(base_folder, "geo_analysis.csv")

df = pd.read_excel(file_path)


# Extract the geo column as a JSON object
def extract_geo_data(geo_data):
    try:
        geo_info = json.loads(geo_data)
        return {
            "city": geo_info.get("city", None),
            "country": geo_info.get("country", None),
            "continent": geo_info.get("continent", None),
            "region": geo_info.get("region", None),
            "sub_continent": geo_info.get("sub_continent", None),
            "metro": geo_info.get("metro", None)
        }
    except (json.JSONDecodeError, TypeError):
        return {
            "city": None,
            "country": None,
            "continent": None,
            "region": None,
            "sub_continent": None,
            "metro": None
        }


# Apply the extraction to the geo column
geo_data_extracted = df["geo"].apply(extract_geo_data)
geo_df = pd.json_normalize(geo_data_extracted)

# Merge the new data back into the main DataFrame
df_geo_analysis = pd.concat([df, geo_df], axis=1)

# Analyze geo attributes
geo_columns = [
    'city',
    'country',
    'continent',
    'region',
    'sub_continent',
    'metro'
]

# Create funnel charts for each geo field
for column in geo_columns:
    geo_counts = df_geo_analysis.groupby(column)["user_pseudo_id"].nunique().reset_index()
    geo_counts.columns = [column, "Unique Users"]

    # Sort by "Unique Users" in descending order
    geo_counts = geo_counts.sort_values(by="Unique Users", ascending=False)

    # Create a funnel chart
    funnel_chart = px.funnel(
        geo_counts,
        x="Unique Users",
        y=column,
        title=f"{column.capitalize()} Usage Funnel"
    )
    funnel_chart.show()

# Aggregate data by each geo column (like the funnel CSV)
geo_summary = {}
for column in geo_columns:
    geo_summary[column] = df_geo_analysis.groupby(column)["user_pseudo_id"].nunique().reset_index()
    geo_summary[column].columns = [column, "Unique Users"]

# Save aggregated data to CSV (summary style)
summary_csv_path = os.path.join(base_folder, "geo_summary.csv")

# Combine all summaries into a single dataframe and save
geo_summary_df = pd.concat([geo_summary[column] for column in geo_columns], axis=0)
geo_summary_df.to_csv(summary_csv_path, index=False)

print(f"Geo summary data saved to: {summary_csv_path}")
