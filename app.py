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
    count = sum([i, ii, iii, iv])
    if count == 4: return 4
    if count == 3: return 3
    if count == 2: return 2
    if count == 1: return 1
    return 0

def hitung_skor_46(peratus, k1, k2, k3):
    # Logik Jadual Skor 4.6 mengikut Dokumen
    if peratus == "50%-100%" and k1 and k2 and k3: return 4
    if peratus == "25%-49%" and (sum([k1, k2, k3]) >= 2): return 3
    if peratus == "10%-24%" and (sum([k1, k2, k3]) >= 1): return 2
    if peratus == "Kurang 10%": return 1
    return 0

# --- DATA ASAS ---
st.title("📋 Instrumen Pencerapan Standard 4 SKPMg2")
st.info("Pecahan item dan logik skor adalah 100% mengikut Dokumen Skor Rasmi.")

# --- FORM INPUT ---
# (Sila masukkan LIST_GURU, KELAS, SUBJEK penuh seperti sebelum ini)
# --- DATABASE GURU & KELAS ---

LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "2 DELTA", "3 GAMMA", "4 BETA", "5 ALPHA", "6 ATAS 1"]
SUBJEK = ["--- Pilih Subjek ---", "BAHASA MELAYU", "SAINS", "MATEMATIK", "SEJARAH", "PJPK"]
#guru_sel = st.selectbox("Nama Guru", ["--- Pilih ---", "ABDULLAH BIN AG. PUTEH", "ZAINUDDIN BIN AG. JALIL"])

total_mata = 0
bil_item = 0

# --- 4.1 (a - c) ---
st.markdown('<span class="section-title">4.1: GURU SEBAGAI PERANCANG</span>', unsafe_allow_html=True)
for label in ["a) Menyediakan RPH", "b) Menentukan Pentaksiran", "c) Menyediakan Sumber/BBM"]:
    st.markdown(f'<div class="item-header">4.1.1 {label}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox("i. Pelbagai aras", key=f"411{label}i"), st.checkbox("ii. Peruntukan masa", key=f"411{label}ii"), st.checkbox("iii. Ketetapan kurikulum", key=f"411{label}iii")
    skor = hitung_skor_3(i, ii, iii)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.2.1 (a - c) ---
st.markdown('<span class="section-title">4.2.1: PENGAWAL PROSES PEMBELAJARAN</span>', unsafe_allow_html=True)
for label in ["a) Mengelola isi pelajaran", "b) Mengelola masa", "c) Memberi peluang murid aktif"]:
    st.markdown(f'<div class="item-header">4.2.1 {label}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox("i. Berhemah/Sesuai", key=f"421{label}i"), st.checkbox("ii. Menyeluruh", key=f"421{label}ii"), st.checkbox("iii. Berterusan", key=f"421{label}iii")
    skor = hitung_skor_3(i, ii, iii)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.2.2 (a - c) ---
st.markdown('<span class="section-title">4.2.2: PENGAWAL SUASANA PEMBELAJARAN</span>', unsafe_allow_html=True)
for label in ["a) Mengurus susun atur murid", "b) Suasana menyeronokkan", "c) Menangani disiplin"]:
    st.markdown(f'<div class="item-header">4.2.2 {label}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox("i. Berhemah/Sesuai", key=f"422{label}i"), st.checkbox("ii. Menyeluruh", key=f"422{label}ii"), st.checkbox("iii. Berterusan", key=f"422{label}iii")
    skor = hitung_skor_3(i, ii, iii)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.3.1 (a - e) ---
st.markdown('<span class="section-title">4.3: GURU SEBAGAI PEMBIMBING</span>', unsafe_allow_html=True)
for label in ["a) Tunjuk ajar isi pelajaran", "b) Pandu buat rumusan", "c) Pandu guna sumber", "d) Gabung jalin kemahiran", "e) Bimbingan terbeza"]:
    st.markdown(f'<div class="item-header">4.3.1 {label}</div>', unsafe_allow_html=True)
    i, ii, iii, iv = st.checkbox("i. Ikut keperluan", key=f"431{label}i"), st.checkbox("ii. Betul/Tepat", key=f"431{label}ii"), st.checkbox("iii. Berhemah", key=f"431{label}iii"), st.checkbox("iv. Bersungguh-sungguh", key=f"431{label}iv")
    skor = hitung_skor_4(i, ii, iii, iv)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.4.1 (a - g) ---
st.markdown('<span class="section-title">4.4.1: PENDORONG MINDA</span>', unsafe_allow_html=True)
for label in ["a) Komunikasi", "b) Kolaboratif", "c) Soalan KBAT", "d) Murid bertanya", "e) Pak21", "f) Selesai masalah", "g) Kreativiti"]:
    st.markdown(f'<div class="item-header">4.4.1 {label}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox("i. Ikut objektif", key=f"441{label}i"), st.checkbox("ii. Aras murid", key=f"441{label}ii"), st.checkbox("iii. Berterusan", key=f"441{label}iii")
    skor = hitung_skor_3(i, ii, iii)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.4.2 (a - d) ---
st.markdown('<span class="section-title">4.4.2: PENDORONG EMOSI</span>', unsafe_allow_html=True)
for label in ["a) Pujian/Galakan", "b) Keyakinan murid", "c) Penghargaan", "d) Empati/Sokongan"]:
    st.markdown(f'<div class="item-header">4.4.2 {label}</div>', unsafe_allow_html=True)
    i, ii, iii = st.checkbox("i. Berhemah", key=f"442{label}i"), st.checkbox("ii. Menyeluruh", key=f"442{label}ii"), st.checkbox("iii. Berterusan", key=f"442{label}iii")
    skor = hitung_skor_3(i, ii, iii)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.5.1 (a - e) ---
st.markdown('<span class="section-title">4.5: GURU SEBAGAI PENILAI</span>', unsafe_allow_html=True)
for label in ["a) Semak hasil kerja", "b) Pentaksiran lisan/tulis", "c) Menilai respon", "d) Pemulihan/Pengayaan", "e) Maklum balas"]:
    st.markdown(f'<div class="item-header">4.5.1 {label}</div>', unsafe_allow_html=True)
    i, ii, iii, iv = st.checkbox("i. Ikut objektif", key=f"451{label}i"), st.checkbox("ii. Ikut ketetapan", key=f"451{label}ii"), st.checkbox("iii. Menyeluruh", key=f"451{label}iii"), st.checkbox("iv. Berterusan", key=f"451{label}iv")
    skor = hitung_skor_4(i, ii, iii, iv)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- 4.6.1 (a - f) ---
st.markdown('<span class="section-title">4.6: MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
for label in ["a) Respon isi pelajaran", "b) Komunikasi", "c) Kolaboratif", "d) KBAT", "e) Kesungguhan", "f) Kaitkan isu"]:
    st.markdown(f'<div class="item-header">4.6.1 {label}</div>', unsafe_allow_html=True)
    pct = st.selectbox(f"Penglibatan Murid ({label})", ["50%-100%", "25%-49%", "10%-24%", "Kurang 10%"], key=f"461{label}p")
    k1 = st.checkbox("ii. Selaras objektif", key=f"461{label}k1")
    k2 = st.checkbox("iii. Dengan yakin", key=f"461{label}k2")
    k3 = st.checkbox("iv. Berhemah/Bersungguh", key=f"461{label}k3")
    skor = hitung_skor_46(pct, k1, k2, k3)
    total_mata += skor; bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)

# --- TOTAL ---
st.divider()
final_peratus = (total_mata / (bil_item * 4)) * 100
st.markdown(f"""
    <div class="total-card">
        <h3>Keputusan Penuh Pencerapan</h3>
        <h1 style="color:#1E88E5;">{final_peratus:.2f}%</h1>
        <p>Jumlah Mata Skor: {total_mata} / {bil_item * 4}</p>
    </div>
""", unsafe_allow_html=True)
