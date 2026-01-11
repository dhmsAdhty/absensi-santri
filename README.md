# Sistem Presensi Madin

Aplikasi presensi digital berbasis Streamlit dan Firebase.

## Setup Lokal

1.  **Clone repository ini**

2.  **Buat Virtual Environment (opsional tapi disarankan)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux / Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Firebase (Development Lokal)**
    *   Sediakan file Firebase Admin SDK (Service Account) di root folder project.
    *   File ini hanya digunakan untuk kebutuhan development lokal.
    *   **PENTING:** File kredensial tidak disertakan ke repository karena telah diamankan melalui `.gitignore`.

5.  **Jalankan Aplikasi**
    ```bash
    streamlit run inde.py
    ```

## Deploy ke Streamlit Cloud

Untuk menjaga keamanan kredensial Firebase, deployment menggunakan fitur **Streamlit Secrets**.

1.  **Push source code ke GitHub**
    *   Pastikan file kredensial Firebase tidak ikut ter-push ke repository.

2.  **Buka Streamlit Cloud**
    *   Hubungkan Streamlit Cloud dengan repository GitHub.

3.  **Deploy Aplikasi**
    *   Repository: pilih repository project
    *   Main file path: `inde.py`

4.  **Konfigurasi Secrets (Kredensial Firebase)**
    *   Masuk ke **Settings → Secrets** pada dashboard Streamlit Cloud.
    *   Kredensial Firebase disimpan dalam format TOML.
    *   **Langkah Praktis:**
        1.  Jalankan script helper di lokal:
            ```bash
            python generate_secrets.py
            ```
        2.  Script akan menghasilkan file `secrets_output.toml`.
        3.  Salin seluruh isi file tersebut.
        4.  Tempelkan ke kolom Secrets di Streamlit Cloud.
        5.  Simpan perubahan.

5.  **Restart / Redeploy**
    *   Lakukan restart aplikasi agar konfigurasi secrets dapat terbaca dengan benar.

## Struktur Project

*   `inde.py`: File utama aplikasi Streamlit
*   `firebase_config.py`: Konfigurasi koneksi Firebase (menyesuaikan environment lokal dan Streamlit Secrets)
*   `generate_secrets.py`: Script bantuan untuk mengonversi kredensial Firebase ke format TOML
*   `requirements.txt`: Daftar dependensi Python

## Catatan Keamanan

*   Kredensial tidak pernah di-commit ke repository
*   Tidak ada informasi sensitif yang ditampilkan di dokumentasi
*   Aman digunakan untuk repository public
