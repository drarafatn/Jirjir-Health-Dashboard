from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Jirjir Health Centre | OPD Intelligence", page_icon="+", layout="wide")
PATH = Path(__file__).parent /  / "opd_august_2026.csv"
REQUIRED = {"period", "age_group", "sex", "disease", "count", "opd_total", "sex_total"}

@st.cache
def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if (df["count"] < 0).any() or (df["opd_total"] <= 0).any() or (df["sex_total"] <= 0).any():
        raise ValueError("Counts and denominators must be non-negative/positive.")
    expected = df.groupby(["period", "age_group", "sex"], as_index=False)["count"].sum()
    # The source file contains selected major diagnoses, not all diagnoses; therefore
    # only denominator integrity, not disease-to-total equality, is asserted.
    if not (df["sex_total"] <= df["opd_total"]).all():
        raise ValueError("Sex denominators cannot exceed age-group OPD totals.")
    return df

def enrich(df: pd.Frame) -> pd.Frame:
    out = df.copy()
    out["share_of_age_opd_pct"] = out["count"] / out["opd_total"] * 100
    out["within_sex_pct"] = out["count"] / out["sex_total"] * 100
    return out

try:
    df = enrich(load_data(str(PATH)))
except Exception as exc:
    st.error(f" validation failed: {exc}")
    st.stop()

st.title("Jirjir Health Centre")
st.caption("Outpatient Department Intelligence | August 2026 | Selected major diagnoses")
st.info("Interpretation note: these are facility attendance proportions among recorded OPD visits, not population incidence rates. Major diagnoses are a selected subset of all diagnoses.")

with st.sidebar:
    st.header("Filters")
    age = st.multiselect("Age group", sorted(df.age_group.unique()), default=sorted(df.age_group.unique()))
    sex = st.multiselect("Sex", sorted(df.sex.unique()), default=sorted(df.sex.unique()))
    diseases = st.multiselect("Diagnosis", sorted(df.disease.unique()), default=sorted(df.disease.unique()))
    view = st.radio("Rate denominator", ["Age-group OPD", "Sex-specific OPD"], index=0)

f = df[df.age_group.isin(age) & df.sex.isin(sex) & df.disease.isin(diseases)]
all_df = df[df.age_group.isin(age)]
major_total = int(f["count"].sum())
selected_opd = int(all_df.drop_duplicates(["period", "age_group"])["opd_total"].sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Selected major cases", f"{major_total:,}")
c2.metric("OPD visits in selected ages", f"{selected_opd:,}")
c3.metric("Major-case share", f"{major_total / selected_opd * 100:.1f}%" if selected_opd else "—")
pneu_u5 = int(df[(df.age_group == "Under 5") & (df.disease == "Pneumonia")]["count"].sum())
c4.metric("Under-5 pneumonia", f"{pneu_u5:,}", f"{pneu_u5 / 240 * 100:.1f}% of under-5 OPD")

left, right = st.columns(2)
with left:
    burden = f.groupby(["age_group", "disease"], as_index=False)["count"].sum().sort_values("count", ascending=True)
    fig = px.bar(burden, x="count", y="disease", color="age_group", barmode="group", orientation="h", title="Selected diagnosis burden")
    fig.update_layout(height=480, legend_title_text="Age group", xaxis_title="Cases", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    sexmix = f.groupby(["disease", "sex"], as_index=False)["count"].sum()
    fig2 = px.bar(sexmix, x="disease", y="count", color="sex", barmode="group", title="Sex distribution by diagnosis")
    fig2.update_layout(height=480, xaxis_title="", yaxis_title="Cases")
    st.plotly_chart(fig2, use_container_width=True)

rate_col = "share_of_age_opd_pct" if view == "Age-group OPD" else "within_sex_pct"
rate_label = "% of age-group OPD" if view == "Age-group OPD" else "% of sex-specific OPD"
rate = f.groupby(["age_group", "disease"], as_index=False).agg(count=("count", "sum"), denominator=("opd_total", "first") if view == "Age-group OPD" else ("sex_total", "sum"))
if view == "Age-group OPD":
    rate["rate"] = rate["count"] / rate["denominator"] * 100
else:
    # Summing sex-specific denominators across selected sexes is appropriate for the filtered view.
    denom = f.groupby("age_group", as_index=False)["sex_total"].sum().rename(columns={"sex_total": "denominator"})
    rate = rate.drop(columns="denominator").merge(denom, on="age_group")
    rate["rate"] = rate["count"] / rate["denominator"] * 100
fig3 = px.bar(rate.sort_values("rate"), x="rate", y="disease", color="age_group", barmode="group", orientation="h", title=f"Diagnosis proportions ({rate_label})")
fig3.update_layout(height=520, xaxis_title=rate_label, yaxis_title="")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Analytical table")
table = f.groupby(["age_group", "disease"], as_index=False).agg(cases=("count", "sum"), age_opd=("opd_total", "first"))
table["share_of_age_opd_%"] = (table["cases"] / table["age_opd"] * 100).round(2)
st.dataframe(table.sort_values(["age_group", "cases"], ascending=[True, False]), use_container_width=True, hide_index=True)

with st.expander("Data quality and interpretation checks"):
    st.write("The dataset is structurally valid when required fields are present, counts are non-negative, and sex-specific denominators do not exceed age-group OPD totals.")
    st.write("Because the source contains selected major diagnoses only, the sum of displayed diagnoses is expected to be below total OPD volume. No disease-specific population denominator, repeat-visit flag, severity marker, outcome, or date-of-visit field was supplied.")

st.caption("Design principles: standardized indicators, explicit denominators, disaggregation by age and sex, transparent data-quality notes, and export-ready tabular views aligned with routine health information system practice.")
