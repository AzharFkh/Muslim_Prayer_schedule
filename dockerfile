# 1. Gunakan base image Python yang ringan
FROM python:3.11

# 2. Set folder kerja di dalam container
WORKDIR /app

# 3. Copy file requirements dulu (agar caching docker bekerja optimal)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install -r requirements.txt

# 5. Copy seluruh sisa kode proyek ke dalam container
COPY . .

# 6. Buka port 5000 (Port default Flask)
EXPOSE 5000

# 7. Perintah untuk menjalankan aplikasi
# Opsi A (Development/Simple):
CMD ["python3", "app.py"]