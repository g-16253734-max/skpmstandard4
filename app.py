import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Pencerapan SMK Kinarut", layout="centered")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 8px; padding-left: 25px; }
    .stSubheader { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 5px; margin-top: 45px;}
    .section-title { font-weight: bold; background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-top: 25px; display: block; border-left: 6px solid #1E88E5; color: #333; }
    .spacer { margin-bottom: 35px; border-bottom: 1px solid #eee; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE KELAS ---
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 CRYSTAL", "1 DELTA", "1 EPSILON", "1 FULCRUM", "1 GAMMA", "1 HEXA", "1 ION", "1 JADE", "1 KAPPA", "1 LAMBDA", "1 MERCURY", "1 NEUTRON", "2 ALPHA", "2 BETA", "2 CRYSTAL", "2 DELTA", "2 EPSILON", "2 FULCRUM", "2 GAMMA", "2 HEXA", "2 ION", "2 JADE", "2 KAPPA", "2 LAMBDA", "2 MERCURY", "2 NEUTRON", "3 ALPHA", "3 BETA", "3 CRYSTAL", "3 DELTA", "3 EPSILON", "3 FULCRUM", "3 GAMMA", "3 HEXA", "3 ION", "3 JADE", "3 KAPPA", "3 LAMBDA", "3 MERCURY", "3 NEUTRON", "4 ALPHA", "4 BETA", "4 CRYSTAL", "4 DELTA", "4 EPSILON", "4 FULCRUM", "4 GAMMA", "4 HEXA", "4 ION", "4 JADE", "4 KAPPA", "4 LAMBDA", "4 MERCURY", "5 ALPHA", "5 BETA", "5 CRYSTAL", "5 DELTA", "5 EPSILON", "5 FULCRUM", "5 GAMMA", "5 HEXA", "5 ION", "5 JADE", "5 KAPPA", "5 LAMBDA", "5 MERCURY", "6 ATAS 1", "6 ATAS 2", "6 ATAS 3"]
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
SUBJEK = ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KESUSASTERAAN MELAYU", "KIMIA", "MUET", "MATEMATIK", "MATEMATIK TAMBAHAN", "PEMBINAAN DOMESTIK", "PENDIDIKAN ISLAM", "PJPK", "PENDIDIKAN MORAL", "PENDIDIKAN MUZIK", "PSV", "PENGAJIAN AM", "PERNIAGAAN", "PERTANIAN", "PRINSIP PERAKAUNAN", "RBT", "REKA CIPTA", "SAINS", "SAINS KOMPUTER", "SAINS SUKAN", "SEJARAH", "SENI VISUAL", "TASAWUR ISLAM"]

# --- SIDEBAR ---
st.sidebar.title("🔐 Akses Pentadbir")
pencerap_nama = st.sidebar.text_input("Nama Pencerap:")
jawatan = st.sidebar.selectbox("Jawatan:", ["--- Pilih Jawatan ---", "Pengetua", "PK", "Ketua Bidang", "Ketua Panitia"])
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

# --- UI UTAMA ---
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

# --- STANDARD 4 (KRITERIA PENUH) ---
st.subheader("4.1: GURU SEBAGAI PERANCANG")
st.markdown('<span class="section-title">4.1.1 (a) RPH: Objektif & Aktiviti</span>', unsafe_allow_html=True)
st.checkbox("i. Mengikut aras keupayaan murid", key="411ai")
st.checkbox("ii. Mengikut peruntukan masa yang ditetapkan", key="411aii")
st.checkbox("iii. Mengikut ketetapan kurikulum", key="411aiii")
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.markdown('<span class="section-title">4.1.1 (b) RPH: Pentaksiran</span>', unsafe_allow_html=True)
st.checkbox("i. Mengikut aras keupayaan murid", key="411bi")
st.checkbox("ii. Mengikut peruntukan masa", key="411bii")
st.checkbox("iii. Mengikut ketetapan kurikulum", key="411biii")
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.subheader("4.2: GURU SEBAGAI PENGAWAL")
st.markdown('<span class="section-title">4.2.1 (a) Mengawal proses pembelajaran</span>', unsafe_allow_html=True)
st.checkbox("i. Mengelola isi pelajaran/skop", key="421ai")
st.checkbox("ii. Menepati objektif pembelajaran", key="421aii")
st.checkbox("iii. Mengikut aras keupayaan murid", key="421aiii")
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.subheader("4.6: MURID SEBAGAI PEMBELAJAR AKTIF")
peratus = st.slider("Peratus Pelibatan Murid:", 0, 100, 85)
st.markdown('<span class="section-title">4.6.1 (a) Pelibatan murid secara aktif</span>', unsafe_allow_html=True)
st.checkbox("i. Memberi respon berkaitan isi pelajaran", key="461ai")
st.checkbox("ii. Berkomunikasi dalam aktiviti", key="461aii")
st.checkbox("iii. Menunjukkan kesungguhan/belajar kendiri", key="461aiii")

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
                # 1. Sambung API
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                
                # 2. AUTO-DISCOVER MODEL (Cari model yang tak 404)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Kita cuba cari gemini-1.5-flash dalam senarai, kalau takda guna yang pertama
                model_to_use = "models/gemini-1.5-flash" 
                if model_to_use not in available_models:
                    model_to_use = available_models[0] # Guna apa-apa yang ada
                
                model = genai.GenerativeModel(model_to_use)
                
                # 3. Prompt
                prompt = f"Tulis ulasan profesional SKPMg2 Standard 4 untuk {guru_opt}, Subjek {sub_opt}, Kelas {kls_opt}. Pelibatan murid {peratus}%."
                
                with st.spinner(f'Menjana menggunakan {model_to_use}...'):
                    res = model.generate_content(prompt)
                    st.success("Berjaya!")
                    st.markdown(res.text)
                    st.download_button("Simpan Laporan", res.text, file_name=f"Laporan_{guru_opt}.txt")
            except Exception as e:
                st.error(f"Ralat: {str(e)}")
                st.info("Sila pastikan API Key di 'Secrets' dashboard adalah tepat tanpa tanda pembuka/penutup.")
