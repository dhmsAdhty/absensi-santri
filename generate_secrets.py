import json
import os

# Nama file JSON credentials Anda
json_file = 'madin-al-hikmah-presensi-firebase-adminsdk-fbsvc-299af8422e.json'
output_file = 'secrets_output.toml'
database_url = 'https://madin-al-hikmah-presensi-default-rtdb.asia-southeast1.firebasedatabase.app/'

if not os.path.exists(json_file):
    print(f"File {json_file} tidak ditemukan!")
    exit(1)

with open(json_file, 'r') as f:
    data = json.load(f)

toml_content = "[firebase]\n"
for key, value in data.items():
    toml_content += f'{key} = "{value}"\n'

# Tambahkan database_url
toml_content += f'database_url = "{database_url}"\n'

with open(output_file, 'w') as f:
    f.write(toml_content)

print(f"Berhasil membuat {output_file}. Silakan copy isinya ke Streamlit Cloud Secrets.")
