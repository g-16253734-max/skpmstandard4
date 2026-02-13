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
# (Saya ringkaskan di sini, sila masukkan senarai penuh 150+ guru sebelum ini)
LIST_GURU = ["--- Pilih Nama Guru ---", "ABDULLAH BIN AG. PUTEH", "ADINA DUANE JOKINOL", "ZAINUDDIN BIN AG. JALIL"] 
KELAS = ["--- Pilih Kelas ---", "1 ALPHA", "2 DELTA", "3 GAMMA", "4 BETA", "5 ALPHA"]
SUBJEK = ["--- Pilih Subjek ---", "BAHASA MELAYU", "SAINS", "MATEMATIK", "SEJARAH"]

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
