import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Função para converter um grafo dirigido em um MultiGraph não direcionado
# Mantém todos os nós, arestas e atributos do grafo original
def to_undirected_multigraph(G):
    H = nx.MultiGraph()
    # Copiar nós e seus atributos
    for n, data in G.nodes(data=True):
        H.add_node(n, **data)

    # Copiar arestas e seus atributos
    for u, v, data in G.edges(data=True):
        H.add_edge(u, v, **data)

    # Copiar atributos de grafo
    H.graph.update(G.graph)
    return H

# Definir local de interesse: Natal, RN, Brasil
place = "Natal, Rio Grande do Norte, Brazil"
# Baixar grafo de ruas para veículos (tipo 'drive')
G = ox.graph_from_place(place, network_type='drive')

# Converter para grafo não direcionado, permitindo múltiplas arestas
G_undirected = to_undirected_multigraph(G)

# Buscar POIs com tag 'library' (biblioteca)
tags = {'amenity': 'library'}
pois = ox.features.features_from_place(place, tags=tags)

# Extrair coordenadas dos POIs, tratando pontos e polígonos
library_points = []
for idx, row in pois.iterrows():
    if row.geometry.geom_type == 'Point':
        library_points.append((row.geometry.y, row.geometry.x))
    else:
        # Para polígonos, usar o centroide
        library_points.append((row.geometry.centroid.y, row.geometry.centroid.x))

# Se não encontrar bibliotecas, tenta buscar escolas como fallback
if not library_points:
    print("Nenhuma biblioteca encontrada. Tentando escolas...")
    tags = {'amenity': 'school'}
    pois = ox.features.features_from_place(place, tags=tags)
    for idx, row in pois.iterrows():
        if row.geometry.geom_type == 'Point':
            library_points.append((row.geometry.y, row.geometry.x))
        else:
            library_points.append((row.geometry.centroid.y, row.geometry.centroid.x))
    if not library_points:
        # Se ainda vazio, interrompe com erro
        raise ValueError("Nenhum POI encontrado para as categorias tentadas.")

# Separar latitudes e longitudes para busca dos nós mais próximos
latitudes = [lp[0] for lp in library_points]
longitudes = [lp[1] for lp in library_points]
# Encontrar nós de grafo mais próximos de cada POI
library_nodes = ox.distance.nearest_nodes(G_undirected, X=longitudes, Y=latitudes)
# Remover duplicatas de nós
library_nodes = list(set(library_nodes))

# Garantir POIs suficientes para cálculo de MST
if len(library_nodes) < 2:
    raise ValueError("POIs insuficientes para criar um MST (menos de 2 pontos).")

# Criar grafo de interesse conectando cada par de POIs
G_interest = nx.Graph()
for i in range(len(library_nodes)):
    for j in range(i+1, len(library_nodes)):
        # Caminho mais curto entre os dois nós, ponderado por 'length'
        route = nx.shortest_path(G_undirected, library_nodes[i], library_nodes[j], weight='length')
        # Calcular comprimento total da rota
        route_length = 0
        for k in range(len(route)-1):
            # MultiGraph: seleciona a primeira aresta [0]
            route_length += G_undirected[route[k]][route[k+1]][0]['length']
        # Adicionar aresta ao grafo de interesse com peso igual à distância da rota
        G_interest.add_edge(library_nodes[i], library_nodes[j], weight=route_length)

# Calcular as arestas do Minimum Spanning Tree (MST)
mst_edges = list(nx.minimum_spanning_edges(G_interest, data=True))
# Somar os pesos para obter comprimento total do MST
total_mst_length = sum(d['weight'] for _, _, d in mst_edges)
# Converter de metros para quilômetros
total_mst_km = total_mst_length / 1000
# Exibir resultado com duas casas decimais em quilômetros
print(f"Comprimento total do MST entre os POIs selecionados: {total_mst_km:.2f} km")

# Reconstruir as rotas completas dos pares conectados pelo MST
mst_routes = []
for (u, v, d) in mst_edges:
    route = nx.shortest_path(G_undirected, u, v, weight='length')
    mst_routes.append(route)

# --- Plotagem ---
# Gerar figura e eixos para matplotlib
fig, ax = plt.subplots(figsize=(10, 10))
# Desenhar grafo base em cinza
ox.plot_graph(
    G_undirected,
    ax=ax,
    node_size=0,
    edge_color="gray",
    edge_linewidth=0.5,
    show=False,
    close=False,
)

# Destacar cada rota do MST em vermelho
for route in mst_routes:
    x = [G_undirected.nodes[n]['x'] for n in route]
    y = [G_undirected.nodes[n]['y'] for n in route]
    ax.plot(x, y, color='purple', linewidth=2, zorder=4)

# Plotar POIs (bibliotecas) em azul com borda preta
poi_x = [G_undirected.nodes[n]['x'] for n in library_nodes]
poi_y = [G_undirected.nodes[n]['y'] for n in library_nodes]
ax.scatter(poi_x, poi_y, c='pink', s=80, edgecolor='black', zorder=5)

# Título e ajustes finais
plt.title("MST entre POIs (bibliotecas) em Natal", fontsize=14)
ax.axis('off')  # remover eixos para melhor visualização
plt.tight_layout()
plt.show()