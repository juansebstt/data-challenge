# Digital Analytical Test: Postpaid Flow Analysis

## Project Description

This project aims to analyze the event flow from Movistar’s website on November 14th, 2024, specifically for postpaid users. The data used is captured by Google Analytics and retrieved from BigQuery. The events are stored in an Excel file containing event details with unique user identifiers (`user_pseudo_id`) and event parameters in JSON format, specifically the `event_params` field, which holds information about the flow step.

### Project Requirements

The analysis is based on the following key points:

1. **Conversion Funnel**: The `paso_flujo` attribute is extracted to reconstruct the conversion funnel for November 14th, 2024, quantifying the number of unique customers at each step of the flow.

1. **Page Views**: The `event_name` field, with the value `page_view`, is used to calculate the number of users who viewed the initial landing page of the flow, serving as the starting point of the funnel.
2. **Funnel Visualization**: The funnel for November 14th, 2024, is plotted, with page views displayed at the top of the funnel.
3. **Exploration of Other Variables**: Other event attributes like `device`, `traffic_source`, `geo` and `user_first_touch_timestamp` are explored to generate additional visualizations, such as peak usage hour analysis.

## Project Structure

```
├── .venv                   # Virtual environment
├── data                    # Folder containing data files
│   ├── device_summary.csv  # Processed device data
│   ├── Events.xlsx         # Excel file with raw event data
│   ├── funnel.csv          # Funnel analysis data
│   ├── geo_summary.csv     # Processed geo-location data
│   ├── peak_usage_hours.csv # Processed peak usage hours data
│   └── traffic_source_summary.csv # Processed traffic source data
├── src                     # Python source files
│   ├── __init__.py
│   ├── data_process.py     # Main data processing script (Requiered)
│   ├── device_data_process.py  # Device data processing
│   ├── geo_location_data_process.py  # Geo-location data processing
│   ├── peak_hours_data_process.py  # Peak hours data processing
│   └── traffic_source_data_process.py  # Traffic source data processing
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

```

## How to Pull the Repository and Run the Analysis

Follow these steps to get started with the project:

### Step 1: Clone the Repository

First, clone the repository to your local machine using Git. Open your terminal or command prompt and run the following command:

```bash
git clone https://github.com/juansebstt/data-challenge.git
```

### Step 2: Navigate to the Project Directory

Once the repository is cloned, navigate to the project directory:

```bash
cd data-challenge
```

### Step 3: Set Up a Virtual Environment

It's recommended to create a virtual environment for the project to avoid conflicts with other Python projects. Run the following commands:

### For Windows:

```python
python -m venv .venv
```

### For macOS/Linux:

```python
python3 -m venv .venv
```

### Step 4: Activate the Virtual Environment

Activate the virtual environment with the following command:

### For Windows:

```python
.venv\Scripts\activate
```

### For macOS/Linux:

```python
source .venv/bin/activate
```

After activating the virtual environment, your terminal prompt should change to show the virtual environment name.

### Step 5: Install Project Dependencies

With the virtual environment activated, install the required dependencies from the `requirements.txt` file:

```python
pip install -r requirements.txt
```

### Step 6: Verify the Data File

Ensure that the `Events.xlsx` file is in the `data` folder of the project. This file contains the event data used for analysis.

### Step 7: Run the Analysis Scripts

To run the entire analysis, use the following command:

```python
python src/run_analysis.py
```

>[!NOTE]
>Additionally you could run each of the scripts individually if you prefer to do so.

 

This script will execute all analysis steps, such as:

1. **Funnel Analysis**
2. **Device Usage Analysis**
3. **Geo-location Usage Analysis**
4. **Peak Hours Usage Analysis**
5. **Traffic Source Analysis**

Each script processes the data, generates visualizations, and saves results to CSV files in the `data` folder.

### Step 8: View the Results

- Visualizations for each analysis will be shown in your browser.
- Aggregated data for each analysis will be saved as CSV files in the `data` folder, such as `funnel.csv`, `device_summary.csv`, `peak_usage_hours.csv`, `traffic_source_summary.csv` and `geo_summary.csv`.

>[!IMPORTANT]
> Visualization: 
>  After running the scripts, the visualizations of the charts (such as funnel charts, bar charts, etc.) will open automatically in your preferred web browser. These charts provide insights into the event flow, device usage, geographical data, and peak usage hours.

>[!TIP]
> Ensure your Python version is 3.x. If you're unsure, check with `python --version` or `python3 --version`.
> If you encounter any issues with dependencies, consider upgrading `pip` by running:
    
```
   pip install --upgrade pip
```

## Analysis Performed

### 1. Conversion Funnel

The funnel analysis is performed by extracting the `paso_flujo` attribute from the `event_params` field of each event. This allows us to reconstruct the user flow and calculate the number of unique customers at each stage. The steps are related to specific events that users perform during their interaction with the Movistar website.

### 2. Page Views Count

The `page_view` event is used as the preliminary data point to count the number of users who viewed the initial landing page. This is essential for establishing the base of users at the start of the funnel and visualizing the drop-offs at each subsequent stage.

### 3. Device Analysis

The devices used by users to interact with the site are analyzed, including:

- Device category (mobile, tablet, desktop).
- Mobile brand and model.
- Operating system and browser.
- Language.

This analysis is displayed as visualizations for each relevant attribute.

### 4. Traffic Source Analysis

Data from the `traffic_source` field is broken down to understand how each source and medium contributes to the funnel. The following parameters are extracted:

- **Medium**: The medium (e.g., CPC, SMS, Organic).
- **Source**: The source (e.g., Google, InfoBip).
- **Campaign Name**: Extracted from the `name` field.

### 5. Peak Usage Hour Analysis

Using the `user_first_touch_timestamp` field, the hours of the day with the most user interactions are calculated. This is visualized with a bar chart showing the peak hours of traffic throughout the day.

### 6. Geo-Location Analysis
This script processes the geographical data from the `geo` column, which is stored as JSON in the events dataset. It extracts attributes such as `city`, `country`, `continent`, `region`, `sub_continent`, and `metro` and generates unique user counts for each attribute. Funnel charts are created to visualize user distribution by these geographical attributes. The processed data is saved as `geo_summary.csv` for further analysis.

## Results

### Conversion Funnel

The generated chart visualizes the number of users at each step of the funnel, highlighting the stages where users drop off.

### Device Summary

A breakdown of users by device type, operating system, and browser is provided, offering insights into the technological profile of the users.

### Traffic Sources

A detailed analysis of traffic sources and mediums is displayed, showing which are the most effective in driving users.

### Peak Hour Analysis

The peak hour chart identifies when users are most active on the website, providing valuable information for optimizing content and campaigns.

### Geo-Location Analysis

The geo-location analysis highlights user distribution across various geographical attributes, such as city, country, continent, and region. This insight helps identify where users are engaging from, enabling better-targeted strategies and localized optimizations.

## Conclusion

This project provides an in-depth analysis of user behavior on Movistar’s website, helping identify key insights into the user journey, device usage, geographical trends, and peak usage times. The visualizations offer valuable data for decision-making and optimization of user experiences, while the CSV outputs allow further analysis or integration with other systems.