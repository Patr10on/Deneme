import requests
from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
import os
import json
import platform
from datetime import timedelta  

app = Flask(__name__)
app.secret_key = "a1b2c3d4e5f60718293a4b5c6d7e8f90"

app.permanent_session_lifetime = timedelta(hours=6)  
CORS(app)


def kullanicilari_yukle():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({
                "admin": {"password": "1234", "banned": False, "ip": "", "device": ""}
            }, f, indent=4)
    with open("users.json", "r") as f:
        return json.load(f)

def kullanicilari_kaydet(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def cihaz_modeli():
    return platform.platform()

def ip_al():
    return request.remote_addr


@app.route("/")
def login():
    if "username" in session:
        if session["username"] == "admin":
            return redirect("/admin")
        else:
            return redirect("/anasayfa")
    return send_from_directory(".", "login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    users = kullanicilari_yukle()

    if username in users and users[username]["password"] == password:
        if users[username]["banned"]:
            return "Bu kullanıcı banlandı."
        session.permanent = True                     # EKLENDİ
        session["username"] = username               # VARDI
        users[username]["ip"] = ip_al()
        users[username]["device"] = cihaz_modeli()
        kullanicilari_kaydet(users)

        if username == "admin":
            return redirect("/admin")
        else:
            return redirect("/anasayfa")
    return "Geçersiz kullanıcı adı veya şifre."


@app.route("/anasayfa")
def anasayfa():
    if "username" not in session:
        return redirect("/")
    return send_from_directory(".", "anasayfa.html")


@app.route("/admin")
def admin():
    if session.get("username") != "admin":
        return redirect("/")
    return send_from_directory(".", "admin.html")


@app.route("/api/users")
def api_users():
    if session.get("username") != "admin":
        return "Yasak", 403
    return jsonify(kullanicilari_yukle())


@app.route("/api/add_user", methods=["POST"])
def api_add_user():
    if session.get("username") != "admin":
        return "Yasak", 403
    data = request.json
    users = kullanicilari_yukle()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return "Eksik bilgi", 400
    if username in users:
        return "Kullanıcı zaten var", 400
    users[username] = {
        "password": password,
        "banned": False,
        "ip": "",
        "device": ""
    }
    kullanicilari_kaydet(users)
    return "OK"


@app.route("/api/ban_user", methods=["POST"])
def api_ban_user():
    if session.get("username") != "admin":
        return "Yasak", 403
    data = request.json
    username = data.get("username")
    users = kullanicilari_yukle()
    if username in users:
        users[username]["banned"] = True
        kullanicilari_kaydet(users)
    return "OK"


@app.route("/api/unban_user", methods=["POST"])
def api_unban_user():
    if session.get("username") != "admin":
        return "Yasak", 403
    data = request.json
    username = data.get("username")
    users = kullanicilari_yukle()
    if username in users:
        users[username]["banned"] = False
        kullanicilari_kaydet(users)
    return "OK"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
    data = request.json
    api = data.get("api")
    sorgu = data.get("sorgu")
    tc = data.get("tc", "")
    gsm = data.get("gsm", "")
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")

    base_url = "https://wazelyapi.vercel.app/api" if api == "1" else "https://api.hexnox.pro/sowixapi"

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


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
