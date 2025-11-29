from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

with open(model_path, "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
scaler = saved["scaler"]
columns = saved["columns"]

label_map = {
    0: "No major deficiency",
    1: "Iron deficiency",
    2: "Vitamin D deficiency",
    3: "Vitamin B12 deficiency",
    4: "Calcium deficiency",
    5: "Protein deficiency"
}

measure_map = {
    0: "Maintain a balanced diet with fruits, vegetables, whole grains, enough water, and regular physical activity.",
    1: "Include iron-rich foods like leafy greens, jaggery, dates, beans, sprouts; take vitamin C rich foods with meals and avoid tea/coffee immediately after eating.",
    2: "Get 10–20 minutes of safe sunlight daily; include milk, eggs, mushrooms, and vitamin D fortified foods after consulting a professional.",
    3: "Add foods like milk, curd, paneer, eggs, fish and fortified cereals; reduce excessive junk and processed foods.",
    4: "Consume milk, curd, paneer, ragi, sesame seeds (til), almonds and other calcium-rich foods; do light weight-bearing exercise.",
    5: "Increase protein intake through dal, pulses, sprouts, soya, paneer, curd, eggs, lean meat and nuts; avoid skipping meals."
}

@app.route("/")
def home():
    return jsonify({"message": "Nutrition Deficiency Prediction API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        x = [data.get(col, 0) for col in columns]
        x = np.array(x).reshape(1, -1)

        x_scaled = scaler.transform(x)
        pred = model.predict(x_scaled)[0]
        pred_int = int(pred)

        label = label_map.get(pred_int, "Unknown")
        measures = measure_map.get(
            pred_int,
            "Follow a balanced diet and consult a qualified healthcare professional if needed."
        )

        return jsonify({
            "success": True,
            "prediction": pred_int,
            "label": label,
            "measures": measures
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
