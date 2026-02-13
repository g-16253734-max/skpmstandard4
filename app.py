import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Sistem Pencerapan SMK Kinarut", layout="wide")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 2px; }
    .section-title { font-weight: bold; background-color: #1E88E5; padding: 10px; border-radius: 5px; margin-top: 25px; display: block; color: white; }
    .item-header { font-weight: bold; color: #202124; margin-top: 15px; padding: 5px; background-color: #e3f2fd; border-left: 5px solid #1E88E5; }
    .score-badge { float: right; background-color: #d32f2f; color: white; padding: 2px 15px; border-radius: 12px; font-weight: bold; }
    .total-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 2px solid #1E88E5; text-align: center; box-shadow: 4px 4px 15px rgba(0,0,0,0.1); margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LENGKAP (GURU, KELAS, SUBJEK) ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 CRYSTAL", "1 DELTA", "1 EPSILON", "1 FULCRUM", "1 GAMMA", "1 HEXA", "1 ION", "1 JADE", "1 KAPPA", "1 LAMBDA", "1 MERCURY", "1 NEUTRON", "2 ALPHA", "2 BETA", "2 CRYSTAL", "2 DELTA", "2 EPSILON", "2 FULCRUM", "2 GAMMA", "2 HEXA", "2 ION", "2 JADE", "2 KAPPA", "2 LAMBDA", "2 MERCURY", "2 NEUTRON", "3 ALPHA", "3 BETA", "3 CRYSTAL", "3 DELTA", "3 EPSILON", "3 FULCRUM", "3 GAMMA", "3 HEXA", "3 ION", "3 JADE", "3 KAPPA", "3 LAMBDA", "3 MERCURY", "3 NEUTRON", "4 ALPHA", "4 BETA", "4 CRYSTAL", "4 DELTA", "4 EPSILON", "4 FULCRUM", "4 GAMMA", "4 HEXA", "4 ION", "4 JADE", "4 KAPPA", "4 LAMBDA", "4 MERCURY", "5 ALPHA", "5 BETA", "5 CRYSTAL", "5 DELTA", "5 EPSILON", "5 FULCRUM", "5 GAMMA", "5 HEXA", "5 ION", "5 JADE", "5 KAPPA", "5 LAMBDA", "5 MERCURY", "6 ATAS 1", "6 ATAS 2", "6 ATAS 3"]
SUBJEK = ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KESUSASTERAAN MELAYU", "KIMIA", "MUET", "MATEMATIK", "MATEMATIK TAMBAHAN", "PEMBINAAN DOMESTIK", "PENDIDIKAN ISLAM", "PJPK", "PENDIDIKAN MORAL", "PENDIDIKAN MUZIK", "PSV", "PENGAJIAN AM", "PERNIAGAAN", "PERTANIAN", "PRINSIP PERAKAUNAN", "RBT", "REKA CIPTA", "SAINS", "SAINS KOMPUTER", "SAINS SUKAN", "SEJARAH", "SENI VISUAL", "TASAWUR ISLAM"]

# --- FUNGSI SKOR (IKUT JADUAL PDF) ---
def hitung_skor_3(i, ii, iii):
    if i and ii and iii: return 4
    if (i and ii) or (i and iii): return 3
    if ii and iii: return 2
    if any([i, ii, iii]): return 1
    return 0

def hitung_skor_4(i, ii, iii, iv):
    count = sum([i, ii, iii, iv])
    if count == 4: return 4
    if count == 3: return 3
    if count == 2: return 2
    if count == 1: return 1
    return 0

# --- FORM MULA ---
st.title("Sistem Pencerapan PdPc SMK Kinarut")
st.write("Format: **Standard 4 SKPMg2 (Pecahan Penuh)**")

c1, c2, c3 = st.columns(3)
with c1: guru_sel = st.selectbox("Nama Guru", LIST_GURU)
with c2: kelas_sel = st.selectbox("Kelas", KELAS)
with c3: subjek_sel = st.selectbox("Subjek", SUBJEK)

st.divider()

# --- 4.1: PERANCANG ---
st.markdown('<span class="section-title">4.1: GURU SEBAGAI PERANCANG</span>', unsafe_allow_html=True)
# 4.1.1 (a)
st.markdown('<div class="item-header">4.1.1 (a) Menyediakan RPH (Objektif & Aktiviti)</div>', unsafe_allow_html=True)
a1i, a1ii, a1iii = st.checkbox("i. Pelbagai aras", key="411ai"), st.checkbox("ii. Peruntukan masa", key="411aii"), st.checkbox("iii. Ketetapan kurikulum", key="411aiii")
s411a = hitung_skor_3(a1i, a1ii, a1iii)
st.markdown(f'<div class="score-badge">Skor: {s411a}</div>', unsafe_allow_html=True)

# 4.1.1 (b)
st.markdown('<div class="item-header">4.1.1 (b) Menentukan Kaedah Pentaksiran</div>', unsafe_allow_html=True)
b1i, b1ii, b1iii = st.checkbox("i. Pelbagai aras", key="411bi"), st.checkbox("ii. Peruntukan masa", key="411bii"), st.checkbox("iii. Ketetapan kurikulum", key="411biii")
s411b = hitung_skor_3(b1i, b1ii, b1iii)
st.markdown(f'<div class="score-badge">Skor: {s411b}</div>', unsafe_allow_html=True)

# 4.1.1 (c)
st.markdown('<div class="item-header">4.1.1 (c) Menyediakan Sumber Pendidikan (BBM/TMK)</div>', unsafe_allow_html=True)
c1i, c2ii, c3iii = st.checkbox("i. Pelbagai aras", key="411ci"), st.checkbox("ii. Peruntukan masa", key="411cii"), st.checkbox("iii. Ketetapan kurikulum", key="411ciii")
s411c = hitung_skor_3(c1i, c2ii, c3iii)
st.markdown(f'<div class="score-badge">Skor: {s411c}</div>', unsafe_allow_html=True)

# --- 4.2: PENGAWAL ---
st.markdown('<span class="section-title">4.2: GURU SEBAGAI PENGAWAL</span>', unsafe_allow_html=True)
# 4.2.1 (a)
st.markdown('<div class="item-header">4.2.1 (a) Mengelola isi pelajaran/masa</div>', unsafe_allow_html=True)
d1, d2, d3 = st.checkbox("i. Menepati objektif", key="421ai"), st.checkbox("ii. Pelbagai aras", key="421aii"), st.checkbox("iii. Berterusan", key="421aiii")
s421a = hitung_skor_3(d1, d2, d3)
st.markdown(f'<div class="score-badge">Skor: {s421a}</div>', unsafe_allow_html=True)

# 4.2.2 (a)
st.markdown('<div class="item-header">4.2.2 (a) Mengurus susun atur murid/disiplin</div>', unsafe_allow_html=True)
e1, e2, e3 = st.checkbox("i. Berhemah/sesuai", key="422ai"), st.checkbox("ii. Menyeluruh", key="422aii"), st.checkbox("iii. Berterusan", key="422aiii")
s422a = hitung_skor_3(e1, e2, e3)
st.markdown(f'<div class="score-badge">Skor: {s422a}</div>', unsafe_allow_html=True)

# --- 4.3: PEMBIMBING ---
st.markdown('<span class="section-title">4.3: GURU SEBAGAI PEMBIMBING</span>', unsafe_allow_html=True)
# 4.3.1 (a)
st.markdown('<div class="item-header">4.3.1 (a) Memberi tunjuk ajar/panduan</div>', unsafe_allow_html=True)
f1, f2, f3, f4 = st.checkbox("i. Mengikut keperluan", key="431ai"), st.checkbox("ii. Betul/Tepat", key="431aii"), st.checkbox("iii. Berhemah", key="431aiii"), st.checkbox("iv. Bersungguh-sungguh", key="431aiv")
s431a = hitung_skor_4(f1, f2, f3, f4)
st.markdown(f'<div class="score-badge">Skor: {s431a}</div>', unsafe_allow_html=True)

# --- 4.4: PENDORONG ---
st.markdown('<span class="section-title">4.4: GURU SEBAGAI PENDORONG</span>', unsafe_allow_html=True)
# 4.4.1 (a)
st.markdown('<div class="item-header">4.4.1 (a) Merangsang murid berkomunikasi</div>', unsafe_allow_html=True)
g1, g2, g3 = st.checkbox("i. Berdasarkan objektif", key="441ai"), st.checkbox("ii. Pelbagai aras", key="441aii"), st.checkbox("iii. Berterusan", key="441aiii")
s441a = hitung_skor_3(g1, g2, g3)
st.markdown(f'<div class="score-badge">Skor: {s441a}</div>', unsafe_allow_html=True)

# 4.4.2 (a)
st.markdown('<div class="item-header">4.4.2 (a) Memberi pujian/keyakinan (Emosi)</div>', unsafe_allow_html=True)
h1, h2, h3 = st.checkbox("i. Berhemah", key="442ai"), st.checkbox("ii. Menyeluruh", key="442aii"), st.checkbox("iii. Berterusan", key="442aiii")
s442a = hitung_skor_3(h1, h2, h3)
st.markdown(f'<div class="score-badge">Skor: {s442a}</div>', unsafe_allow_html=True)

# --- 4.5: PENILAI ---
st.markdown('<span class="section-title">4.5: GURU SEBAGAI PENILAI</span>', unsafe_allow_html=True)
# 4.5.1 (a)
st.markdown('<div class="item-header">4.5.1 (a) Menyemak hasil kerja/pentaksiran</div>', unsafe_allow_html=True)
j1, j2, j3, j4 = st.checkbox("i. Ikut objektif", key="451ai"), st.checkbox("ii. Ikut ketetapan", key="451aii"), st.checkbox("iii. Menyeluruh", key="451aiii"), st.checkbox("iv. Berterusan", key="451aiv")
s451a = hitung_skor_4(j1, j2, j3, j4)
st.markdown(f'<div class="score-badge">Skor: {s451a}</div>', unsafe_allow_html=True)

# --- 4.6: MURID AKTIF ---
st.markdown('<span class="section-title">4.6: MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
# 4.6.1 (a)
st.markdown('<div class="item-header">4.6.1 (a) Pelibatan murid secara aktif</div>', unsafe_allow_html=True)
pct = st.selectbox("Peratus Murid Terlibat", ["90%-100%", "80%-89%", "50%-79%", "1%-49%", "0%"])
k1 = st.checkbox("ii. Selaras dengan objektif", key="46ai")
k2 = st.checkbox("iii. Dengan yakin", key="46aii")
k3 = st.checkbox("iv. Berhemah/Bersungguh-sungguh", key="46aiii")

if pct == "90%-100%" and k1 and k2 and k3: s461a = 4
elif pct == "80%-89%" and (sum([k1, k2, k3]) >= 2): s461a = 3
elif pct == "50%-79%" and (sum([k1, k2, k3]) >= 1): s461a = 2
elif pct == "1%-49%": s461a = 1
else: s461a = 0
st.markdown(f'<div class="score-badge">Skor: {s461a}</div>', unsafe_allow_html=True)

# --- TOTAL ---
total_skor = s411a + s411b + s411c + s421a + s422a + s431a + s441a + s442a + s451a + s461a
peratus = (total_skor / 40) * 100

st.markdown(f"""
    <div class="total-card">
        <h3>Keputusan Penilaian (Standard 4)</h3>
        <h1 style="color:#1E88E5;">{peratus:.2f}%</h1>
        <p>Skor: {total_skor} / 40</p>
    </div>
""", unsafe_allow_html=True)

if st.button("🚀 JANA LAPORAN AI"):
    st.info("Laporan sedang dijana berdasarkan kriteria pecahan a, b, c...")
