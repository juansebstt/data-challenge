import pandas as pd
import json
import plotly.graph_objects as go
import os

file_path = "C:/Users/under/Pycharm-Projects/TelefonicaChallenge/data/Events.xlsx"
df = pd.read_excel(file_path)

folder_path = 'C:/Users/under/Pycharm-Projects/TelefonicaChallenge/data/'

image_path = os.path.join(folder_path, 'funnel.png')
csv_path = os.path.join(folder_path, 'funnel.csv')


def extract_paso_flujo(event_params):
    try:
        params = json.loads(event_params)
        for param in params:
            if param.get("event_param_key") == "paso_flujo":
                return param.get("event_param_string_value")
    except (json.JSONDecodeError, TypeError):
        return None


df['paso_flujo'] = df['event_params'].apply(extract_paso_flujo)

df_filtered = df[df['paso_flujo'].notnull()]

funnel = df_filtered.groupby('paso_flujo')['user_pseudo_id'].nunique().reset_index()
funnel.columns = ['Paso del flujo', 'Clientes únicos']

funnel = funnel.sort_values('Clientes únicos', ascending=False)


def count_page_view_users(df):
    return df[df['event_name'] == 'page_view']['user_pseudo_id'].nunique()


page_view_count = count_page_view_users(df)
print(f"Usuarios únicos que visualizaron la Landing Page: {page_view_count}")


def funnel_data(funnel, page_view_count, date="14-11-2024"):
    funnel_data = funnel.copy()
    funnel_data.loc[-1] = ['Page Views', page_view_count]
    funnel_data.index = funnel_data.index + 1
    funnel_data.sort_index(inplace=True)

    funnel_data = funnel_data.sort_values(by='Clientes únicos', ascending=False)

    return funnel_data


funnel_data = funnel_data(funnel, page_view_count)

labels = funnel_data['Paso del flujo']
values = funnel_data['Clientes únicos']

funnel_chart = go.Figure(
    go.Funnel(
        y=labels,
        x=values,
        textinfo='value+percent previous+percent initial'
    )
)

funnel_chart.update_layout(
    title='Customer convertion funnel',
    yaxis_title='Steps',
    xaxis_title='Number of unique customers',
    showlegend=False
)

if not funnel_data.empty:
    try:
        funnel_data.to_csv(csv_path, index=False)
        print(f"CSV file saved successfully: {csv_path}")
    except Exception as e:
        print(f"Error saving CSV: {e}")
else:
    print("DataFrame is empty, nothing to save.")


funnel_chart.show()
