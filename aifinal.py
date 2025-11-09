#Muhammad Fikri Bagaswara_101022300115_EL4705_Kecerdasan Buatan Tugas 1
import heapq   # modul bawaan Python untuk struktur data priority queue (heap), digunakan agar selalu dapat mengambil node dengan nilai f terkecil dengan efisien

# Representasi Graph dengan dictionary of dictionary
class Graph:
    def __init__(self):
        # self.edges menyimpan struktur adjacency list yang juga mencakup cost antar node
        # contoh: { 'S': {'A':1, 'D':2}, ... } berarti dari node S bisa ke A dengan cost 1 dan ke D dengan cost 2
        self.edges = {}   

        # self.h menyimpan nilai heuristic (h(n)) untuk setiap node
        # heuristic ini biasanya berupa perkiraan jarak ke goal (semakin kecil semakin dekat)
        self.h = {}       

    def neighbors(self, node):
        # Fungsi untuk mengembalikan semua tetangga dari node tertentu (beserta cost-nya)
        # misalnya neighbors('S') -> {'A':1, 'D':2}
        return self.edges[node]  

    def cost(self, from_node, to_node):
        # Fungsi untuk mengambil nilai cost dari satu node ke node lainnya
        # misalnya cost('S','A') -> 1
        return self.edges[from_node][to_node]  


# Implementasi algoritma A* Search
def a_star_search(graph, start, goal):
    # open_list digunakan untuk menyimpan node yang akan dieksplorasi
    # setiap elemen berisi tuple (f, g, node, path)
    # f = g + h → total perkiraan biaya sampai goal
    # g = total cost aktual sejauh ini
    # path = lintasan yang sudah dilalui sampai node tersebut
    open_list = []  
    
    # Masukkan node awal ke open_list
    # f = h(start), g = 0 karena baru mulai dari titik awal
    heapq.heappush(open_list, (graph.h[start], 0, start, [start]))  

    # closed_set digunakan untuk menyimpan node yang sudah dikunjungi
    # tujuannya agar tidak diproses lagi (menghindari looping)
    closed_set = set()  

    step = 1
    while open_list:
        # Ambil node dengan nilai f terkecil dari open_list (karena priority queue)
        f, g, current, path = heapq.heappop(open_list)

        # Jika node sudah pernah dikunjungi, maka dilewati saja
        if current in closed_set:
            continue
        closed_set.add(current)

        # === Debug print untuk menampilkan langkah-langkah proses pencarian ===
        print(f"Langkah {step}: Expand {current}")
        print(f"  g(n) = {g}, h(n) = {graph.h[current]}, f(n) = {f}")
        print(f"  Path sejauh ini: {path}")
        print("  Open list:", [(n, "f="+str(fx)) for fx,_,n,_ in open_list])
        print("  Closed set:", closed_set)
        print("-"*50)
        step += 1
        # ======================================================================

        # Jika node saat ini adalah goal, maka pencarian selesai
        # Kembalikan path (lintasan terbaik) dan total cost-nya
        if current == goal:
            return path, g

        # Jika belum sampai goal, maka expand semua tetangga dari node saat ini
        for neighbor in graph.neighbors(current):
            # Hitung g baru (biaya aktual dari start ke neighbor)
            new_g = g + graph.cost(current, neighbor)    

            # Hitung f baru (total biaya perkiraan = g + h)
            new_f = new_g + graph.h[neighbor]           

            # Masukkan tetangga ke open_list dengan path yang diperbarui
            heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

    # Jika semua kemungkinan sudah dicoba tapi tidak sampai goal
    # maka dianggap tidak ada solusi yang ditemukan
    return None, float('inf')


# Main program
if __name__ == "__main__":
    graph = Graph()
    
    # Definisi edges sesuai dengan ilustrasi graph
    # Setiap node memiliki daftar tetangga dan bobot cost-nya
    # Misalnya: dari 'S' bisa ke 'A' dengan cost 1, dan ke 'D' dengan cost 2
    graph.edges = {
        'S': {'A': 1, 'D': 2},
        'A': {'B': 1},
        'D': {'B': 1, 'E': 3},
        'B': {'C': 2, 'E': 1},
        'C': {},        # Node C tidak memiliki successor (buntu)
        'E': {'G': 3},  # Dari E bisa langsung ke G
        'G': {}         # Node G adalah goal, jadi tidak punya tetangga lagi
    }

    # Definisi nilai heuristic h(n) untuk setiap node
    # Nilai ini bersifat "perkiraan" jarak dari node tersebut ke goal
    # Semakin kecil nilainya berarti semakin dekat ke tujuan
    graph.h = {
        'S': 7,
        'A': 9,
        'B': 4,
        'C': 2,
        'D': 5,
        'E': 3,
        'G': 0
    }

    # Jalankan algoritma A* Search dari node 'S' menuju node 'G'
    path, cost = a_star_search(graph, 'S', 'G')

    # Tampilkan hasil akhir setelah pencarian selesai
    print("\n=== Hasil Akhir ===")
    print("Path ditemukan:", path)
    print("Total cost:", cost)
