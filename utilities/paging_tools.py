from .converter_gregorian import GregorianConverter
from .converter_hijriah import HijriahConverter

# utilities?
bulan_greg = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
    "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12
}
bulan_greg_reverse = {v: k for k, v in bulan_greg.items()}

bulan_hijriah = {
    "Muharram": 1, "Safar": 2, "Rabiul Awwal": 3, "Rabiul Akhir": 4,
    "Jumadil Awal": 5, "Jumadil Akhir": 6, "Rajab": 7, "Sya'ban": 8,
    "Ramadhan": 9, "Syawal": 10, "Dzulqa'dah": 11, "Dzulhijjah": 12
}
bulan_hijriah_reverse = {v: k for k, v in bulan_hijriah.items()}

def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def greg_to_jd(form):
    hari = safe_int(form.get("hari_masehi"))
    bulan = safe_int(form.get("bulan_masehi"))
    tahun = safe_int(form.get("tahun_masehi"))
    if None in (hari, bulan, tahun):
        return None, "Data Gregorian tidak lengkap."
    jd = GregorianConverter(year=tahun, month=bulan, day=hari).to_JD()
    return jd, None


def hij_to_jd(form):
    hari = safe_int(form.get("hari_hijriah"))
    bulan = safe_int(form.get("bulan_hijriah"))
    tahun = safe_int(form.get("tahun_hijriah"))
    if None in (hari, bulan, tahun):
        return None, "Data Hijriah tidak lengkap."
    jd = HijriahConverter(year=tahun, month=bulan, day=hari).to_JD()
    return jd, None


def jd_to_greg(form):
    jd = safe_float(form.get("nilai_JD"))
    if jd is None:
        return None, "Nilai JD tidak valid."
    hari, bulan, tahun = GregorianConverter(JD=jd).from_JD()
    nama_bulan = bulan_greg_reverse.get(bulan, bulan)
    tanggal = [hari, nama_bulan, tahun]
    return tanggal, None


def jd_to_hij(form):
    jd = safe_float(form.get("nilai_JD"))
    if jd is None:
        return None, "Nilai JD tidak valid."
    hari, bulan, tahun = HijriahConverter(JD=jd).from_JD()
    nama_bulan = bulan_hijriah_reverse.get(bulan, bulan)
    tanggal = [hari, nama_bulan, tahun]
    return tanggal, None


def hij_to_greg(form):
    hari = safe_int(form.get("hari_hijriah"))
    bulan = safe_int(form.get("bulan_hijriah"))
    tahun = safe_int(form.get("tahun_hijriah"))
    if None in (hari, bulan, tahun):
        return None, "Data Hijriah tidak lengkap."
    jd = HijriahConverter(year=tahun, month=bulan, day=hari).to_JD()
    hari, bulan, tahun = GregorianConverter(JD=jd).from_JD()
    nama_bulan = bulan_greg_reverse.get(bulan, bulan)
    tanggal = [hari, nama_bulan, tahun]
    return tanggal, None


def greg_to_hij(form):
    hari = safe_int(form.get("hari_masehi"))
    bulan = safe_int(form.get("bulan_masehi"))
    tahun = safe_int(form.get("tahun_masehi"))
    if None in (hari, bulan, tahun):
        return None, "Data Gregorian tidak lengkap."
    jd = GregorianConverter(year=tahun, month=bulan, day=hari).to_JD()
    hari, bulan, tahun = HijriahConverter(JD=jd).from_JD()
    nama_bulan = bulan_hijriah_reverse.get(bulan, bulan)
    tanggal = [hari, nama_bulan, tahun]
    return tanggal, None