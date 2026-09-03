# Jirjir Health Centre OPD Intelligence Case Study

**Reporting period:** August 2026  
**Author:** Arafat  
**Analytical role:** Principal Healthcare Data Scientist, Public Health Epidemiologist, and Senior Operations Researcher

## Executive conclusion

Jirjir Health Centre recorded **470 OPD visits** in the supplied August 2026 extract: 240 among children under five years and 230 among patients over five years. The dataset contains **170 cases in the selected major-diagnosis subset**, equal to **36.2% of all OPD visits**. This is a facility attendance proportion, not population incidence, because no catchment population denominator or unique-patient identifier was supplied.

The principal operational signal is the concentration of respiratory illness in young children. Pneumonia accounted for **27 under-five cases**, or **11.3% of all under-five OPD visits**, compared with 22 cases among older attendees, or **9.6% of over-five OPD visits**. Within the selected major-diagnosis subset, pneumonia represented 32.1% of under-five cases and 25.6% of over-five cases. Acute watery diarrhoea and cough each contributed 17 under-five cases, indicating a combined respiratory and enteric service requirement.

The main sex-disaggregated signal is different by age. Under-five attendance was female-skewed overall, with 130 female and 110 male visits. However, pneumonia cases were male-skewed in this extract: 15 male versus 12 female cases. Among older attendees, the OPD denominator was close to balanced, while UTI was female-skewed: 10 female versus 5 male cases. Using sex-specific OPD denominators, UTI represented **8.9% of female over-five visits** versus **4.2% of male over-five visits**, an attendance-proportion ratio of approximately **2.1**. This should trigger service review and targeted assessment, not a causal conclusion.

The immediate management priority is to protect continuity of care for childhood pneumonia and diarrhoeal disease while strengthening triage, pulse-oximetry/respiratory assessment, ORS and zinc availability, antibiotic stewardship, and routine data quality. WHO guidance emphasizes evidence-informed management of childhood pneumonia and diarrhoea, while its routine health information toolkit emphasizes standardized indicators, explicit denominators, and regular quality review.[1] [2] [3]

## 1. Data and methods

The source is an aggregate, one-month OPD extract with two age strata, sex, selected major diagnoses, age-group OPD totals, and sex-specific attendance totals. The analysis treats each reported diagnosis count as a recorded attendance event. It does not assume that each count represents a unique patient, a new episode, a laboratory-confirmed case, or a population-based incident case.

For each diagnosis, the primary facility indicator is the **diagnosis attendance proportion**:

> Diagnosis attendance proportion = recorded diagnosis count ÷ total OPD visits in the relevant age group × 100.

A secondary indicator is the **sex-specific attendance proportion**:

> Sex-specific attendance proportion = recorded diagnosis count ÷ OPD visits for that sex in the relevant age group × 100.

The supplied diagnoses are explicitly a selected subset. Therefore, their counts must not be summed and interpreted as the full morbidity burden. The analytical dashboard preserves this distinction in its labels and interpretation note.

## 2. Descriptive epidemiology

| Indicator | Under 5 | Over 5 | Total |
|---|---:|---:|---:|
| OPD visits | 240 | 230 | 470 |
| Male visits | 110 | 118 | 228 |
| Female visits | 130 | 112 | 242 |
| Selected major-diagnosis cases | 84 | 86 | 170 |
| Selected major-diagnosis share of OPD | 35.0% | 37.4% | 36.2% |

The age groups contributed similar OPD volumes. Children under five accounted for 51.1% of all visits, while older attendees accounted for 48.9%. The overall female-to-male attendance ratio was 1.06, but the direction differed by age: 1.18 among under-five visits and 0.95 among older visits.

### Disease burden by age group

| Diagnosis | Under 5 cases | Under 5 share of OPD | Over 5 cases | Over 5 share of OPD | Interpretation |
|---|---:|---:|---:|---:|---|
| Pneumonia | 27 | 11.25% | 22 | 9.57% | Highest selected burden in both groups; priority clinical pathway. |
| Acute watery diarrhoea | 17 | 7.08% | 3 | 1.30% | Strongly concentrated among under-five attendees. |
| Cough | 17 | 7.08% | 11 | 4.78% | Respiratory workload, including possible overlap with pneumonia. |
| Unknown fever | 8 | 3.33% | 16 | 6.96% | Higher among older attendees; requires syndromic review and testing/referral rules. |
| Dysentery | 8 | 3.33% | — | — | Under-five enteric disease signal; reinforce dehydration and blood-in-stool triage. |
| Skin disease | 7 | 2.92% | 14 | 6.09% | Higher among older attendees; assess environmental and occupational exposures. |
| UTI | 0 | 0.00% | 15 | 6.52% | Female-skewed older-attendee burden; review diagnostic and treatment practices. |
| Trauma/injury | 0 | 0.00% | 5 | 2.17% | Smaller volume but relevant for emergency readiness and prevention. |

Across both groups, pneumonia was the leading selected diagnosis with 49 cases. The under-five pneumonia count was 1.23 times the over-five count despite similar age-group OPD volumes. This is a comparative facility signal, not a risk ratio for the underlying population.

## 3. Sex disparities

### Under-five group

Under-five OPD attendance was female-skewed, with 130 female and 110 male visits. Pneumonia was recorded in 15 male children and 12 female children. Relative to sex-specific OPD denominators, pneumonia represented **13.6% of male under-five visits** and **9.2% of female under-five visits**. The difference is compatible with a service signal, but it cannot establish biological susceptibility or care-seeking causality from one month of aggregate data.

Acute watery diarrhoea was 9 male versus 8 female cases, while cough was 8 male versus 9 female cases. Dysentery was 3 male versus 5 female cases. These small counts should be monitored over multiple months before operational policy is changed on the basis of sex alone.

### Over-five group

Older OPD attendance was near-balanced, with 118 male and 112 female visits. UTI was recorded in 10 female and 5 male attendees. The corresponding sex-specific attendance proportions were **8.9% for females** and **4.2% for males**. The female-to-male count ratio was 2.0, and the attendance-proportion ratio was approximately 2.1. Plausible explanations include true disease burden, referral and care-seeking patterns, pregnancy-related or reproductive-health service contact, diagnostic coding practices, or differences in testing access. The dashboard should therefore be paired with chart review and, where appropriate, pregnancy status, age bands, and diagnostic confirmation.

Unknown fever was also female-skewed in counts among older attendees, 9 versus 7, but the difference is small. Skin disease was 8 female versus 6 male, while cough was 4 female versus 7 male. The overall pattern is not a uniform sex disparity across diagnoses.

## 4. Seasonal and contextual interpretation

August clustering can be hypothesized but not demonstrated from a single month. Pneumonia and cough may be influenced by respiratory pathogen circulation, indoor crowding, smoke exposure, rainfall-related indoor time, and delayed care. Acute watery diarrhoea and dysentery may be influenced by water, sanitation, hygiene, food handling, flooding, and household transmission. Skin disease may increase with heat, humidity, crowding, or occupational exposure. Unknown fever may reflect a broad syndromic category that requires local differential diagnosis and testing pathways.

These are **contextual hypotheses**, not measured risk factors in this dataset. A defensible seasonal analysis requires at least 12–24 months of monthly counts, preferably with catchment population denominators, rainfall and temperature, water/sanitation indicators, vaccination coverage, stock-out periods, and referral outcomes. The next data model should add date or epidemiological week, residence or catchment area, unique visit identifier, age bands, pregnancy status where clinically appropriate, diagnosis certainty, severity, treatment, referral, outcome, and stock-out indicators.

## 5. Clinical and operational recommendations

### Medicines and commodities

Jirjir should maintain a minimum service-level buffer for oral rehydration salts, zinc, paediatric antibiotics selected under national treatment guidelines, antipyretics, urine-testing supplies where available, skin-disease treatments, gloves, and infection-prevention consumables. The stock plan should use a rolling consumption and morbidity forecast rather than a one-month count. For each tracer commodity, calculate average monthly consumption, lead time, safety stock, months of stock, stock-out days, and expiry exposure.

For diarrhoeal disease, WHO describes low-osmolarity ORS and routine zinc supplementation as effective components of childhood diarrhoea management, with zinc dosing dependent on age and current guidance.[2] The facility should pair commodity availability with caregiver instruction, continued feeding, danger-sign counselling, and a documented dehydration assessment.

For antibiotics, procurement should follow the national essential medicines list and treatment protocols. The WHO AWaRe framework provides evidence-informed guidance on antibiotic choice, dose, route, and duration for common infections and is intended to support appropriate use and antimicrobial-resistance prevention.[3] The dashboard should not infer antibiotic quantities directly from pneumonia counts; it should incorporate clinical classification, treatment regimen, weight bands, and actual consumption.

### Staffing and workflow

The data justify a focused paediatric triage capability during peak OPD hours. The minimum workflow should include a rapid danger-sign screen, respiratory rate by age, oxygen saturation where available, temperature, hydration assessment for diarrhoea, weight for dosing, and escalation criteria. A trained nurse or clinical officer should own triage, while the prescriber and pharmacy team use a standardized pneumonia/diarrhoea checklist.

The facility should conduct a weekly 15-minute morbidity-and-stock huddle. The huddle should review pneumonia, diarrhoea, dysentery, fever, stock-outs, referrals, deaths, and data completeness. This creates a feedback loop between surveillance and operations rather than treating the dashboard as a passive report.

### Prevention and community action

For respiratory disease, reinforce vaccination status review, early care-seeking for respiratory danger signs, smoke-exposure reduction, ventilation, and infection-prevention practices. For diarrhoeal disease, prioritize safe water, hand hygiene, sanitation, food safety, household ORS literacy, and rapid referral for dehydration or blood in stool. For skin disease, assess crowding, hygiene, occupational exposure, and household clustering. For injuries, use brief prevention counselling and maintain emergency first-aid readiness.

## 6. Data-quality and governance plan

WHO’s routine health information systems toolkit identifies health facility data as important for patient management, facility administration, surveillance, monitoring service delivery, and resource utilization. It recommends standardized indicators, explicit attention to representativeness and denominators, and data-quality review covering completeness, timeliness, internal consistency, and external consistency.[1]

The first monthly data-quality review should reconcile the OPD register, diagnosis tally, pharmacy issue records, laboratory log, referral register, and submitted aggregate report. The review should record whether every field is complete, whether totals are internally consistent, whether duplicated visits are possible, whether diagnosis definitions are stable, and whether stock-outs may have altered observed prescribing or attendance.

The dashboard intentionally does not calculate population incidence, case fatality, treatment success, antibiotic consumption, or service coverage because their required denominators or outcome fields were not provided. Those indicators should be added only after the data model is expanded.

## 7. GitHub portfolio structure

```text
jirjir-opd-analytics/
├── README.md
├── CASE_STUDY.md
├── LICENSE
├── requirements.txt
├── app.py
├── data/
│   ├── README.md
│   └── opd_august_2026.csv
├── scripts/
│   └── compute_metrics.py
├── tests/
│   └── test_metrics.py
├── outputs/
│   ├── metrics.json
│   └── figures/
├── docs/
│   ├── data_dictionary.md
│   ├── indicator_reference.md
│   ├── data_quality_plan.md
│   └── privacy_and_governance.md
└── .github/workflows/ci.yml
```

The portfolio should emphasize ten years of clinical operations experience by connecting each analytic output to a real workflow: triage, prescribing, pharmacy replenishment, referral, community prevention, and monthly performance review. It should show both technical depth and operational judgment. Screenshots of the dashboard should be paired with a short decision narrative that states the signal, the denominator, the action, the owner, and the monitoring metric.

## References

[1]: https://www.who.int/data/data-collection-tools/health-service-data/toolkit-for-routine-health-information-system-data/modules "WHO Toolkit for Routine Health Information Systems Data"

[2]: https://www.who.int/tools/elena/bbc/zinc-diarrhoea "WHO Zinc supplementation in the management of diarrhoea"

[3]: https://www.who.int/publications/i/item/9789240062382 "The WHO AWaRe antibiotic book"

[4]: https://www.who.int/publications/i/item/9789240103412 "WHO Guideline on management of pneumonia and diarrhoea in children up to 10 years of age"
