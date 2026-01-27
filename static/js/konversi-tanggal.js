// converrsion selector

document.addEventListener("DOMContentLoaded", () => {
  const modeSelect = document.getElementById("mode");
  const gregorianFields = document.getElementById("gregorian-fields");
  const hijriFields = document.getElementById("hijri-fields");
  const jdField = document.getElementById("jd-field");

  function toggleFields() {
    const mode = modeSelect.value;

    gregorianFields.style.display = "none";
    hijriFields.style.display = "none";
    jdField.style.display = "none";

    if (mode === "greg_to_jd" || mode === "greg_to_hij") {
      gregorianFields.style.display = "block";
    } else if (mode === "hij_to_jd" || mode === "hij_to_greg") {
      hijriFields.style.display = "block";
    } else if (mode === "jd_to_greg" || mode === "jd_to_hij") {
      jdField.style.display = "block";
    }
  }

  toggleFields();

  modeSelect.addEventListener("change", toggleFields);
});

// Bagian untuk hijriah tanggal yang tidak ada

document.addEventListener("DOMContentLoaded", () => {
  const hariHijriah = document.getElementById("hari_hijriah");
  const bulanHijriah = document.getElementById("bulan_hijriah");
  const tahunHijriah = document.getElementById("tahun_hijriah");
  const form = document.querySelector("form");

  const LEAP_SET = new Set([2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]);
  const errorBox = document.createElement("div");
  errorBox.style.color = "#b3261e";
  errorBox.style.fontSize = "0.9rem";
  errorBox.style.marginTop = "4px";
  hariHijriah?.parentNode?.appendChild(errorBox);

  function monthLengths(yearInCycle) {
    const base = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29];
    if (LEAP_SET.has(yearInCycle)) base[11] = 30;
    return base;
  }

  function validateHijriDate() {
    const day = parseInt(hariHijriah.value);
    const month = parseInt(bulanHijriah.value);
    const year = parseInt(tahunHijriah.value);
    errorBox.textContent = "";
    hariHijriah.classList.remove("invalid-input");

    if (isNaN(day) || isNaN(month) || isNaN(year)) return true;

    const yearInCycle = ((year - 1) % 30) + 1;
    const maxDay = monthLengths(yearInCycle)[month - 1];
    hariHijriah.max = maxDay;

    if (day > maxDay) {
      errorBox.textContent = `Tanggal yang dimasukan tidak ada`;
      hariHijriah.classList.add("invalid-input");
      return false; 
    }
    return true; 
  }

  bulanHijriah.addEventListener("change", validateHijriDate);
  tahunHijriah.addEventListener("input", validateHijriDate);
  hariHijriah.addEventListener("input", validateHijriDate);

  form.addEventListener("submit", (e) => {
    if (!validateHijriDate()) {
      e.preventDefault(); 
      errorBox.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
});

// bagian ini untuk masehi tanggal yang tidak ada

document.addEventListener("DOMContentLoaded", () => {
  const hariMasehi = document.getElementById("hari_masehi");
  const bulanMasehi = document.getElementById("bulan_masehi");
  const tahunMasehi = document.getElementById("tahun_masehi");
  const form = document.querySelector("form");

  const errorBoxGreg = document.createElement("div");
  errorBoxGreg.style.color = "#b3261e";
  errorBoxGreg.style.fontSize = "0.9rem";
  errorBoxGreg.style.marginTop = "4px";
  hariMasehi?.parentNode?.appendChild(errorBoxGreg);

  function isLeap(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
  }

  function maxDaysInMonth(month, year) {
    const days = {
      1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
      7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    };
    if (isLeap(year)) days[2] = 29;
    return days[month] || 31;
  }

  function validateGregorianDate() {
    const day = parseInt(hariMasehi.value);
    const month = parseInt(bulanMasehi.value);
    const year = parseInt(tahunMasehi.value);

    errorBoxGreg.textContent = "";
    hariMasehi.classList.remove("invalid-input");

    if (isNaN(day) || isNaN(month) || isNaN(year)) return true; 
    const maxDay = maxDaysInMonth(month, year);
    hariMasehi.max = maxDay;

    if (day > maxDay) {
      errorBoxGreg.textContent = `Tanggal yang dimasukan tidak ada`;
      hariMasehi.classList.add("invalid-input");
      return false;
    }
    return true;
  }

  bulanMasehi.addEventListener("change", validateGregorianDate);
  tahunMasehi.addEventListener("input", validateGregorianDate);
  hariMasehi.addEventListener("input", validateGregorianDate);

  form.addEventListener("submit", (e) => {
    if (!validateGregorianDate()) {
      e.preventDefault();
      errorBoxGreg.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
});

// Error handling untuk selector form konversi tanggal

document.addEventListener("DOMContentLoaded", () => {
  const modeSelect = document.getElementById("mode");
  const gregInputs = document.querySelectorAll("[name^='hari_masehi'], [name^='bulan_masehi'], [name^='tahun_masehi']");
  const hijriInputs = document.querySelectorAll("[name^='hari_hijriah'], [name^='bulan_hijriah'], [name^='tahun_hijriah']");
  const jdInput = document.querySelector("[name='nilai_JD']");

  function setRequired(inputs, required) {
    inputs.forEach(input => input.required = required);
  }

  function updateFields() {
    const mode = modeSelect.value;
    setRequired(gregInputs, false);
    setRequired(hijriInputs, false);
    jdInput.required = false;

    if (mode === "greg_to_jd" || mode === "greg_to_hij") setRequired(gregInputs, true);
    else if (mode === "hij_to_jd" || mode === "hij_to_greg") setRequired(hijriInputs, true);
    else if (mode === "jd_to_greg" || mode === "jd_to_hij") jdInput.required = true;
  }

  modeSelect.addEventListener("change", updateFields);
  updateFields(); 
});