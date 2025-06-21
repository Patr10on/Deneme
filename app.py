from flask import Flask, send_from_directory, redirect, request

app = Flask(__name__)

# 🔐 Giriş sayfası
@app.route("/", methods=["GET"])
def login():
    return send_from_directory(".", "login.html")

# 🔓 Anasayfa: auth=1 olmadan girilemez
@app.route("/anasayfa")
def anasayfa():
    if request.args.get("auth") == "1":
        return send_from_directory(".", "anasayfa.html")
    else:
        return redirect("/")

# 🎨 Statik dosyalar
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
