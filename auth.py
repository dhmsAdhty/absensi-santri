import streamlit as st
from firebase_config import authenticate_user, create_default_users

def show_login_page():
    """Tampilkan halaman login"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f8fffe 0%, #f0f9f7 100%);
        }
        
        .login-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(40, 167, 69, 0.1);
            border: 1px solid rgba(40, 167, 69, 0.1);
        }
        
        .login-header {
            text-align: center;
            color: #1e7e34;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .login-subtitle {
            text-align: center;
            color: #28a745;
            font-size: 1rem;
            font-weight: 400;
            margin-bottom: 2rem;
            opacity: 0.8;
        }
        
        .login-logo {
            text-align: center;
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .logo-container {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            
        }
        
        .logo-container img {
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.25);
            border: 4px solid rgba(40, 167, 69, 0.15);
            display: block;
            margin: 0 auto !important;
            transform: translateX(0);
        }
        
        /* Pastikan kolom logo di tengah */
        .logo-container .stColumn {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* Paksa semua image di tengah */
        .stColumn img {
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Styling untuk teks logo */
        .logo-text {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
        }
        
        /* Responsive untuk mobile */
        @media (max-width: 768px) {
            /* Di mobile, sembunyikan teks dan buat logo full width */
            .logo-text {
                display: none !important;
            }
            
            /* Logo di mobile jadi full width dan center */
            .stColumn:has(img) {
                grid-column: 1 / -1 !important;
                text-align: center !important;
            }
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(40, 167, 69, 0.3);
        }
        
        .stTextInput > div > div > input {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 0.75rem;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #28a745;
            box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
        }
        
        @media (max-width: 768px) {
            .login-container {
                margin: 1rem;
                padding: 1.5rem;
            }
            
            .login-header {
                font-size: 1.5rem;
            }
            
            .login-logo {
                font-size: 3rem;
            }
            
            .logo-container img {
                width: 150px !important;
            }
            
            .logo-container {
                padding: 0.5rem 0;
                margin-bottom: 1.5rem;
                align-items: center;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Logo dan teks PP AL HIKMAH SMG
    # Desktop: Logo dan teks horizontal, Mobile: Logo di tengah, teks di bawah
    
    # Container untuk logo dan teks
    logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
    
    with logo_col2:
        # Sub-kolom untuk logo dan teks di desktop
        logo_sub1, logo_sub2 = st.columns([1, 1])
        
        with logo_sub1:
            try:
                st.image("main-logo.png", width=150)
            except:
                st.markdown('<div style="text-align: center; font-size: 4rem; margin: 1rem 0;">🕌</div>', unsafe_allow_html=True)
        
        with logo_sub2:
            st.markdown("""
            <div class="logo-text">
                <h2 style="color: #1e7e34; font-weight: 700; margin: 0; font-size: 1.8rem; line-height: 1.2; display: flex; align-items: center; height: 150px;">
                    PP AL HIKMAH<br>SMG
                </h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Layout mobile - logo di tengah dengan teks di bawah
    st.markdown("""
    <div class="mobile-logo-container" style="display: none;">
        <div style="text-align: center; margin-bottom: 1rem;">
            <img src="main-logo.png" width="150" style="border-radius: 20px; box-shadow: 0 6px 20px rgba(40, 167, 69, 0.25); border: 4px solid rgba(40, 167, 69, 0.15);">
        </div>
        <div style="text-align: center;">
            <h2 style="color: #1e7e34; font-weight: 700; margin: 0; font-size: 1.5rem;">PP AL HIKMAH SMG</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Form login dengan container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.markdown("### 🔐 Masuk ke Sistem")
                username = st.text_input("👤 Username", placeholder="Masukkan username")
                password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")
                
                login_button = st.form_submit_button("🚀 Masuk", use_container_width=True)
                
                if login_button:
                    if username and password:
                        # Buat user default jika belum ada
                        create_default_users()
                        
                        # Autentikasi
                        user = authenticate_user(username, password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.success(f"Selamat datang, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Username atau password salah!")
                    else:
                        st.warning("⚠️ Mohon isi username dan password!")
    
    # Info akun default dengan lebar yang sama dengan form login
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])

def show_logout_button():
    """Tampilkan tombol logout di sidebar"""
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            # Clear any other session states
            for key in list(st.session_state.keys()):
                if key.startswith('confirm_'):
                    del st.session_state[key]
            st.rerun()

def check_authentication():
    """Cek status autentikasi"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    return st.session_state.authenticated

def get_current_user():
    """Dapatkan user yang sedang login"""
    return st.session_state.get('user', None)

def show_change_password_form():
    """Tampilkan form ganti password"""
    from firebase_config import change_user_password
    
    current_user = get_current_user()
    if not current_user:
        return
    
    st.markdown("#### 🔐 Ganti Password")
    
    with st.form("change_password_form"):
        old_password = st.text_input(
            "Password Lama", 
            type="password", 
            placeholder="Password saat ini"
        )
        
        new_password = st.text_input(
            "Password Baru", 
            type="password", 
            placeholder="Password baru (min 6 karakter)"
        )
        
        confirm_password = st.text_input(
            "Konfirmasi", 
            type="password", 
            placeholder="Ulangi password baru"
        )
        
        submit_button = st.form_submit_button("💾 Ubah Password", use_container_width=True)
        
        if submit_button:
            if not old_password or not new_password or not confirm_password:
                st.error("❌ Semua field harus diisi!")
                return
            
            if new_password != confirm_password:
                st.error("❌ Password baru dan konfirmasi tidak sama!")
                return
            
            if len(new_password) < 6:
                st.error("❌ Password baru minimal 6 karakter!")
                return
            
            if old_password == new_password:
                st.error("❌ Password baru harus berbeda dari password lama!")
                return
            
            # Ubah password
            success, message = change_user_password(
                current_user['username'], 
                old_password, 
                new_password
            )
            
            if success:
                st.success(f"✅ {message}")
                st.info("� Sila kan login ulang dengan password baru")
                
                # Auto logout setelah ganti password
                if st.button("🚪 Logout Sekarang", use_container_width=True):
                    st.session_state.authenticated = False
                    st.session_state.user = None
                    st.rerun()
            else:
                st.error(f"❌ {message}")
    
    # Tips singkat
    with st.expander("💡 Tips Password"):
        st.markdown("""
        **Password yang baik:**
        - Minimal 6 karakter
        - Kombinasi huruf & angka
        - Contoh: `Madin2024`
        """)