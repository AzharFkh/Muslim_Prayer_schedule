import math

def acot(x):
    return math.atan(1 / x) if x != 0 else math.pi / 2

def sudut_deklinasi(JD):
    """Hitung sudut deklinasi (delta) dalam derajat"""
    T = 2.0 * math.pi * (JD - 2451545.0) / 365.25
    delta = (0.37877
             + 23.264 * math.sin(math.radians(57.297 * T - 79.547))
             + 0.3812 * math.sin(math.radians(2 * 57.297 * T - 82.682))
             + 0.17132 * math.sin(math.radians(3 * 57.297 * T - 59.722)))
    return delta

def waktu_transit(JD, longitude, timezone):
    """Hitung waktu transit (jam lokal)"""
    U = (JD - 2451545) / 36525
    L0 = 280.46607 + 36000.7698 * U
    L0_rad = math.radians(L0)

    ET = (-(1789 + 237 * U) * math.sin(L0_rad)
          - (7146 - 62 * U) * math.cos(L0_rad)
          + (9934 - 14 * U) * math.sin(2 * L0_rad)
          - (29 + 5 * U) * math.cos(2 * L0_rad)
          + (74 + 10 * U) * math.sin(3 * L0_rad)
          + (320 - 4 * U) * math.cos(3 * L0_rad)
          - 212 * math.sin(4 * L0_rad)) / 1000.0

    return 12 + timezone - (longitude / 15) - (ET / 60)

def HA(h, L, delta):
    """Hour angle (radian)"""
    return math.acos(
        (math.sin(math.radians(h)) - math.sin(math.radians(L)) * math.sin(math.radians(delta)))
        / (math.cos(math.radians(L)) * math.cos(math.radians(delta)))
    )

def to_hhmm(time_decimal):
    """Ubah jam desimal ke format HH:MM"""
    jam = int(time_decimal)
    menit = int(round((time_decimal - jam) * 60))
    if menit == 60:
        jam += 1
        menit = 0
    return f"{jam:02d}:{menit:02d}"

def jadwal_solat(JD, latitude, longitude, timezone, altitude=0, KA=1, h_subuh=-20, h_isya=-18):
    """
    Hitung waktu sholat (Subuh, Terbit, Zuhur, Ashar, Maghrib, Isya)
    :param JD: Julian Day
    :param latitude: lintang (positif = LU, negatif = LS)
    :param longitude: bujur (derajat)
    :param timezone: zona waktu (jam dari UTC)
    :param altitude: ketinggian lokasi (meter)
    :param KA: konstanta ashar (1 = Syafi'i, 2 = Hanafi)
    :param h_subuh: altitude matahari untuk Subuh (°)
    :param h_isya: altitude matahari untuk Isya (°)
    """
    delta = sudut_deklinasi(JD)
    WT = waktu_transit(JD, longitude, timezone)

    # Altitude untuk maghrib (sunset)
    h_maghrib = -0.8333 - 0.0347 * (altitude ** 0.5)

    # Sudut jam
    h_ashar = math.degrees(acot(KA + math.tan(math.radians(abs(delta - latitude)))))
    HA_ashar = HA(h_ashar, latitude, delta)
    HA_maghrib = HA(h_maghrib, latitude, delta)
    HA_isya = HA(h_isya, latitude, delta)
    HA_subuh = HA(h_subuh, latitude, delta)

    # Waktu sholat (jam desimal)
    zuhur = WT
    ashar = WT + math.degrees(HA_ashar) / 15
    maghrib = WT + math.degrees(HA_maghrib) / 15
    isya = WT + math.degrees(HA_isya) / 15
    subuh = WT - math.degrees(HA_subuh) / 15
    terbit = WT - math.degrees(HA_maghrib) / 15

    return {
        "Subuh": to_hhmm(subuh),
        "Terbit": to_hhmm(terbit),
        "Zuhur": to_hhmm(zuhur),
        "Ashar": to_hhmm(ashar),
        "Maghrib": to_hhmm(maghrib),
        "Isya": to_hhmm(isya)
    }


# JD Date Converter here :

class GregorianConverter:
    def __init__(self, year=2025, month=1, day=1, JD=None):
        self.year = year
        self.month = month
        self.day = day
        self.JD = JD

        if self.day < 1 or self.month < 1 or self.month > 12:
            raise ValueError("Tanggal/bulan tidak valid")

        max_day = self.max_days_in_month()
        if self.day > max_day:
            raise ValueError(f"Tanggal {self.day} tidak ada di bulan {self.month} tahun {self.year}")

    def is_leap(self):
        return (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0)

    def max_days_in_month(self):
        days = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        if self.is_leap():
            days[2] = 29
        return days[self.month]

    @staticmethod
    def _gregorian_to_jdn(y, m, d):
        a = (14 - m) // 12
        y1 = y + 4800 - a
        m1 = m + 12 * a - 3
        return d + (153 * m1 + 2) // 5 + 365 * y1 + y1 // 4 - y1 // 100 + y1 // 400 - 32045

    @staticmethod
    def _julian_to_jdn(y, m, d):
        a = (14 - m) // 12
        y1 = y + 4800 - a
        m1 = m + 12 * a - 3
        return d + (153 * m1 + 2) // 5 + 365 * y1 + y1 // 4 - 32083

    def _is_gregorian_date(self, y, m, d):
        if y > 1582: return True
        if y < 1582: return False
        if m > 10: return True
        if m < 10: return False
        return d >= 15

    def tanggal_sesat(self)->float:
        return self.year == 1582 and self.month == 10 and 5 <= self.day <= 14

    def to_JD(self):
        if self.tanggal_sesat():
            raise ValueError("Tanggal tidak ada di kalender (5–14 Oktober 1582).")

        if self._is_gregorian_date(self.year, self.month, self.day):
            jdn = self._gregorian_to_jdn(self.year, self.month, self.day)
        else:
            jdn = self._julian_to_jdn(self.year, self.month, self.day)

        return jdn - 0.5

    def from_JD(self):
        JD = self.JD + 0.5
        Z = int(JD)
        F = JD - Z

        if Z < 2299161:
            A = Z
        else:
            alpha = int((Z - 1867216.25) // 36524.25)
            A = Z + 1 + alpha - int(alpha // 4)

        B = A + 1524
        C = int((B - 122.1) // 365.25)
        D = int(365.25 * C)
        E = int((B - D) // 30.6001)

        day = B - D - int(30.6001 * E) + F
        month = E - 1 if E < 14 else E - 13
        year = C - 4716 if month > 2 else C - 4715

        self.day, self.month, self.year = int(day), int(month), int(year)
        return self.day, self.month, self.year

