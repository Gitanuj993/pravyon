

import os
import glob
import pandas as pd
from flask import Flask, request, jsonify

from extract_table6 import extract_table6  # your existing, already-tested function

app = Flask(__name__)

DATA_DIR = "data"
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
MONTHLY_DIR = os.path.join(DATA_DIR, "monthly_csv")
COMBINED_PATH = os.path.join(DATA_DIR, "all_months.csv")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MONTHLY_DIR, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload():
    pdf_file = request.files.get("pdf")
    month = request.form.get("month")  # e.g. "2026-08"

    if not pdf_file or not month:
        return jsonify({"error": "pdf file and 'month' form field are required"}), 400

    pdf_path = os.path.join(UPLOAD_DIR, f"{month}.pdf")
    pdf_file.save(pdf_path)

    # This is the expensive step (PDF parsing) - runs ONCE per month.
    df = extract_table6(pdf_path, reporting_month=month)

    csv_path = os.path.join(MONTHLY_DIR, f"{month}.csv")
    df.to_csv(csv_path, index=False)

    return jsonify({
        "month": month,
        "rows_extracted": len(df),
        "saved_to": csv_path,
        "message": "Ready to combine. This month will not be re-parsed again."
    })


@app.route("/combine", methods=["POST"])
def combine():
    monthly_files = sorted(glob.glob(os.path.join(MONTHLY_DIR, "*.csv")))
    if not monthly_files:
        return jsonify({"error": "No monthly CSVs found. Upload PDFs first."}), 400

    frames = [pd.read_csv(f) for f in monthly_files]
    combined = pd.concat(frames, ignore_index=True)

    # Safety net: if the same month was uploaded twice, keep the latest file's
    # rows only (drop older duplicate reporting_month + project_code pairs).
    combined = combined.drop_duplicates(subset=["reporting_month", "project_code"], keep="last")

    combined.to_csv(COMBINED_PATH, index=False)

    return jsonify({
        "months_included": [os.path.basename(f).replace(".csv", "") for f in monthly_files],
        "total_rows": len(combined),
        "saved_to": COMBINED_PATH
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    if not os.path.exists(COMBINED_PATH):
        return jsonify({"error": "No combined dataset yet. Call /combine first."}), 400

    df = pd.read_csv(COMBINED_PATH)

    df["original_cost_cr"] = pd.to_numeric(df["original_cost_cr"], errors="coerce")
    df["revised_cost_cr"] = pd.to_numeric(df["revised_cost_cr"], errors="coerce")
    df["cost_growth_pct"] = (
        (df["revised_cost_cr"] - df["original_cost_cr"]) / df["original_cost_cr"] * 100
    ).round(2)

    # Placeholder rule-based risk flag - swap for your trained classifier later.
    df["risk_flag"] = df["cost_growth_pct"].apply(
        lambda x: "HIGH" if pd.notna(x) and x > 10 else ("LOW" if pd.notna(x) else "UNKNOWN")
    )

    summary = {
        "total_projects": int(df["project_code"].nunique()),
        "high_risk_count": int((df.groupby("project_code")["risk_flag"].last() == "HIGH").sum()),
        "avg_cost_growth_pct": round(float(df["cost_growth_pct"].mean(skipna=True)), 2),
    }

    df.to_csv(os.path.join(DATA_DIR, "analysis_results.csv"), index=False)

    return jsonify({"summary": summary, "results_saved_to": "data/analysis_results.csv"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
