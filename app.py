import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Sistem Pencerapan SMK Kinarut", layout="wide")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 2px; }
    .section-title { font-weight: bold; background-color: #f1f3f4; padding: 8px; border-radius: 5px; margin-top: 20px; display: block; color: #202124; border-left: 5px solid #1E88E5; }
    .score-badge { float: right; background-color: #d32f2f; color: white; padding: 2px 12px; border-radius: 10px; font-weight: bold; }
    .total-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #1E88E5; text-align: center; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LENGKAP ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 CRYSTAL", "1 DELTA", "1 EPSILON", "1 FULCRUM", "1 GAMMA", "1 HEXA", "1 ION", "1 JADE", "1 KAPPA", "1 LAMBDA", "1 MERCURY", "1 NEUTRON", "2 ALPHA", "2 BETA", "2 CRYSTAL", "2 DELTA", "2 EPSILON", "2 FULCRUM", "2 GAMMA", "2 HEXA", "2 ION", "2 JADE", "2 KAPPA", "2 LAMBDA", "2 MERCURY", "2 NEUTRON", "3 ALPHA", "3 BETA", "3 CRYSTAL", "3 DELTA", "3 EPSILON", "3 FULCRUM", "3 GAMMA", "3 HEXA", "3 ION", "3 JADE", "3 KAPPA", "3 LAMBDA", "3 MERCURY", "3 NEUTRON", "4 ALPHA", "4 BETA", "4 CRYSTAL", "4 DELTA", "4 EPSILON", "4 FULCRUM", "4 GAMMA", "4 HEXA", "4 ION", "4 JADE", "4 KAPPA", "4 LAMBDA", "4 MERCURY", "5 ALPHA", "5 BETA", "5 CRYSTAL", "5 DELTA", "5 EPSILON", "5 FULCRUM", "5 GAMMA", "5 HEXA", "5 ION", "5 JADE", "5 KAPPA", "5 LAMBDA", "5 MERCURY", "6 ATAS 1", "6 ATAS 2", "6 ATAS 3"]
SUBJEK = ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KESUSASTERAAN MELAYU", "KIMIA", "MUET", "MATEMATIK", "MATEMATIK TAMBAHAN", "PEMBINAAN DOMESTIK", "PENDIDIKAN ISLAM", "PJPK", "PENDIDIKAN MORAL", "PENDIDIKAN MUZIK", "PSV", "PENGAJIAN AM", "PERNIAGAAN", "PERTANIAN", "PRINSIP PERAKAUNAN", "RBT", "REKA CIPTA", "SAINS", "SAINS KOMPUTER", "SAINS SUKAN", "SEJARAH", "SENI VISUAL", "TASAWUR ISLAM"]

# --- PENGIRAAN SKOR IKUT PDF ---
def skor_3_kriteria(i, ii, iii):
    if i and ii and iii: return 4
    if i and ii: return 3
    if i and iii: return 3
    if ii and iii: return 2
    if any([i, ii, iii]): return 1
    return 0

def skor_4_kriteria(i, ii, iii, iv):
    count = sum([i, ii, iii, iv])
    if count == 4: return 4
    if count == 3: return 3
    if count == 2: return 2
    if count == 1: return 1
    return 0

# Khusus 4.6 (Murid Aktif)
def skor_46(peratus, yakin, berhemah):
    # Logik: Kena selaras dgn % dan kriteria tambahan
    if peratus == "90%-100%" and yakin and berhemah: return 4
    if peratus == "80%-89%" and (yakin or berhemah): return 3
    if peratus == "50%-79%": return 2
    if peratus == "1%-49%": return 1
    return 0

# --- UI START ---
st.title("Sistem SKPMg2 Standard 4 - SMK Kinarut")

col1, col2, col3 = st.columns(3)
with col1: guru = st.selectbox("Nama Guru", LIST_GURU)
with col2: kelas = st.selectbox("Kelas", KELAS)
with col3: subjek = st.selectbox("Subjek", SUBJEK)

# --- 4.1 ---
st.markdown('<span class="section-title">4.1 GURU SEBAGAI PERANCANG</span>', unsafe_allow_html=True)
c411i = st.checkbox("4.1.1(i) Pelbagai aras murid", key="411i")
c411ii = st.checkbox("4.1.1(ii) Peruntukan masa", key="411ii")
c411iii = st.checkbox("4.1.1(iii) Patuh arahan kurikulum", key="411iii")
s411 = skor_3_kriteria(c411i, c411ii, c411iii)
st.markdown(f'<div class="score-badge">Skor: {s411}</div>', unsafe_allow_html=True)

# --- 4.2 ---
st.markdown('<span class="section-title">4.2 GURU SEBAGAI PENGAWAL</span>', unsafe_allow_html=True)
c421i = st.checkbox("4.2.1(i) Menepati objektif", key="421i")
c421ii = st.checkbox("4.2.1(ii) Pelbagai aras murid", key="421ii")
c421iii = st.checkbox("4.2.1(iii) Dari semasa ke semasa", key="421iii")
s421 = skor_3_kriteria(c421i, c421ii, c421iii)
st.markdown(f'<div class="score-badge">Skor: {s421}</div>', unsafe_allow_html=True)

# --- 4.3 ---
st.markdown('<span class="section-title">4.3 GURU SEBAGAI PEMBIMBING</span>', unsafe_allow_html=True)
c431i = st.checkbox("4.3.1(i) Mengikut keperluan", key="431i")
c431ii = st.checkbox("4.3.1(ii) Betul dan tepat", key="431ii")
c431iii = st.checkbox("4.3.1(iii) Secara berhemah", key="431iii")
c431iv = st.checkbox("4.3.1(iv) Bersungguh-sungguh", key="431iv")
s431 = skor_4_kriteria(c431i, c431ii, c431iii, c431iv)
st.markdown(f'<div class="score-badge">Skor: {s431}</div>', unsafe_allow_html=True)

# --- 4.4 ---
st.markdown('<span class="section-title">4.4 GURU SEBAGAI PENDORONG</span>', unsafe_allow_html=True)
c441i = st.checkbox("4.4.1(i) Merangsang komunikasi", key="441i")
c441ii = st.checkbox("4.4.1(ii) Aras kepelbagaian murid", key="441ii")
c441iii = st.checkbox("4.4.1(iii) Dari semasa ke semasa", key="441iii")
s441 = skor_3_kriteria(c441i, c441ii, c441iii)
st.markdown(f'<div class="score-badge">Skor: {s441}</div>', unsafe_allow_html=True)

# --- 4.5 ---
st.markdown('<span class="section-title">4.5 GURU SEBAGAI PENILAI</span>', unsafe_allow_html=True)
c451i = st.checkbox("4.5.1(i) Berdasarkan objektif", key="451i")
c451ii = st.checkbox("4.5.1(ii) Ikut arahan pentaksiran", key="451ii")
c451iii = st.checkbox("4.5.1(iii) Secara menyeluruh", key="451iii")
c451iv = st.checkbox("4.5.1(iv) Dari semasa ke semasa", key="451iv")
s451 = skor_4_kriteria(c451i, c451ii, c451iii, c451iv)
st.markdown(f'<div class="score-badge">Skor: {s451}</div>', unsafe_allow_html=True)

# --- 4.6 (IKUT KRITERIA PDF) ---
st.markdown('<span class="section-title">4.6 MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
pct = st.selectbox("Peratus Penglibatan Murid", ["90%-100%", "80%-89%", "50%-79%", "1%-49%", "0%"])
yakin = st.checkbox("Murid Berkomunikasi dengan yakin", key="46yakin")
hemah = st.checkbox("Murid Bersungguh-sungguh/Berhemah", key="46hemah")
s461 = skor_46(pct, yakin, hemah)
st.markdown(f'<div class="score-badge">Skor: {s461}</div>', unsafe_allow_html=True)

# --- RUMUSAN ---
total = s411 + s421 + s431 + s441 + s451 + s461
peratus = (total / 24) * 100 # Adjust ikut bilangan item aktif

st.markdown(f"""
    <div class="total-card">
        <h2>Keputusan Keseluruhan</h2>
        <h1 style="color:#1E88E5;">{peratus:.2f}%</h1>
        <p>Mata Skor: {total} / 24</p>
    </div>
""", unsafe_allow_html=True)

if st.button("🚀 JANA LAPORAN AI"):
    # Logik AI seperti sebelum ini
    st.write("Laporan sedang dijana...")
