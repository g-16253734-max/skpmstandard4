import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Sistem Pencerapan SMK Kinarut", layout="wide")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 2px; }
    .section-title { font-weight: bold; background-color: #1a237e; padding: 10px; border-radius: 5px; margin-top: 25px; display: block; color: white; text-align: center; font-size: 1.2em; }
    .item-header { font-weight: bold; color: #0d47a1; margin-top: 15px; padding: 8px; background-color: #e3f2fd; border-left: 8px solid #1E88E5; border-radius: 4px; }
    .score-badge { float: right; background-color: #b71c1c; color: white; padding: 2px 15px; border-radius: 12px; font-weight: bold; }
    .total-card { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 3px solid #1E88E5; text-align: center; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE GURU & KELAS ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "2 DELTA", "3 GAMMA", "4 BETA", "5 ALPHA", "6 ATAS 1"]
SUBJEK = ["--- Pilih Subjek ---", "BAHASA MELAYU", "SAINS", "MATEMATIK", "SEJARAH", "PJPK"]

# --- LOGIK PENGIRAAN ---
def hitung_3(i, ii, iii):
    if i and ii and iii: return 4
    if (i and ii) or (i and iii): return 3
    if ii and iii: return 2
    if any([i, ii, iii]): return 1
    return 0

def hitung_4(i, ii, iii, iv):
    c = sum([i, ii, iii, iv])
    return c if c <= 4 else 4

# --- FORM PdPc ---
st.title("Sistem Pencerapan SKPMg2 Standard 4 (Lengkap)")

c1, c2, c3 = st.columns(3)
with c1: guru_sel = st.selectbox("Nama Guru", LIST_GURU)
with c2: kelas_sel = st.selectbox("Kelas", KELAS)
with c3: subjek_sel = st.selectbox("Subjek", SUBJEK)

# --- 4.1 PERANCANG ---
st.markdown('<span class="section-title">4.1: GURU SEBAGAI PERANCANG</span>', unsafe_allow_html=True)
items_411 = ["a) Menyediakan RPH", "b) Menentukan Kaedah Pentaksiran", "c) Menyediakan Sumber Pendidikan"]
skor_411 = []
for item in items_411:
    st.markdown(f'<div class="item-header">4.1.1 {item}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox(f"i. Pelbagai aras", key=f"411{item}i"), st.checkbox(f"ii. Peruntukan masa", key=f"411{item}ii"), st.checkbox(f"iii. Patuh ketetapan", key=f"411{item}iii")
    s = hitung_3(i, ii, iii)
    skor_411.append(s)
    st.markdown(f'<div class="score-badge">Skor: {s}</div>', unsafe_allow_html=True)

# --- 4.2 PENGAWAL ---
st.markdown('<span class="section-title">4.2: GURU SEBAGAI PENGAWAL</span>', unsafe_allow_html=True)
# 4.2.1 a-g
items_421 = ["a) Mengelola isi pelajaran", "b) Mengelola masa PdPc", "c) Memberi peluang murid aktif", "d) Menepati objektif", "e) Mengikut aras murid", "f) Secara berterusan", "g) Mengikut ketetapan"]
skor_421 = []
for item in items_421:
    st.markdown(f'<div class="item-header">4.2.1 {item}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox(f"i. Sesuai/Berhemah", key=f"421{item}i"), st.checkbox(f"ii. Menyeluruh", key=f"421{item}ii"), st.checkbox(f"iii. Berterusan", key=f"421{item}iii")
    s = hitung_3(i, ii, iii)
    skor_421.append(s)
    st.markdown(f'<div class="score-badge">Skor: {s}</div>', unsafe_allow_html=True)

# --- 4.3 PEMBIMBING ---
st.markdown('<span class="section-title">4.3: GURU SEBAGAI PEMBIMBING</span>', unsafe_allow_html=True)
items_431 = ["a) Memberi tunjuk ajar", "b) Memandu murid membuat rumusan", "c) Memandu murid guna sumber"]
skor_431 = []
for item in items_431:
    st.markdown(f'<div class="item-header">4.3.1 {item}</div>', unsafe_allow_html=True)
    i, ii, iii, iv = st.checkbox("i. Ikut keperluan", key=f"431{item}i"), st.checkbox("ii. Betul/Tepat", key=f"431{item}ii"), st.checkbox("iii. Berhemah", key=f"431{item}iii"), st.checkbox("iv. Bersungguh-sungguh", key=f"431{item}iv")
    s = hitung_4(i, ii, iii, iv)
    skor_431.append(s)
    st.markdown(f'<div class="score-badge">Skor: {s}</div>', unsafe_allow_html=True)

# --- 4.4 PENDORONG ---
st.markdown('<span class="section-title">4.4: GURU SEBAGAI PENDORONG</span>', unsafe_allow_html=True)
items_441 = ["a) Merangsang komunikasi", "b) Merangsang kolaboratif", "c) Menggalakkan soalan murid"]
skor_441 = []
for item in items_441:
    st.markdown(f'<div class="item-header">4.4.1 {item} (Minda)</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox("i. Ikut objektif", key=f"441{item}i"), st.checkbox("ii. Aras murid", key=f"441{item}ii"), st.checkbox("iii. Berterusan", key=f"441{item}iii")
    s = hitung_3(i, ii, iii)
    skor_441.append(s)
    st.markdown(f'<div class="score-badge">Skor: {s}</div>', unsafe_allow_html=True)

# --- 4.6 MURID AKTIF (ITEM A-F) ---
st.markdown('<span class="section-title">4.6: MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
items_461 = ["a) Memberi respon", "b) Berkomunikasi dlm aktiviti", "c) Melaksanakan kolaboratif", "d) Memberi respon dlm KBAT", "e) Menunjukkan kesungguhan", "f) Mengaitkan isi pelajaran"]
skor_461 = []
for item in items_461:
    st.markdown(f'<div class="item-header">4.6.1 {item}</div>', unsafe_allow_html=True)
    pct = st.selectbox(f"Peratus Penglibatan ({item})", ["90%-100%", "80%-89%", "50%-79%", "1%-49%", "0%"], key=f"461{item}p")
    k1 = st.checkbox("ii. Selaras objektif", key=f"461{item}k1")
    k2 = st.checkbox("iii. Dengan yakin", key=f"461{item}k2")
    k3 = st.checkbox("iv. Berhemah", key=f"461{item}k3")
    
    # Logik Skor 4.6
    if pct == "90%-100%" and k1 and k2 and k3: s = 4
    elif pct == "80%-89%" and (sum([k1, k2, k3]) >= 2): s = 3
    elif pct == "50%-79%" and (sum([k1, k2, k3]) >= 1): s = 2
    elif pct == "1%-49%": s = 1
    else: s = 0
    skor_461.append(s)
    st.markdown(f'<div class="score-badge">Skor: {s}</div>', unsafe_allow_html=True)

# --- TOTAL ---
total_all = sum(skor_411 + skor_421 + skor_431 + skor_441 + skor_461)
bil_item = len(skor_411 + skor_421 + skor_431 + skor_441 + skor_461)
peratus = (total_all / (bil_item * 4)) * 100

st.markdown(f"""
    <div class="total-card">
        <h2>Keputusan Akhir Pencerapan</h2>
        <h1 style="color:#1E88E5;">{peratus:.2f}%</h1>
        <p>Mata Skor: {total_all} / {bil_item * 4}</p>
    </div>
""", unsafe_allow_html=True)
