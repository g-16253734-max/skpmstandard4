import streamlit as st
import google.generativeai as genai

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Pencerapan SMK Kinarut", layout="centered")

st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; }
    .stSubheader { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 5px; margin-top: 20px;}
    .stHeader { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LENGKAP ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "AHMAD MUSLIM BIN SAMAH", "AIDAH BINTI HANTAR", "AIDY BIN GHANI", "AJIAH BINTI MOHD HAJAR", "ALDRIANA ANDREAS", "ALYANI BINTI KOTLEY", "AMIR HUSSIN BIN MOHD AMIN", "ANIYAH BINTI JOHARI", "ANUGRAH AKHMAD BIN MOHAMAD", "ARITAH BINTI ZAKARIA", "ASMIDAR ASAHARI", "ASNIMAH BINTI ASLIE", "BASRI BIN MUSA", "BEATRICE GANNI", "BIBIANA BINTI JOHNY", "CANAI ANAK BABANG", "CERLOVELA BINTI JOSEPH", "CHIN CHING HSIA", "CHIN TZE JING", "CORNELIA SIMON SAPININ", "CRISTALELIAN JAPLIN", "DG SALEHA BINTI AG LAHAP", "DOLORES PINTOL MOINJIL", "DONA ANAK UNGGANG", "EDNA EDWARD JUAN", "EDWARD BIN APIN", "EILEEN BINTI BINAWAS", "ELIZABETH JERRY", "ELIZABETH LUNA BINTI REYNALDO LUNA", "ESTHER LEONG", "FABIANUS BIN LINUS", "FADILAH BINTI YAMBU", "FAIZAH BT MOHD DIN", "FARIDAH NASIF", "FARIZATUL AKMAM BINTI ARIF", "FARNE BINTI KINSUNG", "FATIMAH BINTI DATO MUTALIB", "FATRINA BINTI MINIS", "FAUZIAH BINTI ABBAS", "FLORA CHONG SUI MI", "FRESCILA DAVID", "HABIBAH BINTI SALLEH", "HANY PUSPITTA BINTI ROHADI", "HARNANI BINTI ALI", "HARTINI BINTI YUSSOF", "HARTINIH BINTI MUSLIM", "HASIFAH BINTI EKING", "HENDRENNA FIFIANA BINTI MOHD JOHAN", "HERDAYANI BINTI AG DAMIT @ MOHD NASIR", "HERMAH BINTI SAPRI", "HII HAI YEN", "IRINEMOLIPAT@ NURSHARINA ABDULLAH", "IRWAN BIN MOHD YUSOF", "ISMAIL BIN HUSSIN", "IZZATI BINTI SHAIFFUDDIN", "JACKQUELINE MOJINA", "JANET GERALD", "JOHANAH BINTI RUSIAN", "JOVIER RYAN JIMON", "JULIANA LEONG SIU FONG", "JULIANAH JAMES", "JULITA BINTI SUTI", "KAMARIYAH BTE MOHAMMAD SERI", "KATINA MATANLUK", "LAI SIU AUN", "LEONA A CANDIA", "LING HUI HSAI", "MAH YUEN CHOI@DANNY MAH", "MAIMUNAH BINTI JUSLEN @ ISMAIL", "MAJID BIN KIFLI", "MARIAHMAH BTE MATLIN", "MARLIZAH BINTI ABD KARIM", "MARYANIE BT BRAHIM", "MASHAYUNI BINTI AWANG BESAR", "MASNIAH BT MUKHTAR", "MASRIDAH BTE EDRIS", "MASUHARNI BT JONGKING", "MISNIE BINTI BUSU", "MOHAMED FAHMI BIN RAMLI", "MOHAMED RASHID BIN MOHAMED JOHAR", "MOHD AMIR BIN ABDUL LATIP", "MOHD RIZAL AIDEY BIN RAIMI", "MOHD SAING BIN HJ HAMZAH", "MUNIRAH BINTI KASSIM", "NADZIRAH BINTI BARSIL", "NAFSIAH BINTI ZAIRUL", "NAJIB BIN ABD LATIFF", "NAJWA SAHIRAH BINTI NORDEEN @ NARUDIN", "NEETU SHAMEETA KOUR", "NETY IRDAWATY", "NG CHEE KEAT", "NOOR AFEZAN @ ANENG BINTI JAFFAR", "NOORHAIDATUL ASMAH BINTI AB RAHMAN", "NOR AZIMAH BINTI JUSOH", "NOR EDA RAHAYU BINTI ABDUL RAHMAN", "NOR MUHAMMAD BIN JUHURI", "NOR ZAWARI BIN HARON", "NORAIMAH BINTI JULAH", "NORATINI ABD WAHID", "NORAZRI BIN MAT PIAH", "NORFAREEZIE BIN NORIZAN", "NORHAFIZAH BINTI NERAWI", "NORIMAH BINTI ASMAIL", "NORIZAH BINTI PIUT", "NORJANAH BINTI AHMAD", "NORLAILA BINTI YAAKOB", "NUR AISYAH BINTI HASAN", "NUR ELINA BINTI SAMSUDDIN", "NUR MUNIRAH BINTI MOHD", "NUR SYAFIQAH ANNISA BINTI MOHD YASSIN", "NURAZIMAH BINTI BONGOH", "NURNASUHATUL AISHAH BINTI HARIS", "NURUL IDAYU BINTI ABDUL RAJAK", "OMAR HASHIM BIN A. THALIB", "PHILIP LEE", "POJI BIN AJAMAIN", "RAFLINA BINTI RUSLI", "RAHIPAH BINTI MD JALIL", "RAMATIA BINTI DULLAH", "RITA CHAU @ RITA JOSEPH", "ROHANA BTE LATIP", "ROMLAN BIN MOHAMMAD", "ROSNAZARIZAH BINTI A. RAHMAN", "ROZY@REGINA JIMMY", "RUMAD BIN ABD RASHID", "RUPIDAH BINTI SAPPIN", "SALMIE BINTI BUSU", "SANIMAH BINTI ARRIS", "SANRA BINTI AMILASAN", "SARAH@SYRA BINTI SADAT", "SHAREN MEMALYN MENSON", "SHARIFA BINTI ABD RAZAK", "SHIRLEY CLARENCE", "SHIRLEY MAGDELIN LAWRENCE", "SIMAA SHAKIRAH BINTI SABUDIN", "SITI HAFIZAH BINTI AWANG", "SITI NUR AFIZAH BINTI SANDRIKI", "SITI WANDAN KARTINI BINTI MOHD FIRDAUS", "SOPIAH HIRWANA BINTI AMBO MASE", "SUHAIMI BIN ABD HAMID", "SULIANI BINTI DANNY", "SUSAN ARGO", "SUTIAH BINTI SALIH", "SYAKINA BINTI SALLEH", "SYAZWANI BT SAWANG", "SYLVIA ZENO", "UMI HAJJAR BINTI MUSLIM", "VERILEY BINTI VERUS", "WULAN BINTI MURUSALIN", "YAP KET KIUN", "YEOH LI-ANN", "ZAINAB BINTI JULASRIN", "ZAINUDDIN BIN AG. JALIL", "ZAMHARIR BIN AHMAD", "ZARINAH BINTI MULUK", "ZUHAMAH @ JUANAH BINTI SAPLI", "ZURIDAH @ ZURAIDAH BINTI HARITH"]
SUBJEK = ["--- Pilih Subjek ---", "ASAS SAINS KOMPUTER", "BAHASA INGGERIS", "BAHASA MELAYU", "BIOLOGI", "EKONOMI", "FIZIK", "GEOGRAFI", "KESUSASTERAAN MELAYU", "KIMIA", "MUET", "MATEMATIK", "MATEMATIK TAMBAHAN", "PEMBINAAN DOMESTIK", "PENDIDIKAN ISLAM", "PJPK", "PENDIDIKAN MORAL", "PENDIDIKAN MUZIK", "PSV", "PENGAJIAN AM", "PERNIAGAAN", "PERTANIAN", "PRINSIP PERAKAUNAN", "RBT", "REKA CIPTA", "SAINS", "SAINS KOMPUTER", "SAINS SUKAN", "SEJARAH", "SENI VISUAL", "TASAWUR ISLAM"]
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "1 BETA", "1 GAMMA", "1 DELTA", "2 ALPHA", "2 BETA", "2 GAMMA", "2 DELTA", "3 ALPHA", "3 BETA", "3 GAMMA", "3 DELTA", "4 ALPHA", "4 BETA", "4 GAMMA", "5 ALPHA", "5 BETA", "6 ATAS 1", "6 ATAS 2"]

# --- SIDEBAR ---
st.sidebar.title("🔐 Akses Pentadbir")
pencerap = st.sidebar.text_input("Nama Pencerap:")
jawatan = st.sidebar.selectbox("Jawatan:", ["--- Pilih Jawatan ---", "Pengetua", "PK", "Ketua Bidang", "Ketua Panitia"])
kod_admin = st.sidebar.text_input("Kod Autoriti:", type="password")

# --- UI UTAMA ---
st.title("📋 Sistem Pencerapan SKPMg2")
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
st.info("💡 Tanda (✓) pada kriteria yang dilaksanakan semasa PdPc.")

# --- SEMUA ITEM STANDARD 4 ---
# 4.1
st.subheader("4.1: Guru Sebagai Perancang")
st.write("**4.1.1(a) Penyediaan RPH (Objektif & Aktiviti)**")
c1, c2, c3 = st.columns(3)
t1 = c1.checkbox("Mengikut Aras", key="411ai")
t2 = c2.checkbox("Menepati Masa", key="411aii")
t3 = c3.checkbox("Ikut Kurikulum", key="411aiii")

st.write("**4.1.1(b) Perancangan Pentaksiran**")
c4, c5, c6 = st.columns(3)
t4 = c4.checkbox("Kaedah Tepat", key="411bi")
t5 = c5.checkbox("Masa Sesuai", key="411bii")
t6 = c6.checkbox("Ikut Ketetapan", key="411biii")

st.write("**4.1.1(c) Sumber Pendidikan (BBM)**")
c7, c8, c9 = st.columns(3)
t7 = c7.checkbox("Pelbagai Aras", key="411ci")
t8 = c8.checkbox("Ikut Masa", key="411cii")
t9 = c9.checkbox("Ikut Kurikulum", key="411ciii")

# 4.2
st.subheader("4.2: Guru Sebagai Pengawal")
st.write("**4.2.1 Pengurusan Proses Pembelajaran**")
c10, c11, c12 = st.columns(3)
t10 = c10.checkbox("Kawal Komunikasi", key="421i")
t11 = c11.checkbox("Peluang Murid", key="421ii")
t12 = c12.checkbox("Ikut Masa", key="421iii")

st.write("**4.2.2 Pengurusan Suasana Pembelajaran**")
c13, c14, c15 = st.columns(3)
t13 = c13.checkbox("Berhemah", key="422i")
t14 = c14.checkbox("Menyeluruh", key="422ii")
t15 = c15.checkbox("Berterusan", key="422iii")

# 4.3
st.subheader("4.3: Guru Sebagai Pembimbing")
st.write("**4.3.1 Memberi Tunjuk Ajar/Panduan**")
c16, c17, c18, c19 = st.columns(4)
t16 = c16.checkbox("Betul & Tepat", key="431i")
t17 = c17.checkbox("Ikut Aras", key="431ii")
t18 = c18.checkbox("Berhemah", key="431iii")
t19 = c19.checkbox("Bersungguh", key="431iv")

# 4.4
st.subheader("4.4: Guru Sebagai Pendorong")
st.write("**4.4.1 Mendorong Minda Murid**")
c20, c21, c22 = st.columns(3)
t20 = c20.checkbox("Rangsang Minda", key="441i")
t21 = c21.checkbox("Peluang Respon", key="441ii")
t22 = c22.checkbox("Berterusan", key="441iii")

st.write("**4.4.2 Mendorong Emosi Murid**")
c23, c24, c25 = st.columns(3)
t23 = c23.checkbox("Puji/Galakan", key="442i")
t24 = c24.checkbox("Prihatin", key="442ii")
t25 = c25.checkbox("Yakin Diri", key="442iii")

# 4.5
st.subheader("4.5: Guru Sebagai Penilai")
st.write("**4.5.1 Melaksanakan Pentaksiran**")
c26, c27, c28, c29 = st.columns(4)
t26 = c26.checkbox("Pelbagai Kaedah", key="451i")
t27 = c27.checkbox("Menyeluruh", key="451ii")
t28 = c28.checkbox("Maklum Balas", key="451iii")
t29 = c29.checkbox("Tindakan Susulan", key="451iv")

# 4.6
st.subheader("4.6: Murid Sebagai Pembelajar Aktif")
peratus = st.slider("Peratus Pelibatan Murid:", 0, 100, 85)
st.write("**Kualiti Tindakan Murid**")
c30, c31, c32 = st.columns(3)
t30 = c30.checkbox("Beri Respon", key="46i")
t31 = c31.checkbox("Yakin & Berani", key="46ii")
t32 = c32.checkbox("Saling Membantu", key="46iii")

st.divider()

# --- JANA LAPORAN ---
if st.button("🚀 JANA LAPORAN AI SEKARANG"):
    if guru_opt == "--- Pilih Nama Guru ---" or mod_opt == "--- Pilih Mod ---" or sub_opt == "--- Pilih Subjek ---":
        st.error("Sila lengkapkan maklumat Guru, Subjek dan Mod!")
    elif kod_admin != "KINARUT2024":
        st.error("Kod Autoriti Salah!")
    else:
        try:
            API_KEY = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            data_tanda = {
                "4.1.1": [t1, t2, t3, t4, t5, t6, t7, t8, t9],
                "4.2": [t10, t11, t12, t13, t14, t15],
                "4.3": [t16, t17, t18, t19],
                "4.4": [t20, t21, t22, t23, t24, t25],
                "4.5": [t26, t27, t28, t29],
                "4.6": [t30, t31, t32, peratus]
            }
            
            prompt = f"""
            Tulis ulasan profesional SKPMg2 Standard 4 untuk:
            Guru: {guru_opt}, Subjek: {sub_opt}, Kelas: {kls_opt}, Mod: {mod_opt}.
            Data Tandanan (True=Dibuat, False=Tidak): {data_tanda}.
            
            Hasilkan ulasan dalam Bahasa Melayu yang merangkumi:
            1. Rumusan Kekuatan (berdasarkan item yang ditanda True).
            2. Analisis Kelemahan (fokus pada item yang False).
            3. Cadangan Penambahbaikan yang spesifik dan praktikal.
            """
            
            with st.spinner('Menjana laporan...'):
                res = model.generate_content(prompt)
                st.success("Laporan Siap!")
                st.markdown(res.text)
                st.download_button("Simpan Laporan (.txt)", res.text, file_name=f"Laporan_{guru_opt}.txt")
                
        except Exception as e:
            st.error(f"Sila pastikan API Key betul dalam Secrets. Error: {e}")
