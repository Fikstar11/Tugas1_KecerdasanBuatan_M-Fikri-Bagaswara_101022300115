import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.edges = {}
        self.h = {}

    def neighbors(self, node):
        return self.edges[node]

    def cost(self, from_node, to_node):
        return self.edges[from_node][to_node]

def a_star_search(graph, start, goal):
    open_list = []
    heapq.heappush(open_list, (graph.h[start], 0, start, [start]))  # (f, g, node, path)
    closed_set = set()

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current in closed_set:
            continue
        closed_set.add(current)

        if current == goal:
            return path, g

        for neighbor in graph.neighbors(current):
            new_g = g + graph.cost(current, neighbor)
            new_f = new_g + graph.h[neighbor]
            heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

    return None, float('inf')

if __name__ == "__main__":
    graph = Graph()
    
    # Graph sesuai gambar (tanpa C → G)
    graph.edges = {
        'S': {'A': 1, 'D': 2},
        'A': {'B': 1},
        'D': {'B': 1, 'E': 3},
        'B': {'C': 2, 'E': 1},
        'C': {},        
        'E': {'G': 3},
        'G': {}
    }

    graph.h = {
        'S': 7,
        'A': 9,
        'B': 4,
        'C': 2,
        'D': 5,
        'E': 3,
        'G': 0
    }

    # Jalankan A*
    path, cost = a_star_search(graph, 'S', 'G')
    print("Path ditemukan:", path)
    print("Total cost:", cost)

    # Visualisasi pakai networkx
    G = nx.DiGraph()
    for node, neighbors in graph.edges.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)  # layout posisi node
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightgreen", font_size=10, font_weight="bold")

    # Tambah label bobot
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Warnai path hasil A* dengan merah
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3)

    plt.title(f"Path A* dari {path[0]} ke {path[-1]} (Cost = {cost})")
    plt.show()
