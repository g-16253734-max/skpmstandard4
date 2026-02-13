import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Sistem Pencerapan SMK Kinarut", layout="wide")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 2px; }
    .section-title { font-weight: bold; background-color: #f1f3f4; padding: 10px; border-radius: 5px; margin-top: 25px; display: block; color: #1E88E5; border-left: 5px solid #1E88E5; }
    .item-header { font-weight: bold; color: #202124; margin-top: 10px; padding-left: 10px; border-bottom: 1px solid #ddd; }
    .score-badge { float: right; background-color: #d32f2f; color: white; padding: 2px 15px; border-radius: 12px; font-weight: bold; font-size: 1.1em; }
    .total-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 2px solid #1E88E5; text-align: center; box-shadow: 4px 4px 15px rgba(0,0,0,0.1); margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LENGKAP ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 CRYSTAL", "1 DELTA", "1 EPSILON", "1 FULCRUM", "1 GAMMA", "1 HEXA", "1 ION", "1 JADE", "1 KAPPA", "1 LAMBDA", "1 MERCURY", "1 NEUTRON", "2 ALPHA", "2 BETA", "2 CRYSTAL", "2 DELTA", "2 EPSILON", "2 FULCRUM", "2 GAMMA", "2 HEXA", "2 ION", "2 JADE", "2 KAPPA", "2 LAMBDA", "2 MERCURY", "2 NEUTRON", "3 ALPHA", "3 BETA", "3 CRYSTAL", "3 DELTA", "3 EPSILON", "3 FULCRUM", "3 GAMMA", "3 HEXA", "3 ION", "3 JADE", "3 KAPPA", "3 LAMBDA", "3 MERCURY", "3 NEUTRON", "4 ALPHA", "4 BETA", "4 CRYSTAL", "4 DELTA", "4 EPSILON", "4 FULCRUM", "4 GAMMA", "4 HEXA", "4 ION", "4 JADE", "4 KAPPA", "4 LAMBDA", "4 MERCURY", "5 ALPHA", "5 BETA", "5 CRYSTAL", "5 DELTA", "5 EPSILON", "5 FULCRUM", "5 GAMMA", "5 HEXA", "5 ION", "5 JADE", "5 KAPPA", "5 LAMBDA", "5 MERCURY", "6 ATAS 1", "6 ATAS 2", "6 ATAS 3"]
SUBJEK = ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KESUSASTERAAN MELAYU", "KIMIA", "MUET", "MATEMATIK", "MATEMATIK TAMBAHAN", "PEMBINAAN DOMESTIK", "PENDIDIKAN ISLAM", "PJPK", "PENDIDIKAN MORAL", "PENDIDIKAN MUZIK", "PSV", "PENGAJIAN AM", "PERNIAGAAN", "PERTANIAN", "PRINSIP PERAKAUNAN", "RBT", "REKA CIPTA", "SAINS", "SAINS KOMPUTER", "SAINS SUKAN", "SEJARAH", "SENI VISUAL", "TASAWUR ISLAM"]

# --- LOGIK PENGIRAAN SKOR (ASLI PDF) ---
def get_skor_3(i, ii, iii):
    if i and ii and iii: return 4
    if (i and ii) or (i and iii): return 3
    if ii and iii: return 2
    if any([i, ii, iii]): return 1
    return 0

def get_skor_4(i, ii, iii, iv):
    # Ikut corak penskoran Aspek 4.3 dan 4.5
    count = sum([i, ii, iii, iv])
    if count == 4: return 4
    if count == 3: return 3
    if count == 2: return 2
    if count == 1: return 1
    return 0

# --- HEADER PDPC ---
st.title("Sistem Pencerapan PdPc SKPMg2 Standard 4")
st.write("**Lokasi:** SMK Kinarut, Papar")

c1, c2, c3 = st.columns(3)
with c1: guru_sel = st.selectbox("Guru Dicerap", LIST_GURU)
with c2: kelas_sel = st.selectbox("Kelas", KELAS)
with c3: subjek_sel = st.selectbox("Subjek", SUBJEK)

st.divider()

# --- ASPEK 4.1: PERANCANG ---
st.markdown('<span class="section-title">ASPEK 4.1: GURU SEBAGAI PERANCANG</span>', unsafe_allow_html=True)

# 4.1.1 (a)
st.markdown('<div class="item-header">4.1.1 (a) Menyediakan RPH (Objektif & Aktiviti)</div>', unsafe_allow_html=True)
a1 = st.checkbox("i. Mengikut pelbagai aras keupayaan murid", key="411ai")
a2 = st.checkbox("ii. Mengikut peruntukan masa yang ditetapkan", key="411aii")
a3 = st.checkbox("iii. Mematuhi arahan kurikulum/ketetapan", key="411aiii")
s411a = get_skor_3(a1, a2, a3)
st.markdown(f'<div class="score-badge">Skor: {s411a}</div>', unsafe_allow_html=True)

# 4.1.1 (b)
st.markdown('<div class="item-header">4.1.1 (b) Menentukan Kaedah Pentaksiran</div>', unsafe_allow_html=True)
b1 = st.checkbox("i. Mengikut pelbagai aras keupayaan murid", key="411bi")
b2 = st.checkbox("ii. Mengikut peruntukan masa yang ditetapkan", key="411bii")
b3 = st.checkbox("iii. Mematuhi arahan kurikulum/ketetapan", key="411biii")
s411b = get_skor_3(b1, b2, b3)
st.markdown(f'<div class="score-badge">Skor: {s411b}</div>', unsafe_allow_html=True)

# 4.1.1 (c)
st.markdown('<div class="item-header">4.1.1 (c) Menyediakan ABM/BBM/BBB/TMK</div>', unsafe_allow_html=True)
c1 = st.checkbox("i. Mengikut pelbagai aras keupayaan murid", key="411ci")
c2 = st.checkbox("ii. Mengikut peruntukan masa yang ditetapkan", key="411cii")
c3 = st.checkbox("iii. Mematuhi arahan kurikulum/ketetapan", key="411ciii")
s411c = get_skor_3(c1, c2, c3)
st.markdown(f'<div class="score-badge">Skor: {s411c}</div>', unsafe_allow_html=True)

# --- ASPEK 4.2: PENGAWAL ---
st.markdown('<span class="section-title">ASPEK 4.2: GURU SEBAGAI PENGAWAL</span>', unsafe_allow_html=True)
st.markdown('<div class="item-header">4.2.1: Mengawal Proses Pembelajaran</div>', unsafe_allow_html=True)
p1 = st.checkbox("i. Menepati objektif pelajaran", key="421i")
p2 = st.checkbox("ii. Mengikut pelbagai aras keupayaan/pembelajaran terbeza", key="421ii")
p3 = st.checkbox("iii. Dari semasa ke semasa", key="421iii")
s421 = get_skor_3(p1, p2, p3)
st.markdown(f'<div class="score-badge">Skor: {s421}</div>', unsafe_allow_html=True)

st.markdown('<div class="item-header">4.2.2: Mengawal Suasana Pembelajaran</div>', unsafe_allow_html=True)
q1 = st.checkbox("i. Secara berhemah/mengikut kesesuaian", key="422i")
q2 = st.checkbox("ii. Secara menyeluruh meliputi semua murid", key="422ii")
q3 = st.checkbox("iii. Dari semasa ke semasa", key="422iii")
s422 = get_skor_3(q1, q2, q3)
st.markdown(f'<div class="score-badge">Skor: {s422}</div>', unsafe_allow_html=True)

# --- ASPEK 4.3: PEMBIMBING ---
st.markdown('<span class="section-title">ASPEK 4.3: GURU SEBAGAI PEMBIMBING</span>', unsafe_allow_html=True)
st.markdown('<div class="item-header">4.3.1: Membimbing murid secara profesional</div>', unsafe_allow_html=True)
r1 = st.checkbox("i. Mengikut keperluan/pelbagai aras keupayaan", key="431i")
r2 = st.checkbox("ii. Dengan betul dan tepat", key="431ii")
r3 = st.checkbox("iii. Secara berhemah", key="431iii")
r4 = st.checkbox("iv. Bersungguh-sungguh", key="431iv")
s431 = get_skor_4(r1, r2, r3, r4)
st.markdown(f'<div class="score-badge">Skor: {s431}</div>', unsafe_allow_html=True)

# --- ASPEK 4.4: PENDORONG ---
st.markdown('<span class="section-title">ASPEK 4.4: GURU SEBAGAI PENDORONG</span>', unsafe_allow_html=True)
st.markdown('<div class="item-header">4.4.1: Mendorong minda murid (Kognitif)</div>', unsafe_allow_html=True)
m1 = st.checkbox("i. Berdasarkan objektif pelajaran", key="441i")
m2 = st.checkbox("ii. Mengikut aras kepelbagaian murid", key="441ii")
m3 = st.checkbox("iii. Dari semasa ke semasa", key="441iii")
s441 = get_skor_3(m1, m2, m3)
st.markdown(f'<div class="score-badge">Skor: {s441}</div>', unsafe_allow_html=True)

st.markdown('<div class="item-header">4.4.2: Mendorong emosi murid (Afektif)</div>', unsafe_allow_html=True)
e1 = st.checkbox("i. Secara berhemah", key="442i")
e2 = st.checkbox("ii. Secara menyeluruh kepada semua murid", key="442ii")
e3 = st.checkbox("iii. Dari semasa ke semasa", key="442iii")
s442 = get_skor_3(e1, e2, e3)
st.markdown(f'<div class="score-badge">Skor: {s442}</div>', unsafe_allow_html=True)

# --- ASPEK 4.5: PENILAI ---
st.markdown('<span class="section-title">ASPEK 4.5: GURU SEBAGAI PENILAI</span>', unsafe_allow_html=True)
st.markdown('<div class="item-header">4.5.1: Melaksanakan penilaian secara sistematik</div>', unsafe_allow_html=True)
n1 = st.checkbox("i. Berdasarkan objektif pelajaran", key="451i")
n2 = st.checkbox("ii. Ikut arahan pelaksanaan pentaksiran yang berkuat kuasa", key="451ii")
n3 = st.checkbox("iii. Secara menyeluruh kepada semua murid", key="451iii")
n4 = st.checkbox("iv. Dari semasa ke semasa", key="451iv")
s451 = get_skor_4(n1, n2, n3, n4)
st.markdown(f'<div class="score-badge">Skor: {s451}</div>', unsafe_allow_html=True)

# --- ASPEK 4.6: MURID AKTIF (LOGIK PENGLIBATAN + KRITERIA) ---
st.markdown('<span class="section-title">ASPEK 4.6: MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
st.markdown('<div class="item-header">4.6.1: Melibatkan diri secara berkesan</div>', unsafe_allow_html=True)
pct = st.selectbox("Peratus Murid Terlibat:", ["90%-100%", "80%-89%", "50%-79%", "1%-49%", "0%"])
k1 = st.checkbox("ii. Selaras dengan objektif pelajaran", key="46k1")
k2 = st.checkbox("iii. Dengan yakin", key="46k2")
k3 = st.checkbox("iv. Secara berhemah/Bersungguh-sungguh", key="46k3")

# Logik Skor 4.6 mengikut mukasurat 22 PDF
if pct == "90%-100%" and k1 and k2 and k3: s461 = 4
elif pct == "80%-89%" and (sum([k1, k2, k3]) >= 2): s461 = 3
elif pct == "50%-79%" and (sum([k1, k2, k3]) >= 1): s461 = 2
elif pct == "1%-49%": s461 = 1
else: s461 = 0
st.markdown(f'<div class="score-badge">Skor: {s461}</div>', unsafe_allow_html=True)

# --- TOTAL RUMUSAN ---
total_skpm = (s411a + s411b + s411c + s421 + s422 + s431 + s441 + s442 + s451 + s461)
peratus_final = (total_skpm / 40) * 100

st.markdown(f"""
    <div class="total-card">
        <h3>Keputusan Penilaian Standard 4</h3>
        <h1 style="color:#1E88E5;">{peratus_final:.2f}%</h1>
        <p>Mata Skor Diperolehi: <b>{total_skpm} / 40</b></p>
    </div>
""", unsafe_allow_html=True)

# --- JANA LAPORAN ---
if st.button("🚀 JANA ULASAN AI BERDASARKAN SKOR"):
    if guru_sel == "--- Pilih Nama Guru ---":
        st.warning("Sila pilih nama guru terlebih dahulu!")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Tulis ulasan profesional untuk guru {guru_sel} (Subjek: {subjek_sel}, Kelas: {kelas_sel}) berdasarkan skor SKPMg2 Standard 4: {peratus_final}%. Nyatakan Kekuatan dan Penambahbaikan."
            res = model.generate_content(prompt)
            st.info("Ulasan Dijana:")
            st.write(res.text)
        except:
            st.error("Ralat: Sila pastikan API Key ada di 'Secrets'.")
