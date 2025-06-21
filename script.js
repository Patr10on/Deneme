// --- Giriş Paneli Formu ---

const form = document.getElementById("loginForm");
const errorMsg = document.getElementById("errorMsg");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  errorMsg.style.display = "none";
  const pwd = form.password.value.trim();
  if (pwd === "patronsorgu") {
    window.location.href = "/anasayfa";
  } else {
    errorMsg.style.display = "block";
    errorMsg.style.animation = 'none';
    errorMsg.offsetHeight; // reflow
    errorMsg.style.animation = null;
    form.password.focus();
  }
});

// --- Yıldız ve Nebula Animasyonları ---

const canvas = document.getElementById('starCanvas');
const ctx = canvas.getContext('2d');
let width, height;
function resize() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
}
window.addEventListener('resize', resize);
resize();

class Star {
  constructor() {
    this.reset();
  }
  reset() {
    this.x = Math.random() * width;
    this.y = Math.random() * height;
    this.size = Math.random() * 1.5 + 0.5;
    this.speed = (Math.random() * 0.5) + 0.05;
    this.opacity = Math.random();
    this.opacityChange = (Math.random() * 0.02) + 0.005;
    this.color = this.pickColor();
  }
  pickColor() {
    const colors = [
      '255, 255, 255',
      '180, 210, 255',
      '255, 240, 180'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }
  update() {
    this.x += this.speed;
    this.y += this.speed;
    if(this.x > width) this.x = 0;
    if(this.y > height) this.y = 0;
    this.opacity += this.opacityChange;
    if(this.opacity > 1 || this.opacity < 0.1) this.opacityChange = -this.opacityChange;
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(${this.color}, ${this.opacity})`;
    ctx.shadowColor = `rgba(${this.color}, 0.7)`;
    ctx.shadowBlur = 8;
    ctx.fill();
  }
}

const stars = [];
const starCount = 150;
for(let i=0; i<starCount; i++) stars.push(new Star());

let mouseX = width/2;
let mouseY = height/2;
window.addEventListener('mousemove', e => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

function animate() {
  ctx.clearRect(0,0,width,height);
  stars.forEach(s => {
    const dx = mouseX - s.x;
    const dy = mouseY - s.y;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if(dist < 150) {
      s.opacity += 0.05;
      s.x += dx * 0.002;
      s.y += dy * 0.002;
    } else {
      s.opacity -= 0.01;
    }
    if(s.opacity > 1) s.opacity = 1;
    if(s.opacity < 0.1) s.opacity = 0.1;

    s.update();
    s.draw();
  });
  requestAnimationFrame(animate);
}
animate();

const shootingContainer = document.getElementById('shootingStars');
function createShootingStar() {
  const star = document.createElement('div');
  star.classList.add('shooting-star');
  star.style.top = Math.random() * 30 + 'vh';
  star.style.left = '-150px';
  const duration = Math.random() * 1 + 0.8;
  star.style.animationDuration = duration + 's';
  shootingContainer.appendChild(star);

  star.style.opacity = '1';
  star.style.transform = 'rotate(45deg) translateX(0)';

  star.addEventListener('animationend', () => {
    shootingContainer.removeChild(star);
  });
}
setInterval(() => {
  if(Math.random() < 0.6) {
    createShootingStar();
  }
}, 1200);

// --- Dinamik input yönetimi ve API sorgu işlemleri ---

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
  } else if (val === "8") {
    addInput("instagram", "Instagram Kullanıcı Adı:", "örn: patron123");
  }
}

sorguSelect.addEventListener("change", updateInputs);
window.onload = updateInputs;

document.getElementById("submit").addEventListener("click", async () => {
  const api = document.getElementById("api").value;
  const sorgu = sorguSelect.value;

  if (sorgu === "8") {
    const username = document.getElementById("instagram")?.value.trim() || "belirtilmemiş";
    const content = `bunlara inanıyor musun? mal insta=@by_.ram : ${username}`;
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "hack.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    return;
  }

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
      let resultText = json.result;
      resultText += "\n\ninsta=@by_.ram";

      const blob = new Blob([resultText], { type: "text/plain;charset=utf-8" });
      const link = document.createElement("a");
      const sorguAdiMap = {
        "1": "Sulale",
        "2": "TC_Bilgi",
        "3": "Adres",
        "4": "AdSoyadİl",
        "5": "Aile",
        "6": "Numaradan_TC",
        "7": "TCden_Numara",
        "8": "Instagramhack",
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
