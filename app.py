from flask import Flask, render_template, request
from utilities.JDtoJadwalSolat import (
    jadwal_solat,
    sudut_deklinasi,
    waktu_transit,
    equation_of_time,
    to_hhmm,
)
from utilities.paging_tools import *
from datetime import timedelta
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Lokasi default: Kota Malang (WIB / GMT+7)
    default_lokasi = {
        "nama": "Kota Malang",
        "latitude": -7.9666,
        "longitude": 112.6326,
        "timezone": 7,
        "altitude": 450,
    }

    wib = datetime.timezone(datetime.timedelta(hours=default_lokasi["timezone"]))
    now = datetime.datetime.now(wib)
    today = now.date()

    hari_indonesia = [
        "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"
    ]
    nama_hari = hari_indonesia[today.weekday()]

    jd_today = GregorianConverter(
        year=today.year, month=today.month, day=today.day
    ).to_JD()
    h_day, h_month, h_year = HijriahConverter(JD=jd_today).from_JD()

    tanggal_masehi = f"{nama_hari}, {today.day} {bulan_greg_reverse.get(today.month, today.month)} {today.year}"
    tanggal_hijriah = f"{h_day} {bulan_hijriah_reverse.get(h_month, h_month)} {h_year} H"

    jadwal_hari_ini = jadwal_solat(
        jd_today,
        default_lokasi["latitude"],
        default_lokasi["longitude"],
        default_lokasi["timezone"],
        default_lokasi["altitude"],
        KA=1,
        h_subuh=-20,
        h_isya=-18,
    )

    now_hhmm = now.strftime("%H:%M")
    next_prayer = None
    for nama, waktu in jadwal_hari_ini.items():
        if waktu > now_hhmm:
            next_prayer = {"nama": nama, "waktu": waktu, "besok": False}
            break
    if next_prayer is None:
        next_prayer = {
            "nama": "Subuh",
            "waktu": jadwal_hari_ini["Subuh"],
            "besok": True,
        }

    astro_data = {
        "deklinasi": sudut_deklinasi(jd_today),
        "equation_of_time": equation_of_time(jd_today),
        "waktu_transit": to_hhmm(
            waktu_transit(
                jd_today,
                default_lokasi["longitude"],
                default_lokasi["timezone"],
            )
        ),
        "h_maghrib": -0.8333 - 0.0347 * (default_lokasi["altitude"] ** 0.5),
    }

    return render_template(
        "index.html",
        tanggal_masehi=tanggal_masehi,
        tanggal_hijriah=tanggal_hijriah,
        jd_today=jd_today,
        jadwal_hari_ini=jadwal_hari_ini,
        lokasi=default_lokasi,
        next_prayer=next_prayer,
        astro_data=astro_data,
    )

@app.route("/konversi-tanggal", methods=["GET", "POST"])
def konversi_tanggal():
    result = None
    tanggal = None
    error = None

    if request.method == "POST":
        mode = request.form.get("mode")

        actions = {
            "greg_to_jd": greg_to_jd,
            "hij_to_jd": hij_to_jd,
            "jd_to_greg": jd_to_greg,
            "jd_to_hij": jd_to_hij,
            "hij_to_greg": hij_to_greg,
            "greg_to_hij": greg_to_hij
        }

        func = actions.get(mode)
        if func:
            result_value, error = func(request.form)
            if mode in ["greg_to_jd", "hij_to_jd"]:
                result = result_value
                tanggal = None
            else:
                tanggal = result_value
                result = None
        else:
            error = "Mode konversi tidak dikenali."

    return render_template("konversi-tanggal.html", result=result, tanggal=tanggal, error=error)

@app.route("/jadwal-solat", methods=["GET", "POST"])
def jadwal_solat_page():
    if request.method == "POST":
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        timezone = float(request.form["timezone"])
        altitude = float(request.form["altitude"])
        tanggal = request.form["tanggal"]
        KA = int(request.form["asharMethod"])
        mode = request.form.get("mode")  # daily or weekly mode

        tahun, bulan, hari = map(int, tanggal.split("-"))
        tanggal_obj = datetime.date(tahun, bulan, hari)

        # DAILY MODE
        if mode == "daily":
            JD_local = GregorianConverter(year=tahun, month=bulan, day=hari).to_JD()

            hasil = jadwal_solat(
                JD_local,
                latitude,
                longitude,
                timezone,
                altitude,
                KA=KA,
                h_subuh=-20,
                h_isya=-18
            )

            return render_template(
                "jadwal-solat.html",
                hasil=hasil,
                tanggal=tanggal_obj,
                latitude=latitude,
                longitude=longitude,
            )

        # WEEKLY MODE
        elif mode == "weekly":
            hasil_mingguan = []

            for i in range(7):
                target_date = tanggal_obj + timedelta(days=i)
                JD_loop = GregorianConverter(
                    year=target_date.year,
                    month=target_date.month,
                    day=target_date.day
                ).to_JD()

                jadwal = jadwal_solat(
                    JD_loop,
                    latitude,
                    longitude,
                    timezone,
                    altitude,
                    KA=KA,
                    h_subuh=-20,
                    h_isya=-18
                )

                hasil_mingguan.append({"tanggal": target_date, "jadwal": jadwal})

            return render_template(
                "jadwal-solat.html",
                hasil_mingguan=hasil_mingguan,
                latitude=latitude,
                longitude=longitude,
                tanggal=tanggal_obj
            )

    return render_template("jadwal-solat.html")

if __name__ == "__main__":
    app.run(debug=False,
            host="0.0.0.0", 
            port=5100)

