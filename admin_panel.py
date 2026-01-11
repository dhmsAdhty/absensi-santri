import streamlit as st
from firebase_config import add_pengurus, get_all_pengurus, update_pengurus_status, delete_pengurus
from auth import get_current_user
from rekap_panel import show_rekap_panel
import pandas as pd

def show_admin_panel():
    """Tampilkan panel admin untuk mengelola pengurus"""
    current_user = get_current_user()
    
    if current_user['role'] != 'admin':
        st.error("❌ Akses ditolak! Hanya admin yang dapat mengakses halaman ini.")
        return
    
    # CSS untuk tema hijau yang sama dengan presensi
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f8fffe 0%, #f0f9f7 100%);
        }
        
        /* Header Styles */
        .admin-header {
            text-align: center;
            color: #1e7e34;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            font-weight: 700;
            margin: 1rem 0 2rem 0;
            letter-spacing: -0.02em;
        }
        
        .admin-subtitle {
            text-align: center;
            color: #28a745;
            font-size: clamp(1rem, 2.5vw, 1.2rem);
            font-weight: 400;
            margin-bottom: 2rem;
            opacity: 0.8;
        }
        
        /* Card Styles */
        .admin-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.1);
            border: 1px solid rgba(40, 167, 69, 0.1);
            margin-bottom: 1.5rem;
        }
        
        .stats-card {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.2s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-2px);
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
            background: linear-gradient(135deg, #218838 0%, #1e7e34 100%);
        }
        
        /* Form Elements */
        .stTextInput > div > div > input,
        .stSelectbox > div > div {
            background-color: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            transition: border-color 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within {
            border-color: #28a745;
            box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
        }
        
        /* Tab Styles */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: #495057;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border-color: #28a745;
        }
        
        /* Dataframe Styles */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
        }
        
        /* Expander Styles */
        .streamlit-expanderHeader {
            background-color: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 1rem;
            font-weight: 500;
            color: #495057;
        }
        
        .streamlit-expanderContent {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .admin-header {
                font-size: 1.8rem;
                margin: 0.5rem 0 1rem 0;
            }
            
            .admin-card {
                padding: 1rem;
                margin-bottom: 1rem;
            }
            
            .stButton > button {
                padding: 0.6rem 1rem;
                font-size: 0.9rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header dengan logo yang sama
    st.markdown("""
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="admin-header">Panel Administrator</h1>', unsafe_allow_html=True)
    
    # Navigation untuk admin panel
    admin_page = st.radio(
        "Pilih Menu:",
        ["👥 Manajemen Pengurus", "📊 Rekapan Presensi", "🗑️ Kelola Presensi"],
        horizontal=True
    )
    
    if admin_page == "📊 Rekapan Presensi":
        show_rekap_panel()
        return
    
    if admin_page == "🗑️ Kelola Presensi":
        show_manage_presensi()
        return
   
    
    # Tabs untuk berbagai fungsi admin
    tab1, tab2, tab3 = st.tabs(["➕ Tambah Pengurus", "👥 Kelola Pengurus", "📊 Statistik"])
    
    with tab1:
        st.markdown("### ➕ Tambah Pengurus Baru")
        
        with st.form("add_pengurus_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("👤 Username", placeholder="contoh: wisnu")
                new_name = st.text_input("📝 Nama Lengkap", placeholder="contoh: Kg Wisnu")
            
            with col2:
                new_password = st.text_input("🔒 Password", type="password", placeholder="Minimal 6 karakter")
                confirm_password = st.text_input("🔒 Konfirmasi Password", type="password")
            
            submit_button = st.form_submit_button("➕ Tambah Pengurus", use_container_width=True)
            
            if submit_button:
                if not all([new_username, new_name, new_password, confirm_password]):
                    st.error("❌ Semua field harus diisi!")
                elif new_password != confirm_password:
                    st.error("❌ Password dan konfirmasi password tidak sama!")
                elif len(new_password) < 6:
                    st.error("❌ Password minimal 6 karakter!")
                else:
                    success, message = add_pengurus(new_username, new_password, new_name, current_user['username'])
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    with tab2:
        st.markdown("### 👥 Kelola Pengurus")
        
        pengurus_list = get_all_pengurus()
        
        if pengurus_list:
            # Tampilkan dalam bentuk tabel yang interaktif
            df = pd.DataFrame(pengurus_list)
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(
                df[['username', 'name', 'active', 'created_at', 'created_by']], 
                use_container_width=True,
                column_config={
                    'username': 'Username',
                    'name': 'Nama Lengkap',
                    'active': st.column_config.CheckboxColumn('Status Aktif'),
                    'created_at': 'Dibuat Pada',
                    'created_by': 'Dibuat Oleh'
                }
            )
            
            st.markdown("---")
            st.markdown("### ⚙️ Aksi Pengurus")
            
            # Pilih pengurus untuk dikelola
            pengurus_options = {p['username']: f"{p['name']} (@{p['username']})" for p in pengurus_list}
            selected_pengurus = st.selectbox("Pilih Pengurus", options=list(pengurus_options.keys()), 
                                           format_func=lambda x: pengurus_options[x])
            
            if selected_pengurus:
                selected_data = next(p for p in pengurus_list if p['username'] == selected_pengurus)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if selected_data['active']:
                        if st.button("🚫 Nonaktifkan", use_container_width=True):
                            if update_pengurus_status(selected_pengurus, False):
                                st.success("✅ Pengurus berhasil dinonaktifkan")
                                st.rerun()
                    else:
                        if st.button("✅ Aktifkan", use_container_width=True):
                            if update_pengurus_status(selected_pengurus, True):
                                st.success("✅ Pengurus berhasil diaktifkan")
                                st.rerun()
                
                with col2:
                    if st.button("🔄 Reset Password", use_container_width=True):
                        # Implementasi reset password bisa ditambahkan nanti
                        st.info("Fitur reset password akan segera tersedia")
                
                with col3:
                    if st.button("🗑️ Hapus Pengurus", use_container_width=True, type="secondary"):
                        # Konfirmasi hapus
                        if st.session_state.get('confirm_delete') != selected_pengurus:
                            st.session_state.confirm_delete = selected_pengurus
                            st.warning("⚠️ Klik sekali lagi untuk konfirmasi hapus!")
                        else:
                            if delete_pengurus(selected_pengurus):
                                st.success("✅ Pengurus berhasil dihapus")
                                if 'confirm_delete' in st.session_state:
                                    del st.session_state.confirm_delete
                                st.rerun()
        else:
            st.info("📝 Belum ada pengurus yang terdaftar")
    
    with tab3:
        st.markdown("### 📊 Statistik Sistem")
        
        pengurus_list = get_all_pengurus()
        total_pengurus = len(pengurus_list)
        active_pengurus = len([p for p in pengurus_list if p['active']])
        inactive_pengurus = total_pengurus - active_pengurus
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👥 Total Pengurus", total_pengurus)
        
        with col2:
            st.metric("✅ Pengurus Aktif", active_pengurus)
        
        with col3:
            st.metric("🚫 Pengurus Nonaktif", inactive_pengurus)
        
        if pengurus_list:
            # Chart status pengurus
            status_data = pd.DataFrame({
                'Status': ['Aktif', 'Nonaktif'],
                'Jumlah': [active_pengurus, inactive_pengurus]
            })
            
            st.bar_chart(status_data.set_index('Status'))
            
            # Tabel detail pengurus
            st.markdown("### 📋 Detail Pengurus")
            df_detail = pd.DataFrame(pengurus_list)
            df_detail['created_at'] = pd.to_datetime(df_detail['created_at']).dt.strftime('%Y-%m-%d')
            st.dataframe(df_detail, use_container_width=True)

def show_manage_presensi():
    """Tampilkan panel kelola presensi untuk admin"""
    from firebase_config import get_all_presensi_for_admin, delete_presensi
    from rekap_panel import get_day_name
    
    st.markdown('<h1 class="admin-header">🗑️ Kelola Presensi</h1>', unsafe_allow_html=True)
    st.markdown("### Hapus atau kelola data presensi yang sudah tersimpan")
    
    # Ambil semua data presensi
    presensi_list = get_all_presensi_for_admin()
    
    if not presensi_list:
        st.info("📝 Belum ada data presensi yang tersimpan")
        return
    
    # Filter berdasarkan bulan
    st.markdown("#### 🔍 Filter Data")
    col1, col2 = st.columns(2)
    
    with col1:
        # Ambil tahun yang tersedia
        available_years = sorted(list(set([p['tanggal'][:4] for p in presensi_list if p['tanggal']])), reverse=True)
        selected_year = st.selectbox("Tahun", available_years, index=0 if available_years else None)
    
    with col2:
        # Ambil bulan yang tersedia untuk tahun terpilih
        if selected_year:
            available_months = sorted(list(set([int(p['tanggal'][5:7]) for p in presensi_list 
                                              if p['tanggal'] and p['tanggal'].startswith(selected_year)])))
            month_names = ["Semua Bulan"] + [
                ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                 "Juli", "Agustus", "September", "Oktober", "November", "Desember"][m-1] 
                for m in available_months
            ]
            selected_month_idx = st.selectbox("Bulan", range(len(month_names)), 
                                            format_func=lambda x: month_names[x])
            selected_month = available_months[selected_month_idx - 1] if selected_month_idx > 0 else None
        else:
            selected_month = None
    
    # Filter data berdasarkan pilihan
    filtered_data = presensi_list
    if selected_year:
        filtered_data = [p for p in filtered_data if p['tanggal'] and p['tanggal'].startswith(selected_year)]
    if selected_month:
        month_str = f"{selected_month:02d}"
        filtered_data = [p for p in filtered_data if p['tanggal'] and p['tanggal'][5:7] == month_str]
    
    # Tampilkan statistik
    st.markdown("#### 📊 Statistik")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total Data", len(filtered_data))
    
    with col2:
        tingkat_1_count = len([p for p in filtered_data if p['tingkat'] == 'Tingkat 1'])
        st.metric("🎓 Tingkat 1", tingkat_1_count)
    
    with col3:
        tingkat_2_count = len([p for p in filtered_data if p['tingkat'] == 'Tingkat 2'])
        st.metric("🎓 Tingkat 2", tingkat_2_count)
    
    with col4:
        total_hadir = sum([p['total_hadir'] for p in filtered_data])
        st.metric("👥 Total Kehadiran", total_hadir)
    
    # Tabel data presensi
    st.markdown("#### 📋 Data Presensi")
    
    if filtered_data:
        # Buat DataFrame untuk ditampilkan
        display_data = []
        for p in filtered_data:
            hari = get_day_name(p['tanggal']) if p['tanggal'] else "Unknown"
            persentase = (p['total_hadir'] / p['total_santri'] * 100) if p['total_santri'] > 0 else 0
            
            display_data.append({
                'ID': p['id'],
                'Tanggal': p['tanggal'],
                'Hari': hari,
                'Tingkat': p['tingkat'],
                'Pengurus': p['pengurus'],
                'Hadir': f"{p['total_hadir']}/{p['total_santri']}",
                'Persentase': f"{persentase:.1f}%",
                'Input By': p['input_by'],
                'Aksi': '🗑️'
            })
        
        df_display = pd.DataFrame(display_data)
        
        # Tampilkan tabel dengan pagination
        items_per_page = 10
        total_pages = (len(df_display) - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox("Halaman", range(1, total_pages + 1), index=0)
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            df_page = df_display.iloc[start_idx:end_idx]
        else:
            df_page = df_display
        
        # Tampilkan tabel
        st.dataframe(df_page.drop('ID', axis=1), use_container_width=True)
        
        # Bagian hapus data
        st.markdown("#### 🗑️ Hapus Data Presensi")
        st.warning("⚠️ **Peringatan:** Penghapusan data tidak dapat dibatalkan!")
        
        # Pilih data untuk dihapus
        presensi_options = {}
        for p in filtered_data:
            hari = get_day_name(p['tanggal']) if p['tanggal'] else "Unknown"
            label = f"{p['tanggal']} ({hari}) - {p['tingkat']} - {p['pengurus']}"
            presensi_options[p['id']] = label
        
        selected_presensi = st.selectbox(
            "Pilih data yang akan dihapus:",
            options=list(presensi_options.keys()),
            format_func=lambda x: presensi_options[x],
            index=None,
            placeholder="-- Pilih data presensi --"
        )
        
        if selected_presensi:
            # Tampilkan detail data yang akan dihapus
            selected_data = next(p for p in filtered_data if p['id'] == selected_presensi)
            
            with st.expander("📋 Detail Data yang Akan Dihapus"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Tanggal:** {selected_data['tanggal']}")
                    st.write(f"**Hari:** {get_day_name(selected_data['tanggal'])}")
                    st.write(f"**Tingkat:** {selected_data['tingkat']}")
                    st.write(f"**Pengurus:** {selected_data['pengurus']}")
                
                with col2:
                    st.write(f"**Kehadiran:** {selected_data['total_hadir']}/{selected_data['total_santri']}")
                    st.write(f"**Diinput oleh:** {selected_data['input_by']}")
                    st.write(f"**Waktu input:** {selected_data['created_at']}")
                
                # Tampilkan santri yang tidak hadir jika ada
                alasan_data = selected_data.get('alasan_tidak_hadir', {})
                santri_data = selected_data.get('santri', {})
                santri_tidak_hadir = [nama for nama, hadir in santri_data.items() if not hadir]
                
                if santri_tidak_hadir:
                    st.write("**Santri tidak hadir:**")
                    for nama in santri_tidak_hadir:
                        alasan = alasan_data.get(nama, "Tidak ada keterangan")
                        st.write(f"- {nama}: {alasan}")
            
            # Tombol hapus dengan konfirmasi
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                if st.button("🗑️ Hapus Data Presensi", use_container_width=True, type="secondary"):
                    # Konfirmasi hapus
                    confirm_key = f'confirm_delete_presensi_{selected_presensi}'
                    if st.session_state.get(confirm_key) != selected_presensi:
                        st.session_state[confirm_key] = selected_presensi
                        st.error("⚠️ Klik sekali lagi untuk konfirmasi hapus!")
                    else:
                        # Hapus data
                        success, message = delete_presensi(selected_presensi)
                        if success:
                            st.success(f"✅ {message}")
                            # Hapus session state konfirmasi
                            if confirm_key in st.session_state:
                                del st.session_state[confirm_key]
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
    else:
        st.info("📝 Tidak ada data presensi untuk filter yang dipilih")
    
    # Tips keamanan
    with st.expander("💡 Tips Keamanan"):
        st.markdown("""
        **Sebelum menghapus data:**
        - Pastikan data yang akan dihapus benar-benar salah atau duplikat
        - Backup data jika diperlukan
        - Data yang sudah dihapus tidak dapat dikembalikan
        
        **Kapan menghapus data:**
        - Data input salah tanggal
        - Data duplikat
        - Data test/percobaan
        - Koreksi kesalahan input
        """)