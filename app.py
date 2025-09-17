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
        with open("users.json", "w", encoding='utf-8') as f:
            json.dump({
                "admin": {"password": "1234", "banned": False, "ip": "", "device": ""}
            }, f, indent=4)
    with open("users.json", "r", encoding='utf-8') as f:
        return json.load(f)

def kullanicilari_kaydet(users):
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

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
            return "Bu kullanıcı yasaklanmıştır.", 403
        
        session.permanent = True
        session["username"] = username
        users[username]["ip"] = ip_al()
        users[username]["device"] = cihaz_modeli()
        kullanicilari_kaydet(users)

        if username == "admin":
            return redirect("/admin")
        else:
            return redirect("/anasayfa")
            
    return "Geçersiz kullanıcı adı veya şifre.", 401

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
        return jsonify(error="Yetkiniz yok"), 403
    return jsonify(kullanicilari_yukle())

@app.route("/api/add_user", methods=["POST"])
def api_add_user():
    if session.get("username") != "admin":
        return jsonify(error="Yetkiniz yok"), 403
    
    data = request.json
    users = kullanicilari_yukle()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(error="Eksik bilgi"), 400
    if username in users:
        return jsonify(error="Kullanıcı zaten mevcut"), 400
        
    users[username] = {
        "password": password,
        "banned": False,
        "ip": "",
        "device": ""
    }
    kullanicilari_kaydet(users)
    return jsonify(success=True, message="Kullanıcı başarıyla eklendi")

@app.route("/api/ban_user", methods=["POST"])
def api_ban_user():
    if session.get("username") != "admin":
        return jsonify(error="Yetkiniz yok"), 403
    
    data = request.json
    username = data.get("username")
    users = kullanicilari_yukle()
    if username in users and username != "admin":
        users[username]["banned"] = True
        kullanicilari_kaydet(users)
        return jsonify(success=True, message=f"{username} yasaklandı")
    return jsonify(error="Kullanıcı bulunamadı veya admin yasaklanamaz"), 404

@app.route("/api/unban_user", methods=["POST"])
def api_unban_user():
    if session.get("username") != "admin":
        return jsonify(error="Yetkiniz yok"), 403
    
    data = request.json
    username = data.get("username")
    users = kullanicilari_yukle()
    if username in users:
        users[username]["banned"] = False
        kullanicilari_kaydet(users)
        return jsonify(success=True, message=f"{username} yasağı kaldırıldı")
    return jsonify(error="Kullanıcı bulunamadı"), 404

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def filtrele_veri(metin):
    if not isinstance(metin, str):
        return ""
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
    sorgu_tipi = data.get("sorgu")
    headers = data.get("headers", {})

    tc = data.get("tc", "")
    gsm = data.get("gsm", "")
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")
    imei = data.get("imei", "")
    username = data.get("username", "")
    plaka = data.get("plaka", "")
    ilce = data.get("ilce", "")
    
    url = ""
    base_url = "https://hanedansystem.alwaysdata.net/hanesiz" if api == "1" else "https://api.hexnox.pro/sowixapi"

    if sorgu_tipi == "1":
        url = f"{base_url}/sulale.php?tc={tc}"
    elif sorgu_tipi == "2":
        url = f"{base_url}/tc.php?tc={tc}" if api == "1" else f"{base_url}/tcpro.php?tc={tc}"
    elif sorgu_tipi == "3":
        url = f"{base_url}/adres.php?tc={tc}"
    elif sorgu_tipi == "4":
        url = f"{base_url}/adsoyad.php?ad={ad}&soyad={soyad}&il={il}" if api == "1" else f"{base_url}/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}"
    elif sorgu_tipi == "5":
        url = f"{base_url}/aile.php?tc={tc}"
    elif sorgu_tipi == "6":
        url = f"{base_url}/gsmtc.php?gsm={gsm}" if api == "1" else f"{base_url}/gsmdetay.php?gsm={gsm}"
    elif sorgu_tipi == "7":
        url = f"{base_url}/tcgsm.php?tc={tc}"
    elif sorgu_tipi == "8":
        url = f"{base_url}/diploma/diploma.php?tc={tc}"
    elif sorgu_tipi == "9":
        url = f"{base_url}/ayak.php?tc={tc}"
    elif sorgu_tipi == "10":
        url = f"{base_url}/boy.php?tc={tc}"
    elif sorgu_tipi == "11":
        url = f"{base_url}/burc.php?tc={tc}"
    elif sorgu_tipi == "12":
        url = f"{base_url}/cm.php?tc={tc}"
    elif sorgu_tipi == "13":
        url = f"{base_url}/cocuk.php?tc={tc}"
    elif sorgu_tipi == "14":
        url = f"{base_url}/anne.php?tc={tc}"
    elif sorgu_tipi == "15":
        url = f"{base_url}/ehlt.php?tc={tc}"
    elif sorgu_tipi == "16":
        url = f"{base_url}/imei.php?imei={imei}"
    elif sorgu_tipi == "17":
        url = f"{base_url}/operator.php?gsm={gsm}"
    elif sorgu_tipi == "18":
        url = f"{base_url}/telegram_sorgu.php?username={username}"
    elif sorgu_tipi == "19":
        url = f"{base_url}/hikaye.php?tc={tc}"
    elif sorgu_tipi == "20":
        url = f"https://hexnox.pro/sowix/vesika.php?tc={tc}"
    elif sorgu_tipi == "21":
        url = f"{base_url}/hane.php?tc={tc}"
    elif sorgu_tipi == "22":
        url = f"{base_url}/muhallev.php?tc={tc}"
    elif sorgu_tipi == "23":
        url = f"https://hexnox.pro/sowixfree/lgs/lgs.php?tc={tc}"
    elif sorgu_tipi == "24":
        url = f"https://hexnox.pro/sowixfree/plaka.php?plaka={plaka}"
    elif sorgu_tipi == "25":
        url = "https://hexnox.pro/sowixfree/nude.php"
    elif sorgu_tipi == "26":
        url = f"https://hexnox.pro/sowixfree/sertifika.php?tc={tc}"
    elif sorgu_tipi == "27":
        url = f"https://hexnox.pro/sowixfree/üni.php?tc={tc}"
    elif sorgu_tipi == "28":
        url = f"https://hexnox.pro/sowixfree/aracparca.php?plaka={plaka}"
    elif sorgu_tipi == "29":
        url = f"https://hexnox.pro/sowixfree/şehit.php?Ad={ad}&Soyad={soyad}"
    elif sorgu_tipi == "30":
        url = f"https://hexnox.pro/sowixfree/interpol.php?ad={ad}&soyad={soyad}"
    elif sorgu_tipi == "31":
        url = f"https://hexnox.pro/sowixfree/personel.php?tc={tc}"
    elif sorgu_tipi == "32":
        url = f"https://hexnox.pro/sowixfree/internet.php?tc={tc}"
    elif sorgu_tipi == "33":
        url = f"https://hexnox.pro/sowixfree/nvi.php?tc={tc}"
    elif sorgu_tipi == "34":
        url = f"https://hexnox.pro/sowixfree/nezcane.php?il={il}&ilce={ilce}"
    elif sorgu_tipi == "35":
        url = f"https://hexnox.pro/sowixfree/basvuru/basvuru.php?tc={tc}"
    elif sorgu_tipi == "36":
        url = f"https://hexnox.pro/sowixfree/police/police.php?tc={tc}"
    elif sorgu_tipi == "37":
        url = f"{base_url}/tapu.php?tc={tc}"
    elif sorgu_tipi == "38":
        url = f"{base_url}/okulno.php?tc={tc}"
    elif sorgu_tipi == "39":
        url = f"{base_url}/isyeriyetkili.php?tc={tc}"
    elif sorgu_tipi == "40":
        url = f"{base_url}/isyeri.php?tc={tc}"
    elif sorgu_tipi == "41":
        # Kombine sorgu (1, 2, 3 ve 5)
        try:
            results = {}
            
            # Sorgu 1 (Sülale)
            url1 = f"{base_url}/sulale.php?tc={tc}"
            response1 = requests.get(url1, headers=headers, timeout=90)
            results['sulale'] = filtrele_veri(response1.text) if response1.status_code == 200 else "Sorgu başarısız"
            
            # Sorgu 2 (TC)
            url2 = f"{base_url}/tc.php?tc={tc}" if api == "1" else f"{base_url}/tcpro.php?tc={tc}"
            response2 = requests.get(url2, headers=headers, timeout=90)
            results['tc'] = filtrele_veri(response2.text) if response2.status_code == 200 else "Sorgu başarısız"
            
            # Sorgu 3 (Adres)
            url3 = f"{base_url}/adres.php?tc={tc}"
            response3 = requests.get(url3, headers=headers, timeout=90)
            results['adres'] = filtrele_veri(response3.text) if response3.status_code == 200 else "Sorgu başarısız"
            
            # Sorgu 5 (Aile)
            url5 = f"{base_url}/aile.php?tc={tc}"
            response5 = requests.get(url5, headers=headers, timeout=90)
            results['aile'] = filtrele_veri(response5.text) if response5.status_code == 200 else "Sorgu başarısız"
            
            return jsonify(success=True, results=results)
            
        except requests.exceptions.RequestException as e:
            return jsonify(success=False, message=f"Hata: {str(e)}")
    else:
        return jsonify(success=False, message="Geçersiz sorgu tipi"), 400

    try:
        response = requests.get(url, headers=headers, timeout=90, verify=False)
        response.raise_for_status()
        filtrelenmis = filtrele_veri(response.text)
        if filtrelenmis:
            return jsonify(success=True, result=filtrelenmis)
        else:
            return jsonify(success=False, message="Veri bulunamadı veya geçersiz")
    except requests.exceptions.RequestException as e:
        return jsonify(success=False, message=f"Hata: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
