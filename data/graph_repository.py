import math

# ==========================================
# 1. KOORDINAT KOTA (Mapping Visual & Kalkulasi)
# ==========================================
# Menggunakan sistem koordinat kartesius yang 'direnggangkan' (Stretched)
# agar visualisasi di layar komputer tidak bertumpuk, namun posisi relatifnya tetap benar secara geografis.
# Format: 'Kota': (X, Y) -> X=Barat-Timur, Y=Utara-Selatan

CITY_COORDS = {
    # --- BANTEN & DKI ---
    'Merak': (0, 10), 'Cilegon': (2, 10), 'Serang': (5, 9), 'Pandeglang': (4, 5),
    'Tangerang': (10, 9), 'Jakarta': (15, 10),
    
    # --- JAWA BARAT ---
    'Bekasi': (18, 10), 'Depok': (15, 7), 'Bogor': (15, 5), 'Sukabumi': (16, 2),
    'Cianjur': (20, 3), 'Karawang': (22, 11), 'Purwakarta': (24, 9),
    'Bandung': (25, 5), 'Sumedang': (28, 6), 'Garut': (28, 3),
    'Tasikmalaya': (32, 3), 'Ciamis': (35, 3), 'Banjar': (37, 2),
    'Indramayu': (32, 13), 'Cirebon': (38, 11), 'Kuningan': (38, 9),
    
    # --- JAWA TENGAH (Utara) ---
    'Brebes': (42, 10), 'Tegal': (44, 10), 'Pemalang': (48, 10),
    'Pekalongan': (52, 9), 'Kendal': (58, 9), 'Semarang': (62, 9),
    'Demak': (65, 10), 'Kudus': (68, 10), 'Pati': (72, 10), 'Rembang': (76, 10),
    
    # --- JAWA TENGAH (Tengah & Selatan) ---
    'Purwokerto': (46, 5), 'Purbalingga': (49, 6), 'Banjarnegara': (52, 6),
    'Wonosobo': (55, 6), 'Temanggung': (58, 7), 'Magelang': (60, 5),
    'Salatiga': (62, 7), 'Boyolali': (65, 6), 'Solo': (68, 6),
    'Sragen': (72, 7), 'Wonogiri': (70, 4),
    'Kebumen': (55, 2), 'Purworejo': (58, 2), 'Yogyakarta': (62, 1),
    'Klaten': (65, 3),
    
    # --- JAWA TIMUR (Barat & Utara) ---
    'Cepu': (80, 9), 'Bojonegoro': (85, 9), 'Tuban': (85, 11),
    'Lamongan': (90, 9), 'Gresik': (93, 10), 'Surabaya': (95, 9),
    'Sidoarjo': (95, 7), 'Bangil': (97, 6), 'Pasuruan': (100, 6),
    'Probolinggo': (105, 6), 'Situbondo': (115, 7),
    
    # --- JAWA TIMUR (Tengah & Selatan) ---
    'Ngawi': (76, 6), 'Magetan': (78, 4), 'Madiun': (80, 5),
    'Ponorogo': (80, 2), 'Nganjuk': (84, 5), 'Jombang': (88, 6),
    'Mojokerto': (92, 7), 'Kediri': (86, 3), 'Blitar': (90, 1),
    'Malang': (95, 3), 'Lumajang': (105, 3), 'Jember': (112, 3),
    'Banyuwangi': (120, 5)
}

# ==========================================
# 2. GRAPH JALUR KOTA (REAL CONNECTIONS)
# ==========================================
JAVA_MAP = {
    # Banten - DKI
    'Merak': [('Cilegon', 15)],
    'Cilegon': [('Merak', 15), ('Serang', 25)],
    'Serang': [('Cilegon', 25), ('Pandeglang', 20), ('Tangerang', 60)],
    'Pandeglang': [('Serang', 20), ('Rangkasbitung', 25)], # Rangkas optional
    'Tangerang': [('Serang', 60), ('Jakarta', 30)],
    'Jakarta': [('Tangerang', 30), ('Bekasi', 25), ('Depok', 30), ('Bogor', 50)],
    
    # Jabar Barat
    'Bekasi': [('Jakarta', 25), ('Karawang', 40)],
    'Depok': [('Jakarta', 30), ('Bogor', 25)],
    'Bogor': [('Jakarta', 50), ('Depok', 25), ('Sukabumi', 60), ('Cianjur', 50)],
    'Sukabumi': [('Bogor', 60), ('Cianjur', 30)],
    'Cianjur': [('Bogor', 50), ('Sukabumi', 30), ('Bandung', 65)],
    'Karawang': [('Bekasi', 40), ('Purwakarta', 30), ('Indramayu', 100)],
    'Purwakarta': [('Karawang', 30), ('Bandung', 60)],
    
    # Bandung Raya & Priangan
    'Bandung': [('Cianjur', 65), ('Purwakarta', 60), ('Sumedang', 45), ('Garut', 60)],
    'Sumedang': [('Bandung', 45), ('Cirebon', 80)],
    'Garut': [('Bandung', 60), ('Tasikmalaya', 55)],
    'Tasikmalaya': [('Garut', 55), ('Ciamis', 20)],
    'Ciamis': [('Tasikmalaya', 20), ('Banjar', 25)],
    'Banjar': [('Ciamis', 25), ('Purwokerto', 90), ('Cirebon', 110)], # Jalur Banjar-Cirebon via Kuningan
    
    # Pantura Jabar-Jateng
    'Indramayu': [('Karawang', 100), ('Cirebon', 55)],
    'Cirebon': [('Sumedang', 80), ('Indramayu', 55), ('Kuningan', 35), ('Brebes', 60)],
    'Kuningan': [('Cirebon', 35), ('Banjar', 90)],
    
    # Jateng (Utara)
    'Brebes': [('Cirebon', 60), ('Tegal', 15), ('Purwokerto', 80)],
    'Tegal': [('Brebes', 15), ('Pemalang', 30), ('Purwokerto', 90)],
    'Pemalang': [('Tegal', 30), ('Pekalongan', 35), ('Purbalingga', 60)],
    'Pekalongan': [('Pemalang', 35), ('Kendal', 50)],
    'Kendal': [('Pekalongan', 50), ('Semarang', 30)],
    'Semarang': [('Kendal', 30), ('Demak', 30), ('Salatiga', 50), ('Magelang', 70)],
    'Demak': [('Semarang', 30), ('Kudus', 25)],
    'Kudus': [('Demak', 25), ('Pati', 25)],
    'Pati': [('Kudus', 25), ('Rembang', 35)],
    'Rembang': [('Pati', 35), ('Tuban', 95)],
    
    # Jateng (Selatan & Tengah)
    'Purwokerto': [('Brebes', 80), ('Tegal', 90), ('Purbalingga', 20), ('Kebumen', 70)],
    'Purbalingga': [('Purwokerto', 20), ('Pemalang', 60), ('Banjarnegara', 30)],
    'Banjarnegara': [('Purbalingga', 30), ('Wonosobo', 30)],
    'Wonosobo': [('Banjarnegara', 30), ('Temanggung', 40), ('Purworejo', 50)],
    'Temanggung': [('Wonosobo', 40), ('Magelang', 25), ('Salatiga', 40)],
    'Magelang': [('Semarang', 70), ('Temanggung', 25), ('Yogyakarta', 45)],
    'Salatiga': [('Semarang', 50), ('Temanggung', 40), ('Boyolali', 25)],
    'Boyolali': [('Salatiga', 25), ('Solo', 30)],
    'Solo': [('Boyolali', 30), ('Sragen', 35), ('Klaten', 30), ('Wonogiri', 35)],
    'Klaten': [('Solo', 30), ('Yogyakarta', 30)],
    'Yogyakarta': [('Magelang', 45), ('Klaten', 30), ('Purworejo', 60), ('Wonogiri', 70)],
    'Purworejo': [('Kebumen', 45), ('Wonosobo', 50), ('Yogyakarta', 60)],
    'Kebumen': [('Purwokerto', 70), ('Purworejo', 45)],
    'Sragen': [('Solo', 35), ('Ngawi', 50)],
    'Wonogiri': [('Solo', 35), ('Yogyakarta', 70), ('Ponorogo', 60)],
    
    # Jatim (Barat)
    'Ngawi': [('Sragen', 50), ('Madiun', 30), ('Bojonegoro', 60)],
    'Madiun': [('Ngawi', 30), ('Magetan', 25), ('Nganjuk', 40), ('Ponorogo', 30)],
    'Magetan': [('Madiun', 25)],
    'Ponorogo': [('Madiun', 30), ('Wonogiri', 60), ('Trenggalek', 40)], # Trenggalek optional
    'Nganjuk': [('Madiun', 40), ('Jombang', 40), ('Kediri', 30)],
    'Kediri': [('Nganjuk', 30), ('Jombang', 35), ('Blitar', 45), ('Malang', 80)],
    'Blitar': [('Kediri', 45), ('Malang', 50)],
    
    # Jatim (Pantura & Timur)
    'Tuban': [('Rembang', 95), ('Bojonegoro', 40), ('Lamongan', 50)],
    'Bojonegoro': [('Ngawi', 60), ('Tuban', 40), ('Lamongan', 60)],
    'Lamongan': [('Tuban', 50), ('Bojonegoro', 60), ('Gresik', 30)],
    'Gresik': [('Lamongan', 30), ('Surabaya', 20)],
    'Surabaya': [('Gresik', 20), ('Sidoarjo', 25), ('Mojokerto', 50)],
    'Sidoarjo': [('Surabaya', 25), ('Bangil', 20)],
    'Mojokerto': [('Surabaya', 50), ('Jombang', 25), ('Pasuruan', 55)],
    'Jombang': [('Nganjuk', 40), ('Kediri', 35), ('Mojokerto', 25)],
    'Bangil': [('Sidoarjo', 20), ('Pasuruan', 15)],
    'Pasuruan': [('Bangil', 15), ('Mojokerto', 55), ('Malang', 50), ('Probolinggo', 40)],
    'Malang': [('Pasuruan', 50), ('Blitar', 50), ('Kediri', 80), ('Lumajang', 70)],
    'Probolinggo': [('Pasuruan', 40), ('Lumajang', 50), ('Situbondo', 95)],
    'Lumajang': [('Malang', 70), ('Probolinggo', 50), ('Jember', 60)],
    'Situbondo': [('Probolinggo', 95), ('Banyuwangi', 90)],
    'Jember': [('Lumajang', 60), ('Banyuwangi', 100)],
    'Banyuwangi': [('Situbondo', 90), ('Jember', 100)]
}

# ==========================================
# 3. FUNGSI HEURISTIK DINAMIS
# ==========================================
def generate_heuristics(goal_city):
    """
    Menghitung jarak heuristik (Euclidean Distance) dari SEMUA kota
    menuju kota TUJUAN (Goal) yang dipilih user.
    
    Ini membuat A* bisa bekerja dinamis, tidak hanya ke satu tujuan.
    """
    if goal_city not in CITY_COORDS:
        return {}
    
    goal_x, goal_y = CITY_COORDS[goal_city]
    heuristics = {}
    
    for city, (x, y) in CITY_COORDS.items():
        # Rumus Pythagoras sederhana (Euclidean)
        # Skala dikali 10 agar mendekati KM nyata (Estimasi kasar)
        distance = math.sqrt((x - goal_x)**2 + (y - goal_y)**2) * 10
        heuristics[city] = distance
        
    return heuristics