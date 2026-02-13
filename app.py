import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Pencerapan SMK Kinarut", layout="centered")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 2px; }
    .section-title { font-weight: bold; background-color: #f1f3f4; padding: 8px; border-radius: 5px; margin-top: 20px; display: block; color: #202124; border-left: 5px solid #1E88E5; }
    .score-badge { float: right; background-color: #d32f2f; color: white; padding: 2px 12px; border-radius: 10px; font-weight: bold; }
    .total-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #1E88E5; text-align: center; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PENGIRAAN SKOR IKUT DOKUMEN ---

# Untuk 4.1, 4.2, 4.4 (3 Kriteria)
def calc_3_criteria(i, ii, iii):
    count = sum([i, ii, iii])
    if count == 3: return 4
    if count == 2: return 3
    if count == 1: return 1 # Mengikut dokumen, 1 kriteria selalunya skor 1
    # Pengecualian spesifik: Jika (ii & iii) sahaja ditanda dalam sesetengah aspek boleh jadi skor 2
    if not i and ii and iii: return 2 
    return 0

# Untuk 4.3, 4.5 (4 Kriteria)
def calc_4_criteria(i, ii, iii, iv):
    count = sum([i, ii, iii, iv])
    if count == 4: return 4
    if count == 3: return 3
    if count == 2: return 2
    if count == 1: return 1
    return 0

# --- DATA GURU & KELAS ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "ZAINUDDIN BIN AG. JALIL"]
# ... (Sila tambah senarai guru yang saya berikan sebelum ini jika perlu)

st.title("📋 Sistem Pencerapan PdPc (Standard 4)")
st.write("Sistem ini mengikut jadual penskoran **Standard4 SKPM Skor.pdf**")

# --- INPUT ASAS ---
guru_opt = st.selectbox("Guru Dicerap:", LIST_GURU)
sub_opt = st.text_input("Subjek:")
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

st.divider()

# --- 4.1: GURU SEBAGAI PERANCANG ---
st.markdown('<span class="section-title">4.1.1: Guru Merancang Pelaksanaan PdPc</span>', unsafe_allow_html=True)
c411_i = st.checkbox("i. Mengikut pelbagai aras keupayaan murid", key="411i")
c411_ii = st.checkbox("ii. Mengikut peruntukan masa yang ditetapkan", key="411ii")
c411_iii = st.checkbox("iii. Mematuhi arahan/ketetapan kurikulum", key="411iii")
# Logik: i+ii+iii=4, i+ii=3, ii+iii=2, mana-mana 1=1
if c411_i and c411_ii and c411_iii: s411 = 4
elif (c411_i and c411_ii) or (c411_i and c411_iii): s411 = 3
elif (c411_ii and c411_iii): s411 = 2
elif any([c411_i, c411_ii, c411_iii]): s411 = 1
else: s411 = 0
st.markdown(f'<div class="score-badge">Skor: {s411}</div>', unsafe_allow_html=True)

# --- 4.3: GURU SEBAGAI PEMBIMBING (4 KRITERIA) ---
st.subheader("4.3: GURU SEBAGAI PEMBIMBING")
st.markdown('<span class="section-title">4.3.1: Membimbing murid secara profesional</span>', unsafe_allow_html=True)
c431_i = st.checkbox("i. Mengikut keperluan/pelbagai aras", key="431i")
c431_ii = st.checkbox("ii. Dengan betul dan tepat", key="431ii")
c431_iii = st.checkbox("iii. Secara berhemah", key="431iii")
c431_iv = st.checkbox("iv. Bersungguh-sungguh", key="431iv")
s431 = calc_4_criteria(c431_i, c431_ii, c431_iii, c431_iv)
st.markdown(f'<div class="score-badge">Skor: {s431}</div>', unsafe_allow_html=True)

# --- 4.6: MURID SEBAGAI PEMBELAJAR AKTIF (IKUT % PENGLIBATAN) ---
st.subheader("4.6: MURID SEBAGAI PEMBELAJAR AKTIF")
st.markdown('<span class="section-title">4.6.1: Pelibatan murid secara aktif</span>', unsafe_allow_html=True)
penglibatan = st.radio("Tahap penglibatan murid (90-100% untuk skor 4):", 
                       ["90% - 100% (Skor 4)", "80% - 89% (Skor 3)", "50% - 79% (Skor 2)", "1% - 49% (Skor 1)", "0% (Skor 0)"])
# Map skor
s461 = {"90% - 100% (Skor 4)": 4, "80% - 89% (Skor 3)": 3, "50% - 79% (Skor 2)": 2, "1% - 49% (Skor 1)": 1, "0% (Skor 0)": 0}[penglibatan]

# --- RUMUSAN ---
total_skor = s411 + s431 + s461 # Sila tambah aspek lain (4.2, 4.4, 4.5) menggunakan fungsi di atas
st.divider()
st.markdown(f"""
    <div class="total-card">
        <h3>Jumlah Skor Semasa</h3>
        <h1 style="color:#1E88E5;">{total_skor}</h1>
    </div>
""", unsafe_allow_html=True)

# --- JANA ULASAN ---
if st.button("🚀 JANA ULASAN AI"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Berikan ulasan pencerapan untuk {guru_opt} berdasarkan skor SKPMg2 Standard 4: {total_skor}."
        res = model.generate_content(prompt)
        st.write(res.text)
    except:
        st.error("Sila semak API Key dalam Secrets.")
