import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from src.algorithms.fuzzy_logic import TippingSystem

def render():
    st.markdown("## 🍽️ Smart Restaurant Tip Advisor")
    st.markdown("Sistem pakar penentuan tip berbasis Fuzzy Logic.")
    st.markdown("---")

    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.subheader("📝 Penilaian Pelanggan")
        
        food_input = st.slider("⭐⭐⭐ Kualitas Makanan (0-10)", 0.0, 10.0, 7.0, 0.1)
        st.caption("0 = Sangat Buruk, 10 = Sempurna")
        
        service_input = st.slider("⭐⭐⭐ Kualitas Layanan (0-10)", 0.0, 10.0, 3.0, 0.1)
        st.caption("0 = Sangat Lambat/Kasar, 10 = Sangat Ramah/Cepat")
        
        calculate = st.button("💡 Hitung Rekomendasi Tip", type="primary")

    if calculate or st.session_state.get('fuzzy_result') is None:
        try:
            system = TippingSystem()
            result = system.compute(food_input, service_input)
            st.session_state['fuzzy_result'] = result
        except Exception as e:
            st.error(f"Error: {e}"); st.stop()

    res = st.session_state['fuzzy_result']

    with col_right:
        if res is not None:
            st.subheader("📊 Hasil Analisis & Rekomendasi")
            
            # Metric dengan Emoji
            c1, c2 = st.columns(2)
            c1.metric("Rekomendasi Tip", f"{res['centroid']:.2f}%", delta="Final Result")
            
            # Tentukan kategori berdasarkan hasil
            kat = "💰 Rendah" if res['centroid'] < 5 else "💰💰 Sedang" if res['centroid'] < 15 else "💰💰💰 Tinggi"
            c2.metric("Kategori", kat)

            # Visualisasi Grafik Premium
            x, y_low, y_high, y_agg = res['plot_data']
            
            # Menggunakan Style 'ggplot' agar lebih modern
            plt.style.use('ggplot')
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Plot Area dengan warna tematik
            ax.fill_between(x, y_low, color='#e74c3c', alpha=0.5, label=f'Tip Rendah (Rule 1: {res["alpha"][0]:.2f})')
            ax.fill_between(x, y_high, color='#2ecc71', alpha=0.5, label=f'Tip Tinggi (Rule 2: {res["alpha"][1]:.2f})')
            
            # Garis Aggregasi
            ax.plot(x, y_agg, color='#34495e', linewidth=2.5, label='Hasil Agregasi')
            
            # Garis Centroid
            ax.axvline(res['centroid'], color='#f1c40f', linestyle='--', linewidth=3, label=f'Centroid: {res["centroid"]:.2f}%')
            
            ax.set_title("Visualisasi Logika Fuzzy (Area Defuzzifikasi)", fontsize=12, fontweight='bold')
            ax.set_xlabel("Persentase Tip (%)", fontweight='bold')
            ax.set_ylabel("Derajat Keanggotaan (μ)", fontweight='bold')
            ax.legend(loc='upper right', frameon=True)
            ax.set_xlim(0, 20)
            ax.set_ylim(0, 1.1)
            
            st.pyplot(fig)
            
            # Penjelasan
            st.info(f"""
            **Mengapa hasilnya demikian?**
            Sistem menilai bahwa kondisi saat ini lebih condong ke **Rule 1 (Tip Rendah)** dengan kekuatan {res['alpha'][0]:.2f}, 
            dibandingkan **Rule 2 (Tip Tinggi)** yang kekuatannya {res['alpha'][1]:.2f}. 
            Titik tengah (centroid) dari area yang terbentuk adalah **{res['centroid']:.2f}%**.
            """)
        else:
            st.warning("Silakan berikan penilaian dan klik tombol hitung.")