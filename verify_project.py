from pathlib import Path
import json
import py_compile
import pandas as pd

root = Path(__file__).parents[1]
required = [root / "README.md", root / "CASE_STUDY.md", root / "app.py", root / "requirements.txt", root / "data/opd_august_2026.csv", root / "outputs/metrics.json", root / "tests/test_metrics.py"]
for path in required:
    assert path.exists() and path.stat().st_size > 0, path
py_compile.compile(str(root / "app.py"), doraise=True)
df = pd.read_csv(root / "data/opd_august_2026.csv")
assert df.groupby("age_group").opd_total.first().to_dict() == {"Over 5": 230, "Under 5": 240}
assert df[df.disease == "Pneumonia"].groupby("age_group")["count"].sum().to_dict() == {"Over 5": 22, "Under 5": 27}
metrics = json.loads((root / "outputs/metrics.json").read_text())
assert metrics["cross_age"]["all_major_cases"] == 170
print("verification passed: files, syntax, denominators, pneumonia counts, and metrics")
