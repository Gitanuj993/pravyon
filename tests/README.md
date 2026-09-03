
## API Testing 
From Google Colab 
```txt
import requests

url = "https://pravyon-backend-1.onrender.com/predict"

# json me jayega
project = {
    "reporting_month": "2026-04",
    "ministry": "Ministry of Civil Aviation",
    "sector": "Aviation & Aviation Infrastructure",
    "sl_no": 1,
    "project_name": "...",
    "agency": "Airport Authority of India [AAI]",
    "project_code": 612786,
    "legacy_ocms_code": "N04000106",
    "pmgid": None,
    "state": "Andhra Pradesh",
    "approval_start_date": "03/2023",
    "revised_start_date": "01/2024",
    "target_doc": "01/2026",
    "revised_doc": "07/2026",
    "original_cost_cr": 265.91,
    "revised_cost_cr": 265.91,
    "cumulative_expenditure_cr": 129.07,
    "physical_progress_pct": 65.0
}
response = requests.post(url, json=project)
print(response.status_code)
print(response.text)
```
Curl Testing 

```txt
curl -X POST "https://pravyon-backend-1.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "reporting_month": "2026-04",
    "ministry": "Ministry of Civil Aviation",
    "sector": "Aviation & Aviation Infrastructure",
    "sl_no": 1,
    "project_name": "...",
    "agency": "Airport Authority of India [AAI]",
    "project_code": 612786,
    "legacy_ocms_code": "N04000106",
    "pmgid": null,
    "state": "Andhra Pradesh",
    "approval_start_date": "03/2023",
    "revised_start_date": "01/2024",
    "target_doc": "01/2026",
    "revised_doc": "07/2026",
    "original_cost_cr": 265.91,
    "revised_cost_cr": 265.91,
    "cumulative_expenditure_cr": 129.07,
    "physical_progress_pct": 65.0
  }'
```
Expected Output 
```txt
200
[{"cost_overrun":0,"cost_overrun_probability":0.0672,"risk_level":"Medium","risk_score":33.49,"status":"success","time_overrun":1,"time_overrun_probability":0.6026},200]
```



