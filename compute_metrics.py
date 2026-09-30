from pathlib import Path
import json
import pandas as pd

root = Path(__file__).parents[1]
df = pd.read_csv(root / "data" / "opd_august_2026.csv")

summary = {}
for age, g in df.groupby("age_group"):
    total = int(g.opd_total.iloc[0])
    summary[age] = {
        "opd_total": total,
        "male_total": int(g[g.sex == "Male"].sex_total.iloc[0]),
        "female_total": int(g[g.sex == "Female"].sex_total.iloc[0]),
        "major_cases": int(g["count"].sum()),
        "major_share_pct": round(g["count"].sum() / total * 100, 2),
        "disease_cases": {k: int(v) for k, v in g.groupby("disease")["count"].sum().sort_values(ascending=False).items()},
    }

# Xisaabta cross_age si firfircoon (dynamic) ah
all_opd = int(df.groupby(["period", "age_group"])["opd_total"].first().sum())
all_major_cases = int(df["count"].sum())

summary["cross_age"] = {
    "pneumonia_u5_vs_over5_ratio": round(
        summary["Under 5"]["disease_cases"].get("Pneumonia", 0) / 
        summary["Over 5"]["disease_cases"].get("Pneumonia", 1), 2
    ),
    "u5_pneumonia_share_pct": round(
        summary["Under 5"]["disease_cases"].get("Pneumonia", 0) / 
        summary["Under 5"]["opd_total"] * 100, 2
    ),
    "over5_uti_female_male_ratio": round(
        summary["Over 5"]["disease_cases"].get("UTI", 0) / 
        max(summary["Over 5"].get("male_total", 1), 1), 2
    ),
    "all_major_cases": all_major_cases,
    "all_opd": all_opd,
}

(root / "outputs").mkdir(exist_ok=True)
(root / "outputs" / "metrics.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
