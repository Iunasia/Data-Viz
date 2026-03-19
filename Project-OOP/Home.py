import streamlit as st

st.set_page_config(
    page_title="ASEAN Dashboard",
    layout="wide",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Epilogue:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Epilogue', sans-serif; }
.stApp { background: #080b12; }

section[data-testid="stSidebar"] {
    background: #070a10 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
section[data-testid="stSidebar"] * { color: #6b7280 !important; }
#MainMenu, footer, header { visibility: hidden; }

.hero-wrap {
    position: relative;
    padding: 64px 0 48px;
    overflow: hidden;
}
.hero-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, black 40%, transparent 100%);
}
.hero-glow {
    position: absolute; top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse, rgba(56,189,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 11px; font-weight: 500; letter-spacing: 0.2em;
    text-transform: uppercase; color: #38bdf8; margin-bottom: 16px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 800; line-height: 1.08;
    color: #f1f5f9; margin: 0 0 20px; letter-spacing: -1.5px;
}
.hero-title span { color: #38bdf8; }
.hero-sub {
    font-size: 16px; font-weight: 300; color: #64748b;
    line-height: 1.7; max-width: 520px;
}

.stat-strip {
    display: flex; gap: 0;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; overflow: hidden;
    margin: 40px 0 52px; background: #0d1117;
}
.stat-item {
    flex: 1; padding: 22px 28px;
    border-right: 1px solid rgba(255,255,255,0.06);
    transition: background 0.2s;
}
.stat-item:last-child { border-right: none; }
.stat-item:hover { background: rgba(56,189,248,0.04); }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px; font-weight: 700;
    color: #f1f5f9; line-height: 1; margin-bottom: 4px;
}
.stat-label { font-size: 11px; color: #475569; letter-spacing: 0.08em; text-transform: uppercase; }

.section-head { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.section-line { flex: 1; height: 1px; background: rgba(255,255,255,0.06); }
.section-label { font-size: 11px; font-weight: 500; color: #334155; letter-spacing: 0.14em; text-transform: uppercase; }

.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 52px; }
.page-card {
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 26px 24px;
    transition: all 0.22s ease; position: relative; overflow: hidden;
}
.page-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: var(--accent); opacity: 0; transition: opacity 0.22s;
}
.page-card:hover { border-color: rgba(255,255,255,0.14); transform: translateY(-2px); background: #0f1621; }
.page-card:hover::before { opacity: 1; }
.card-icon { font-size: 24px; margin-bottom: 14px; display: block; }
.card-title {
    font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700;
    color: #e2e8f0; margin-bottom: 6px; letter-spacing: -0.3px;
}
.card-desc { font-size: 12.5px; color: #475569; line-height: 1.6; margin-bottom: 16px; }
.card-meta { display: flex; align-items: center; gap: 8px; }
.card-tag {
    font-size: 10px; font-weight: 500; letter-spacing: 0.06em;
    padding: 3px 9px; border-radius: 20px;
    background: rgba(255,255,255,0.05); color: #64748b; text-transform: uppercase;
}
.card-rows { font-size: 10.5px; color: #334155; margin-left: auto; }

.feature-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 52px; }
.feature-box {
    background: #0d1117; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 22px 20px;
}
.feature-icon { font-size: 20px; margin-bottom: 10px; }
.feature-title { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; }
.feature-text { font-size: 12px; color: #475569; line-height: 1.65; }
.feature-text code { font-size: 11px; color: #38bdf8; background: rgba(56,189,248,0.08); padding: 1px 5px; border-radius: 4px; }

.footer {
    border-top: 1px solid rgba(255,255,255,0.05); padding: 28px 0 40px;
    display: flex; justify-content: space-between; align-items: center;
}
.footer-left { font-size: 12px; color: #1e293b; }
.footer-right { display: flex; gap: 6px; }
.footer-pill { font-size: 10px; color: #334155; border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 3px 10px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-grid"></div>
    <div class="hero-glow"></div>
    <div class="hero-eyebrow">Southeast Asia · Data Visualization</div>
    <div class="hero-title">ASEAN<br><span>Data Dashboard</span></div>
    <p class="hero-sub">
        Six datasets. Six interactive pages. Explore economic indicators,
        job markets, population trends, and tourism data across Southeast Asia —
        all in one place.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Stat strip ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
    <div class="stat-item">
        <div class="stat-num">6</div>
        <div class="stat-label">Datasets</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">1,610</div>
        <div class="stat-label">Total Records</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">10</div>
        <div class="stat-label">ASEAN Countries</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">2000–2026</div>
        <div class="stat-label">Year Coverage</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">8</div>
        <div class="stat-label">Chart Types</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pages section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-head">
    <div class="section-label">Available Pages</div>
    <div class="section-line"></div>
</div>

<div class="card-grid">
    <div class="page-card" style="--accent:#38bdf8;">
        <span class="card-icon">🤖</span>
        <div class="card-title">AI Job Market</div>
        <div class="card-desc">Salaries, demand ratings, and role distribution for AI &amp; ML positions in 2025–2026.</div>
        <div class="card-meta">
            <span class="card-tag">2025–2026</span>
            <span class="card-tag">Salary</span>
            <span class="card-rows">300 rows</span>
        </div>
    </div>
    <div class="page-card" style="--accent:#f59e0b;">
        <span class="card-icon">📈</span>
        <div class="card-title">CPI Inflation</div>
        <div class="card-desc">Consumer Price Index and inflation rate trends across all 10 ASEAN nations from 2000 to 2025.</div>
        <div class="card-meta">
            <span class="card-tag">2000–2025</span>
            <span class="card-tag">Economics</span>
            <span class="card-rows">260 rows</span>
        </div>
    </div>
    <div class="page-card" style="--accent:#10b981;">
        <span class="card-icon">💼</span>
        <div class="card-title">Data Science Salary</div>
        <div class="card-desc">Global compensation benchmarks for Data Scientists, ML Engineers, and Analysts.</div>
        <div class="card-meta">
            <span class="card-tag">2022–2025</span>
            <span class="card-tag">Salary</span>
            <span class="card-rows">250 rows</span>
        </div>
    </div>
    <div class="page-card" style="--accent:#a78bfa;">
        <span class="card-icon">🌏</span>
        <div class="card-title">GDP per Capita</div>
        <div class="card-desc">Economic growth trajectories and GDP per capita for ASEAN countries 2000–2026.</div>
        <div class="card-meta">
            <span class="card-tag">2000–2026</span>
            <span class="card-tag">Economics</span>
            <span class="card-rows">270 rows</span>
        </div>
    </div>
    <div class="page-card" style="--accent:#f472b6;">
        <span class="card-icon">👥</span>
        <div class="card-title">Population</div>
        <div class="card-desc">Demographic trends, urbanisation rates, and population growth across ASEAN 2000–2026.</div>
        <div class="card-meta">
            <span class="card-tag">2000–2026</span>
            <span class="card-tag">Demographics</span>
            <span class="card-rows">270 rows</span>
        </div>
    </div>
    <div class="page-card" style="--accent:#34d399;">
        <span class="card-icon">✈️</span>
        <div class="card-title">Tourism Visitors</div>
        <div class="card-desc">International arrivals and tourism revenue across Southeast Asia, including COVID-19 impact years.</div>
        <div class="card-meta">
            <span class="card-tag">2000–2025</span>
            <span class="card-tag">Tourism</span>
            <span class="card-rows">260 rows</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">ASEAN Data Dashboard · Project-OOP</div>
    <div class="footer-right">
        <span class="footer-pill">Streamlit</span>
        <span class="footer-pill">Plotly</span>
        <span class="footer-pill">Pandas</span>
        <span class="footer-pill">Python OOP</span>
    </div>
</div>
""", unsafe_allow_html=True)