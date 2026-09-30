from pathlib import Path
import json
import py_compile
import pandas as pd

root = Path(__file__).parents[1]

# Liiska faylasha loo baahan yahay (la saxay)
required = [
    root / "app.py",
    root / "requirements.txt",
    root / "data" / "opd_august_2026.csv",
    root / "outputs" / "metrics.json",
]

for path in required:
    assert path.exists() and path.stat().st_size > 0, f"Missing or empty file: {path}"

# Hubi in app.py uu si sax ah u shaqeynayo (syntax)
py_compile.compile(str(root / "app.py"), doraise=True)

# Akhri xogta CSV-ga
df = pd.read_csv(root / "data" / "opd_august_2026.csv")

# Hubi in OPD totals ay sax yihiin
opd_totals = df.groupby("age_group").opd_total.first().to_dict()
assert opd_totals == {"Over 5": 230, "Under 5": 240}, f"OPD totals mismatch: {opd_totals}"

# Hubi in Pneumonia counts ay sax yihiin
pneumonia_counts = df[df.disease == "Pneumonia"].groupby("age_group")["count"].sum().to_dict()
assert pneumonia_counts == {"Over 5": 22, "Under 5": 27}, f"Pneumonia counts mismatch: {pneumonia_counts}"

# Hubi in metrics.json uu sax yahay
metrics = json.loads((root / "outputs" / "metrics.json").read_text())
assert metrics["cross_age"]["all_major_cases"] == 170, f"Major cases mismatch: {metrics['cross_age']['all_major_cases']}"

print("verification passed: files, syntax, denominators, pneumonia counts, and metrics")
