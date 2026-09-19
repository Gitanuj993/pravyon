from fastapi import FastAPI
from app.routers.projects import router as project_router
from app.routers.prediction import router as prediction_router



app = FastAPI(
    title="PRAVYON API",
    description="Project monitoring and prediction backend",
    version="1.0.0"
)

print("Server is running")
app.include_router(project_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to PRAVYON API"
    }
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }



#
# @app.route("/predict", methods=["POST"])
# def predict():
#
#     # Client JSON
#     project = request.get_json()
#     print(" project data is received ")
#
#     # API Gateway ML Model API
#     url = "https://model-service-dev-6h80.onrender.com/predict"
#
#     response = requests.post(url, json=project)
#
#     print("ML Service Status:", response.status_code)
#
#
#     return jsonify(response.json(), response.status_code)
#
#
# if __name__ == "__main__":
#     app.run()
