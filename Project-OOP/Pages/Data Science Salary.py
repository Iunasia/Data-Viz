import streamlit as st
from models.dataset import Dataset
from Visualization.bar_chart import BarChart
from Visualization.histogram import HistogramChart
from Visualization.pie_chart import PieChart

st.set_page_config(page_title="DS Salaries", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; }
section[data-testid="stSidebar"] { background: #090c11 !important; }

.hero { padding: 40px 0 32px; border-bottom: 1px solid #1e2130; margin-bottom: 32px; }
.hero-tag { font-size: 11px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #10b981; margin-bottom: 12px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #f1f5f9; letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px; }
.hero-desc { font-size: 14px; font-weight: 300; color: #64748b; line-height: 1.7; max-width: 560px; }

.metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 36px; }
.metric-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 18px 20px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; color: #f1f5f9; line-height: 1; margin-bottom: 4px; }
.metric-label { font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-accent { color: #10b981; }

.chart-header { margin: 28px 0 6px; }
.chart-title { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.chart-desc { font-size: 12px; color: #475569; line-height: 1.5; }
.divider { height: 1px; background: #1e2130; margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── Load ──────────────────────────────────────────────────────────────────────
dataset = Dataset("Datasets/ds_salaries.csv")
dataset.load()
dataset.clean()
df = dataset.df

LEVEL_MAP = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}
df["level_label"] = df["experience_level"].map(LEVEL_MAP)

# ── Stats ─────────────────────────────────────────────────────────────────────
total        = len(df)
avg_sal      = int(df["salary_in_usd"].mean())
max_sal      = int(df["salary_in_usd"].max())
top_job      = df.groupby("job_title")["salary_in_usd"].mean().idxmax()
remote_pct   = round((df["remote_ratio"] == 100).mean() * 100, 1)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Salary · 2020 – 2022</div>
    <div class="hero-title">Data Science Salaries</div>
    <div class="hero-desc">
        Compensation data for <b style="color:#e2e8f0">{total:,} DS & ML roles</b>
        across {df['company_location'].nunique()} countries and
        {df['job_title'].nunique()} job titles.
        <b style="color:#e2e8f0">{top_job}</b> commands
        the highest average salary in the dataset.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{total:,}</div>
        <div class="metric-label">Total records</div>
    </div>
    <div class="metric-card">
        <div class="metric-value"><span class="metric-accent">${avg_sal//1000}k</span></div>
        <div class="metric-label">Avg salary</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">${max_sal//1000}k</div>
        <div class="metric-label">Max salary</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{remote_pct}%</div>
        <div class="metric-label">Fully remote</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{df['job_title'].nunique()}</div>
        <div class="metric-label">Job titles</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 1 ────────────────────────────────────────────────────────
df_bar = dataset.group_by("job_title", "salary_in_usd")
df_bar = df_bar.sort_values("salary_in_usd", ascending=False).head(10)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Avg Salary by Job Title</div>
    <div class="chart-desc">
        Top 10 roles ranked by average annual salary in USD.
        <b style="color:#e2e8f0">{top_job}</b> leads
        with the highest average compensation across all records.
    </div>
</div>
""", unsafe_allow_html=True)

BarChart(df_bar, x="job_title", y="salary_in_usd",
         title="Avg Salary by Job Title", horizontal=True).show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 2 ──────────────────────────────────────────────────
st.markdown("""
<div class="chart-header">
    <div class="chart-title">Salary Distribution by Experience Level</div>
    <div class="chart-desc">
        Overlapping distributions for Entry, Mid, Senior, and Executive levels.
        Higher experience levels shift the distribution rightward toward
        higher salary bands.
    </div>
</div>
""", unsafe_allow_html=True)

HistogramChart(df, column="salary_in_usd", bins=25,
               group="level_label",
               title="Salary Distribution by Experience Level").show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 3 ────────────────────────────────────────────────────────
size_map = {"L": "Large", "M": "Medium", "S": "Small"}
df["company_size_label"] = df["company_size"].map(size_map)
df_pie = df["company_size_label"].value_counts().reset_index()
df_pie.columns = ["company_size_label", "count"]
top_size = df_pie.iloc[0]["company_size_label"]
top_size_pct = round(df_pie.iloc[0]["count"] / total * 100, 1)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Company Size Mix</div>
    <div class="chart-desc">
        Breakdown of records by company size.
        <b style="color:#e2e8f0">{top_size}</b> companies
        account for <b style="color:#e2e8f0">{top_size_pct}%</b>
        of all DS job listings in this dataset.
    </div>
</div>
""", unsafe_allow_html=True)

PieChart(df_pie, labels="company_size_label", values="count",
         title="Company Size Mix").show(st)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:11px;color:#1e2130;text-align:center;">'
    'Data Science Salaries · 2020–2022 · Project-OOP</p>',
    unsafe_allow_html=True
)