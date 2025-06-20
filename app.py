from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Giriş sayfası
@app.route("/")
def login():
    return send_from_directory(".", "login.html")

# Panel sayfası
@app.route("/anasayfa")
def panel():
    return send_from_directory(".", "anasayfa.html")

# Static dosyalar (CSS, JS, vs.)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# Cevap filtreleme (boş, geçersiz vs. satırları siler)
def filtrele_veri(metin):
    satirlar = metin.strip().splitlines()
    temiz = []
    for s in satirlar:
        s = s.strip()
        if not s or "GEÇERSİZ" in s.upper() or s.startswith("http"):
            continue
        temiz.append(s)
    return "\n".join(temiz)

# Sorgu işlemi
@app.route("/api/sorgu", methods=["POST"])
def sorgu():
    data = request.json
    api = data.get("api")
    sorgu = data.get("sorgu")
    tc = data.get("tc", "")
    gsm = data.get("gsm", "")
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")

    # API seçimi
    base_url = "http://ramowolf.xyz/ramowlf" if api == "1" else "https://api.hexnox.pro/sowixapi"

    # Sorgu türüne göre API adresleri
    if sorgu == "1":  # Sülale
        url = f"{base_url}/sulale.php?tc={tc}"
    elif sorgu == "2":  # TC Bilgi
        url = f"{base_url}/tcpro.php?tc={tc}"
    elif sorgu == "3":  # Adres
        url = f"{base_url}/adres.php?tc={tc}"
    elif sorgu == "4":  # Ad Soyad İl
        url = f"{base_url}/adsoyad.php?ad={ad}&soyad={soyad}&il={il}" if api == "1" else f"{base_url}/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}"
    elif sorgu == "5":  # Aile
        url = f"{base_url}/aile.php?tc={tc}"
    elif sorgu == "6":  # Numara → TC
        url = f"{base_url}/gsmtc.php?gsm={gsm}" if api == "1" else f"{base_url}/gsmdetay.php?gsm={gsm}"
    elif sorgu == "7":  # TC → Numara
        url = f"{base_url}/tcgsm.php?tc={tc}"
    elif sorgu == "8":  # Instagram Jack (sahte işlem, txt oluşturuluyor sadece JS ile)
        return jsonify(success=True, result="Instagram Jack sorgusu - sonuç yok")
    else:
        return jsonify(success=False, message="Geçersiz sorgu tipi")

    # API isteği gönder
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200 and response.text.strip():
            filtrelenmis = filtrele_veri(response.text)
            return jsonify(success=True, result=filtrelenmis)
        else:
            return jsonify(success=False, message="Boş yanıt döndü.")
    except requests.exceptions.RequestException as e:
        return jsonify(success=False, message=f"API hatası: {str(e)}")

# Sunucuyu başlat
if __name__ == "__main__":
    app.run(debug=True)
