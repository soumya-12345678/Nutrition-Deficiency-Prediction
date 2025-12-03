from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load Model and Scaler
try:
    with open('model.pkl', 'rb') as f:
        data = pickle.load(f)
        model = data['model']
        scaler = data['scaler']
    print("Model and Scaler loaded successfully.")
except FileNotFoundError:
    print("Error: model.pkl not found. Run train_model.py first.")
    model = None
    scaler = None

# Labels based on our NHANES training logic
RISK_MAP = {
    0: {
        "label": "Low Risk / Healthy Range",
        "measures": "Your profile matches individuals with healthy lab results. Maintain a balanced diet rich in fruits, vegetables, and whole grains."
    },
    1: {
        "label": "High Risk: Anemia / Iron Deficiency",
        "measures": "Your profile shares characteristics with groups prone to low hemoglobin. Increase Iron intake (Spinach, Red Meat, Lentils) and Vitamin C to aid absorption."
    },
    2: {
        "label": "High Risk: Elevated Cholesterol / Dietary Imbalance",
        "measures": "Your profile suggests a risk of metabolic imbalance. Consider reducing saturated fats and increasing fiber intake (Oats, Beans)."
    }
}


@app.route('/predict', methods=['POST'])
def predict():
    if not model or not scaler:
        return jsonify({'success': False, 'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        
        # 1. Extract Basic Features
        age = float(data.get('age'))
        gender = int(data.get('gender')) # 0=Male, 1=Female
        height_cm = float(data.get('height'))
        weight_kg = float(data.get('weight'))
        
        # 2. Feature Engineering (Match training logic)
        # Calculate BMI
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m ** 2)
        
        # Prepare input vector: [Age, Gender, BMI]
        features = np.array([[age, gender, bmi]])
        
        # 3. Scale Inputs
        features_scaled = scaler.transform(features)
        
        # 4. Predict
        prediction_class = int(model.predict(features_scaled)[0])
        
        # 5. Symptom Boosting (Heuristic Layer)
        # If the model says "Healthy" (0) but user reports specific symptoms, 
        # we can override or append to the warning.
        
        # Check for user-reported symptoms
        reported_pale = data.get('pale_skin') == 1
        reported_fatigue = data.get('fatigue') == 1
        
        result = RISK_MAP.get(prediction_class, RISK_MAP[0])
        
        # Heuristic Override: If healthy but has anemia symptoms
        if prediction_class == 0 and (reported_pale or reported_fatigue):
            result = {
                "label": "Moderate Risk: Possible Iron Deficiency",
                "measures": "While your demographic profile is low-risk, your reported symptoms (Pale Skin/Fatigue) are strong indicators of Anemia. Consider a blood test."
            }

        return jsonify({
            'success': True,
            'label': result['label'],
            'measures': result['measures']
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)