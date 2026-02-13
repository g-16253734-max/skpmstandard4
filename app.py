import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="Sistem Pencerapan PdPc SMK Kinarut", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .section-title { font-weight: bold; background-color: #1a237e; padding: 12px; border-radius: 5px; margin-top: 25px; display: block; color: white; text-align: center; }
    .item-header { font-weight: bold; color: #0d47a1; margin-top: 15px; padding: 8px; background-color: #e3f2fd; border-left: 8px solid #1E88E5; }
    .score-badge { float: right; background-color: #b71c1c; color: white; padding: 2px 15px; border-radius: 12px; font-weight: bold; }
    .total-card { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 3px solid #1E88E5; text-align: center; margin-top: 30px; }
    .pct-box { background-color: #fff3e0; padding: 10px; border-radius: 5px; border: 1px solid #ffb74d; }
    .crit-box { background-color: #f1f8e9; padding: 10px; border-radius: 5px; border: 1px solid #8bc34a; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PENGIRAAN SKOR ---
def hitung_skor_3(i, ii, iii):
    if i and ii and iii: return 4
    if (i and ii) or (i and iii): return 3
    if ii and iii: return 2
    if any([i, ii, iii]): return 1
    return 0

def hitung_skor_4(i, ii, iii, iv):
    count = sum([1 for x in [i, ii, iii, iv] if x])
    if count == 4: return 4
    if count == 3: return 3
    if count == 2: return 2
    if count == 1: return 1
    return 0

def hitung_skor_46_tick(p1, p2, p3, p4, k1, k2, k3):
    count_k = sum([1 for x in [k1, k2, k3] if x])
    if p1: # 50%-100%
        if count_k == 3: return 4
        if count_k == 2: return 3
        if count_k == 1: return 2
        return 1
    if p2: # 25%-49%
        if count_k >= 2: return 3
        if count_k == 1: return 2
        return 1
    if p3: # 10%-24%
        if count_k >= 1: return 2
        return 1
    if p4: # Kurang 10%
        return 1
    return 0

# --- DATABASE GURU (SEMUA NAMA) ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
LIST_KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 GAMMA", "2 ALPHA", "2 DELTA", "3 GAMMA", "4 BETA", "5 ALPHA", "6 ATAS 1", "6 ATAS 2"]
LIST_SUBJEK = ["--- Pilih Subjek ---", "BAHASA MELAYU", "BAHASA INGGERIS", "MATEMATIK", "SAINS", "SEJARAH", "PENDIDIKAN ISLAM", "PJPK", "PSV", "RBT", "GEOGRAFI"]

# --- UI ---
st.title("📋 Instrumen PdPc Standard 4 (SKPMg2)")

c1, c2, c3 = st.columns(3)
with c1: guru_sel = st.selectbox("Nama Guru", LIST_GURU)
with c2: kls_sel = st.selectbox("Kelas", LIST_KELAS)
with c3: sbj_sel = st.selectbox("Subjek", LIST_SUBJEK)

total_mata = 0
bil_item = 0

# --- ITEM 4.1 HINGGA 4.5 (RINGKASAN LOGIK) ---
def render_section(title, prefix, labels, mode="skor3"):
    global total_mata, bil_item
    st.markdown(f'<span class="section-title">{title}</span>', unsafe_allow_html=True)
    for i_idx, label in enumerate(labels):
        k = chr(97 + i_idx) # a, b, c...
        st.markdown(f'<div class="item-header">{prefix} ({k}) {label}</div>', unsafe_allow_html=True)
        if mode == "skor3":
            c1, c2, c3 = st.columns(3)
            with c1: v1 = st.checkbox("i. Pelbagai aras / Berhemah", key=f"{prefix}{k}1")
            with c2: v2 = st.checkbox("ii. Masa / Menyeluruh", key=f"{prefix}{k}2")
            with c3: v3 = st.checkbox("iii. Ketetapan / Berterusan", key=f"{prefix}{k}3")
            skor = hitung_skor_3(v1, v2, v3)
        else:
            c1, c2, c3, c4 = st.columns(4)
            with c1: v1 = st.checkbox("i. Ikut Keperluan / Objektif", key=f"{prefix}{k}1")
            with c2: v2 = st.checkbox("ii. Betul / Ketetapan", key=f"{prefix}{k}2")
            with c3: v3 = st.checkbox("iii. Berhemah / Menyeluruh", key=f"{prefix}{k}3")
            with c4: v4 = st.checkbox("iv. Bersungguh / Berterusan", key=f"{prefix}{k}4")
            skor = hitung_skor_4(v1, v2, v3, v4)
        
        total_mata += skor
        bil_item += 1
        st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# 4.1 (a-c)
render_section("4.1: GURU SEBAGAI PERANCANG", "4.1.1", ["Sediakan RPH", "Tentukan Pentaksiran", "Sediakan Sumber/BBM"], "skor3")
# 4.2.1 (a-c)
render_section("4.2.1: PENGAWAL PROSES", "4.2.1", ["Isi Pelajaran", "Masa PdPc", "Peluang Murid Aktif"], "skor3")
# 4.2.2 (a-c)
render_section("4.2.2: PENGAWAL SUASANA", "4.2.2", ["Susun Atur Murid", "Suasana Menyeronokkan", "Tangani Disiplin"], "skor3")
# 4.3.1 (a-e)
render_section("4.3.1: GURU SEBAGAI PEMBIMBING", "4.3.1", ["Tunjuk Ajar Isi", "Pandu Rumusan", "Pandu Sumber", "Gabung Jalin", "Bimbing Terbeza"], "skor4")
# 4.4.1 (a-g)
render_section("4.4.1: PENDORONG MINDA", "4.4.1", ["Komunikasi", "Kolaboratif", "KBAT", "Murid Bertanya", "PAK21", "Selesai Masalah", "Kreativiti"], "skor3")
# 4.4.2 (a-d)
render_section("4.4.2: PENDORONG EMOSI", "4.4.2", ["Pujian/Galakan", "Keyakinan Murid", "Penghargaan", "Empati/Sokongan"], "skor3")
# 4.5.1 (a-e)
render_section("4.5.1: GURU SEBAGAI PENILAI", "4.5.1", ["Semak Kerja", "Pentaksiran Lisan/Tulis", "Respon Murid", "Pemulihan/Pengayaan", "Maklum Balas"], "skor4")

# --- 4.6 (VERSI TICK PERATUS) ---
st.markdown('<span class="section-title">4.6: MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
items_46 = ["Respon Isi", "Komunikasi", "Kolaboratif", "Respon KBAT", "Kesungguhan", "Kaitkan Isu/Kehidupan"]
for i_idx, label in enumerate(items_46):
    k = chr(97 + i_idx)
    st.markdown(f'<div class="item-header">4.6.1 ({k}) {label}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 2])
    with col1:
        st.markdown('<div class="pct-box"><b>Pilih SATU Peratus (i):</b></div>', unsafe_allow_html=True)
        p1 = st.checkbox("50% - 100% Murid", key=f"461{k}p1")
        p2 = st.checkbox("25% - 49% Murid", key=f"461{k}p2")
        p3 = st.checkbox("10% - 24% Murid", key=f"461{k}p3")
        p4 = st.checkbox("Kurang 10% Murid", key=f"461{k}p4")
    
    with col2:
        st.markdown('<div class="crit-box"><b>Kriteria Tambahan:</b></div>', unsafe_allow_html=True)
        k1 = st.checkbox("ii. Selaras dengan objektif", key=f"461{k}k1")
        k2 = st.checkbox("iii. Dengan yakin", key=f"461{k}k2")
        k3 = st.checkbox("iv. Berhemah / Bersungguh", key=f"461{k}k3")
    
    skor = hitung_skor_46_tick(p1, p2, p3, p4, k1, k2, k3)
    total_mata += skor
    bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- TOTAL ---
st.divider()
if bil_item > 0:
    final_score = (total_mata / (bil_item * 4)) * 100
    st.markdown(f"""
        <div class="total-card">
            <h2>Keputusan Penuh Pencerapan</h2>
            <h1 style="color:#1E88E5;">{final_score:.2f}%</h1>
            <p>Jumlah Mata: {total_mata} / {bil_item * 4}</p>
            <p>Guru: <b>{guru_sel}</b> | Kelas: <b>{kls_sel}</b></p>
        </div>
    """, unsafe_allow_html=True)
