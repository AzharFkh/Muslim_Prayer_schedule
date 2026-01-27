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

    def tanggal_sesat(self):
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
