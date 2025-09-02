import requests
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json

# -------------------------
# ASCII kutu formatlama fonksiyonu
# -------------------------
def format_box(title, data: dict):
    # En uzun anahtar ve değerin uzunluğunu bul
    max_key_len = max(len(k) for k in data.keys()) if data else 0
    max_value_len = max(len(str(v)) for v in data.values()) if data else 0
    
    # Kutu genişliğini belirle
    content_width = max_key_len + max_value_len + 3
    title_width = len(title)
    width = max(content_width, title_width) + 4
    
    top = f"╔{'═' * (width)}╗"
    middle_title = f"║{title.center(width)}║"
    separator = f"╠{'═' * (width)}╣"
    bottom = f"╚{'═' * (width)}╝"
    imza = "@by_.ram"

    content_lines = []
    for key, value in data.items():
        line = f"{key.capitalize()}: {value}"
        content_lines.append(f"║ {line.ljust(width-2)} ║")
    
    box = [top, middle_title, separator] + content_lines + [bottom, imza]
    return "\n".join(box)

# -------------------------
# Basit veri filtreleme fonksiyonu
# -------------------------
def filtrele_veri(data):
    if not isinstance(data, dict):
        return {"Hata": "Geçersiz veri formatı"}
    
    temiz_veri = {}
    for key, value in data.items():
        if isinstance(value, str) and ("GEÇERSİZ" in value.upper() or value.startswith("http")):
            continue
        temiz_veri[key] = value
            
    return temiz_veri

app = Flask(__name__)
CORS(app)

@app.route("/")
def anasayfa():
    return send_from_directory(".", "anasayfa.html")

@app.route("/admin")
def admin():
    return send_from_directory(".", "admin.html")

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
    base_url = "https://wazelyapi.vercel.app/api" if api == "1" else "https://api.hexnox.pro/sowixapi"

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
        try:
            results = {}

            url1 = f"{base_url}/sulale.php?tc={tc}"
            response1 = requests.get(url1, headers=headers, timeout=90)
            results['Sülale'] = response1.json().get('data', {}) if response1.status_code == 200 else {"Hata": "Sorgu başarısız"}

            url2 = f"{base_url}/tc.php?tc={tc}" if api == "1" else f"{base_url}/tcpro.php?tc={tc}"
            response2 = requests.get(url2, headers=headers, timeout=90)
            results['TC'] = response2.json().get('data', {}) if response2.status_code == 200 else {"Hata": "Sorgu başarısız"}

            url3 = f"{base_url}/adres.php?tc={tc}"
            response3 = requests.get(url3, headers=headers, timeout=90)
            results['Adres'] = response3.json().get('data', {}) if response3.status_code == 200 else {"Hata": "Sorgu başarısız"}

            url5 = f"{base_url}/aile.php?tc={tc}"
            response5 = requests.get(url5, headers=headers, timeout=90)
            results['Aile'] = response5.json().get('data', {}) if response5.status_code == 200 else {"Hata": "Sorgu başarısız"}

            # Her bir sonucu tek bir kutuda düzenlemek için
            all_results = {}
            for k, v in results.items():
                if isinstance(v, dict):
                    all_results.update({f"{k.capitalize()}_{key}": value for key, value in v.items()})
                else:
                    all_results[k] = v
                    
            formatted_results = format_box("Kombine Sorgu Sonuçları", all_results)
            return jsonify(success=True, result=formatted_results)

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            return jsonify(success=False, message=f"Hata: {str(e)}")
    else:
        return jsonify(success=False, message="Geçersiz sorgu tipi"), 400

    try:
        response = requests.get(url, headers=headers, timeout=90, verify=False)
        response.raise_for_status()
        
        # Yanıtı JSON olarak işle
        api_data = response.json()
        
        # Sadece 'data' anahtarındaki veriyi al, yoksa boş bir sözlük kullan
        result_data = api_data.get('data', {})

        if result_data:
            formatted_result = format_box("Sorgu Sonucu", result_data)
            return jsonify(success=True, result=formatted_result)
        else:
            return jsonify(success=False, message="Veri bulunamadı veya geçersiz")
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        return jsonify(success=False, message=f"Hata: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
