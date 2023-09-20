from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/portal")
def portal():
    return render_template("portal.html")

@app.route("/descomplica")
def descomplica():
    return render_template("descomplica.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)