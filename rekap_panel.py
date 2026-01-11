import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from firebase_config import get_monthly_summary, get_weekly_summary, get_santri_attendance_detail
from auth import get_current_user

def show_rekap_panel():
    """Tampilkan panel rekapan untuk admin"""
    current_user = get_current_user()
    
    if current_user['role'] != 'admin':
        st.error("❌ Akses ditolak! Hanya admin yang dapat mengakses rekapan.")
        return
    
    # CSS untuk tema hijau yang sama
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
        .rekap-header {
            text-align: center;
            color: #1e7e34;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            font-weight: 700;
            margin: 1rem 0 2rem 0;
            letter-spacing: -0.02em;
        }
        
        /* Card Styles */
        .rekap-card {
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
        
        /* Download Button Special */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 1rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(40, 167, 69, 0.3);
        }
        
        /* Form Elements */
        .stSelectbox > div > div {
            background-color: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            transition: border-color 0.3s ease;
        }
        
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
            .rekap-header {
                font-size: 1.8rem;
                margin: 0.5rem 0 1rem 0;
            }
            
            .rekap-card {
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
    
    # Tabs untuk berbagai jenis rekapan (hapus tab detail santri)
    tab1, tab2 = st.tabs(["📅 Rekapan Bulanan", "📆 Rekapan Mingguan"])
    
    with tab1:
        show_monthly_recap()
    
    with tab2:
        show_weekly_recap()

def get_day_name(date_str):
    """Konversi tanggal ke nama hari dalam bahasa Indonesia"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        return days[date_obj.weekday()]
    except:
        return "Unknown"

def get_absent_students(summary_data):
    """Ambil daftar santri yang tidak hadir per tanggal dengan alasan"""
    absent_data = []
    
    for record in summary_data['raw_data']:
        santri_data = record.get('santri', {})
        alasan_data = record.get('alasan_tidak_hadir', {})
        absent_students = []
        
        for nama, hadir in santri_data.items():
            if not hadir:
                alasan = alasan_data.get(nama, "Tidak ada keterangan")
                absent_students.append({
                    'nama': nama,
                    'alasan': alasan
                })
        
        if absent_students:
            # Hitung minggu ke berapa dalam bulan
            date_obj = datetime.strptime(record['tanggal'], "%Y-%m-%d")
            week_of_month = (date_obj.day - 1) // 7 + 1
            
            absent_data.append({
                'tanggal': record['tanggal'],
                'hari': get_day_name(record['tanggal']),
                'minggu_ke': week_of_month,
                'tingkat': record['tingkat'],
                'santri_tidak_hadir': absent_students,
                'jumlah_tidak_hadir': len(absent_students)
            })
    
    return absent_data

def show_monthly_recap():
    """Tampilkan rekapan bulanan"""
    st.markdown("### 📅 Rekapan Presensi Bulanan")
    
    # Input bulan dan tahun
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Tahun", range(2024, 2030), index=0)
    with col2:
        month = st.selectbox("Bulan", range(1, 13), 
                           format_func=lambda x: [
                               "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                               "Juli", "Agustus", "September", "Oktober", "November", "Desember"
                           ][x-1])
    
    if st.button("📊 Generate Rekapan Bulanan", use_container_width=True):
        with st.spinner("Menganalisis data..."):
            summary = get_monthly_summary(year, month)
            
            if summary and summary['raw_data']:
                st.markdown('</div>', unsafe_allow_html=True)  # Close input card
                
                # Tampilkan ringkasan umum
                st.markdown('<div class="rekap-card">', unsafe_allow_html=True)
                st.markdown("#### 📈 Ringkasan Umum")
                
                # Hitung total santri tidak hadir
                total_tidak_hadir_t1 = 0
                total_tidak_hadir_t2 = 0
                
                for record in summary['raw_data']:
                    santri_data = record.get('santri', {})
                    tidak_hadir = len([nama for nama, hadir in santri_data.items() if not hadir])
                    
                    if record['tingkat'] == 'Tingkat 1':
                        total_tidak_hadir_t1 += tidak_hadir
                    else:
                        total_tidak_hadir_t2 += tidak_hadir
                
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    st.metric("📅 Total Hari Aktif", summary['total_hari'])
                with col2:
                    st.metric("🎓 Pertemuan Tingkat 1", summary['tingkat_1']['total_pertemuan'])
                with col3:
                    st.metric("🎓 Pertemuan Tingkat 2", summary['tingkat_2']['total_pertemuan'])
                with col4:
                    total_pertemuan = summary['tingkat_1']['total_pertemuan'] + summary['tingkat_2']['total_pertemuan']
                    st.metric("📚 Total Pertemuan", total_pertemuan)
                with col5:
                    st.metric("❌ Tidak Hadir T1", total_tidak_hadir_t1)
                with col6:
                    st.metric("❌ Tidak Hadir T2", total_tidak_hadir_t2)
                
                # Chart kehadiran per tingkat
                st.markdown("#### 📊 Grafik Kehadiran")
                
                # Data untuk chart
                tingkat_data = []
                if summary['tingkat_1']['total_pertemuan'] > 0:
                    avg_hadir_t1 = summary['tingkat_1']['total_hadir'] / summary['tingkat_1']['total_pertemuan']
                    avg_total_t1 = summary['tingkat_1']['total_santri_per_pertemuan'] / summary['tingkat_1']['total_pertemuan']
                    tingkat_data.append({
                        'Tingkat': 'Tingkat 1',
                        'Rata-rata Hadir': avg_hadir_t1,
                        'Rata-rata Total': avg_total_t1,
                        'Persentase': (avg_hadir_t1 / avg_total_t1 * 100) if avg_total_t1 > 0 else 0
                    })
                
                if summary['tingkat_2']['total_pertemuan'] > 0:
                    avg_hadir_t2 = summary['tingkat_2']['total_hadir'] / summary['tingkat_2']['total_pertemuan']
                    avg_total_t2 = summary['tingkat_2']['total_santri_per_pertemuan'] / summary['tingkat_2']['total_pertemuan']
                    tingkat_data.append({
                        'Tingkat': 'Tingkat 2',
                        'Rata-rata Hadir': avg_hadir_t2,
                        'Rata-rata Total': avg_total_t2,
                        'Persentase': (avg_hadir_t2 / avg_total_t2 * 100) if avg_total_t2 > 0 else 0
                    })
                
                if tingkat_data:
                    df_tingkat = pd.DataFrame(tingkat_data)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig_bar = px.bar(df_tingkat, x='Tingkat', y='Rata-rata Hadir', 
                                        title='Rata-rata Kehadiran per Tingkat',
                                        color='Tingkat')
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    with col2:
                        fig_pie = px.pie(df_tingkat, values='Rata-rata Hadir', names='Tingkat',
                                        title='Distribusi Kehadiran')
                        st.plotly_chart(fig_pie, use_container_width=True)
                
                # Tren kehadiran harian
                st.markdown("#### 📈 Tren Kehadiran Harian")
                daily_data = []
                for record in summary['raw_data']:
                    daily_data.append({
                        'Tanggal': record['tanggal'],
                        'Tingkat': record['tingkat'],
                        'Hadir': record['total_hadir'],
                        'Total': record['total_santri'],
                        'Persentase': (record['total_hadir'] / record['total_santri'] * 100) if record['total_santri'] > 0 else 0
                    })
                
                if daily_data:
                    df_daily = pd.DataFrame(daily_data)
                    fig_line = px.line(df_daily, x='Tanggal', y='Persentase', color='Tingkat',
                                      title='Tren Persentase Kehadiran Harian',
                                      markers=True)
                    st.plotly_chart(fig_line, use_container_width=True)
                
                # Daftar santri yang tidak hadir
                st.markdown("#### ❌ Daftar Santri Tidak Hadir")
                absent_data = get_absent_students(summary)
                
                if absent_data:
                    for tingkat in ['Tingkat 1', 'Tingkat 2']:
                        tingkat_absent = [data for data in absent_data if data['tingkat'] == tingkat]
                        
                        if tingkat_absent:
                            st.markdown(f"##### 🎓 {tingkat}")
                            
                            for data in tingkat_absent:
                                with st.expander(f"📅 {data['hari']}, {data['tanggal']} (Minggu ke-{data['minggu_ke']}) - {data['jumlah_tidak_hadir']} santri"):
                                    # Tampilkan dalam format yang rapi dengan alasan
                                    for i, santri_info in enumerate(data['santri_tidak_hadir']):
                                        col1, col2 = st.columns([1, 2])
                                        with col1:
                                            st.write(f"**{santri_info['nama']}**")
                                        with col2:
                                            alasan_text = santri_info['alasan']
                                            if alasan_text and alasan_text != "Tidak ada keterangan":
                                                st.write(f"📝 {alasan_text}")
                                            else:
                                                st.write("📝 *Tidak ada keterangan*")
                else:
                    st.success("🎉 Semua santri hadir lengkap di bulan ini!")
                
                # Tabel detail dengan hari
                st.markdown("#### 📋 Detail Presensi")
                df_detail = pd.DataFrame(summary['raw_data'])
                
                # Tambahkan kolom hari
                df_detail['hari'] = df_detail['tanggal'].apply(get_day_name)
                
                # Reorder kolom
                df_detail = df_detail[['tanggal', 'hari', 'tingkat', 'total_hadir', 'total_santri', 'pengurus', 'input_by']]
                df_detail['persentase'] = (df_detail['total_hadir'] / df_detail['total_santri'] * 100).round(1)
                
                st.dataframe(df_detail, use_container_width=True)
                
                # Export ke CSV - Hanya Semua Tingkat
                st.markdown("#### 📥 Download Data")
                
                # Buat tombol download di tengah
                col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
                
                with col_center2:
                    # CSV Semua Tingkat
                    df_all_tingkat = generate_all_tingkat_attendance_csv(summary)
                    
                    # Cek apakah DataFrame kosong atau None
                    if df_all_tingkat is None or df_all_tingkat.empty:
                        st.warning("⚠️ Tidak ada data untuk didownload")
                        st.button(
                            label="📥 Download Laporan Lengkap",
                            disabled=True,
                            help="Tidak ada data untuk didownload",
                            use_container_width=True
                        )
                    else:
                        csv_all_tingkat = df_all_tingkat.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Laporan Lengkap",
                            data=csv_all_tingkat,
                            file_name=f"LAPORAN_PRESENSI_BULANAN_{year}_{month:02d}.csv",
                            mime="text/csv",
                            help="Download laporan kehadiran lengkap semua santri",
                            use_container_width=True
                        )
            else:
                st.info("📝 Tidak ada data presensi untuk bulan yang dipilih")

def generate_detailed_csv(summary_data):
    """Generate CSV dengan format yang rapi dan bagus"""
    detailed_data = []
    
    # Pastikan summary_data dan raw_data ada
    if not summary_data or 'raw_data' not in summary_data or not summary_data['raw_data']:
        return pd.DataFrame(columns=[
            'TANGGAL', 'HARI', 'TINGKAT', 'PENGURUS_BERTUGAS', 'DIINPUT_OLEH',
            'JUMLAH_HADIR', 'JUMLAH_TOTAL', 'PERSENTASE_KEHADIRAN',
            'DAFTAR_SANTRI_HADIR', 'DAFTAR_SANTRI_TIDAK_HADIR_DAN_ALASAN'
        ])
    
    for record in summary_data['raw_data']:
        santri_data = record.get('santri', {})
        alasan_data = record.get('alasan_tidak_hadir', {})
        
        # Pisahkan santri hadir dan tidak hadir
        santri_hadir = []
        santri_tidak_hadir_detail = []
        
        for nama, hadir in santri_data.items():
            if hadir:
                santri_hadir.append(nama)
            else:
                alasan = alasan_data.get(nama, "Tidak ada keterangan")
                santri_tidak_hadir_detail.append(f"{nama} ({alasan})")
        
        # Format yang lebih rapi
        santri_hadir_str = ", ".join(sorted(santri_hadir)) if santri_hadir else "-"
        santri_tidak_hadir_str = " | ".join(santri_tidak_hadir_detail) if santri_tidak_hadir_detail else "-"
        
        # Buat row untuk CSV dengan format yang rapi
        row = {
            'TANGGAL': record['tanggal'],
            'HARI': get_day_name(record['tanggal']).upper(),
            'TINGKAT': record['tingkat'],
            'PENGURUS_BERTUGAS': record['pengurus'],
            'DIINPUT_OLEH': record.get('input_by', 'Unknown'),
            'JUMLAH_HADIR': record['total_hadir'],
            'JUMLAH_TOTAL': record['total_santri'],
            'PERSENTASE_KEHADIRAN': f"{(record['total_hadir'] / record['total_santri'] * 100):.1f}%" if record['total_santri'] > 0 else "0%",
            'DAFTAR_SANTRI_HADIR': santri_hadir_str,
            'DAFTAR_SANTRI_TIDAK_HADIR_DAN_ALASAN': santri_tidak_hadir_str
        }
        
        detailed_data.append(row)
    
    return pd.DataFrame(detailed_data)

def generate_weekly_detailed_csv(summary_data):
    """Generate CSV detail untuk rekapan mingguan dengan format rapi"""
    detailed_data = []
    
    # Pastikan summary_data dan raw_data ada
    if not summary_data or 'raw_data' not in summary_data or not summary_data['raw_data']:
        return pd.DataFrame(columns=[
            'TANGGAL', 'HARI', 'TINGKAT', 'PENGURUS_BERTUGAS', 'DIINPUT_OLEH',
            'JUMLAH_HADIR', 'JUMLAH_TOTAL', 'PERSENTASE_KEHADIRAN',
            'DAFTAR_SANTRI_HADIR', 'DAFTAR_SANTRI_TIDAK_HADIR_DAN_ALASAN'
        ])
    
    for record in summary_data['raw_data']:
        santri_data = record.get('santri', {})
        alasan_data = record.get('alasan_tidak_hadir', {})
        
        # Pisahkan santri hadir dan tidak hadir
        santri_hadir = []
        santri_tidak_hadir_detail = []
        
        for nama, hadir in santri_data.items():
            if hadir:
                santri_hadir.append(nama)
            else:
                alasan = alasan_data.get(nama, "Tidak ada keterangan")
                santri_tidak_hadir_detail.append(f"{nama} ({alasan})")
        
        # Format yang lebih rapi
        santri_hadir_str = ", ".join(sorted(santri_hadir)) if santri_hadir else "-"
        santri_tidak_hadir_str = " | ".join(santri_tidak_hadir_detail) if santri_tidak_hadir_detail else "-"
        
        # Buat row untuk CSV dengan format yang rapi
        row = {
            'TANGGAL': record['tanggal'],
            'HARI': get_day_name(record['tanggal']).upper(),
            'TINGKAT': record['tingkat'],
            'PENGURUS_BERTUGAS': record['pengurus'],
            'DIINPUT_OLEH': record.get('input_by', 'Unknown'),
            'JUMLAH_HADIR': record['total_hadir'],
            'JUMLAH_TOTAL': record['total_santri'],
            'PERSENTASE_KEHADIRAN': f"{(record['total_hadir'] / record['total_santri'] * 100):.1f}%" if record['total_santri'] > 0 else "0%",
            'DAFTAR_SANTRI_HADIR': santri_hadir_str,
            'DAFTAR_SANTRI_TIDAK_HADIR_DAN_ALASAN': santri_tidak_hadir_str
        }
        
        detailed_data.append(row)
    
    return pd.DataFrame(detailed_data)

def generate_individual_attendance_csv(summary_data, tingkat):
    """Generate CSV dengan format per santri (satu baris per santri)"""
    individual_data = []
    
    # Pastikan summary_data dan raw_data ada
    if not summary_data or 'raw_data' not in summary_data or not summary_data['raw_data']:
        return pd.DataFrame(columns=[
            'NAMA_SANTRI', 'TINGKAT', 'TOTAL_PERTEMUAN', 'JUMLAH_HADIR',
            'JUMLAH_TIDAK_HADIR', 'PERSENTASE_KEHADIRAN', 'KATEGORI_KEHADIRAN',
            'TANGGAL_TIDAK_HADIR', 'ALASAN_KETIDAKHADIRAN'
        ])
    
    # Kumpulkan semua santri dari tingkat yang dipilih
    all_santri = set()
    tingkat_records = [r for r in summary_data['raw_data'] if r['tingkat'] == tingkat]
    
    if not tingkat_records:
        return pd.DataFrame(columns=[
            'NAMA_SANTRI', 'TINGKAT', 'TOTAL_PERTEMUAN', 'JUMLAH_HADIR',
            'JUMLAH_TIDAK_HADIR', 'PERSENTASE_KEHADIRAN', 'KATEGORI_KEHADIRAN',
            'TANGGAL_TIDAK_HADIR', 'ALASAN_KETIDAKHADIRAN'
        ])
    
    for record in tingkat_records:
        santri_data = record.get('santri', {})
        if santri_data:
            all_santri.update(santri_data.keys())
    
    # Buat data per santri
    for santri in sorted(all_santri):
        total_pertemuan = len(tingkat_records)
        hadir_count = 0
        tidak_hadir_dates = []
        alasan_list = []
        
        for record in tingkat_records:
            santri_data = record.get('santri', {})
            alasan_data = record.get('alasan_tidak_hadir', {})
            
            if santri_data.get(santri, False):
                hadir_count += 1
            else:
                tanggal = record['tanggal']
                hari = get_day_name(tanggal)
                alasan = alasan_data.get(santri, "Tidak ada keterangan")
                tidak_hadir_dates.append(f"{tanggal} ({hari})")
                alasan_list.append(f"{tanggal}: {alasan}")
        
        persentase = (hadir_count / total_pertemuan * 100) if total_pertemuan > 0 else 0
        
        # Tentukan kategori kehadiran
        if persentase >= 95:
            kategori = "SANGAT BAIK"
        elif persentase >= 85:
            kategori = "BAIK"
        elif persentase >= 75:
            kategori = "CUKUP"
        else:
            kategori = "PERLU PERHATIAN"
        
        row = {
            'NAMA_SANTRI': santri,
            'TINGKAT': tingkat,
            'TOTAL_PERTEMUAN': total_pertemuan,
            'JUMLAH_HADIR': hadir_count,
            'JUMLAH_TIDAK_HADIR': total_pertemuan - hadir_count,
            'PERSENTASE_KEHADIRAN': f"{persentase:.1f}%",
            'KATEGORI_KEHADIRAN': kategori,
            'TANGGAL_TIDAK_HADIR': " | ".join(tidak_hadir_dates) if tidak_hadir_dates else "-",
            'ALASAN_KETIDAKHADIRAN': " | ".join(alasan_list) if alasan_list else "-"
        }
        
        individual_data.append(row)
    
    return pd.DataFrame(individual_data)
    
def generate_all_tingkat_attendance_csv(summary_data):
    """Generate CSV dengan format per santri untuk SEMUA tingkat"""
    all_data = []
    
    # Pastikan summary_data dan raw_data ada
    if not summary_data or 'raw_data' not in summary_data or not summary_data['raw_data']:
        # Return DataFrame kosong dengan kolom yang benar
        return pd.DataFrame(columns=[
            'NO', 'NAMA_SANTRI', 'TINGKAT', 'TOTAL_PERTEMUAN', 'JUMLAH_HADIR', 
            'JUMLAH_TIDAK_HADIR', 'PERSENTASE_KEHADIRAN', 'KATEGORI_KEHADIRAN', 
            'STATUS_FOLLOWUP', 'TANGGAL_TIDAK_HADIR', 'DETAIL_ALASAN_KETIDAKHADIRAN'
        ])
    
    # Proses untuk kedua tingkat
    for tingkat in ["Tingkat 1", "Tingkat 2"]:
        # Kumpulkan semua santri dari tingkat ini
        all_santri = set()
        tingkat_records = [r for r in summary_data['raw_data'] if r['tingkat'] == tingkat]
        
        if not tingkat_records:
            continue  # Skip jika tidak ada data untuk tingkat ini
        
        for record in tingkat_records:
            santri_data = record.get('santri', {})
            if santri_data:
                all_santri.update(santri_data.keys())
        
        # Buat data per santri
        for santri in sorted(all_santri):
            total_pertemuan = len(tingkat_records)
            hadir_count = 0
            tidak_hadir_dates = []
            alasan_list = []
            
            for record in tingkat_records:
                santri_data = record.get('santri', {})
                alasan_data = record.get('alasan_tidak_hadir', {})
                
                if santri_data.get(santri, False):
                    hadir_count += 1
                else:
                    tanggal = record['tanggal']
                    hari = get_day_name(tanggal)
                    alasan = alasan_data.get(santri, "Tidak ada keterangan")
                    tidak_hadir_dates.append(f"{tanggal} ({hari})")
                    alasan_list.append(f"{tanggal}: {alasan}")
            
            persentase = (hadir_count / total_pertemuan * 100) if total_pertemuan > 0 else 0
            
            # Tentukan kategori kehadiran
            if persentase >= 95:
                kategori = "SANGAT BAIK"
            elif persentase >= 85:
                kategori = "BAIK"
            elif persentase >= 75:
                kategori = "CUKUP"
            else:
                kategori = "PERLU PERHATIAN"
            
            # Tentukan status untuk follow-up
            if persentase < 75:
                status_followup = "PRIORITAS TINGGI"
            elif persentase < 85:
                status_followup = "PERLU PERHATIAN"
            elif persentase < 95:
                status_followup = "PANTAU"
            else:
                status_followup = "BAIK"
            
            row = {
                'NO': len(all_data) + 1,
                'NAMA_SANTRI': santri,
                'TINGKAT': tingkat,
                'TOTAL_PERTEMUAN': total_pertemuan,
                'JUMLAH_HADIR': hadir_count,
                'JUMLAH_TIDAK_HADIR': total_pertemuan - hadir_count,
                'PERSENTASE_KEHADIRAN': f"{persentase:.1f}%",
                'KATEGORI_KEHADIRAN': kategori,
                'STATUS_FOLLOWUP': status_followup,
                'TANGGAL_TIDAK_HADIR': " | ".join(tidak_hadir_dates) if tidak_hadir_dates else "-",
                'DETAIL_ALASAN_KETIDAKHADIRAN': " | ".join(alasan_list) if alasan_list else "-"
            }
            
            all_data.append(row)
    
    # Jika tidak ada data sama sekali, return DataFrame kosong
    if not all_data:
        return pd.DataFrame(columns=[
            'NO', 'NAMA_SANTRI', 'TINGKAT', 'TOTAL_PERTEMUAN', 'JUMLAH_HADIR', 
            'JUMLAH_TIDAK_HADIR', 'PERSENTASE_KEHADIRAN', 'KATEGORI_KEHADIRAN', 
            'STATUS_FOLLOWUP', 'TANGGAL_TIDAK_HADIR', 'DETAIL_ALASAN_KETIDAKHADIRAN'
        ])
    
    # Urutkan berdasarkan tingkat, lalu persentase kehadiran (terendah dulu untuk prioritas)
    df = pd.DataFrame(all_data)
    df = df.sort_values(['TINGKAT', 'PERSENTASE_KEHADIRAN'], ascending=[True, True])
    
    # Reset nomor urut setelah sorting
    df['NO'] = range(1, len(df) + 1)
    
    return df

def show_weekly_recap():
    """Tampilkan rekapan mingguan"""
    st.markdown("### 📆 Rekapan Presensi Mingguan")
    
    # Input tahun dan minggu
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Tahun", range(2024, 2030), index=0, key="week_year")
    with col2:
        week = st.selectbox("Minggu ke-", range(1, 53), index=0)
    
    if st.button("📊 Generate Rekapan Mingguan", use_container_width=True):
        with st.spinner("Menganalisis data..."):
            summary = get_weekly_summary(year, week)
            
            if summary and summary['raw_data']:
                st.markdown('</div>', unsafe_allow_html=True)  # Close input card
                
                st.markdown('<div class="rekap-card">', unsafe_allow_html=True)
                st.markdown(f"#### 📅 Minggu ke-{week} ({summary['start_date']} s/d {summary['end_date']})")
                
                # Tampilkan data per hari
                daily_data = summary['daily_data']
                
                if daily_data:
                    # Buat tabel mingguan
                    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
                    week_table = []
                    
                    start_date = datetime.strptime(summary['start_date'], "%Y-%m-%d")
                    
                    for i, day_name in enumerate(days):
                        current_date = start_date + timedelta(days=i)
                        date_str = current_date.strftime("%Y-%m-%d")
                        
                        row = {
                            'Hari': day_name,
                            'Tanggal': date_str,
                            'Tingkat 1 Hadir': '-',
                            'Tingkat 1 Total': '-',
                            'Tingkat 1 %': '-',
                            'Tingkat 2 Hadir': '-',
                            'Tingkat 2 Total': '-',
                            'Tingkat 2 %': '-'
                        }
                        
                        if date_str in daily_data:
                            if daily_data[date_str]['Tingkat 1']:
                                t1_data = daily_data[date_str]['Tingkat 1']
                                row['Tingkat 1 Hadir'] = t1_data['hadir']
                                row['Tingkat 1 Total'] = t1_data['total']
                                row['Tingkat 1 %'] = f"{(t1_data['hadir']/t1_data['total']*100):.1f}%" if t1_data['total'] > 0 else "0%"
                            
                            if daily_data[date_str]['Tingkat 2']:
                                t2_data = daily_data[date_str]['Tingkat 2']
                                row['Tingkat 2 Hadir'] = t2_data['hadir']
                                row['Tingkat 2 Total'] = t2_data['total']
                                row['Tingkat 2 %'] = f"{(t2_data['hadir']/t2_data['total']*100):.1f}%" if t2_data['total'] > 0 else "0%"
                        
                        week_table.append(row)
                    
                    df_week = pd.DataFrame(week_table)
                    st.dataframe(df_week, use_container_width=True)
                    
                    # Chart kehadiran mingguan
                    chart_data = []
                    for record in summary['raw_data']:
                        chart_data.append({
                            'Tanggal': record['tanggal'],
                            'Hari': get_day_name(record['tanggal']),
                            'Tingkat': record['tingkat'],
                            'Persentase': (record['total_hadir'] / record['total_santri'] * 100) if record['total_santri'] > 0 else 0
                        })
                    
                    if chart_data:
                        df_chart = pd.DataFrame(chart_data)
                        fig = px.bar(df_chart, x='Hari', y='Persentase', color='Tingkat',
                                    title='Persentase Kehadiran Mingguan',
                                    barmode='group')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Export - Hanya Semua Tingkat
                    st.markdown("#### 📥 Download Data")
                    
                    # Buat tombol download di tengah
                    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
                    
                    with col_center2:
                        # CSV Semua Tingkat
                        df_all_tingkat_weekly = generate_all_tingkat_attendance_csv(summary)
                        
                        # Cek apakah DataFrame kosong atau None
                        if df_all_tingkat_weekly is None or df_all_tingkat_weekly.empty:
                            st.warning("⚠️ Tidak ada data untuk didownload")
                            st.button(
                                label="📥 Download Laporan Lengkap",
                                disabled=True,
                                help="Tidak ada data untuk didownload",
                                use_container_width=True
                            )
                        else:
                            csv_all_tingkat_weekly = df_all_tingkat_weekly.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Laporan Lengkap",
                                data=csv_all_tingkat_weekly,
                                file_name=f"LAPORAN_PRESENSI_MINGGUAN_{year}_W{week:02d}.csv",
                                mime="text/csv",
                                help="Download laporan kehadiran lengkap semua santri",
                                use_container_width=True
                            )
                else:
                    st.info("📝 Tidak ada data presensi untuk minggu yang dipilih")
            else:
                st.info("📝 Tidak ada data presensi untuk minggu yang dipilih")