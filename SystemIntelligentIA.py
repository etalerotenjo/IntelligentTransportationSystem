import networkx as nx

class SistemaTransporte:
    def __init__(self, grafo: nx.Graph):
        self.grafo = grafo
    
    def encontrar_mejor_ruta(self, origen: str, destino: str):
        try:
            ruta_optima = nx.shortest_path(self.grafo, source=origen, target=destino, weight='peso')
            costo_total = nx.shortest_path_length(self.grafo, source=origen, target=destino, weight='peso')
            print(f"Mejor ruta de {origen} a {destino}: {ruta_optima} con un costo total de {costo_total}")
        except nx.NetworkXNoPath:
            print(f"No hay ruta disponible entre {origen} y {destino}.")
        except KeyError:
            print(f"Uno o ambos nodos ({origen}, {destino}) no existen en el sistema.")

    def sugerir_destinos(self, origen: str):
        if origen in self.grafo:
            destinos = list(self.grafo.neighbors(origen))
            print(f"Desde {origen} puedes viajar a: {', '.join(destinos)}")
        else:
            print(f"La estación {origen} no existe en el sistema de transporte.")

# Creación del grafo del sistema de transporte
G = nx.Graph()
G.add_weighted_edges_from([
    ("Estación A", "Estación B", 5),
    ("Estación B", "Estación C", 3),
    ("Estación C", "Estación D", 2),
    ("Estación A", "Estación D", 10),
    ("Estación B", "Estación D", 7),
    (# The line `"Estación C", "Estación E"` is adding a weighted edge to the graph `G` in the
    # SistemaTransporte class. This edge connects "Estación C" to "Estación E" with a weight of 4
    # units. In the context of a transportation system, this edge represents a direct connection or
    # route between these two stations with a cost or distance of 4 units. This information is used
    # by the `encontrar_mejor_ruta` method to calculate the shortest path and total cost between
    # stations in the system.
    "Estación C", "Estación E", 4),
    ("Estación E", "Estación F", 6)
], weight='peso')

# Instanciamos el sistema de transporte
if __name__ == "__main__":
    sistema = SistemaTransporte(G)
    sistema.encontrar_mejor_ruta("Estación A", "Estación X")
    sistema.sugerir_destinos("Estación C")