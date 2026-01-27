from flask import Flask, render_template, request
from utilities.JDtoJadwalSolat import jadwal_solat
from utilities.paging_tools import *
from datetime import timedelta
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

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
    app.run(debug=True,
            host="0.0.0.0", 
            port=5000)

