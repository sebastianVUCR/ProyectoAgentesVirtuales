import json
import pandas as pd

# 1. Cargar el contenido desde el archivo local 'data.json'
try:
    with open('datos_finales.json', 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
except FileNotFoundError:
    print("Error: El archivo 'data.json' no se encuentra en el mismo directorio que este script.")
    exit()

# 2. Extraer el diccionario interno de respuestas
respuestas = data["respuestas_cuestionarios"]

# 3. Convertir a DataFrame de Pandas (usando las llaves del JSON como filas)
df = pd.DataFrame.from_dict(respuestas, orient='index')

# 4. Guardar la llave única (ID) como una columna explícita llamada 'usuario_id'
df.index.name = 'usuario_id'
df.reset_index(inplace=True)

# 5. Exportar a CSV con codificación utf-8-sig para compatibilidad con Excel
df.to_csv("datos_finales.csv", index=False, encoding="utf-8-sig")

print("¡Archivo 'resultado_encuesta.csv' generado con éxito a partir de 'data.json'!")