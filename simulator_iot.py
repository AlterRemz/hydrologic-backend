import requests

URL = "http://127.0.0.1:8000/api/sensor-data"

print("=== 🚜 SIMULATOR IoT Hydro Logic ===")
print("Gunakan alat ini untuk mengirim data dummy ke server FastAPI\n")

sektor = input("Masukkan nama sektor (cth: Sektor A) : ")
kelembapan = float(input("Masukkan kelembapan tanah (0-100)  : "))
air = float(input("Masukkan level air cadangan (0-100): "))

payload = {
    "sektor_lahan": sektor,
    "kelembapan_tanah": kelembapan,
    "level_air_cadangan": air
}

print("\nMengirim data ke server...")

try:
    response = requests.post(URL, json=payload)
    if response.status_code == 200:
        data_server = response.json()
        print("\n[✅ BERHASIL] Data diterima oleh server FastAPI!")
        print("-" * 40)
        print("💡 HASIL KEPUTUSAN SISTEM (SWP):")
        print(f">> {data_server['status_rekomendasi']} <<")
        print("-" * 40)
    else:
        print(f"[❌ GAGAL] Status Code: {response.status_code}")
except Exception as e:
    print(f"[💥 ERROR] Gagal terhubung. Pastikan server FastAPI (main.py) sudah menyala! Detail: {e}")