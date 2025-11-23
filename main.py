import streamlit as st
from config.settings import APP_CONFIG

# Konfigurasi Halaman (Ambil dari Config)
st.set_page_config(
    page_title=f"{APP_CONFIG['page_title']} - {APP_CONFIG['student_name']}",
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout']
)

from ui.pages import home, fuzzy_ui, search_ui

# Inisialisasi Session State
if 'page' not in st.session_state:
    st.session_state['page'] = "Home"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🤖 Menu Utama")
    st.markdown(f"**{APP_CONFIG['student_name']}**")
    st.caption(f"NIM: {APP_CONFIG['student_nim']}")
    st.caption(APP_CONFIG['university'])
    st.markdown("---")
    
    nav_options = ["Home", "Fuzzy Logic (Soal 3)", "Searching (Soal 1&2)"]
    selection = st.radio("Pilih Modul:", nav_options, index=nav_options.index(st.session_state['page']))
    
    if selection != st.session_state['page']:
        st.session_state['page'] = selection
        st.rerun()

# --- ROUTING ---
if st.session_state['page'] == "Home":
    home.render()
elif st.session_state['page'] == "Fuzzy Logic (Soal 3)":
    fuzzy_ui.render()
elif st.session_state['page'] == "Searching (Soal 1&2)":
    search_ui.render()