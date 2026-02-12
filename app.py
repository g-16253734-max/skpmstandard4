import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Pencerapan SMK Kinarut", layout="centered")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 4px; padding-left: 30px; }
    .stSubheader { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 5px; margin-top: 30px;}
    .section-title { font-weight: bold; background-color: #f1f3f4; padding: 8px; border-radius: 5px; margin-top: 20px; display: block; color: #202124; border-left: 5px solid #1E88E5; }
    .score-box { float: right; background-color: #e8f0fe; color: #1967d2; padding: 2px 10px; border-radius: 15px; font-weight: bold; font-size: 0.9em; border: 1px solid #1E88E5; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE KELAS & GURU ---
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 CRYSTAL", "1 DELTA", "1 EPSILON", "1 FULCRUM", "1 GAMMA", "1 HEXA", "1 ION", "1 JADE", "1 KAPPA", "1 LAMBDA", "1 MERCURY", "1 NEUTRON", "2 ALPHA", "2 BETA", "2 CRYSTAL", "2 DELTA", "2 EPSILON", "2 FULCRUM", "2 GAMMA", "2 HEXA", "2 ION", "2 JADE", "2 KAPPA", "2 LAMBDA", "2 MERCURY", "2 NEUTRON", "3 ALPHA", "3 BETA", "3 CRYSTAL", "3 DELTA", "3 EPSILON", "3 FULCRUM", "3 GAMMA", "3 HEXA", "3 ION", "3 JADE", "3 KAPPA", "3 LAMBDA", "3 MERCURY", "3 NEUTRON", "4 ALPHA", "4 BETA", "4 CRYSTAL", "4 DELTA", "4 EPSILON", "4 FULCRUM", "4 GAMMA", "4 HEXA", "4 ION", "4 JADE", "4 KAPPA", "4 LAMBDA", "4 MERCURY", "5 ALPHA", "5 BETA", "5 CRYSTAL", "5 DELTA", "5 EPSILON", "5 FULCRUM", "5 GAMMA", "5 HEXA", "5 ION", "5 JADE", "5 KAPPA", "5 LAMBDA", "5 MERCURY", "6 ATAS 1", "6 ATAS 2", "6 ATAS 3"]
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]

# --- SIDEBAR & HEADER ---
st.sidebar.title("🔐 Akses Pentadbir")
pencerap_nama = st.sidebar.text_input("Nama Pencerap:")
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

st.title("📋 Sistem Pencerapan PdPc SMK Kinarut")
st.write(f"**Sekolah:** SMK Kinarut, Papar")
st.divider()

col1, col2 = st.columns(2)
with col1:
    guru_opt = st.selectbox("Guru Dicerap:", LIST_GURU)
    sub_opt = st.selectbox("Subjek:", ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KIMIA", "MATEMATIK", "PENDIDIKAN ISLAM", "PJPK", "PSV", "RBT", "SAINS", "SEJARAH"])
with col2:
    kls_opt = st.selectbox("Kelas:", KELAS)
    mod_opt = st.selectbox("Mod Pencerapan:", ["--- Pilih Mod ---", "Kendiri", "Pertama", "Kedua"])

st.divider()

# --- FUNGSI SKORING ---
def calculate_score(checks):
    return sum(checks)

# --- STANDARD 4 ---

# 4.1
st.subheader("4.1: GURU SEBAGAI PERANCANG")
# 4.1.1 (a)
st.markdown('<span class="section-title">4.1.1 (a) RPH: Menentukan objektif & aktiviti</span>', unsafe_allow_html=True)
a1 = st.checkbox("i. Mengikut aras keupayaan murid", key="411ai")
a2 = st.checkbox("ii. Mengikut peruntukan masa yang ditetapkan", key="411aii")
a3 = st.checkbox("iii. Mengikut ketetapan kurikulum", key="411aiii")
s411a = calculate_score([a1, a2, a3])
st.markdown(f'<div class="score-box">Skor: {s411a} / 3</div>', unsafe_allow_html=True)

# 4.1.1 (b)
st.markdown('<span class="section-title">4.1.1 (b) RPH: Menentukan kaedah pentaksiran</span>', unsafe_allow_html=True)
b1 = st.checkbox("i. Mengikut aras keupayaan murid (Pentaksiran)", key="411bi")
b2 = st.checkbox("ii. Mengikut peruntukan masa (Pentaksiran)", key="411bii")
b3 = st.checkbox("iii. Mengikut ketetapan kurikulum (Pentaksiran)", key="411biii")
s411b = calculate_score([b1, b2, b3])
st.markdown(f'<div class="score-box">Skor: {s411b} / 3</div>', unsafe_allow_html=True)

# 4.2
st.subheader("4.2: GURU SEBAGAI PENGAWAL")
st.markdown('<span class="section-title">4.2.1 (a) Mengawal proses pembelajaran</span>', unsafe_allow_html=True)
c1 = st.checkbox("i. Mengelola isi pelajaran/skop", key="421ai")
c2 = st.checkbox("ii. Menepati objektif pembelajaran", key="421aii")
c3 = st.checkbox("iii. Mengikut aras keupayaan murid secara berterusan", key="421aiii")
s421a = calculate_score([c1, c2, c3])
st.markdown(f'<div class="score-box">Skor: {s421a} / 3</div>', unsafe_allow_html=True)

st.markdown('<span class="section-title">4.2.2 (a) Mengawal suasana pembelajaran</span>', unsafe_allow_html=True)
d1 = st.checkbox("i. Mengurus susun atur murid", key="422ai")
d2 = st.checkbox("ii. Mewujudkan suasana menyeronokkan", key="422aii")
d3 = st.checkbox("iii. Secara berhemah & menyeluruh", key="422aiii")
s422a = calculate_score([d1, d2, d3])
st.markdown(f'<div class="score-box">Skor: {s422a} / 3</div>', unsafe_allow_html=True)

# 4.3
st.subheader("4.3: GURU SEBAGAI PEMBIMBING")
st.markdown('<span class="section-title">4.3.1 (a) Memberi tunjuk ajar/panduan</span>', unsafe_allow_html=True)
e1 = st.checkbox("i. Memberi tunjuk ajar yang betul dan tepat", key="431ai")
e2 = st.checkbox("ii. Mengikut aras keupayaan murid", key="431aii")
e3 = st.checkbox("iii. Secara berhemah & bersungguh-sungguh", key="431aiii")
s431a = calculate_score([e1, e2, e3])
st.markdown(f'<div class="score-box">Skor: {s431a} / 3</div>', unsafe_allow_html=True)

# 4.4
st.subheader("4.4: GURU SEBAGAI PENDORONG")
st.markdown('<span class="section-title">4.4.1 (a) Mendorong minda murid</span>', unsafe_allow_html=True)
f1 = st.checkbox("i. Merangsang murid berkomunikasi", key="441ai")
f2 = st.checkbox("ii. Memberi peluang murid memberi respon", key="441aii")
f3 = st.checkbox("iii. Secara berterusan & berkesan", key="441aiii")
s441a = calculate_score([f1, f2, f3])
st.markdown(f'<div class="score-box">Skor: {s441a} / 3</div>', unsafe_allow_html=True)

st.markdown('<span class="section-title">4.4.2 (a) Mendorong emosi murid</span>', unsafe_allow_html=True)
g1 = st.checkbox("i. Memberi pujian/galakan terhadap perlakuan positif", key="442ai")
g2 = st.checkbox("ii. Memberi keyakinan diri dalam berkomunikasi", key="442aii")
g3 = st.checkbox("iii. Secara berhemah & menyeluruh", key="442aiii")
s442a = calculate_score([g1, g2, g3])
st.markdown(f'<div class="score-box">Skor: {s442a} / 3</div>', unsafe_allow_html=True)

# 4.5
st.subheader("4.5: GURU SEBAGAI PENILAI")
st.markdown('<span class="section-title">4.5.1 (a) Melaksanakan pentaksiran</span>', unsafe_allow_html=True)
h1 = st.checkbox("i. Menggunakan pelbagai kaedah pentaksiran", key="451ai")
h2 = st.checkbox("ii. Memberi maklum balas hasil kerja murid", key="451aii")
h3 = st.checkbox("iii. Secara menyeluruh & berterusan", key="451aiii")
s451a = calculate_score([h1, h2, h3])
st.markdown(f'<div class="score-box">Skor: {s451a} / 3</div>', unsafe_allow_html=True)

# 4.6
st.subheader("4.6: MURID SEBAGAI PEMBELAJAR AKTIF")
peratus = st.slider("Peratus Pelibatan Murid Secara Aktif:", 0, 100, 85)
st.markdown('<span class="section-title">4.6.1 (a) Pelibatan murid secara aktif</span>', unsafe_allow_html=True)
i1 = st.checkbox("i. Memberi respon berkaitan isi pelajaran", key="461ai")
i2 = st.checkbox("ii. Berkomunikasi dalam aktiviti", key="461aii")
i3 = st.checkbox("iii. Menunjukkan kesungguhan/belajar sendiri", key="461aiii")
s461a = calculate_score([i1, i2, i3])
st.markdown(f'<div class="score-box">Skor: {s461a} / 3</div>', unsafe_allow_html=True)

st.divider()

# --- LOGIK JANA ---
if st.button("🚀 JANA LAPORAN AI"):
    if guru_opt == "--- Pilih Nama Guru ---" or kls_opt == "--- Pilih Kelas ---" or mod_opt == "--- Pilih Mod ---":
        st.error("Sila lengkapkan maklumat utama!")
    else:
        authorized = (mod_opt == "Kendiri") or (kod_admin == "KINARUT2024")
        if not authorized:
            st.error("Kod Autoriti Salah!")
        else:
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                # Fallback model selection
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_to_use = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
                
                model = genai.GenerativeModel(model_to_use)
                
                # Sediakan ringkasan skor untuk AI
                skor_summary = f"4.1.1a:{s411a}, 4.1.1b:{s411b}, 4.2.1a:{s421a}, 4.2.2a:{s422a}, 4.3.1a:{s431a}, 4.4.1a:{s441a}, 4.4.2a:{s442a}, 4.5.1a:{s451a}, 4.6.1a:{s461a}. Pelibatan:{peratus}%."
                
                prompt = f"""Sebagai pakar SKPMg2, tulis ulasan pencerapan profesional untuk {guru_opt}, Subjek {sub_opt}, Kelas {kls_opt}. 
                Berdasarkan data skor berikut: {skor_summary}.
                Berikan: 1. Kekuatan utama, 2. Aspek perlu diperbaiki, 3. Cadangan tindakan.
                Tulis dalam Bahasa Melayu yang formal dan membina."""
                
                with st.spinner('Menjana laporan berdasarkan skor...'):
                    res = model.generate_content(prompt)
                    st.success("Laporan Berjaya!")
                    st.markdown(res.text)
                    st.download_button("Simpan Laporan", res.text, file_name=f"Laporan_{guru_opt}.txt")
            except Exception as e:
                st.error(f"Ralat: {str(e)}")
