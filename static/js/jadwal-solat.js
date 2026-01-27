flatpickr("#tanggal", {
  dateFormat: "Y-m-d",     
  altInput: true,
  altFormat: "d-m-Y",      
  allowInput: true,
  defaultDate: "today",    
  disableMobile: true
});

// cari kota

async function searchCity() {
  const city = document.getElementById("city-input").value;
  if (!city) return;

  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${city}`;
  const response = await fetch(url, {
    headers: {
      "User-Agent": "AzharSolatApp/1.0 (https://example.com/contact)"
    }
  });

  const data = await response.json();

  if (data.length > 0) {
    const lat = data[0].lat;
    const lon = data[0].lon;

    document.getElementById("latitude").value = lat;
    document.getElementById("longitude").value = lon;

    updateTimezone(lat, lon);
  }
}

// timezone nya

async function updateTimezone(lat, lon) {
  const url = `https://timeapi.io/api/timezone/coordinate?latitude=${lat}&longitude=${lon}`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data.currentUtcOffset && data.currentUtcOffset.seconds !== undefined) {
      const gmt = data.currentUtcOffset.seconds / 3600;
      document.getElementById("timezone").value = gmt.toFixed(1);
    }
  } catch (err) {
    console.error("Gagal mengambil timezone:", err);
  }
}
