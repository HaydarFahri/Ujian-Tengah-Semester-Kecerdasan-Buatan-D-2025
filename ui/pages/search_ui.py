import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from src.algorithms.search_algo import SearchEngine
from data.graph_repository import JAVA_MAP, CITY_COORDS, generate_heuristics

def calculate_path_cost(graph, path):
    """Menghitung total jarak (KM) dari jalur."""
    total_cost = 0
    if not path or len(path) < 2:
        return 0
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        neighbors = graph.get(u, [])
        for neighbor, cost in neighbors:
            if neighbor == v:
                total_cost += cost
                break
    return total_cost

def render_map(graph_data, path=None):
    """Visualisasi Peta Jawa Lengkap."""
    G = nx.Graph()
    
    # Bangun Graph
    for city, neighbors in graph_data.items():
        if city in CITY_COORDS: 
            G.add_node(city, pos=CITY_COORDS[city])
            for neighbor, cost in neighbors:
                if neighbor in CITY_COORDS:
                    G.add_edge(city, neighbor, weight=cost)
            
    pos = nx.get_node_attributes(G, 'pos')
    
    # Canvas Besar agar semua kota muat
    fig, ax = plt.subplots(figsize=(16, 8)) 
    
    # Gambar Edge
    nx.draw_networkx_edges(G, pos, edge_color='#95a5a6', alpha=0.4, width=1, ax=ax)
    
    # Gambar Node
    nx.draw_networkx_nodes(G, pos, node_color='#3498db', node_size=150, edgecolors='white', linewidths=1, ax=ax)
    
    # Label Kota (Font kecil 6pt agar muat)
    label_pos = {k: (v[0], v[1] + 0.3) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, font_size=6, font_weight='bold', ax=ax)
    
    # Highlight Jalur
    if path:
        valid_path = [city for city in path if city in CITY_COORDS]
        if len(valid_path) > 1:
            path_edges = list(zip(valid_path, valid_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#e74c3c', width=3, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=valid_path, node_color='#e74c3c', node_size=200, ax=ax)
            
            # Label Start/End
            nx.draw_networkx_labels(G, {valid_path[0]: pos[valid_path[0]]}, labels={valid_path[0]: 'START'}, font_color='green', font_weight='bold', ax=ax)
            nx.draw_networkx_labels(G, {valid_path[-1]: pos[valid_path[-1]]}, labels={valid_path[-1]: 'FINISH'}, font_color='red', font_weight='bold', ax=ax)

    ax.set_title("Jaringan Kota & Jalur Transportasi Pulau Jawa", fontsize=14)
    ax.axis('off')
    st.pyplot(fig)

def render():
    st.markdown("## 🗺️ Java Island Pathfinder (Ultimate Edition)")
    st.markdown("Simulasi pencarian rute lintas provinsi (Banten - Jatim).")
    st.markdown("---")

    cities = sorted(JAVA_MAP.keys())

    # Tampilkan Peta
    with st.expander("📍 Lihat Peta Pulau Jawa Lengkap", expanded=True):
        render_map(JAVA_MAP)

    st.markdown("### ⚙️ Konfigurasi Perjalanan")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        start_node = st.selectbox("Asal", cities, index=cities.index("Merak"))
    with c2:
        goal_node = st.selectbox("Tujuan", cities, index=cities.index("Banyuwangi"))
    with c3:
        algo = st.selectbox("Algoritma", ["A* (Recommended)", "BFS", "DFS"])

    # --- FITUR HEURISTIK DINAMIS ---
    # Hitung heuristik baru berdasarkan tujuan yang dipilih user saat ini
    current_heuristics = generate_heuristics(goal_node)
    
    # Inisialisasi Engine dengan heuristik dinamis tersebut
    engine = SearchEngine(JAVA_MAP, current_heuristics)

    run_search = st.button("🚀 Mulai Navigasi", type="primary", use_container_width=True)

    if run_search:
        path, log, cost = None, [], 0
        
        if algo.startswith("BFS"):
            path, log = engine.bfs(start_node, goal_node)
            cost = calculate_path_cost(JAVA_MAP, path)
        elif algo.startswith("DFS"):
            path, log = engine.dfs(start_node, goal_node)
            cost = calculate_path_cost(JAVA_MAP, path)
        else: # A*
            path, log, cost = engine.a_star(start_node, goal_node)

        st.markdown("---")
        if path:
            st.success(f"**✅ Rute Tercepat Ditemukan!**")
            render_map(JAVA_MAP, path)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Jarak Tempuh", f"{cost} KM")
            c2.metric("Kota Dilewati", len(path))
            c3.metric("Effisiensi Node", f"{len(log)} checked")
            
            st.info(f"**Rute Lengkap:** {' ➝ '.join(path)}")
            with st.expander("Analisis Log Algoritma"):
                st.write(log)
        else:
            st.error("❌ Tidak ada jalur yang tersedia antar kota ini.")