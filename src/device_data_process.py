import json
import pandas as pd
import plotly.express as px
import os

base_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
base_folder = os.path.abspath(base_folder)

# File paths
file_path = os.path.join(base_folder, "Events.xlsx")
image_path = os.path.join(base_folder, "funnel.png")
csv_path = os.path.join(base_folder, "funnel.csv")

df = pd.read_excel(file_path)


# Extract the device column as a JSON object
def extract_device_data(device_data):
    try:
        device_info = json.loads(device_data)
        return {
            "category": device_info.get("category", None),
            "mobile_brand_name": device_info.get("mobile_brand_name", None),
            "mobile_model_name": device_info.get("mobile_model_name", None),
            "operating_system": device_info.get("operating_system", None),
            "operating_system_version": device_info.get("operating_system_version", None),
            "browser": device_info.get("web_info", {}).get("browser", None),
            "language": device_info.get("language", None),
        }
    except (json.JSONDecodeError, TypeError):
        return {
            "category": None,
            "mobile_brand_name": None,
            "mobile_model_name": None,
            "operating_system": None,
            "operating_system_version": None,
            "browser": None,
            "language": None,
        }


# Apply the extraction to the device column
device_data_extracted = df["device"].apply(extract_device_data)
device_df = pd.json_normalize(device_data_extracted)

# Merge the new data back into the main DataFrame
df_device_analysis = pd.concat([df, device_df], axis=1)

# Analyze category, brand, model, OS, browser, and language
device_columns = [
    'category',
    'mobile_brand_name',
    'mobile_model_name',
    'operating_system',
    'operating_system_version',
    'browser',
    'language'
]

# Create funnel charts for each field in the device data
for column in device_columns:
    device_counts = df_device_analysis.groupby(column)["user_pseudo_id"].nunique().reset_index()
    device_counts.columns = [column, "Unique Users"]

    # Sort by "Unique Users" in descending order
    device_counts = device_counts.sort_values(by="Unique Users", ascending=False)

    # Create a funnel chart
    funnel_chart = px.funnel(
        device_counts,
        x="Unique Users",
        y=column,
        title=f"{column.capitalize()} Usage Funnel"
    )
    funnel_chart.show()

# Aggregate data by each device column (like the funnel CSV)
device_summary = {}
for column in device_columns:
    device_summary[column] = df_device_analysis.groupby(column)["user_pseudo_id"].nunique().reset_index()
    device_summary[column].columns = [column, "Unique Users"]

# Save aggregated data to CSV (summary style)
summary_csv_path = os.path.join(base_folder, "device_summary.csv")

# Combine all summaries into a single dataframe and save
device_summary_df = pd.concat([device_summary[column] for column in device_columns], axis=0)
device_summary_df.to_csv(summary_csv_path, index=False)

print(f"Device summary data saved to: {summary_csv_path}")

