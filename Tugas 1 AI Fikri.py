import heapq   # modul bawaan Python untuk struktur data priority queue (heap)

# Representasi Graph dengan dictionary of dictionary
class Graph:
    def __init__(self):
        self.edges = {}   # adjacency list dengan cost, contoh: { 'S': {'A':1, 'D':2}, ... }
        self.h = {}       # heuristic value setiap node

    def neighbors(self, node):
        return self.edges[node]  # mengembalikan semua neighbor dari node tertentu

    def cost(self, from_node, to_node):
        return self.edges[from_node][to_node]  # ambil bobot/cost dari from_node ke to_node


# Implementasi algoritma A* Search
def a_star_search(graph, start, goal):
    open_list = []  
    # Simpan node dalam bentuk (f, g, node, path)

    heapq.heappush(open_list, (graph.h[start], 0, start, [start]))  # mulai dari start
    closed_set = set()  # set untuk menyimpan node yang sudah diexplore

    step = 1
    while open_list:
        # Ambil node dengan f paling kecil (priority queue)
        f, g, current, path = heapq.heappop(open_list)

        # Jika node sudah pernah dikunjungi, skip
        if current in closed_set:
            continue
        closed_set.add(current)

        # === Debug print untuk visualisasi langkah ===
        print(f"Langkah {step}: Expand {current}")
        print(f"  g(n) = {g}, h(n) = {graph.h[current]}, f(n) = {f}")
        print(f"  Path sejauh ini: {path}")
        print("  Open list:", [(n, "f="+str(fx)) for fx,_,n,_ in open_list])
        print("  Closed set:", closed_set)
        print("-"*50)
        step += 1
        # ============================================

        # Jika sampai ke goal → return path dan total cost
        if current == goal:
            return path, g

        # Expand semua tetangga node saat ini
        for neighbor in graph.neighbors(current):
            new_g = g + graph.cost(current, neighbor)    # update cost g
            new_f = new_g + graph.h[neighbor]           # hitung f = g + h
            heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

    # Jika tidak ada solusi
    return None, float('inf')


# Main program
if __name__ == "__main__":
    graph = Graph()
    
    # Definisi edges sesuai dengan gambar (C tidak punya successor langsung ke G)
    graph.edges = {
        'S': {'A': 1, 'D': 2},
        'A': {'B': 1},
        'D': {'B': 1, 'E': 3},
        'B': {'C': 2, 'E': 1},
        'C': {},        # C buntu, tidak menuju ke G
        'E': {'G': 3},
        'G': {}
    }

    # Definisi nilai heuristic h(n) untuk tiap node
    graph.h = {
        'S': 7,
        'A': 9,
        'B': 4,
        'C': 2,
        'D': 5,
        'E': 3,
        'G': 0
    }

    # Jalankan A* dari S ke G
    path, cost = a_star_search(graph, 'S', 'G')
    print("\n=== Hasil Akhir ===")
    print("Path ditemukan:", path)
    print("Total cost:", cost)
