import streamlit as st
import pandas as pd
from datetime import datetime, date
from firebase_config import get_database
from auth import show_login_page, show_logout_button, check_authentication, get_current_user, show_change_password_form
from admin_panel import show_admin_panel

# Konfigurasi halaman
st.set_page_config(
    page_title="Presensi Madin Al Hikmah",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cek autentikasi
if not check_authentication():
    show_login_page()
    st.stop()

# Dapatkan user yang sedang login
current_user = get_current_user()

# Navigation untuk admin
if current_user['role'] == 'admin':
    # Sidebar navigation untuk admin
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        page = st.radio("Pilih Halaman:", ["📚 Presensi", "👨‍💼 Panel Admin"])
    
    if page == "👨‍💼 Panel Admin":
        show_admin_panel()
        st.stop()

# Minimal CSS untuk UI yang clean dan responsif
st.markdown("""
<style>
    /* Import Google Fonts yang lebih clean */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
    }
    
    /* Clean header */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .header-title {
        color: #1e7e34;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.8rem;
    }
    
    .header-subtitle {
        color: #64748b;
        font-weight: 400;
        font-size: 1rem;
    }
    
    /* Clean card design */
    .summary-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* User info in sidebar */
    .user-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #bbf7d0;
        margin-bottom: 1.5rem;
    }
    
    /* Clean checkbox styling */
    .stCheckbox > label {
        font-weight: 400;
        padding: 0.4rem 0;
        margin: 0;
        border-radius: 6px;
        transition: background-color 0.2s;
    }
    
    .stCheckbox > label:hover {
        background-color: #f8fafc;
    }
    
    /* Clean button */
    .stButton > button {
        background: #10b981;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #059669;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.15);
    }
    
    /* Clean progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.5rem;
        }
        
        .summary-card {
            padding: 1rem;
        }
    }
    
    /* Clean scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    /* Form ganti password styling */
    .stTextInput > div > div > input[type="password"] {
        background-color: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.95rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input[type="password"]:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Password form container */
    .password-form {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Data Santri dari Hasil Seleksi
data_tingkat_1 = ["Raffih", "Raffa", "Fahri", "Reyhan", "Nabbih", "Dhobit", "Isham", "Rifqi", "Wilal", "Faiq", "Syafin", "Wildan", "Duha", "Haidar", "Lutfi", "Alkaf", "Fahmal", "Yusuf", "Nayyif", "Tiyo", "Fathir", "Ihsan", "Azka", "Raffif", "Rizki Bengkulu", "Bayu", "Islah", "Arrum Muzakki", "Bintang (7)", "Emil", "Alaik", "Arsya", "Irvan", "Fathkhur", "Zakkariya", "Ilham Kembar", "Nabhan"]
data_tingkat_2 = ["Riski", "Dzarukl", "Anam", "Nurfa", "Qohar", "Mirza", "Bintang (10)", "Ali", "Albas", "Ari", "Kholiq", "Farel", "Azzam", "David", "Rosyad", "Tahsin", "Rilo", "Zuhdan", "Sahal", "Afif", "Fachri", "Wildan Jauhari", "Rafa Fajriya", "Kayza", "Rasheef", "Bondan", "Hilal", "Aziz", "Royyan", "Farid", "Hamdan"]

# Fungsi Firebase
def save_presensi_to_firebase(absensi_data, tingkat, pengurus_name, alasan_data=None):
    """Simpan data presensi ke Firebase Realtime Database"""
    try:
        db = get_database()
        if db is None:
            return False
        
        today = date.today().isoformat()
        current_user = get_current_user()
        
        # Buat struktur data presensi
        presensi_data = {
            'tanggal': today,
            'tingkat': tingkat,
            'pengurus': pengurus_name,
            'input_by': current_user['name'],
            'username': current_user['username'],
            'created_at': datetime.now().isoformat(),
            'santri': absensi_data,
            'alasan_tidak_hadir': alasan_data or {},
            'total_hadir': sum(1 for status in absensi_data.values() if status),
            'total_santri': len(absensi_data)
        }
        
        # Simpan langsung ke path: presensi/{tanggal}_{tingkat}
        path = f"presensi/{today}_{tingkat.replace(' ', '_')}"
        ref = db.reference(path)
        ref.set(presensi_data)
        
        return True
            
    except Exception as e:
        st.error(f"Error menyimpan ke Firebase: {e}")
        return False

def get_presensi_history(limit=10):
    """Ambil riwayat presensi dari Firebase Realtime Database"""
    try:
        db = get_database()
        if db is None:
            return []
        
        ref = db.reference('presensi')
        data = ref.get()
        
        if not data:
            return []
        
        history = []
        for key, value in data.items():
            history.append({
                'id': key,
                'tanggal': value.get('tanggal'),
                'tingkat': value.get('tingkat'),
                'pengurus': value.get('pengurus'),
                'input_by': value.get('input_by', 'Unknown'),
                'total_hadir': value.get('total_hadir', 0),
                'total_santri': value.get('total_santri', 0),
                'created_at': value.get('created_at')
            })
        
        history.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return history[:limit]
    except Exception as e:
        st.error(f"Error mengambil data: {e}")
        return []

# Header clean
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Madin Al Hikmah</h1>
    <p class="header-subtitle">Sistem Presensi Digital • {}</p>
</div>
""".format(datetime.now().strftime("%A, %d %B %Y")), unsafe_allow_html=True)

# Sidebar clean
with st.sidebar:
    # Info user yang login
    st.markdown(f"""
    <div class="user-card">
        <div style="font-size: 0.9rem; color: #166534; margin-bottom: 0.25rem;">👤 Login sebagai</div>
        <div style="font-size: 1rem; font-weight: 600; color: #166534;">{current_user['name']}</div>
        <div style="font-size: 0.85rem; color: #4ade80;">{current_user['role'].title()} • @{current_user['username']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan")
    
    # Form ganti password langsung di pengaturan
    show_change_password_form()
    
    # Pilih tingkat
    st.markdown("---")
    st.markdown("### 🎓 Pilih Tingkat")
    tingkat = st.radio(
        "",
        ["Tingkat 1", "Tingkat 2"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Statistik tingkat
    daftar_nama = data_tingkat_1 if tingkat == "Tingkat 1" else data_tingkat_2
    st.markdown(f"""
    <div class="summary-card">
        <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">Total Santri</div>
        <div style="font-size: 1.5rem; font-weight: 600; color: #1e7e34;">{len(daftar_nama)}</div>
        <div style="font-size: 0.85rem; color: #94a3b8;">{tingkat}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tombol logout
    st.markdown("---")
    show_logout_button()

# Layout utama
col1, col2 = st.columns([3, 1])

with col1:
    # Container untuk daftar hadir
    st.markdown(f"### ✅ Daftar Hadir {tingkat}")
    
    # Buat checkbox dalam grid yang benar
    absensi = {}
    
    # Urutkan nama untuk tampilan yang rapi
    daftar_nama_sorted = sorted(daftar_nama)
    
    # Buat 3 kolom untuk checkbox
    col_a, col_b, col_c = st.columns(3)
    
    # Bagi nama ke dalam 3 kolom
    chunk_size = len(daftar_nama_sorted) // 3
    if len(daftar_nama_sorted) % 3 != 0:
        chunk_size += 1
    
    # Tampilkan checkbox di kolom A
    with col_a:
        for i in range(0, len(daftar_nama_sorted), 3):
            if i < len(daftar_nama_sorted):
                nama = daftar_nama_sorted[i]
                absensi[nama] = st.checkbox(
                    f"{nama}",
                    value=True,
                    key=f"santri_a_{i}"
                )
    
    # Tampilkan checkbox di kolom B
    with col_b:
        for i in range(1, len(daftar_nama_sorted), 3):
            if i < len(daftar_nama_sorted):
                nama = daftar_nama_sorted[i]
                absensi[nama] = st.checkbox(
                    f"{nama}",
                    value=True,
                    key=f"santri_b_{i}"
                )
    
    # Tampilkan checkbox di kolom C
    with col_c:
        for i in range(2, len(daftar_nama_sorted), 3):
            if i < len(daftar_nama_sorted):
                nama = daftar_nama_sorted[i]
                absensi[nama] = st.checkbox(
                    f"{nama}",
                    value=True,
                    key=f"santri_c_{i}"
                )
    
    # Alasan ketidakhadiran
    st.markdown("---")
    
    alasan_data = {}
    if absensi:
        santri_tidak_hadir = [nama for nama, hadir in absensi.items() if not hadir]
        
        if santri_tidak_hadir:
            st.markdown(f"### 📝 Alasan Ketidakhadiran ({len(santri_tidak_hadir)} santri)")
            
            # Input alasan untuk setiap santri yang tidak hadir
            for nama in santri_tidak_hadir:
                alasan = st.text_input(
                    f"Alasan {nama} tidak hadir:",
                    placeholder="Opsional - kosongkan jika tidak perlu",
                    key=f"alasan_{nama}"
                )
                if alasan:
                    alasan_data[nama] = alasan
        else:
            st.success("✅ **Semua santri hadir!**")

with col2:
    # Statistik real-time
    st.markdown("### 📊 Ringkasan")
    
    if absensi:
        total_hadir = sum(1 for status in absensi.values() if status)
        total_santri = len(absensi)
        persentase = (total_hadir / total_santri * 100) if total_santri > 0 else 0
        
        # Tampilkan statistik
        st.markdown(f"""
        <div class="summary-card">
            <div style="font-size: 1.8rem; font-weight: 600; color: #1e7e34;">{total_hadir}/{total_santri}</div>
            <div style="font-size: 0.9rem; color: #64748b;">Santri Hadir</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-card">
            <div style="font-size: 1.8rem; font-weight: 600; color: #1e7e34;">{persentase:.1f}%</div>
            <div style="font-size: 0.9rem; color: #64748b;">Tingkat Kehadiran</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(persentase / 100)

# Tombol simpan
st.markdown("---")
if absensi:
    if st.button("💾 **Simpan Presensi**", use_container_width=True, type="primary"):
        with st.spinner('Menyimpan data...'):
            alasan_untuk_simpan = alasan_data
            
            if save_presensi_to_firebase(absensi, tingkat, current_user['name'], alasan_untuk_simpan):
                total_hadir = sum(1 for status in absensi.values() if status)
                total_santri = len(absensi)
                
                st.success(f"""
                ✅ **Data berhasil disimpan!**
                
                **Detail:**
                - Tingkat: {tingkat}
                - Kehadiran: {total_hadir}/{total_santri} santri
                - Pengurus: {current_user['name']}
                - Dicatat oleh: {current_user['name']}
                """)
                
                # Tampilkan alasan jika ada
                if alasan_untuk_simpan:
                    st.info("**Alasan ketidakhadiran:**")
                    for nama, alasan in alasan_untuk_simpan.items():
                        st.write(f"• **{nama}**: {alasan}")
                
                st.balloons()
            else:
                st.error("❌ Gagal menyimpan data presensi. Silakan coba lagi.")

# Riwayat presensi
st.markdown("---")
st.markdown("### 📋 Riwayat Presensi")

history = get_presensi_history(5)
if history:
    for record in history:
        persen = (record['total_hadir'] / record['total_santri'] * 100) if record['total_santri'] > 0 else 0
        
        with st.expander(f"📅 {record['tanggal']} - {record['tingkat']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Pengurus:** {record['pengurus']}")
                st.write(f"**Dicatat oleh:** {record['input_by']}")
            with col_b:
                st.write(f"**Kehadiran:** {record['total_hadir']}/{record['total_santri']}")
                st.write(f"**Persentase:** {persen:.1f}%")
else:
    st.info("Belum ada data presensi yang tersimpan.")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem 0;">© 2024 Madin Al Hikmah • Sistem Presensi Digital</div>', 
    unsafe_allow_html=True
)