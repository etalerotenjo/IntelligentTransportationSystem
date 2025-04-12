import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Cargar el archivo CSV desde la URL
url_csv = "https://media.githubusercontent.com/media/EL-BID/Matriz-Origen-Destino-Transporte-Publico/refs/heads/main/data/transacciones.csv"
df = pd.read_csv(url_csv)

# Verificar las primeras filas del dataset
print(df.head())

# Tomar una muestra de 1000 registros para reducir el tiempo de ejecución
df = df.sample(n=100, random_state=42)

# Verificar los valores nulos antes de procesar
print("Valores nulos por columna:")
print(df.isnull().sum())

# Asegurarnos de que las columnas necesarias no tengan valores nulos
df = df.dropna(subset=['lat', 'lon', 'hora'])

# Convertir la columna 'hora' a formato datetime
df['hora'] = pd.to_datetime(df['hora'], errors='coerce')

# Verificar que la conversión de 'hora' no haya generado valores nulos
print(f"Valores nulos en 'hora' después de la conversión: {df['hora'].isnull().sum()}")

# Si hay valores nulos en la columna 'hora', eliminarlos
df = df.dropna(subset=['hora'])

# Extraer la hora del día
df['hora_del_dia'] = df['hora'].dt.hour

# Seleccionar las características 'lat', 'lon', 'hora_del_dia'
X = df[['lat', 'lon', 'hora_del_dia']]

# Verificar que no haya valores nulos en X
print("Valores nulos en X (lat, lon, hora_del_dia):")
print(X.isnull().sum())

# Si todo está bien, proceder a estandarizar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar K-means con un número arbitrario de clusters (por ejemplo, 3 clusters)
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Ver los resultados de los clusters
print(df[['lat', 'lon', 'hora_del_dia', 'cluster']].head())

# Visualización de los clusters
plt.figure(figsize=(10, 6))
plt.scatter(df['lat'], df['lon'], c=df['cluster'], cmap='viridis', alpha=0.5)
plt.title('Clustering de Rutas por Latitud y Longitud')
plt.xlabel('Latitud')
plt.ylabel('Longitud')
plt.colorbar(label='Cluster')
plt.show()