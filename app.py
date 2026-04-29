import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="AI ESG Dashboard", layout="wide")

# Title
st.title("AI ESG Dashboard")

# File path
file_path = "brsr_2024-2025 _Final.xlsx"

# Load data
@st.cache_data
def load_data(file_path):
    all_sheets = pd.read_excel(file_path, sheet_name=None)

    df = pd.concat(
        [sheet.assign(sheet_name=name) for name, sheet in all_sheets.items()],
        ignore_index=True
    )
    return df

df = load_data(file_path)

# -------------------------------
# DATA CLEANING
# -------------------------------

df = df[['company_name', 'sector_name', 'value', 'sheet_name']].dropna()

# Reduce data for performance
selected_companies = df['company_name'].unique()[:40]
df = df[df['company_name'].isin(selected_companies)]

# Scoring
df['value_clean'] = df['value'].astype(str).str.lower()
df['score'] = df['value_clean'].apply(lambda x: 1 if 'true' in x else 0)

# -------------------------------
# KPI SECTION
# -------------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Companies", df['company_name'].nunique())
col2.metric("Total Records", len(df))
col3.metric("Avg Compliance Score", round(df['score'].mean(), 2))

# -------------------------------
# FILTER
# -------------------------------

st.sidebar.title("Filters")

selected_company = st.sidebar.selectbox(
    "Select Company",
    df['company_name'].unique()
)

filtered_df = df[df['company_name'] == selected_company]

# -------------------------------
# COMPANY INSIGHT
# -------------------------------

company_avg = filtered_df['score'].mean()

st.subheader(f"📌 {selected_company} Compliance Score")
st.metric("Score", round(company_avg, 2))

# -------------------------------
# MOCK AI FUNCTION (NO API)
# -------------------------------

def generate_ai_insights(data):
    avg_score = round(data['score'].mean(), 2)

    insights = f"""
### 🔍 Key Trends
- Average compliance score is **{avg_score}**
- Companies show varying ESG disclosure quality

### ⚠️ Risk Areas
- Low scoring companies indicate weak compliance
- Some principles have consistently low scores

### 🏭 Sector Insights
- Performance varies significantly across sectors
- Certain sectors demonstrate stronger ESG practices

### 💡 Recommendations
- Improve disclosure consistency across all principles
- Focus on low-performing ESG areas
- Benchmark against top-performing companies
"""
    return insights

# -------------------------------
# COMPANY RANKING
# -------------------------------

company_score = df.groupby('company_name')['score'].mean().reset_index()
company_score = company_score.sort_values(by='score', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Companies")
    st.dataframe(company_score.head(5))

with col2:
    st.subheader("⚠️ Low Compliance")
    st.dataframe(company_score.tail(5))

# -------------------------------
# SECTOR ANALYSIS
# -------------------------------

sector_score = df.groupby('sector_name')['score'].mean()

st.subheader("📊 Sector-wise Compliance")
st.bar_chart(sector_score)

# -------------------------------
# PRINCIPLE ANALYSIS
# -------------------------------

principle_score = df.groupby('sheet_name')['score'].mean()

st.subheader("📈 Principle-wise Compliance")
st.bar_chart(principle_score)

# -------------------------------
# AI INSIGHTS (MOCK)
# -------------------------------

st.subheader("🧠 AI ESG Insights")

if st.button("Generate AI Insights"):
    with st.spinner("Analyzing ESG data..."):
        insights = generate_ai_insights(df)

    st.success("Analysis Complete!")
    st.markdown(insights)

# -------------------------------
# COMPANY AI ANALYSIS
# -------------------------------

st.subheader("🏢 Company Analysis")

if st.button("Analyze Selected Company"):
    with st.spinner("Analyzing company..."):
        insights = generate_ai_insights(filtered_df)

    st.markdown(insights)