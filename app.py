import re
import argparse
import pdfplumber
import pandas as pd
def is_table6_page(text: str) -> bool:
    return "All Ongoing Projects" in text and "Sl.No" in text
def split_project_name_cell(cell: str):

    if not cell:
        return None, None, None, None, None

    lines = [l.strip() for l in cell.split("\n") if l.strip()]
    name_lines, paren_lines = [], []
    for l in lines:
        (paren_lines if l.startswith("(") else name_lines).append(l)

    project_name = " ".join(name_lines) if name_lines else None
    agency = paren_lines[0].strip("()") if len(paren_lines) > 0 else None
    project_code = paren_lines[1].strip("()") if len(paren_lines) > 1 else None

    legacy_code, pmgid = None, None
    if len(paren_lines) > 2:
        groups = re.findall(r"\(([^)]*)\)", paren_lines[2])
        if len(groups) >= 1:
            legacy_code = groups[0] if groups[0] != "-" else None
        if len(groups) >= 2:
            pmgid = groups[1] if groups[1] != "-" else None

    return project_name, agency, project_code, legacy_code, pmgid


def split_original_revised(cell: str):
    
    if not cell:
        return None, None
    parts = [p.strip() for p in cell.split("\n") if p.strip()]
    original = parts[0] if len(parts) > 0 else None
    revised = parts[1].strip("()") if len(parts) > 1 else None
    if revised == "-":
        revised = None
    return original, revised


def extract_table6(pdf_path: str, reporting_month: str) -> pd.DataFrame:
    records = []
    pending_headers = []      # buffered ministry/sector header lines
    current_ministry = None
    current_sector = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if not is_table6_page(text):
                continue

            tables = page.extract_tables()
            if not tables:
                continue

            for row in tables[0][1:]:  # skip the repeated header row
                if row is None or len(row) < 8:
                    continue
                sl_no = (row[0] or "").strip()
                col2 = (row[1] or "").strip()

                # Section-header pseudo-row: Sl.No blank and only col2 filled
                is_header_row = sl_no == "" and col2 != "" and all(
                    (c is None or str(c).strip() == "") for c in row[2:]
                )
                if is_header_row:
                    pending_headers.append(col2)
                    continue

                if sl_no == "":
                    continue  # blank/garbage row, skip

                # A real data row: consume any pending ministry/sector headers
                if pending_headers:
                    if len(pending_headers) >= 2:
                        current_ministry, current_sector = pending_headers[-2], pending_headers[-1]
                    else:
                        current_sector = pending_headers[-1]
                    pending_headers = []

                project_name, agency, project_code, legacy_code, pmgid = split_project_name_cell(row[1])
                state = (row[2] or "").replace("\n", " ").strip() or None
                start_date, revised_start_date = split_original_revised(row[3])
                target_doc, revised_doc = split_original_revised(row[4])
                original_cost, revised_cost = split_original_revised(row[5])
                cum_expenditure = (row[6] or "").strip() or None
                physical_progress = (row[7] or "").strip() or None

                records.append({
                    "reporting_month": reporting_month,
                    "ministry": current_ministry,
                    "sector": current_sector,
                    "sl_no": sl_no,
                    "project_name": project_name,
                    "agency": agency,
                    "project_code": project_code,
                    "legacy_ocms_code": legacy_code,
                    "pmgid": pmgid,
                    "state": state,
                    "approval_start_date": start_date,
                    "revised_start_date": revised_start_date,
                    "target_doc": target_doc,
                    "revised_doc": revised_doc,
                    "original_cost_cr": original_cost,
                    "revised_cost_cr": revised_cost,
                    "cumulative_expenditure_cr": cum_expenditure,
                    "physical_progress_pct": physical_progress,
                })

    return pd.DataFrame(records)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("--month", required=True, help="e.g. 2026-06")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    df = extract_table6(args.pdf_path, args.month)
    df.to_csv(args.out, index=False)
    print(f"Extracted {len(df)} project rows -> {args.out}")
    print(df.head(10).to_string())
