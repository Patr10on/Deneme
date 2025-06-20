from flask import Flask, request, session, redirect, url_for, send_from_directory
import requests

app = Flask(__name__)
app.secret_key = "f3d8a1b7c9e24f5d8a9b6c1e2f7d3a4b"  # Güvenli secret key

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == "patronsorgu":
            session["logged_in"] = True
            return redirect(url_for("panel"))
        else:
            return send_from_directory(".", "login.html", 401)
    else:
        if session.get("logged_in"):
            return redirect(url_for("panel"))
        return send_from_directory(".", "login.html")

@app.route("/anasayfa")
def panel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_from_directory(".", "anasayfa.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def filtrele_veri(metin):
    satirlar = metin.strip().splitlines()
    temiz = []
    for s in satirlar:
        s = s.strip()
        if not s or "GEÇERSİZ" in s.upper() or s.startswith("http"):
            continue
        temiz.append(s)
    return "\n".join(temiz)

@app.route("/api/sorgu", methods=["POST"])
def sorgu():
    if not session.get("logged_in"):
        return {"success": False, "message": "Yetkisiz erişim"}, 401

    data = request.json
    api = data.get("api")
    sorgu = data.get("sorgu")
    tc = data.get("tc", "")
    gsm = data.get("gsm", "")
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")

    # API 1 yeni URL'ler
    base_url = "http://ramowolf.xyz/ramowlf" if api == "1" else "https://api.hexnox.pro/sowixapi"

    if sorgu == "1":  # Sülale
        url = f"{base_url}/sulale.php?tc={tc}"
    elif sorgu == "2":  # TC Bilgi
        url = f"{base_url}/tcpro.php?tc={tc}" if api == "1" else f"{base_url}/tcpro.php?tc={tc}"
    elif sorgu == "3":  # Adres
        url = f"{base_url}/adres.php?tc={tc}"
    elif sorgu == "4":  # Ad+Soyad+İl
        url = f"{base_url}/adsoyad.php?ad={ad}" if api == "1" else f"{base_url}/adsoyadilce.php?ad={ad}"
        url += f"&soyad={soyad}&il={il}"
    elif sorgu == "5":  # Aile
        url = f"{base_url}/aile.php?tc={tc}"
    elif sorgu == "6":  # Numaradan TC
        url = f"{base_url}/gsmtc.php?gsm={gsm}"
    elif sorgu == "7":  # TC'den Numara
        url = f"{base_url}/tcgsm.php?tc={tc}"
    elif sorgu == "8":  # Instagram Jack (sabit içerik)
        # Bu sorgu API çağrısı yapmaz, frontend'de işleniyor
        return {"success": True, "result": "bunlara inanıyor musun? mal insta=@by_.ram"}
    else:
        return {"success": False, "message": "Geçersiz sorgu tipi"}

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200 and response.text.strip():
            filtrelenmis = filtrele_veri(response.text)
            return {"success": True, "result": filtrelenmis}
        else:
            return {"success": False, "message": "Boş yanıt döndü."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"API hatası: {str(e)}"}

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
