import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Pencerapan SMK Kinarut", layout="centered")

# Custom CSS untuk nampak lebih kemas
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; }
    .stSubheader { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "ALDRIANA ANDREAS", "ZAINUDDIN BIN AG. JALIL"]
LIST_SUBJEK = ["--- Pilih Subjek ---", "BAHASA MELAYU", "BAHASA INGGERIS", "SAINS", "MATEMATIK", "SEJARAH"]
LIST_KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "2 ALPHA", "2 BETA", "3 ALPHA", "4 ALPHA", "5 ALPHA"]

# --- SIDEBAR (AUTH) ---
st.sidebar.title("🔐 Akses Pentadbir")
pencerap = st.sidebar.text_input("Nama Pencerap:")
jawatan = st.sidebar.selectbox("Jawatan:", ["--- Pilih Jawatan ---", "Pengetua", "PK", "Ketua Bidang", "Ketua Panitia"])
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

# --- UI UTAMA ---
st.title("📋 Sistem Pencerapan SKPMg2")
st.write(f"**Sekolah:** SMK Kinarut, Papar")
st.divider()

# DATA ASAS
col1, col2 = st.columns(2)
with col1:
    guru_opt = st.selectbox("Guru Dicerap:", LIST_GURU)
    sub_opt = st.selectbox("Subjek:", LIST_SUBJEK)
with col2:
    kls_opt = st.selectbox("Kelas:", LIST_KELAS)
    mod_opt = st.selectbox("Mod Pencerapan:", ["--- Pilih Mod ---", "Kendiri", "Pertama", "Kedua"])

st.divider()

# --- BORANG TICK-BOX (BERSTRUKTUR) ---
st.info("💡 Tanda (✓) pada kriteria yang dilaksanakan semasa PdPc.")

# 4.1 PERANCANG
st.subheader("Standard 4.1: Guru Sebagai Perancang")

st.write("**4.1.1 (a) Penyediaan RPH (Objektif/Aktiviti)**")
c1, c2, c3 = st.columns(3)
t1 = c1.checkbox("Mengikut Aras", key="411ai")
t2 = c2.checkbox("Menepati Masa", key="411aii")
t3 = c3.checkbox("Ikut Kurikulum", key="411aiii")

st.write("**4.1.1 (b) Perancangan Pentaksiran**")
c4, c5, c6 = st.columns(3)
t4 = c4.checkbox("Kaedah Tepat", key="411bi")
t5 = c5.checkbox("Masa Sesuai", key="411bii")
t6 = c6.checkbox("Ikut Ketetapan", key="411biii")

st.write("**4.1.1 (c) Sumber Pendidikan (BBM)**")
c7, c8, c9 = st.columns(3)
t7 = c7.checkbox("BBM Pelbagai", key="411ci")
t8 = c8.checkbox("BBM Berkesan", key="411cii")
t9 = c9.checkbox("BBM Interaktif", key="411ciii")

# 4.2 PENGAWAL
st.subheader("Standard 4.2: Guru Sebagai Pengawal")
st.write("**4.2.1 Pengurusan Proses Pembelajaran**")
c10, c11, c12 = st.columns(3)
t10 = c10.checkbox("Kawal Komunikasi", key="421i")
t11 = c11.checkbox("Peluang Murid", key="421ii")
t12 = c12.checkbox("Kawal Masa", key="421iii")

# 4.6 MURID AKTIF
st.subheader("Standard 4.6: Murid Sebagai Pembelajar Aktif")
peratus = st.slider("Peratus Pelibatan Murid:", 0, 100, 85)
st.write("**Kualiti Tindakan Murid**")
c13, c14, c15 = st.columns(3)
t13 = c13.checkbox("Beri Respon", key="46i")
t14 = c14.checkbox("Yakin & Berani", key="46ii")
t15 = c15.checkbox("Saling Membantu", key="46iii")

st.divider()

# --- PROSES JANA ---
if st.button("🚀 JANA LAPORAN AI SEKARANG"):
    # VALIDASI
    if guru_opt == "--- Pilih Nama Guru ---" or mod_opt == "--- Pilih Mod ---":
        st.error("Sila pilih Nama Guru dan Mod Pencerapan terlebih dahulu!")
    elif kod_admin != "KINARUT2024":
        st.error("Kod Autoriti Salah!")
    else:
        # Panggil Secret API Key dari Streamlit
        try:
            API_KEY = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Ringkasan Data untuk AI
            data_tanda = {
                "4.1.1a": [t1, t2, t3],
                "4.1.1b": [t4, t5, t6],
                "4.6.1": [t13, t14, t15]
            }
            
            prompt = f"""
            Tulis ulasan profesional SKPMg2 Standard 4:
            Guru: {guru_opt}, Subjek: {sub_opt}, Kelas: {kls_opt}, Mod: {mod_opt}.
            Data Tandanan: {data_tanda}. Peratus Murid: {peratus}%.
            
            Format:
            1. Rumusan Kekuatan.
            2. Analisis Kelemahan (sebut kriteria yang TIDAK ditanda).
            3. Cadangan Penambahbaikan (3 idea kreatif).
            Ulasan mestilah dalam Bahasa Melayu yang formal.
            """
            
            with st.spinner('AI sedang berfikir...'):
                res = model.generate_content(prompt)
                st.success("Laporan Berjaya Dijana!")
                st.markdown(res.text)
                
        except Exception as e:
            st.error(f"Sila pastikan API Key telah dimasukkan di 'Secrets' Streamlit. Error: {e}")
