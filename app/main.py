from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
print("Server is running")


@app.route("/predict", methods=["POST"])
def predict():

    # Client JSON
    project = request.get_json()
    print(" project data is received ")

    # API Gateway ML Model API
    url = "https://model-service-dev-6h80.onrender.com/predict"

    response = requests.post(url, json=project)
    
    print("ML Service Status:", response.status_code)

    
    return jsonify(response.json(), response.status_code)


if __name__ == "__main__":
    app.run()
