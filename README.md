# AWS SaaS Sales Analysis

A statistical deep dive into ~10,000 AWS SaaS transactions across three global regions, built as an interactive Streamlit app — combining Kaggle sales data with World Bank macroeconomic indicators to answer one question: **why are some regions profitable while others bleed money?**

---

## Built With

- **Python 3.11**
- **Streamlit** — multipage app framework
- **Pandas / NumPy** — data manipulation
- **Plotly** — interactive charts
- **SciPy** — statistical hypothesis testing
- **World Bank API** — macroeconomic enrichment (`requests`)

---

## Project Structure

```
week_19_project-week3/
├── app.py                          # Entry point — navigation config
├── requirements.txt
├── pages/
│   ├── home.py                     # Page 1: The Story (landing page)
│   ├── 1_📊_The_Protagonist.py     # Page 2: Confidence intervals
│   ├── 2_🔍_Business_Questions.py  # Page 3: 5 hypothesis tests
│   └── 3_📋_Summary.py             # Page 4: Findings & recommendations
├── utils/
│   └── styles.py                   # Global styles, fonts, divider component
├── data/
│   ├── raw/                        # Original CSV files
│   └── cleaned/
│       └── saas_sales_clean.csv    # Cleaned dataset used by the app
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   └── 04_hypothesis_testing.ipynb
└── src/
    ├── cleaning.py
    └── analysis.py
```

---

## Key Findings

| # | Business Question | Test | Result |
|---|---|---|---|
| BQ1 | Does national wealth predict profit? | Linear Regression | H₀ not rejected — R² = 0.005 |
| BQ2 | Is SaaS adoption higher in connected countries? | Pearson Correlation | H₀ not rejected — r = 0.07 |
| BQ3 | Do discount strategies differ across regions? | Independent t-Test | **H₀ rejected** — p < 0.001 |
| BQ4 | Does customer segment affect profitability? | One-Way ANOVA | H₀ not rejected — p = 0.21 |
| BQ5 | Do discounts cause losses? | Chi-Square Test | **H₀ rejected** — χ² = 2,123 |

**The central finding:** 100% of all 1,871 loss-making transactions had a discount applied. Zero non-discounted transactions resulted in a loss. External factors (GDP, internet access, customer segment) have no meaningful effect on profitability — discount governance is the only lever that matters.

Regional discount averages: AMER 10.9% / EMEA 14.1% / APJ 27.0% (nearly 3x AMER).

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app runs locally at `http://localhost:8501`.

**Live demo:** [Deployed on Streamlit Cloud](https://streamlit.io/cloud)

---

## Data Sources

- **AWS SaaS Sales Dataset** — [Kaggle](https://www.kaggle.com/datasets/nnthanh101/aws-saas-sales) — 9,994 transactions across EMEA, AMER, and APJ (2020–2023)
- **GDP per Capita** — World Bank API indicator `NY.GDP.PCAP.CD`
- **Internet Penetration** — World Bank API indicator `IT.NET.USER.ZS`
