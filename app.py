from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# --- 1. DEGAANKA BOGGA ---
st.set_page_config(
    page_title="Jirjir Health Centre | OPD Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. XEERKA XOGTA ---
# Fiiro gaar ah: Hubi in faylka CSV uu la mid yahay magaca kan hoos ku qoran
PATH = Path(__file__).parent / "opd_august_2026.csv"
REQUIRED = {"period", "age_group", "sex", "disease", "count", "opd_total", "sex_total"}

# --- 3. SHAQADA XOGTA (DATA LOADING & VALIDATION) ---
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    """Xogta CSV-ga ayuu akhriyaa oo hubiyaa in ay sax tahay."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Faylka xogta lama helin: {path}")
    
    df = pd.read_csv(path)
    
    # Hubinta tiirarka loo baahan yahay
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Tiirar muhiim ah ayaa maqan: {sorted(missing)}")
    
    # Nadiifinta xogta (Data Cleaning)
    df = df.dropna(subset=["disease", "age_group", "sex"])
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df["opd_total"] = pd.to_numeric(df["opd_total"], errors="coerce").fillna(1).astype(int)
    df["sex_total"] = pd.to_numeric(df["sex_total"], errors="coerce").fillna(1).astype(int)
    
    # Hubinta xisaabta (Logical Checks)
    if (df["count"] < 0).any() or (df["opd_total"] <= 0).any() or (df["sex_total"] <= 0).any():
        raise ValueError("Tirada (counts) iyo denominator-ka waa inay noqdaan kuwo togan.")
    
    # Hubi in sex_total uusan ka badnayn opd_total
    if not (df["sex_total"] <= df["opd_total"]).all():
        raise ValueError("sex_total ma dhaafi karo opd_total.")
        
    return df

def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """Xisaabinta boqolleyda (Percentages)."""
    out = df.copy()
    out["share_of_age_opd_pct"] = (out["count"] / out["opd_total"]) * 100
    out["within_sex_pct"] = (out["count"] / out["sex_total"]) * 100
    return out

# --- 4. SOO DEEJINTA XOGTA ---
try:
    with st.spinner("Xogta ayaa la soo dejinayaa..."):
        raw_df = load_data(str(PATH))
        df = enrich_data(raw_df)
except Exception as exc:
    st.error(f"⚠️ Khalad ayaa dhacay inta xogta la soo dejinayay: {exc}")
    st.stop()

# --- 5. QORAALKA BOGGA ---
st.title("🏥 Jirjir Health Centre")
st.caption("Outpatient Department Intelligence | August 2026 | Selected major diagnoses")
st.info(
    "**Fiiro gaar ah:** Tirooyinkan waa saamiga (proportions) ee bukaannada OPD-da ka soo muuqday, "
    "ma aha heerka cudurrada bulshada dhexdeeda (population incidence). "
    "Cudurrada waaweyn waa qayb ka mid ah dhammaan cudurrada la diiwaangeliyay."
)

# --- 6. FILTERS-KA (SIDEBAR) ---
with st.sidebar:
    st.header("🔍 Filters")
    st.markdown("---")
    
    age_options = sorted(df.age_group.unique())
    selected_age = st.multiselect("Age Group", age_options, default=age_options)
    
    sex_options = sorted(df.sex.unique())
    selected_sex = st.multiselect("Sex", sex_options, default=sex_options)
    
    disease_options = sorted(df.disease.unique())
    selected_diseases = st.multiselect("Diagnosis", disease_options, default=disease_options)
    
    st.markdown("---")
    view = st.radio(
        "Rate Denominator", 
        ["Age-group OPD", "Sex-specific OPD"], 
        index=0,
        help="Dooro qeybta loo isticmaalayo xisaabta boqolleyda."
    )
    
    st.markdown("---")
    st.caption("Jirjir Health Centre © 2026")

# --- 7. FILTERING XOGTA ---
f_df = df[
    df.age_group.isin(selected_age) & 
    df.sex.isin(selected_sex) & 
    df.disease.isin(selected_diseases)
]

if f_df.empty:
    st.warning("Ma jiraan xog ku habboon filter-ka aad dooratay. Fadlan beddel filters-ka.")
    st.stop()

# --- 8. METRICS-KA MUHIIMKA AH ---
all_df = df[df.age_group.isin(selected_age)]

# Xisaabta saxda ah ee selected_opd
selected_opd = int(all_df.groupby(["period", "age_group"])["opd_total"].first().sum())
major_total = int(f_df["count"].sum())

# Xisaabta Under-5 Pneumonia (si firfircoon)
u5_df = df[df.age_group == "Under 5"]
u5_opd = int(u5_df.groupby(["period", "age_group"])["opd_total"].first().sum()) if not u5_df.empty else 1
pneu_u5 = int(u5_df[u5_df.disease == "Pneumonia"]["count"].sum())
pneu_u5_pct = (pneu_u5 / u5_opd * 100) if u5_opd > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Selected Major Cases", f"{major_total:,}")
c2.metric("OPD Visits (Selected Ages)", f"{selected_opd:,}")
c3.metric("Major-Case Share", f"{major_total / selected_opd * 100:.1f}%" if selected_opd > 0 else "—")
c4.metric("Under-5 Pneumonia", f"{pneu_u5:,}", f"{pneu_u5_pct:.1f}% of under-5 OPD")

st.markdown("---")

# --- 9. JAANTUSYADA (CHARTS) ---
# Qaabka guud ee jaantusyada
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQ = px.colors.qualitative.Set2

# Jaantuska 1: Selected Diagnosis Burden
left_col, right_col = st.columns(2)

with left_col:
    burden = f_df.groupby(["age_group", "disease"], as_index=False)["count"].sum()
    burden = burden.sort_values("count", ascending=True)
    
    fig1 = px.bar(
        burden, 
        x="count", 
        y="disease", 
        color="age_group", 
        barmode="stack", 
        orientation="h",
        title="Selected Diagnosis Burden by Age Group",
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_SEQ
    )
    fig1.update_layout(
        height=480, 
        legend_title_text="Age Group", 
        xaxis_title="Cases", 
        yaxis_title="",
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="y unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Jaantuska 2: Sex Distribution by Diagnosis
with right_col:
    sexmix = f_df.groupby(["disease", "sex"], as_index=False)["count"].sum()
    
    fig2 = px.bar(
        sexmix, 
        x="disease", 
        y="count", 
        color="sex", 
        barmode="stack", 
        title="Sex Distribution by Diagnosis",
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=["#1f77b4", "#ff7f0e"] # Midabada lab iyo dheddig
    )
    fig2.update_layout(
        height=480, 
        xaxis_title="", 
        yaxis_title="Cases",
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="x unified"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Jaantuska 3: Diagnosis Proportions (Rate)
st.markdown("### 📊 Diagnosis Proportions")

rate_col = "share_of_age_opd_pct" if view == "Age-group OPD" else "within_sex_pct"
rate_label = "% of Age-group OPD" if view == "Age-group OPD" else "% of Sex-specific OPD"

if view == "Age-group OPD":
    rate_df = f_df.groupby(["age_group", "disease"], as_index=False).agg(
        count=("count", "sum"),
        denominator=("opd_total", "first")
    )
    rate_df["rate"] = (rate_df["count"] / rate_df["denominator"]) * 100
else:
    # Xisaabta saxda ah ee Sex-specific OPD
    denom_df = f_df.groupby("age_group", as_index=False)["sex_total"].sum().rename(columns={"sex_total": "denominator"})
    rate_df = f_df.groupby(["age_group", "disease"], as_index=False)["count"].sum()
    rate_df = rate_df.merge(denom_df, on="age_group", how="left")
    rate_df["rate"] = (rate_df["count"] / rate_df["denominator"]) * 100

rate_df = rate_df.sort_values("rate", ascending=True)

fig3 = px.bar(
    rate_df, 
    x="rate", 
    y="disease", 
    color="age_group", 
    barmode="stack", 
    orientation="h",
    title=f"Diagnosis Proportions ({rate_label})",
    template=PLOTLY_TEMPLATE,
    color_discrete_sequence=COLOR_SEQ
)
fig3.update_layout(
    height=520, 
    xaxis_title=rate_label, 
    yaxis_title="",
    margin=dict(l=0, r=0, t=40, b=0),
    hovermode="y unified"
)
st.plotly_chart(fig3, use_container_width=True)

# --- 10. TABLES-KA XOGTA ---
st.markdown("### 📋 Analytical Table")
table = f_df.groupby(["age_group", "disease"], as_index=False).agg(
    cases=("count", "sum"),
    age_opd=("opd_total", "first")
)
table["share_of_age_opd_%"] = (table["cases"] / table["age_opd"] * 100).round(2)
table = table.sort_values(["age_group", "cases"], ascending=[True, False])

st.dataframe(
    table, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "cases": st.column_config.NumberColumn("Cases", format="%d"),
        "age_opd": st.column_config.NumberColumn("Age OPD", format="%d"),
        "share_of_age_opd_%": st.column_config.ProgressColumn(
            "Share of Age OPD (%)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=100
        )
    }
)

# --- 11. DATA QUALITY NOTES ---
with st.expander("🔍 Data Quality & Interpretation Checks"):
    st.markdown("""
    **Habka xogta:**
    * Xogta waxaa lagu hubiyay in tiirarka loo baahan yahay ay jiraan, tirada aanay ka yarayn 0, iyo in `sex_total` uusan ka badnayn `opd_total`.
    * Ma jiro xog ku saabsan da'da bukaanka, jinsiga, ama taariikhda booqashada ee qayb ahaan loo isticmaali karo.
    
    **Xaddidaadda:**
    * Sababtoo ah xogta waxay ka kooban tahay oo kaliya cudurrada waaweyn ee la doortay, wadarta cudurrada la soo bandhigay waxay ka yaraanaan doontaa wadarta guud ee OPD-da.
    * Ma jiro denominator-ka dadweynaha (population denominator), calaamad soo noqnoqod (repeat-visit flag), ama natiijada bukaanka (outcome).
    
    **Talo:**
    * Marka la fasiraayo xogta, la xisaabtamo in tirooyinkani ay yihiin kuwa la xiriira booqashada xarunta caafimaadka, ma aha heerka cudurka ee bulshada.
    """)

st.caption(
    "Design principles: Standardized indicators, explicit denominators, disaggregation by age and sex, "
    "transparent data-quality notes, and export-ready tabular views aligned with routine health information system practice."
)
