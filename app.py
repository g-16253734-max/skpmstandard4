import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI ---
st.set_page_config(page_title="Sistem Pencerapan SMK Kinarut", layout="wide")

# DATABASE SENARAI (Diringkaskan untuk kod, anda boleh tambah lagi)
LIST_GURU = ["ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "ALDRIANA ANDREAS", "ZAINUDDIN BIN AG. JALIL"] # Tambah semua nama di sini
SUBJEK = ["BAHASA MELAYU", "BAHASA INGGERIS", "SAINS", "MATEMATIK", "SEJARAH"]
KELAS = [f"{i} ALPHA" for i in range(1,6)] + [f"{i} BETA" for i in range(1,6)]

# --- FUNGSI KIRA SKOR ---
def kira_skor_3(kriteria_list):
    count = sum(kriteria_list)
    if count == 3: return 4
    if count == 2: return 3
    if count == 1: return 2
    return 1

def kira_skor_4(kriteria_list):
    count = sum(kriteria_list)
    if count >= 3: return 4
    if count == 2: return 3
    if count == 1: return 2
    return 1

# --- SIDEBAR ---
st.sidebar.header("🔐 Akses Pentadbir")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")
pencerap = st.sidebar.text_input("Nama Pencerap:")
jawatan = st.sidebar.selectbox("Jawatan:", ["Pengetua", "PK", "Ketua Bidang", "Ketua Panitia"])
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

# --- UI UTAMA ---
st.title("📋 Sistem Pencerapan PdPc SMK Kinarut")
st.info("Sila tanda (✓) pada kriteria yang dilaksanakan oleh guru.")

# DATA ASAS
c1, c2, c3, c4 = st.columns(4)
guru_opt = c1.selectbox("Guru Dicerap:", LIST_GURU)
sub_opt = c2.selectbox("Subjek:", SUBJEK)
kls_opt = c3.selectbox("Kelas:", KELAS)
mod_opt = c4.selectbox("Mod:", ["Kendiri", "Pertama", "Kedua"])

# BORANG KRITERIA
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["4.1 Perancang", "4.2 Pengawal", "4.3 Pembimbing", "4.4 Pendorong", "4.5 Penilai", "4.6 Murid"])

with tab1:
    st.subheader("4.1.1 Perancangan PdPc")
    a411a = [st.checkbox(f"4.1.1a: {txt}", key=f"411a{i}") for i, txt in enumerate(["Aras Murid", "Masa", "Kurikulum"])]
    a411b = [st.checkbox(f"4.1.1b: {txt}", key=f"411b{i}") for i, txt in enumerate(["Kaedah Taksir", "Masa Taksir", "Kurikulum Taksir"])]
    a411c = [st.checkbox(f"4.1.1c: {txt}", key=f"411c{i}") for i, txt in enumerate(["BBM Berasaskan Aras", "BBM Ikut Masa", "BBM Ikut Kurikulum"])]

with tab2:
    st.subheader("4.2.1 Kawalan PdPc")
    a421 = [st.checkbox(f"4.2.1: {txt}", key=f"421{i}") for i, txt in enumerate(["Menepati Objektif", "Mengikut Aras", "Secara Berterusan"])]
    st.subheader("4.2.2 Kawalan Suasana")
    a422 = [st.checkbox(f"4.2.2: {txt}", key=f"422{i}") for i, txt in enumerate(["Berhemah", "Menyeluruh", "Berterusan"])]

with tab3:
    st.subheader("4.3.1 Membimbing Murid")
    a431 = [st.checkbox(f"4.3.1: {txt}", key=f"431{i}") for i, txt in enumerate(["Ikut Aras", "Betul/Tepat", "Berhemah", "Bersungguh"])]

with tab4:
    st.subheader("4.4.1 Mendorong Minda")
    a441 = [st.checkbox(f"4.4.1: {txt}", key=f"441{i}") for i, txt in enumerate(["Ikut Objektif", "Ikut Aras", "Berterusan"])]
    st.subheader("4.4.2 Mendorong Emosi")
    a442 = [st.checkbox(f"4.4.2: {txt}", key=f"442{i}") for i, txt in enumerate(["Berhemah", "Menyeluruh", "Berterusan"])]

with tab5:
    st.subheader("4.5.1 Pentaksiran")
    a451 = [st.checkbox(f"4.5.1: {txt}", key=f"451{i}") for i, txt in enumerate(["Ikut Objektif", "Patuh Ketetapan", "Menyeluruh", "Berterusan"])]

with tab6:
    st.subheader("4.6.1 Pelibatan Murid")
    peratus = st.slider("Peratus Murid Aktif:", 0, 100, 85)
    a461 = [st.checkbox(f"4.6.1 Kualiti: {txt}", key=f"461{i}") for i, txt in enumerate(["Selaras Objektif", "Yakin", "Berhemah/Bersungguh"])]

# --- PROSES JANA ---
if st.button("🚀 JANA LAPORAN AI"):
    if not api_key: st.warning("Sila masukkan API Key!")
    elif kod_admin != "KINARUT2024": st.error("Kod Autoriti Salah!")
    else:
        # Kira semua skor
        s411a = kira_skor_3(a411a); s411b = kira_skor_3(a411b); s411c = kira_skor_3(a411c)
        s421 = kira_skor_3(a421); s422 = kira_skor_3(a422)
        s431 = kira_skor_4(a431)
        s441 = kira_skor_3(a441); s442 = kira_skor_3(a442)
        s451 = kira_skor_4(a451)
        
        # Kira Skor 4.6 (Logik Khas)
        s461_val = 1
        if peratus >= 90 and sum(a461) == 3: s461_val = 4
        elif peratus >= 80: s461_val = 3
        elif peratus >= 50: s461_val = 2

        # Prompt AI
        full_data = f"Guru:{guru_opt}, Skor:[4.1.1a:{s411a}, 4.2.1:{s421}, 4.3.1:{s431}, 4.4.1:{s441}, 4.5.1:{s451}, 4.6.1:{s461_val}]"
        prompt = f"Berdasarkan data SKPMg2 ini: {full_data}, jana laporan profesional dalam Bahasa Melayu. Sertakan Kekuatan, Kelemahan (analisis kriteria yang tidak ditanda), dan 3 Cadangan Intervensi."

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(prompt)
            st.success("Laporan Siap!")
            st.markdown(res.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
