from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)
print("Server is running")

# Load trained models
cost_model = joblib.load("./models/cost_overrun_model_v1.pkl")
print(" Cost Overrun Model Loaded Successfully" )
time_model = joblib.load("./models/time_overrun_model_v1.pkl")
print(" Time Overrun Model loaded Successfully")
features = [
    "ministry",
    "sector",
    "agency",
    "state",
    "original_cost_cr",
    "cumulative_expenditure_cr",
    "physical_progress_pct",
    "financial_progress_pct",
    "progress_gap",
    "start_delay_months"
]
print(" Features : ")
print(features)


@app.route("/predict", methods=["POST"])
def predict():

    # Client JSON
    project = request.get_json()
    print(" project data is received ")

    # JSON → DataFrame
    df = pd.DataFrame([project])
    print(" project is converted into Dataframe ")

    # Derived features
    df["financial_progress_pct"] = (
        df["cumulative_expenditure_cr"] /
        df["original_cost_cr"].replace(0, pd.NA)
    ) * 100

    df["progress_gap"] = (
        df["financial_progress_pct"] -
        df["physical_progress_pct"]
    )

    # Dates
    df["approval_start_date"] = pd.to_datetime(
        df["approval_start_date"],
        format="%m/%Y",
        errors="coerce"
    )

    df["revised_start_date"] = pd.to_datetime(
        df["revised_start_date"],
        format="%m/%Y",
        errors="coerce"
    )

    df["start_delay_months"] = (
        (df["revised_start_date"].dt.year -
         df["approval_start_date"].dt.year) * 12
        +
        (df["revised_start_date"].dt.month -
         df["approval_start_date"].dt.month)
    )

    print(" Derived Features added ")

    # Select model features
    X = df[features]
    print(" feature selection done ")

    # Predictions
    cost_prediction = cost_model.predict(X)
    time_prediction = time_model.predict(X)

    cost_probability = cost_model.predict_proba(X)[:, 1]
    time_probability = time_model.predict_proba(X)[:, 1]
    print(" Cost and Time Overrun Prediction Done ")
    # Risk score
    risk_score = (
        0.5 * cost_probability[0] +
        0.5 * time_probability[0]
    ) * 100

    print(" Risk score generated ")

    # Risk level
    if risk_score < 30:
        risk_level = "Low"
    elif risk_score < 70:
        risk_level = "Medium"
    else:
        risk_level = "High"
    print(" risk level determined " )

    return jsonify({
        "cost_overrun": int(cost_prediction[0]),
        "cost_overrun_probability": round(float(cost_probability[0]), 4),

        "time_overrun": int(time_prediction[0]),
        "time_overrun_probability": round(float(time_probability[0]), 4),

        "risk_score": round(float(risk_score), 2),
        "risk_level": risk_level
    })


if __name__ == "__main__":
    app.run()
