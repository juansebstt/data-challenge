import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = "C:/Users/under/Pycharm-Projects/TelefonicaChallenge/data/Events.xlsx"
df = pd.read_excel(file_path)


# Función para extraer el paso del flujo
def extract_paso_flujo(event_params):
    try:
        params = json.loads(event_params)
        for param in params:
            if param.get("event_param_key") == "paso_flujo":
                return param.get("event_param_string_value")
    except (json.JSONDecodeError, TypeError):
        return None


# Aplicamos la función de extracción al dataframe
df['paso_flujo'] = df['event_params'].apply(extract_paso_flujo)

# Filtramos las filas donde no se encontró paso_flujo
df_filtered = df[df['paso_flujo'].notnull()]

# Contamos los clientes únicos por paso
funnel = df_filtered.groupby('paso_flujo')['user_pseudo_id'].nunique().reset_index()
funnel.columns = ['Paso del flujo', 'Clientes únicos']

# Ordenamos los pasos por clientes únicos
funnel = funnel.sort_values('Clientes únicos', ascending=False)


# Función para contar usuarios únicos que vieron la Landing Page
def count_page_view_users(df):
    return df[df['event_name'] == 'page_view']['user_pseudo_id'].nunique()


page_view_count = count_page_view_users(df)
print(f"Usuarios únicos que visualizaron la Landing Page: {page_view_count}")


# Función para crear el gráfico de embudo
def plot_funnel(funnel, page_view_count, date="14-11-2024"):
    funnel_data = funnel.copy()
    # Insertar el paso de Page Views al principio del funnel
    funnel_data.loc[-1] = ['Page Views', page_view_count]
    funnel_data.index = funnel_data.index + 1  # Ajustar el índice
    funnel_data.sort_index(inplace=True)

    # Revertir el orden para que el embudo empiece desde arriba
    funnel_data = funnel_data.sort_values(by='Clientes únicos', ascending=False)

    # Crear el gráfico de embudo con forma de polígono
    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # Usar la función fill_between para crear un gráfico de área que se va estrechando
    y_positions = np.arange(len(funnel_data))
    area_width = funnel_data['Clientes únicos']

    # Calculamos la posición de cada lado del embudo (deberían ir estrechándose)
    left = area_width / 2
    right = -left  # Hacer que se estreche hacia el centro

    # Dibujar el gráfico de embudo
    for i in range(len(funnel_data)):
        ax.fill_betweenx(
            [y_positions[i] - 0.5, y_positions[i] + 0.5],
            left[i], right[i],
            color=sns.color_palette("YlGnBu", len(funnel_data))[i],
            edgecolor='black'
        )

    # Etiquetas de los pasos
    for index, value in enumerate(funnel_data['Clientes únicos']):
        ax.text(
            0,  # Colocamos el texto en el centro del embudo
            y_positions[index],
            f"{value}",
            ha='center',
            va='center',
            fontsize=12,
            color='black'
        )

    # Etiquetas de los pasos en el gráfico
    for index, step in enumerate(funnel_data['Paso del flujo']):
        ax.text(
            0,  # Colocamos el texto en el centro del embudo
            y_positions[index] - 0.5,
            f"{step}",
            ha='center',
            va='center',
            fontsize=14,
            color='black'
        )

    # Ajustes para el gráfico
    plt.gca().invert_yaxis()  # Invertir el eje Y para que el embudo esté en orden descendente
    plt.title(f"Funnel de Conversión - {date}", fontsize=16)
    plt.xlabel("Cantidad de Usuarios Únicos", fontsize=12)
    plt.ylabel("Paso del Flujo", fontsize=12)

    # Guardar el gráfico como imagen
    output_image_path = "C:/Users/under/Pycharm-Projects/TelefonicaChallenge/data/funnel_plot.png"
    plt.tight_layout()
    plt.savefig(output_image_path)
    print(f"Gráfico guardado en {output_image_path}")

    # Mostrar el gráfico
    plt.show()


# Llamar a la función para graficar el embudo
plot_funnel(funnel, page_view_count)
