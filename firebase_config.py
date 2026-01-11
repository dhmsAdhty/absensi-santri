import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import os
import hashlib
from datetime import datetime

@st.cache_resource
def initialize_firebase():
    """Initialize Firebase app for Realtime Database"""
    if not firebase_admin._apps:
        # Untuk development, gunakan service account key
        if os.path.exists('madin-al-hikmah-presensi-firebase-adminsdk-fbsvc-299af8422e.json'):
            cred = credentials.Certificate('madin-al-hikmah-presensi-firebase-adminsdk-fbsvc-299af8422e.json')
        else:
            # Fallback untuk deployment (gunakan secrets dari Streamlit)
            try:
                firebase_secrets = st.secrets["firebase"]
                cred = credentials.Certificate({
                    "type": firebase_secrets["type"],
                    "project_id": firebase_secrets["project_id"],
                    "private_key_id": firebase_secrets["private_key_id"],
                    "private_key": firebase_secrets["private_key"],
                    "client_email": firebase_secrets["client_email"],
                    "client_id": firebase_secrets["client_id"],
                    "auth_uri": firebase_secrets["auth_uri"],
                    "token_uri": firebase_secrets["token_uri"],
                    "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
                })
                # Gunakan URL dari secrets jika ada, jika tidak gunakan default
                if "database_url" in firebase_secrets:
                    database_url = firebase_secrets["database_url"]
                else:
                    database_url = 'https://madin-al-hikmah-presensi-default-rtdb.asia-southeast1.firebasedatabase.app/'
            except Exception as e:
                st.error(f"Firebase configuration error: {e}. Please add serviceAccountKey.json or configure Streamlit secrets.")
                return None
        
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
    
    return db

def get_database():
    """Get Realtime Database reference"""
    return initialize_firebase()

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_default_users():
    """Buat user admin default jika belum ada"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return False
        
        users_ref = db_ref.reference('users')
        existing_users = users_ref.get()
        
        if not existing_users:
            # Hanya buat admin default
            default_admin = {
                'admin': {
                    'password': hash_password('admin123'),
                    'name': 'Administrator',
                    'role': 'admin',
                    'active': True,
                    'created_at': datetime.now().isoformat(),
                    'created_by': 'system'
                }
            }
            
            users_ref.set(default_admin)
            return True
        return True
    except Exception as e:
        st.error(f"Error creating default admin: {e}")
        return False

def add_pengurus(username, password, name, created_by_admin):
    """Tambah pengurus baru oleh admin"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return False, "Database connection failed"
        
        users_ref = db_ref.reference('users')
        
        # Cek apakah username sudah ada
        existing_user = users_ref.child(username).get()
        if existing_user:
            return False, "Username sudah digunakan"
        
        # Buat user pengurus baru
        new_pengurus = {
            'password': hash_password(password),
            'name': name,
            'role': 'pengurus',
            'active': True,
            'created_at': datetime.now().isoformat(),
            'created_by': created_by_admin
        }
        
        users_ref.child(username).set(new_pengurus)
        return True, "Pengurus berhasil ditambahkan"
        
    except Exception as e:
        return False, f"Error: {e}"

def get_all_pengurus():
    """Ambil semua data pengurus"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return []
        
        users_ref = db_ref.reference('users')
        all_users = users_ref.get()
        
        if not all_users:
            return []
        
        pengurus_list = []
        for username, data in all_users.items():
            if data.get('role') == 'pengurus':
                pengurus_list.append({
                    'username': username,
                    'name': data.get('name'),
                    'active': data.get('active', True),
                    'created_at': data.get('created_at'),
                    'created_by': data.get('created_by')
                })
        
        return pengurus_list
    except Exception as e:
        st.error(f"Error getting pengurus: {e}")
        return []

def update_pengurus_status(username, active_status):
    """Update status aktif/nonaktif pengurus"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return False
        
        users_ref = db_ref.reference('users')
        users_ref.child(username).child('active').set(active_status)
        return True
    except Exception as e:
        st.error(f"Error updating status: {e}")
        return False

def delete_pengurus(username):
    """Hapus pengurus"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return False
        
        users_ref = db_ref.reference('users')
        users_ref.child(username).delete()
        return True
    except Exception as e:
        st.error(f"Error deleting pengurus: {e}")
        return False

def get_presensi_by_date_range(start_date, end_date):
    """Ambil data presensi berdasarkan rentang tanggal"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return []
        
        presensi_ref = db_ref.reference('presensi')
        all_data = presensi_ref.get()
        
        if not all_data:
            return []
        
        filtered_data = []
        for key, value in all_data.items():
            tanggal = value.get('tanggal')
            if tanggal and start_date <= tanggal <= end_date:
                filtered_data.append({
                    'id': key,
                    'tanggal': tanggal,
                    'tingkat': value.get('tingkat'),
                    'pengurus': value.get('pengurus'),
                    'input_by': value.get('input_by', 'Unknown'),
                    'total_hadir': value.get('total_hadir', 0),
                    'total_santri': value.get('total_santri', 0),
                    'created_at': value.get('created_at'),
                    'santri': value.get('santri', {}),
                    'alasan_tidak_hadir': value.get('alasan_tidak_hadir', {})
                })
        
        # Urutkan berdasarkan tanggal
        filtered_data.sort(key=lambda x: x.get('tanggal', ''))
        return filtered_data
    except Exception as e:
        st.error(f"Error getting presensi data: {e}")
        return []

def get_monthly_summary(year, month):
    """Ambil ringkasan presensi bulanan"""
    try:
        # Format tanggal untuk filter
        start_date = f"{year}-{month:02d}-01"
        
        # Tentukan hari terakhir bulan
        if month == 12:
            next_month = f"{year + 1}-01-01"
        else:
            next_month = f"{year}-{month + 1:02d}-01"
        
        from datetime import datetime, timedelta
        end_date_obj = datetime.strptime(next_month, "%Y-%m-%d") - timedelta(days=1)
        end_date = end_date_obj.strftime("%Y-%m-%d")
        
        data = get_presensi_by_date_range(start_date, end_date)
        
        # Analisis data
        summary = {
            'total_hari': len(set(d['tanggal'] for d in data)),
            'tingkat_1': {
                'total_pertemuan': len([d for d in data if d['tingkat'] == 'Tingkat 1']),
                'total_hadir': sum(d['total_hadir'] for d in data if d['tingkat'] == 'Tingkat 1'),
                'total_santri_per_pertemuan': sum(d['total_santri'] for d in data if d['tingkat'] == 'Tingkat 1'),
            },
            'tingkat_2': {
                'total_pertemuan': len([d for d in data if d['tingkat'] == 'Tingkat 2']),
                'total_hadir': sum(d['total_hadir'] for d in data if d['tingkat'] == 'Tingkat 2'),
                'total_santri_per_pertemuan': sum(d['total_santri'] for d in data if d['tingkat'] == 'Tingkat 2'),
            },
            'raw_data': data
        }
        
        return summary
    except Exception as e:
        st.error(f"Error getting monthly summary: {e}")
        return None

def get_weekly_summary(year, week_number):
    """Ambil ringkasan presensi mingguan"""
    try:
        from datetime import datetime, timedelta
        
        # Hitung tanggal awal dan akhir minggu
        jan_1 = datetime(year, 1, 1)
        start_of_week = jan_1 + timedelta(weeks=week_number - 1)
        start_of_week = start_of_week - timedelta(days=start_of_week.weekday())  # Mulai dari Senin
        end_of_week = start_of_week + timedelta(days=6)  # Sampai Minggu
        
        start_date = start_of_week.strftime("%Y-%m-%d")
        end_date = end_of_week.strftime("%Y-%m-%d")
        
        data = get_presensi_by_date_range(start_date, end_date)
        
        # Analisis data per hari
        daily_summary = {}
        for d in data:
            tanggal = d['tanggal']
            if tanggal not in daily_summary:
                daily_summary[tanggal] = {'Tingkat 1': None, 'Tingkat 2': None}
            daily_summary[tanggal][d['tingkat']] = {
                'hadir': d['total_hadir'],
                'total': d['total_santri'],
                'pengurus': d['pengurus']
            }
        
        summary = {
            'start_date': start_date,
            'end_date': end_date,
            'daily_data': daily_summary,
            'raw_data': data
        }
        
        return summary
    except Exception as e:
        st.error(f"Error getting weekly summary: {e}")
        return None

def get_santri_attendance_detail(start_date, end_date, tingkat):
    """Ambil detail kehadiran per santri"""
    try:
        data = get_presensi_by_date_range(start_date, end_date)
        tingkat_data = [d for d in data if d['tingkat'] == tingkat]
        
        # Kumpulkan semua nama santri
        all_santri = set()
        for d in tingkat_data:
            all_santri.update(d['santri'].keys())
        
        # Hitung kehadiran per santri
        santri_summary = {}
        for santri in all_santri:
            hadir_count = 0
            total_pertemuan = len(tingkat_data)
            
            for d in tingkat_data:
                if d['santri'].get(santri, False):
                    hadir_count += 1
            
            persentase = (hadir_count / total_pertemuan * 100) if total_pertemuan > 0 else 0
            santri_summary[santri] = {
                'hadir': hadir_count,
                'total_pertemuan': total_pertemuan,
                'persentase': persentase
            }
        
        return santri_summary
    except Exception as e:
        st.error(f"Error getting santri detail: {e}")
        return {}

def authenticate_user(username, password):
    """Autentikasi user"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return None
        
        users_ref = db_ref.reference('users')
        user_data = users_ref.child(username).get()
        
        if user_data and user_data.get('active', False):
            hashed_password = hash_password(password)
            if user_data.get('password') == hashed_password:
                return {
                    'username': username,
                    'name': user_data.get('name'),
                    'role': user_data.get('role')
                }
        return None
    except Exception as e:
        st.error(f"Error authenticating user: {e}")
        return None

def change_user_password(username, old_password, new_password):
    """Ubah password user"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return False, "Database connection failed"
        
        users_ref = db_ref.reference('users')
        user_data = users_ref.child(username).get()
        
        if not user_data:
            return False, "User tidak ditemukan"
        
        if not user_data.get('active', False):
            return False, "User tidak aktif"
        
        # Verifikasi password lama
        old_hashed = hash_password(old_password)
        if user_data.get('password') != old_hashed:
            return False, "Password lama tidak benar"
        
        # Update password baru
        new_hashed = hash_password(new_password)
        users_ref.child(username).update({
            'password': new_hashed,
            'password_changed_at': datetime.now().isoformat()
        })
        
        return True, "Password berhasil diubah"
        
    except Exception as e:
        return False, f"Error: {e}"

def delete_presensi(presensi_id):
    """Hapus data presensi berdasarkan ID"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return False, "Database connection failed"
        
        presensi_ref = db_ref.reference('presensi')
        
        # Cek apakah data ada
        existing_data = presensi_ref.child(presensi_id).get()
        if not existing_data:
            return False, "Data presensi tidak ditemukan"
        
        # Hapus data
        presensi_ref.child(presensi_id).delete()
        
        return True, "Data presensi berhasil dihapus"
        
    except Exception as e:
        return False, f"Error: {e}"

def get_all_presensi_for_admin():
    """Ambil semua data presensi untuk admin dengan detail lengkap"""
    try:
        db_ref = get_database()
        if db_ref is None:
            return []
        
        presensi_ref = db_ref.reference('presensi')
        all_data = presensi_ref.get()
        
        if not all_data:
            return []
        
        presensi_list = []
        for key, value in all_data.items():
            presensi_list.append({
                'id': key,
                'tanggal': value.get('tanggal'),
                'tingkat': value.get('tingkat'),
                'pengurus': value.get('pengurus'),
                'input_by': value.get('input_by', 'Unknown'),
                'total_hadir': value.get('total_hadir', 0),
                'total_santri': value.get('total_santri', 0),
                'created_at': value.get('created_at'),
                'santri': value.get('santri', {}),
                'alasan_tidak_hadir': value.get('alasan_tidak_hadir', {})
            })
        
        # Urutkan berdasarkan tanggal terbaru
        presensi_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return presensi_list
        
    except Exception as e:
        st.error(f"Error getting presensi data: {e}")
        return []