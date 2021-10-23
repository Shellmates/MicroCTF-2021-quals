import os
from flask import Flask, flash, request, redirect, render_template
from dotenv import load_dotenv
from serializer import serialize, deserialize, InvalidSignature

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("FLASK_ENV") == "development"
FLAG = os.getenv("FLAG")

# Routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/serialize", methods=["GET", "POST"])
def serialize_route():
    if request.method == "GET":
        return redirect("/")
    data = request.form.get("data")
    if not data:
        flash("Data not specified", "red")
        return redirect("/")
    signature, serialized_hex = serialize(data)
    return render_template("index.html", action="serialize", signature=signature, serialized_hex=serialized_hex)

@app.route("/deserialize", methods=["GET", "POST"])
def deserialize_route():
    if request.method == "GET":
        return redirect("/")
    signature = request.form.get("signature")
    serialized_hex = request.form.get("serialized_hex")
    if not signature or not serialized_hex:
        flash("Signature or serialized data not specified", "red")
        return redirect("/")
    try:
        data = deserialize(signature, serialized_hex)
    except InvalidSignature as e:
        flash("Invalid signature", "red")
        return redirect("/")
    except:
        flash("Deserialization error", "red")
        return redirect("/")

    if data == [1337, 1337.0, '1337', b'1337']:
        return render_template("index.html", flag=FLAG)
    else:
        return render_template("index.html", action="deserialize", data=data)

# Error handling

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
