import streamlit as st

def render():
    # Header Section
    st.title("🚀 UTS Kecerdasan Buatan 2025")
    st.markdown("### Haydar Fahri Alaudin | Teknik Informatika")
    st.markdown("---")

    # Introduction
    st.info("""
    Selamat datang di **Nexus Optima AI Dashboard**. 
    Aplikasi ini dibangun untuk memenuhi Tugas UTS Kecerdasan Buatan dengan pendekatan **Software Engineering Modular**.
    """)

    # Module Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧩 Soal Fuzzy Logic")
        st.markdown("""
        Sistem Pakar penentuan **Tip Restoran** menggunakan metode **Mamdani**.
        * **Input:** Kualitas Makanan & Layanan.
        * **Output:** Persentase Tip.
        * **Fitur:** Grafik Visualisasi Area Fuzzy & Centroid.
        """)
        if st.button("Buka Modul Fuzzy ➡️"):
            st.session_state['page'] = "Fuzzy Logic"
            st.rerun()

    with col2:
        st.markdown("### 🗺️ Java Pathfinder") # Ganti Judul
        st.markdown("""
        Agen pencari rute antar kota di **Pulau Jawa** (Merak - Banyuwangi).
        * **Algoritma:** BFS, DFS, dan A* (A-Star).
        * **Data:** Graph Kota Utama & Jarak KM.
        * **Fitur:** Visualisasi Peta Interaktif.
        """)
        if st.button("Buka Peta Jawa ➡️"): # Ganti Tombol
            st.session_state['page'] = "Searching"
            st.rerun()
            
    # Footer
    st.markdown("---")
    st.caption("© 2025 Haydar Fahri Alaudin - Universitas Islam Sultan Agung")