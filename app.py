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
    /* Menjadikan radio button nampak lebih jelas */
    .stRadio > div { flex-direction: column; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PENGIRAAN ---
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

def hitung_skor_46(p_val, k1, k2, k3):
    count_k = sum([1 for x in [k1, k2, k3] if x])
    if p_val == "50% - 100%":
        if count_k == 3: return 4
        if count_k == 2: return 3
        if count_k == 1: return 2
        return 1
    if p_val == "25% - 49%":
        if count_k >= 2: return 3
        if count_k == 1: return 2
        return 1
    if p_val == "10% - 24%":
        if count_k >= 1: return 2
        return 1
    if p_val == "Kurang 10%":
        return 1
    return 0

# --- DATABASE GURU (DIPENDEKKAN TAPI BOS GUNA SENARAI LENGKAP SEBELUM INI) ---
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "ZAINUDDIN BIN AG. JALIL"] 

# --- UI START ---
st.title("📋 Instrumen Pencerapan SMK Kinarut")

c1, c2, c3 = st.columns(3)
with c1: guru_sel = st.selectbox("Nama Guru", LIST_GURU)
with c2: kls_sel = st.selectbox("Kelas", ["1 ALPHA", "1 BETA", "2 DELTA", "3 GAMMA", "4 BETA", "5 ALPHA", "6 ATAS"])
with c3: sbj_sel = st.selectbox("Subjek", ["BAHASA MELAYU", "SAINS", "MATEMATIK", "SEJARAH"])

total_mata = 0
bil_item = 0

# --- LOOPING UNTUK 4.1 HINGGA 4.5 ---
# (Sila masukkan render_section bos kat sini)

# --- 4.6 (VERSI RADIO - TAKLEH TICK SEMUA) ---
st.markdown('<span class="section-title">4.6: MURID SEBAGAI PEMBELAJAR AKTIF</span>', unsafe_allow_html=True)
items_46 = ["Respon Isi", "Komunikasi", "Kolaboratif", "Respon KBAT", "Kesungguhan", "Kaitkan Isu"]

for i_idx, label in enumerate(items_46):
    k = chr(97 + i_idx)
    st.markdown(f'<div class="item-header">4.6.1 ({k}) {label}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # Guna radio supaya hanya boleh pilih SATU sahaja peratus
        p_pilih = st.radio(f"Pilih Tahap Peratus (i) untuk {k}:", 
                          ["50% - 100%", "25% - 49%", "10% - 24%", "Kurang 10%"], 
                          index=None, key=f"461{k}p")
    
    with col2:
        st.write("**Kriteria Tambahan:**")
        k1 = st.checkbox("ii. Selaras dengan objektif", key=f"461{k}k1")
        k2 = st.checkbox("iii. Dengan yakin", key=f"461{k}k2")
        k3 = st.checkbox("iv. Berhemah / Bersungguh", key=f"461{k}k3")
    
    skor = hitung_skor_46(p_pilih, k1, k2, k3)
    total_mata += skor
    bil_item += 1
    st.markdown(f'<div class="score-badge">Skor: {skor}</div>', unsafe_allow_html=True)
    st.write("---")

# --- RUMUSAN ---
st.divider()
if bil_item > 0:
    final_score = (total_mata / (bil_item * 4)) * 100
    st.markdown(f"""
        <div class="total-card">
            <h2>Keputusan Penuh Pencerapan</h2>
            <h1 style="color:#1E88E5;">{final_score:.2f}%</h1>
            <p>Jumlah Mata: {total_mata} / {bil_item * 4}</p>
        </div>
    """, unsafe_allow_html=True)
