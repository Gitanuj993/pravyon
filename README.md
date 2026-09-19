# PROVYON
A plateform which identify and predict infrastructure projects.

Link 🖇️ : https://youtu.be/9vcc0LKXQ2s

## File Structure : intended

```txt
pravyon-backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   └── supabase.py
│   │
│   ├── schemas/
│   │   ├── project.py
│   │   └── report.py
│   │
│   └── routers/
│       ├── projects.py
│       └── reports.py
│
├── .env
├── .gitignore
└── requirements.txt

```

## Responsibilities
| File          | Responsibility               |
| ------------- | ---------------------------- |
| `main.py`     | Initialize FastAPI           |
| `config.py`   | Manage environment variables |
| `supabase.py` | Connect to Supabase          |
| `project.py`  | Validate project data        |
| `report.py`   | Validate report data         |
| `projects.py` | Project endpoints            |
| `reports.py`  | Report endpoints             |


## PRAVYON: CRUD Operations

| CRUD Operation | PRAVYON Example      | Backend Action                   | HTTP Method     |
| -------------- | -------------------- | -------------------------------- | --------------- |
| **Create**     | Add a new project    | Insert project into the database | `POST`          |
| **Read**       | View your projects   | Fetch projects from the database | `GET`           |
| **Update**     | Edit project details | Modify existing project data     | `PUT` / `PATCH` |
| **Delete**     | Remove a project     | Delete project from the database | `DELETE`        |


## How PRAVYON CRUD Works
```txt
             PRAVYON Frontend
                    │
                    ▼
               FastAPI
                    │
             CRUD Endpoints
                    │
                    ▼
                Database
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Projects   Reports     Predictions
```

## Example API Endpoints

| Endpoint         | Method   | Purpose                |
| ---------------- | -------- | ---------------------- |
| `/projects`      | `POST`   | Create a project       |
| `/projects`      | `GET`    | Get all projects       |
| `/projects/{id}` | `GET`    | Get a specific project |
| `/projects/{id}` | `PUT`    | Update project details |
| `/projects/{id}` | `DELETE` | Delete a project       |


## Database Schema

### Table `monthly_reports`

**Columns**

| Name | Type | Constraints |
|------|------|-------------|
| `report_id` | `int8` | Primary Identity |
| `project_id` | `int8` |  |
| `reporting_month` | `date` |  |
| `revised_start_date` | `date` |  Nullable |
| `target_doc` | `date` |  Nullable |
| `revised_doc` | `date` |  Nullable |
| `revised_cost_cr` | `numeric` |  Nullable |
| `cumulative_expenditure_cr` | `numeric` |  Nullable |
| `physical_progress_pct` | `numeric` |  Nullable |
| `created_at` | `timestamptz` |  |

### Table `projects`

**Columns**

| Name | Type | Constraints |
|------|------|-------------|
| `project_id` | `int8` | Primary Identity |
| `project_code` | `text` |  Nullable Unique |
| `project_name` | `text` |  |
| `agency` | `text` |  Nullable |
| `legacy_ocms_code` | `text` |  Nullable |
| `pmgid` | `text` |  Nullable |
| `ministry` | `text` |  Nullable |
| `sector` | `text` |  Nullable |
| `state` | `text` |  Nullable |
| `approval_start_date` | `date` |  Nullable |
| `original_cost_cr` | `numeric` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |


## PRAVYON API Architecture
```txt
                    PRAVYON FRONTEND
                          │
                          ▼
                    FASTAPI BACKEND
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        PROJECT APIs           REPORT APIs
              │                       │
              ▼                       ▼
        projects Table        monthly_reports Table
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                    SUPABASE DB
                    PostgreSQL
```                    

## Projects API

### 1. Create a project
- Creates a new project in the database.
```http
POST /api/v1/projects
```

### Request body:
```json
{
  "project_code": "PRJ001",
  "project_name": "Highway Construction",
  "agency": "NHAI",
  "legacy_ocms_code": null,
  "pmgid": null,
  "ministry": "Ministry of Road Transport",
  "sector": "Infrastructure",
  "state": "Madhya Pradesh",
  "approval_start_date": "2025-01-15",
  "original_cost_cr": 150.50
}
```

## 2. Get all projects ( Optional : not required)
```http
GET /api/v1/projects
```

## 3. Get a specific project
- Retrieves the details of a particular project.
```http
GET /api/v1/projects/{project_id}
```

## 4. Update a project

```http
PUT /api/v1/projects/{project_id}
```

### Request body: ( Needs Improvments)
```json
{
  "project_name": "Updated Highway Construction",
  "sector": "Transport",
  "original_cost_cr": 175.00
}
```

## 5. For partial updates :
```http
PATCH /api/v1/projects/{project_id}
```


## 6. Delete a project ( Not required )

```http
DELETE /api/v1/projects/{project_id}
```

