class HijriahConverter:
    _LEAP_SET = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}

    def __init__(self, year=1446, month=1, day=1, JD=None):
        self.year = year
        self.month = month
        self.day = day
        self.JD = JD

        if self.day < 1 or self.month < 1 or self.month > 12:
            raise ValueError("Tanggal/bulan tidak valid")

        year_in_cycle = (self.year - 1) % 30 + 1
        max_day = self._month_lengths(year_in_cycle)[self.month - 1]
        if self.day > max_day:
            raise ValueError(f"Tanggal {self.day} tidak ada di bulan {self.month} tahun {self.year} H")

    @classmethod
    def _month_lengths(cls, year_in_cycle):
        base = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        if year_in_cycle in cls._LEAP_SET:
            base[-1] = 30
        return base

    def to_JD(self):
        jd0 = 1948439.5
        cycles = (self.year - 1) // 30
        year_in_cycle = (self.year - 1) % 30 + 1

        days = cycles * 10631
        for y in range(1, year_in_cycle):
            days += 355 if y in self._LEAP_SET else 354

        days += sum(self._month_lengths(year_in_cycle)[: self.month - 1])
        days += self.day - 1
        return jd0 + days

    def from_JD(self):
        jd0 = 1948439.5
        d = int((self.JD - jd0) + 0.5)

        cycles = d // 10631
        rem = d % 10631

        acc = 0
        year_in_cycle = 0
        for y in range(1, 30 + 1):
            span = 355 if y in self._LEAP_SET else 354
            if rem < acc + span:
                year_in_cycle = y
                day_in_year = rem - acc
                break
            acc += span

        acc = 0
        for m, L in enumerate(self._month_lengths(year_in_cycle), start=1):
            if day_in_year < acc + L:
                month = m
                day = day_in_year - acc + 1
                break
            acc += L

        year = cycles * 30 + year_in_cycle
        self.year, self.month, self.day = int(year), int(month), int(day)
        return self.day, self.month, self.year
