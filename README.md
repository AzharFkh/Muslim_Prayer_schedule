# Muslim Prayer Schedule & Calendar Converter

Aplikasi web berbasis Flask untuk konversi sistem penanggalan (Masehi, Hijriah, Julian Day) dan perhitungan jadwal waktu sholat menggunakan pendekatan komputasi astronomis.

Proyek ini dikembangkan sebagai bagian dari pembelajaran mata kuliah **Fisika Komputasi Astronomi** (Universitas Brawijaya) dengan bimbingan **Prof. Dr. rer. nat. Abdurrouf, S.Si., M.Si.**

## Fitur Utama

- **Dashboard Hari Ini (`/`)**
  - Menampilkan tanggal Masehi, Hijriah, dan nilai Julian Day (`00:00 UT`) hari ini.
  - Deteksi lokasi otomatis melalui browser (`navigator.geolocation`) dengan penyimpanan di `localStorage` dan pencarian nama kota via Nominatim OpenStreetMap (fallback ke lokasi default Kota Malang jika akses lokasi tidak tersedia).
  - Jadwal sholat harian (Subuh, Terbit, Zuhur, Ashar, Maghrib, Isya) beserta penanda dan hitung mundur menuju waktu sholat berikutnya.
  - Ringkasan data astronomi matahari harian: sudut deklinasi matahari, *Equation of Time*, waktu transit/istiwa, dan koreksi ufuk Maghrib.
- **Konversi Tanggal (`/konversi-tanggal`)**
  - Konversi antar sistem penanggalan Masehi (Gregorian/Julian), Hijriah, dan Julian Day.
- **Jadwal Sholat (`/jadwal-solat`)**
  - Perhitungan jadwal sholat mode harian maupun mingguan (7 hari).
  - Pencarian koordinat kota (Nominatim OpenStreetMap) dan deteksi zona waktu otomatis, serta input manual latitude, longitude, timezone, ketinggian (mdpl), dan metode Ashar (Syafi'i / Hanafi).

## Struktur Proyek

```text
.
├── app.py                  # Aplikasi utama Flask & routing
├── requirements.txt        # Daftar dependensi Python (Flask, Gunicorn)
├── dockerfile              # Konfigurasi image Docker
├── docker-compose.yml      # Konfigurasi container & port mapping (8100:5100)
├── static/                 # Stylesheet CSS, font, dan script JS
├── templates/              # Template HTML (Jinja2)
└── utilities/              # Modul perhitungan astronomi & konversi kalender
    ├── JDtoJadwalSolat.py
    ├── converter_gregorian.py
    ├── converter_hijriah.py
    └── paging_tools.py
```

## Cara Menjalankan

### 1. Menjalankan Secara Lokal

Pastikan Python 3 sudah terpasang, lalu buat virtual environment dan install dependensi:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Aplikasi dapat diakses melalui `http://localhost:5100`.

### 2. Menjalankan dengan Docker Compose

```bash
docker compose up -d --build
```

Secara default container berjalan di port `5100` dan dipetakan ke port `8100` pada host (`http://localhost:8100`).

> **Catatan:** Fitur deteksi lokasi otomatis di browser memerlukan koneksi HTTPS (atau `localhost` saat pengembangan lokal).
