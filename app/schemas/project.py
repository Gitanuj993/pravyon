from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    project_code: str | None = None
    project_name: str
    agency: str | None = None
    legacy_ocms_code: str | None = None
    pmgid: str | None = None
    ministry: str | None = None
    sector: str | None = None
    state: str | None = None
    approval_start_date: date | None = None
    original_cost_cr: Decimal | None = None


class ProjectUpdate(BaseModel):
    project_code: str | None = None
    project_name: str | None = None
    agency: str | None = None
    legacy_ocms_code: str | None = None
    pmgid: str | None = None
    ministry: str | None = None
    sector: str | None = None
    state: str | None = None
    approval_start_date: date | None = None
    original_cost_cr: Decimal | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    project_code: str | None = None
    project_name: str
    agency: str | None = None
    legacy_ocms_code: str | None = None
    pmgid: str | None = None
    ministry: str | None = None
    sector: str | None = None
    state: str | None = None
    approval_start_date: date | None = None
    original_cost_cr: Decimal | None = None