import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Pencerapan SMK Kinarut", layout="centered")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 4px; padding-left: 30px; }
    .stSubheader { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 5px; margin-top: 30px;}
    .section-title { font-weight: bold; background-color: #f1f3f4; padding: 8px; border-radius: 5px; margin-top: 20px; display: block; color: #202124; border-left: 5px solid #1E88E5; }
    .score-badge { float: right; background-color: #1E88E5; color: white; padding: 2px 12px; border-radius: 10px; font-weight: bold; }
    .total-score-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
LIST_GURU = ["--- Pilih Nama Guru ---", "FARIZATUL AKMAM BINTI ARIF", "ABDULLAH BIN AG. PUTEH", "ZAINUDDIN BIN AG. JALIL"] # Dipendekkan untuk contoh
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "2 DELTA", "3 DELTA", "4 BETA", "5 ALPHA"]

# --- SIDEBAR ---
st.sidebar.title("🔐 Akses Pentadbir")
pencerap_nama = st.sidebar.text_input("Nama Pencerap:")
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

st.title("📋 Sistem Pencerapan PdPc SKPMg2")
st.write(f"**Institusi:** SMK Kinarut, Papar")
st.divider()

col1, col2 = st.columns(2)
with col1:
    guru_opt = st.selectbox("Guru Dicerap:", LIST_GURU)
    sub_opt = st.selectbox("Subjek:", ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA MELAYU", "SAINS", "MATEMATIK"])
with col2:
    kls_opt = st.selectbox("Kelas:", KELAS)
    mod_opt = st.selectbox("Mod Pencerapan:", ["--- Pilih Mod ---", "Kendiri", "Pertama", "Kedua"])

st.divider()

# --- FUNGSI PENGIRAAN SKOR (Standard 4 SKPMg2) ---
# Biasanya: 3 kriteria = Skor 4, 2 kriteria = Skor 3, 1 kriteria = Skor 2, 0 = Skor 1 (ikut kualiti)
def get_skpm_score(checks):
    count = sum(checks)
    if count == 3: return 4
    if count == 2: return 3
    if count == 1: return 2
    return 1

# --- STANDARD 4 (KRITERIA LENGKAP) ---

# 4.1: PERANCANG
st.subheader("4.1: GURU SEBAGAI PERANCANG")
st.markdown('<span class="section-title">4.1.1: Guru merancang pelaksanaan PdPc</span>', unsafe_allow_html=True)
a1 = st.checkbox("i. Menyediakan RPH (Objektif & Aktiviti)", key="411i")
a2 = st.checkbox("ii. Menentukan kaedah pentaksiran", key="411ii")
a3 = st.checkbox("iii. Menyediakan sumber pendidikan (BBM/TMK)", key="411iii")
s411 = get_skpm_score([a1, a2, a3])
st.markdown(f'<div class="score-badge">Skor: {s411}</div>', unsafe_allow_html=True)

# 4.2: PENGAWAL
st.subheader("4.2: GURU SEBAGAI PENGAWAL")
st.markdown('<span class="section-title">4.2.1: Mengawal proses pembelajaran</span>', unsafe_allow_html=True)
b1 = st.checkbox("i. Mengelola isi pelajaran/masa", key="421i")
b2 = st.checkbox("ii. Menepati objektif pembelajaran", key="421ii")
b3 = st.checkbox("iii. Melibatkan murid secara berterusan", key="421iii")
s421 = get_skpm_score([b1, b2, b3])
st.markdown(f'<div class="score-badge">Skor: {s421}</div>', unsafe_allow_html=True)

st.markdown('<span class="section-title">4.2.2: Mengawal suasana pembelajaran</span>', unsafe_allow_html=True)
c1 = st.checkbox("i. Mengurus susun atur murid", key="422i")
c2 = st.checkbox("ii. Mewujudkan suasana menyeronokkan", key="422ii")
c3 = st.checkbox("iii. Menangani disiplin murid", key="422iii")
s422 = get_skpm_score([c1, c2, c3])
st.markdown(f'<div class="score-badge">Skor: {s422}</div>', unsafe_allow_html=True)

# 4.3: PEMBIMBING
st.subheader("4.3: GURU SEBAGAI PEMBIMBING")
st.markdown('<span class="section-title">4.3.1: Membimbing murid secara profesional</span>', unsafe_allow_html=True)
d1 = st.checkbox("i. Memberi tunjuk ajar/panduan", key="431i")
d2 = st.checkbox("ii. Memandu murid membuat keputusan/menyelesaikan masalah", key="431ii")
d3 = st.checkbox("iii. Menggunakan sumber pendidikan", key="431iii")
s431 = get_skpm_score([d1, d2, d3])
st.markdown(f'<div class="score-badge">Skor: {s431}</div>', unsafe_allow_html=True)

# 4.4: PENDORONG
st.subheader("4.4: GURU SEBAGAI PENDORONG")
st.markdown('<span class="section-title">4.4.1: Mendorong minda murid (Kognitif)</span>', unsafe_allow_html=True)
e1 = st.checkbox("i. Merangsang murid berkomunikasi", key="441i")
e2 = st.checkbox("ii. Mewujudkan peluang murid memimpin", key="441ii")
e3 = st.checkbox("iii. Menggalakkan murid mengemukakan soalan", key="441iii")
s441 = get_skpm_score([e1, e2, e3])
st.markdown(f'<div class="score-badge">Skor: {s441}</div>', unsafe_allow_html=True)

st.markdown('<span class="section-title">4.4.2: Mendorong emosi murid (Afektif)</span>', unsafe_allow_html=True)
f1 = st.checkbox("i. Memberi pujian/galakan", key="442i")
f2 = st.checkbox("ii. Memberi keyakinan diri", key="442ii")
f3 = st.checkbox("iii. Secara berhemah & menyeluruh", key="442iii")
s442 = get_skpm_score([f1, f2, f3])
st.markdown(f'<div class="score-badge">Skor: {s442}</div>', unsafe_allow_html=True)

# 4.5: PENILAI
st.subheader("4.5: GURU SEBAGAI PENILAI")
st.markdown('<span class="section-title">4.5.1: Melaksanakan pentaksiran</span>', unsafe_allow_html=True)
g1 = st.checkbox("i. Pelbagai kaedah pentaksiran", key="451i")
g2 = st.checkbox("ii. Menjalankan aktiviti pemulihan/pengayaan", key="451ii")
g3 = st.checkbox("iii. Memberi maklum balas hasil kerja murid", key="451iii")
s451 = get_skpm_score([g1, g2, g3])
st.markdown(f'<div class="score-badge">Skor: {s451}</div>', unsafe_allow_html=True)

# 4.6: MURID
st.subheader("4.6: MURID SEBAGAI PEMBELAJAR AKTIF")
st.markdown('<span class="section-title">4.6.1: Pelibatan murid secara aktif</span>', unsafe_allow_html=True)
h1 = st.checkbox("i. Memberi respon berkaitan isi pelajaran", key="461i")
h2 = st.checkbox("ii. Berkomunikasi dalam melaksanakan aktiviti", key="461ii")
h3 = st.checkbox("iii. Menunjukkan kesungguhan belajar", key="461iii")
s461 = get_skpm_score([h1, h2, h3])
st.markdown(f'<div class="score-badge">Skor: {s461}</div>', unsafe_allow_html=True)

# --- RUMUSAN SKOR ---
total_skor = s411 + s421 + s422 + s431 + s441 + s442 + s451 + s461
peratus_akhir = (total_skor / 32) * 100

st.markdown(f"""
    <div class="total-score-card">
        <h3>Rumusan Skor Standard 4</h3>
        <h1 style="color:#1E88E5;">{peratus_akhir:.2f}%</h1>
        <p>Jumlah Mata Skor: {total_skor} / 32</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- BUTTON JANA ---
if st.button("🚀 JANA ULASAN AI BERDASARKAN SKOR"):
    if guru_opt == "--- Pilih Nama Guru ---" or mod_opt == "--- Pilih Mod ---":
        st.error("Sila pilih Nama Guru dan Mod!")
    else:
        authorized = (mod_opt == "Kendiri") or (kod_admin == "KINARUT2024")
        if not authorized:
            st.error("Kod Autoriti Salah!")
        else:
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                sum_data = f"Skor: 4.1.1={s411}, 4.2.1={s421}, 4.2.2={s422}, 4.3.1={s431}, 4.4.1={s441}, 4.4.2={s442}, 4.5.1={s451}, 4.6.1={s461}. Total={peratus_akhir}%."
                
                prompt = f"Sebagai pencerap sekolah, tulis ulasan pencerapan PdPc untuk {guru_opt}. Data: {sum_data}. Gunakan format: Rumusan Kekuatan, Penambahbaikan dan Cadangan."
                
                with st.spinner('Menjana ulasan...'):
                    res = model.generate_content(prompt)
                    st.success("Laporan Berjaya!")
                    st.markdown(res.text)
                    st.download_button("Simpan Laporan", res.text, file_name=f"Laporan_{guru_opt}.txt")
            except Exception as e:
                st.error(f"Ralat API: {str(e)}")
