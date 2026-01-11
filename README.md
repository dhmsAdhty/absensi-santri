# Sistem Presensi Madin Al Hikmah

Aplikasi presensi digital berbasis Streamlit dan Firebase.

## Setup Lokal

1.  **Clone repository ini.**
2.  **Buat Virtual Environment (opsional tapi disarankan):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Konfigurasi Firebase:**
    *   Pastikan file `madin-al-hikmah-presensi-firebase-adminsdk-fbsvc-299af8422e.json` ada di root folder project. File ini digunakan untuk autentikasi saat development lokal.
    *   **PENTING:** File ini sudah dimasukkan ke `.gitignore` sehingga tidak akan terupload ke repository public.

5.  **Jalankan Aplikasi:**
    ```bash
    streamlit run inde.py
    ```

## Cara Deploy ke Streamlit Cloud

Karena file credentials Firebase tidak boleh di-publish, kita akan menggunakan fitur **Streamlit Secrets**.

1.  **Push code ke GitHub** (pastikan file JSON credentials tidak ikut terupload - sudah dihandle oleh `.gitignore`).
2.  **Buka Streamlit Cloud** (share.streamlit.io) dan hubungkan dengan repository GitHub Anda.
3.  **Deploy App:**
    *   Repository: Pilih repo Anda.
    *   Main file path: `inde.py`
4.  **Setting Secrets (Kredensial Database):**
    *   Sebelum atau sesudah klik Deploy, masuk ke **Settings** -> **Secrets** di dashboard Streamlit Cloud aplikasi Anda.
    *   Kita perlu memasukkan isi dari file JSON credentials ke dalam format TOML.
    *   **Cara Mudah:**
        1.  Jalankan script helper di lokal Anda:
            ```bash
            python generate_secrets.py
            ```
        2.  Script ini akan membuat file `secrets_output.toml`.
        3.  Buka file `secrets_output.toml`, copy semua isinya.
        4.  Paste ke kolom Secrets di Streamlit Cloud.
        5.  Save.

5.  **Reboot/Redeploy:** Jika aplikasi sudah berjalan namun error, restart aplikasi agar secrets baru terbaca.

## Struktur Project

*   `inde.py`: File utama aplikasi.
*   `firebase_config.py`: Konfigurasi koneksi ke Firebase (menghandle local file vs secrets).
*   `generate_secrets.py`: Script bantuan untuk convert JSON ke format Secrets TOML.
*   `requirements.txt`: Daftar library yang dibutuhkan.
