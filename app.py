import requests
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔐 Güçlü ve rastgele bir secret key (oturumları korur)
app.secret_key = "b2c4f5a19e7d63b8a09f4c1d2e8b75a6c3f0e1d2948765b1f3a2d7e9c6b8a5d4"

# 🔐 Giriş (şifre kontrolü)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == "patronsorgu":
            session["authenticated"] = True
            return redirect("/anasayfa")
        else:
            return send_from_directory(".", "login.html")  # Şifre yanlışsa tekrar göster
    return send_from_directory(".", "login.html")

# 🔒 Şifreli giriş yapılmadıysa /anasayfa'ya erişim engellenir
@app.route("/anasayfa")
def panel():
    if not session.get("authenticated"):
        return redirect("/")
    return send_from_directory(".", "anasayfa.html")

# 🔧 Sonuçları temizleme fonksiyonu
def filtrele_veri(metin):
    satirlar = metin.strip().splitlines()
    temiz = []
    for s in satirlar:
        s = s.strip()
        if not s or "GEÇERSİZ" in s.upper() or s.startswith("http"):
            continue
        temiz.append(s)
    return "\n".join(temiz)

# 🔄 API sorgu işlemi
@app.route("/api/sorgu", methods=["POST"])
def sorgu():
    if not session.get("authenticated"):
        return jsonify(success=False, message="Yetkisiz erişim")
    
    data = request.json
    api = data.get("api")
    sorgu = data.get("sorgu")
    tc = data.get("tc", "")
    gsm = data.get("gsm", "")
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")

    base_url = "http://ramowlf.xyz/ramowlf" if api == "1" else "https://api.hexnox.pro/sowixapi"

    if sorgu == "1":
        url = f"{base_url}/sulale.php?tc={tc}"
    elif sorgu == "2":
        url = f"{base_url}/tc.php?tc={tc}" if api == "1" else f"{base_url}/tcpro.php?tc={tc}"
    elif sorgu == "3":
        url = f"{base_url}/adres.php?tc={tc}"
    elif sorgu == "4":
        url = f"{base_url}/adsoyad.php?ad={ad}&soyad={soyad}&il={il}" if api == "1" else f"{base_url}/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}"
    elif sorgu == "5":
        url = f"{base_url}/aile.php?tc={tc}"
    elif sorgu == "6":
        url = f"{base_url}/gsmtc.php?gsm={gsm}" if api == "1" else f"{base_url}/gsmdetay.php?gsm={gsm}"
    elif sorgu == "7":
        url = f"{base_url}/tcgsm.php?tc={tc}"
    else:
        return jsonify(success=False, message="Geçersiz sorgu tipi")

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200 and response.text.strip():
            filtrelenmis = filtrele_veri(response.text)
            return jsonify(success=True, result=filtrelenmis)
        else:
            return jsonify(success=False, message="Boş yanıt döndü.")
    except requests.exceptions.RequestException as e:
        return jsonify(success=False, message=f"API hatası: {str(e)}")

# 🔧 Statik dosyaları sunmak için
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# 🔁 Termux veya sunucuda dış erişime açık çalıştırmak için
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
