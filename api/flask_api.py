from flask import Flask, request, jsonify
import joblib
import numpy as np

# ✅ Define the Flask app
app = Flask(__name__)

# ✅ Load the trained model
model = joblib.load('../model/cybersecurity_ai_model.pkl')

# ✅ (Optional) Home route to test Flask is working
@app.route('/')
def home():
    return "✅ Flask API is running! Use POST /predict to test"

# ✅ Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['features']
    prediction = model.predict([np.array(data)])
    return jsonify({'prediction': int(prediction[0])})

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
