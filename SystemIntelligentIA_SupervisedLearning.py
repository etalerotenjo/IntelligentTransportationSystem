import networkx as nx
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error


class SistemaTransporteInteligente:
    def __init__(self, grafo: nx.Graph):
        self.grafo = grafo
        self.modelo = None
        self.columnas_entrenamiento = []  # Guardamos las columnas originales

    def entrenar_modelo_desde_url(self, url_csv: str):
        try:
            df = pd.read_csv(url_csv)
            df = pd.get_dummies(df, columns=["origen", "destino"])

            X = df.drop(columns=["tiempo_viaje"])
            y = df["tiempo_viaje"]

            self.columnas_entrenamiento = X.columns.tolist()  # Guardamos las columnas exactas

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            self.modelo = DecisionTreeRegressor()
            self.modelo.fit(X_train, y_train)

            y_pred = self.modelo.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            print(f"✅ Modelo entrenado correctamente. MSE: {mse:.2f}")
        except Exception as e:
            print(f"❌ Error al leer o entrenar desde la URL: {e}")

    def predecir_tiempo(self, origen: str, destino: str):
        if self.modelo is None:
            print("⚠️ El modelo no ha sido entrenado aún.")
            return

        # Creamos un DataFrame con las columnas usadas en el entrenamiento
        data = {col: 0 for col in self.columnas_entrenamiento}

        origen_key = f"origen_{origen}"
        destino_key = f"destino_{destino}"

        if origen_key not in data or destino_key not in data:
            print("⚠️ El origen o destino no estaban en los datos de entrenamiento.")
            return

        data[origen_key] = 1
        data[destino_key] = 1

        df_input = pd.DataFrame([data])
        prediccion = self.modelo.predict(df_input)[0]
        print(f"🕒 Tiempo estimado de viaje de {origen} a {destino}: {prediccion:.2f} minutos")



# Grafo de ejemplo
G = nx.Graph()
G.add_weighted_edges_from([
    ("Estación A", "Estación B", 5),
    ("Estación B", "Estación C", 3),
    ("Estación C", "Estación D", 2),
    ("Estación A", "Estación D", 10),
    ("Estación B", "Estación D", 7),
    ("Estación C", "Estación E", 4),
    ("Estación E", "Estación F", 6)
], weight='peso')

G.add_node("Estación X")  # Estación sin conexión

# Ejecutar
if __name__ == "__main__":
    sistema = SistemaTransporteInteligente(G)

    # 🔗 Reemplaza esta URL por la tuya
    url = "https://raw.githubusercontent.com/etalerotenjo/IntelligentTransportationSystem/refs/heads/main/rutas_historicas.csv"

    sistema.entrenar_modelo_desde_url(url)
    sistema.predecir_tiempo("Estación A", "Estación D")