# 🏥 Jirjir Health Centre OPD Intelligence Dashboard

An interactive data analytics dashboard for Outpatient Department (OPD) intelligence at Jirjir Health Centre, Somalia. This project analyzes August 2026 OPD attendance data to identify major disease burdens, sex disparities, and operational priorities.

## 📊 Project Overview

This dashboard provides:
- **Age-disaggregated disease burden** (Under 5 vs. Over 5)
- **Sex-disaggregated analysis** (Male vs. Female)
- **Top major diseases** ranking
- **Diagnosis proportions** with adjustable denominators
- **Data quality and interpretation notes**

## 🎯 Key Findings (August 2026)

- **470 OPD visits** recorded (240 Under 5, 230 Over 5)
- **170 selected major-diagnosis cases** (36.2% of all OPD visits)
- **Pneumonia** was the leading diagnosis with **49 cases** (27 Under 5, 22 Over 5)
- **UTI** was female-skewed among older attendees (10 Female vs. 5 Male)
- **Acute Watery Diarrhoea** was strongly concentrated in Under 5 (17 cases)

## 🛠️ Technologies Used

- **Python 3.10+**
- **Streamlit** — Interactive web dashboard
- **Pandas** — Data manipulation
- **Plotly** — Interactive visualizations
- **Pytest** — Unit testing

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/drarafatn/Jirjir-Health-Dashboard.git
cd Jirjir-Health-Dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
