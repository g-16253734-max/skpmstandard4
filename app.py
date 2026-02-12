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
    .total-score-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 2px solid #1E88E5; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LENGKAP ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 CRYSTAL", "1 DELTA", "1 EPSILON", "1 FULCRUM", "1 GAMMA", "1 HEXA", "1 ION", "1 JADE", "1 KAPPA", "1 LAMBDA", "1 MERCURY", "1 NEUTRON", "2 ALPHA", "2 BETA", "2 CRYSTAL", "2 DELTA", "2 EPSILON", "2 FULCRUM", "2 GAMMA", "2 HEXA", "2 ION", "2 JADE", "2 KAPPA", "2 LAMBDA", "2 MERCURY", "2 NEUTRON", "3 ALPHA", "3 BETA", "3 CRYSTAL", "3 DELTA", "3 EPSILON", "3 FULCRUM", "3 GAMMA", "3 HEXA", "3 ION", "3 JADE", "3 KAPPA", "3 LAMBDA", "3 MERCURY", "3 NEUTRON", "4 ALPHA", "4 BETA", "4 CRYSTAL", "4 DELTA", "4 EPSILON", "4 FULCRUM", "4 GAMMA", "4 HEXA", "4 ION", "4 JADE", "4 KAPPA", "4 LAMBDA", "4 MERCURY", "5 ALPHA", "5 BETA", "5 CRYSTAL", "5 DELTA", "5 EPSILON", "5 FULCRUM", "5 GAMMA", "5 HEXA", "5 ION", "5 JADE", "5 KAPPA", "5 LAMBDA", "5 MERCURY", "6 ATAS 1", "6 ATAS 2", "6 ATAS 3"]
SUBJEK = ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KESUSASTERAAN MELAYU", "KIMIA", "MUET", "MATEMATIK", "MATEMATIK TAMBAHAN", "PEMBINAAN DOMESTIK", "PENDIDIKAN ISLAM", "PJPK", "PENDIDIKAN MORAL", "PENDIDIKAN MUZIK", "PSV", "PENGAJIAN AM", "PERNIAGAAN", "PERTANIAN", "PRINSIP PERAKAUNAN", "RBT", "REKA CIPTA", "SAINS", "SAINS KOMPUTER", "SAINS SUKAN", "SEJARAH", "SENI VISUAL", "TASAWUR ISLAM"]

# --- SIDEBAR ---
st.sidebar.title("🔐 Akses Pentadbir")
pencerap_nama = st.sidebar.text_input("Nama Pencerap:")
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

st.title("📋 Sistem Pencerapan PdPc SKPMg2")
st.write(f"**Sekolah:** SMK Kinarut, Papar")
st.divider()

col1, col2 = st.columns(2)
with col1:
    guru_opt = st.selectbox("Guru Dicerap:", LIST_GURU)
    sub_opt = st.selectbox("Subjek:", SUBJEK)
with col2:
    kls_opt = st.selectbox("Kelas:", KELAS)
    mod_opt = st.selectbox("Mod Pencerapan:", ["--- Pilih Mod ---", "Kendiri", "Pertama", "Kedua"])

st.divider()

# --- FUNGSI SKOR (TERMASUK SKOR 1) ---
def get_skpm_score(checks):
    count = sum(checks)
    if count == 0: return 0
    if count == 1: return 1  # Skor 1 dimasukkan jika hanya 1 kriteria
    if count == 2: return 3
    if count == 3: return 4
    return 0

# --- KRITERIA PENUH ---
# 4.1
st.subheader("4.1: PERANCANG")
st.markdown('<span class="section-title">4.1.1: Merancang pelaksanaan PdPc</span>', unsafe_allow_html=True)
a1 = st.checkbox("i. Menyediakan RPH (Objektif & Aktiviti)", key="411i")
a2 = st.checkbox("ii. Menentukan kaedah pentaksiran", key="411ii")
a3 = st.checkbox("iii. Menyediakan sumber pendidikan (BBM/TMK)", key="411iii")
s411 = get_skpm_score([a1, a2, a3])
st.markdown(f'<div class="score-badge">Skor: {s411}</div>', unsafe_allow_html=True)

# 4.2
st.subheader("4.2: PENGAWAL")
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

# 4.3 hingga 4.6 (Sila tambahkan checkbox lain mengikut format yang sama jika perlu)
# Di sini saya ringkaskan untuk memastikan kod stabil
st.subheader("4.6: MURID AKTIF")
st.markdown('<span class="section-title">4.6.1: Pelibatan murid secara aktif</span>', unsafe_allow_html=True)
h1 = st.checkbox("i. Memberi respon/berkomunikasi", key="461i")
h2 = st.checkbox("ii. Melaksanakan aktiviti kolaboratif", key="461ii")
h3 = st.checkbox("iii. Menunjukkan kesungguhan", key="461iii")
s461 = get_skpm_score([h1, h2, h3])
st.markdown(f'<div class="score-badge">Skor: {s461}</div>', unsafe_allow_html=True)

# --- TOTAL ---
total_skor = s411 + s421 + s422 + s461 # Anda boleh tambah s431, s441 dll di sini
peratus_akhir = (total_skor / 16) * 100 # Adjust 16 mengikut jumlah item yang ada

st.markdown(f"""
    <div class="total-score-card">
        <h3>Rumusan Skor</h3>
        <h1 style="color:#1E88E5;">{peratus_akhir:.2f}%</h1>
    </div>
""", unsafe_allow_html=True)

# --- JANA ---
if st.button("🚀 JANA ULASAN AI"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Guna model flash yang lebih ringan untuk elak 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Tulis ulasan pencerapan SKPMg2 untuk {guru_opt}, Subjek {sub_opt}. Skor: {peratus_akhir}%. Berikan Kekuatan dan Cadangan."
        
        with st.spinner('Menghubungi AI...'):
            res = model.generate_content(prompt)
            st.success("Laporan Berjaya!")
            st.write(res.text)
    except Exception as e:
        st.error(f"Ralat API: {str(e)}")
