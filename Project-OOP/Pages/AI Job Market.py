import streamlit as st
from models.dataset import Dataset
from Visualization.bar_chart import BarChart
from Visualization.histogram import HistogramChart
from Visualization.pie_chart import PieChart

st.set_page_config(page_title="AI Job Market", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; }

section[data-testid="stSidebar"] { background: #090c11 !important; }

.hero {
    padding: 40px 0 32px;
    border-bottom: 1px solid #1e2130;
    margin-bottom: 32px;
}
.hero-tag {
    font-size: 11px; font-weight: 500; letter-spacing: 0.18em;
    text-transform: uppercase; color: #6366f1; margin-bottom: 12px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 36px; font-weight: 800;
    color: #f1f5f9; letter-spacing: -1px;
    line-height: 1.1; margin-bottom: 12px;
}
.hero-desc {
    font-size: 14px; font-weight: 300;
    color: #64748b; line-height: 1.7; max-width: 560px;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 36px;
}
.metric-card {
    background: #13151c;
    border: 1px solid #1e2130;
    border-radius: 12px;
    padding: 18px 20px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 24px; font-weight: 700;
    color: #f1f5f9; line-height: 1; margin-bottom: 4px;
}
.metric-label {
    font-size: 11px; color: #475569;
    text-transform: uppercase; letter-spacing: 0.08em;
}
.metric-accent { color: #6366f1; }

.chart-header { margin: 28px 0 6px; }
.chart-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px; font-weight: 700;
    color: #e2e8f0; margin-bottom: 4px;
}
.chart-desc { font-size: 12px; color: #475569; line-height: 1.5; }

.divider {
    height: 1px; background: #1e2130;
    margin: 28px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
dataset = Dataset("Datasets/ai_jobs_market_2025_2026.csv")
dataset.load()
dataset.clean()
df = dataset.df

# ── Compute stats ─────────────────────────────────────────────────────────────
total_jobs   = len(df)
avg_salary   = int(df["annual_salary_usd"].mean())
max_salary   = int(df["annual_salary_usd"].max())
remote_pct   = round(df["remote_work"].isin(["Fully Remote","Hybrid"]).mean() * 100, 1)
top_job      = df.groupby("job_title")["annual_salary_usd"].mean().idxmax()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Data · 2025 – 2026</div>
    <div class="hero-title">AI Job Market</div>
    <div class="hero-desc">
        Explore salary trends, job distribution, and work preferences across
        <b style="color:#e2e8f0">{total_jobs:,} AI & ML listings</b> from
        {df['country'].nunique()} countries. Data covers roles from entry-level
        to lead positions across {df['job_title'].nunique()} distinct job titles.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{total_jobs:,}</div>
        <div class="metric-label">Total listings</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">${avg_salary//1000}k</div>
        <div class="metric-label">Avg salary</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">${max_salary//1000}k</div>
        <div class="metric-label">Max salary</div>
    </div>
    <div class="metric-card">
        <div class="metric-value"><span class="metric-accent">{remote_pct}%</span></div>
        <div class="metric-label">Remote / hybrid</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{df['country'].nunique()}</div>
        <div class="metric-label">Countries</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 1 ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Avg Salary by Job Title</div>
    <div class="chart-desc">
        Top 10 roles ranked by average annual salary (USD).
        <b style="color:#e2e8f0">{top_job}</b> leads with the highest avg compensation.
    </div>
</div>
""", unsafe_allow_html=True)

df_bar = dataset.group_by("job_title", "annual_salary_usd")
df_bar = df_bar.sort_values("annual_salary_usd", ascending=False).head(10)
BarChart(df_bar, x="job_title", y="annual_salary_usd",
         title="Avg Salary by Job Title", horizontal=True).show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 2 ───────────────────────────────────────────────────────────────────
remote_counts = df["remote_work"].value_counts()
top_work = remote_counts.index[0]
top_work_pct = round(remote_counts.iloc[0] / len(df) * 100, 1)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Work Type Mix</div>
    <div class="chart-desc">
        Breakdown of work arrangements across all listings.
        <b style="color:#e2e8f0">{top_work}</b> is the most common at
        <b style="color:#e2e8f0">{top_work_pct}%</b> of all roles.
    </div>
</div>
""", unsafe_allow_html=True)

df_pie = dataset.value_counts("remote_work")
PieChart(df_pie, labels="remote_work", values="count",
         title="Work Type Mix").show(st)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:11px;color:#1e2130;text-align:center;">'
    'AI Job Market · 2025–2026 · Project-OOP</p>',
    unsafe_allow_html=True
)