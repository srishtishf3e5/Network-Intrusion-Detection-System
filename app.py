from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load Model
model = joblib.load("models/network_intrusion_model.pkl")

@app.route("/")
def home():
    return render_template("index.html", prediction=None)

@app.route("/predict", methods=["POST"])
def predict():

    duration = float(request.form["duration"])
    protocol_type = int(request.form["protocol_type"])
    service = int(request.form["service"])
    flag = int(request.form["flag"])
    src_bytes = float(request.form["src_bytes"])
    dst_bytes = float(request.form["dst_bytes"])

    # 42 Features
    sample = [
        duration,
        protocol_type,
        service,
        flag,
        src_bytes,
        dst_bytes,
        0,0,0,0,0,
        1,0,0,0,
        0,0,0,0,
        0,0,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,
        0,0,0,0,
        0,0,0,0,
        20
    ]

    prediction = model.predict(pd.DataFrame([sample]))

    if prediction[0] == 1:
        result = "🟢 NORMAL TRAFFIC"
        color = "#2ecc71"
    else:
        result = "🔴 INTRUSION DETECTED"
        color = "#e74c3c"

    return render_template(
        "index.html",
        prediction=result,
        color=color
    )

if __name__ == "__main__":
    app.run(debug=True)