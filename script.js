const inputsDiv = document.getElementById("inputs");
const sorguSelect = document.getElementById("sorgu");

function clearInputs() {
  inputsDiv.innerHTML = "";
}
function addInput(id, label, placeholder = "", type = "text") {
  const lbl = document.createElement("label");
  lbl.textContent = label;
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
    data.tc = document.getElementById("tc").value.trim();
    if (!data.tc) return alert("TC gir!");
  } else if (sorgu === "4") {
    data.ad = document.getElementById("ad").value.trim();
    data.soyad = document.getElementById("soyad").value.trim();
    data.il = document.getElementById("il").value.trim();
  } else if (sorgu === "6") {
    data.gsm = document.getElementById("gsm").value.trim();
  }

  try {
    const res = await fetch("/api/sorgu", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (json.success) {
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
