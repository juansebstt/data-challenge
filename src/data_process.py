import pandas as pd

file_path = "C:/Users/under/Pycharm-Projects/TelefonicaChallenge/data/Events.xlsx"

data = pd.read_excel(file_path)

print(data['event_params'].iloc[0])