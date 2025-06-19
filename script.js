const inputsDiv = document.getElementById("inputs");
const sorguSelect = document.getElementById("sorgu");

function clearInputs() {
  inputsDiv.innerHTML = "";
}

function addInput(id, label, placeholder = "", type = "text") {
  const lbl = document.createElement("label");
  lbl.textContent = label;
  lbl.htmlFor = id;
  const inp = document.createElement("input");
  inp.type = type;
  inp.id = id;
  inp.placeholder = placeholder;
  inputsDiv.appendChild(lbl);
  inputsDiv.appendChild(inp);
}

function updateInputs() {
  clearInputs();
  const val = sorguSelect.value;
  if (["1", "2", "3", "5", "7"].includes(val)) {
    addInput("tc", "TC Numarası:", "TC girin");
  } else if (val === "4") {
    addInput("ad", "Ad:");
    addInput("soyad", "Soyad:");
    addInput("il", "İl:");
  } else if (val === "6") {
    addInput("gsm", "Telefon:", "5xx...", "tel");
  }
}

sorguSelect.addEventListener("change", updateInputs);
window.onload = updateInputs;

document.getElementById("submit").addEventListener("click", async () => {
  const api = document.getElementById("api").value;
  const sorgu = sorguSelect.value;
  const data = { api, sorgu };

  if (["1", "2", "3", "5", "7"].includes(sorgu)) {
    const tcVal = document.getElementById("tc")?.value.trim();
    if (!tcVal) {
      alert("Lütfen TC giriniz!");
      return;
    }
    data.tc = tcVal;
  } else if (sorgu === "4") {
    const adVal = document.getElementById("ad")?.value.trim();
    const soyadVal = document.getElementById("soyad")?.value.trim();
    const ilVal = document.getElementById("il")?.value.trim();
    if (!adVal || !soyadVal || !ilVal) {
      alert("Ad, Soyad ve İl alanları boş bırakılamaz!");
      return;
    }
    data.ad = adVal;
    data.soyad = soyadVal;
    data.il = ilVal;
  } else if (sorgu === "6") {
    const gsmVal = document.getElementById("gsm")?.value.trim();
    if (!gsmVal) {
      alert("Telefon numarasını giriniz!");
      return;
    }
    data.gsm = gsmVal;
  }

  try {
    const res = await fetch("/api/sorgu", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const json = await res.json();

    if (json.success) {
      // Gelen sonucu .txt dosyası olarak indir
      const blob = new Blob([json.result], { type: "text/plain;charset=utf-8" });
      const link = document.createElement("a");
      const sorguAdiMap = {
        "1": "Sulale",
        "2": "TC_Bilgi",
        "3": "Adres",
        "4": "AdSoyadİl",
        "5": "Aile",
        "6": "Numaradan_TC",
        "7": "TCden_Numara",
      };
      const filename = (sorguAdiMap[sorgu] || "sonuc") + ".txt";
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      alert("Hata: " + json.message);
    }
  } catch (err) {
    alert("İstek hatası: " + err.message);
  }
});
