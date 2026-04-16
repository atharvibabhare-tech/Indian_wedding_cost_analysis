import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# =======================
# ⚙️ PAGE CONFIG
# =======================
st.set_page_config(
    page_title="Indian Wedding Analytics 🫶🏻",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# 🎨 LUXURY ROSE GOLD THEME
# =======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500;600&display=swap');

/* ── ROOT PALETTE ── */
:root {
    --ivory:       #fdf8f2;
    --cream:       #f5ede0;
    --rose-light:  #f9e4d4;
    --rose:        #c9826b;
    --rose-deep:   #a5614e;
    --gold:        #c9a84c;
    --gold-light:  #e8d5a3;
    --burgundy:    #6b2737;
    --ink:         #1c1410;
    --muted:       #7a6a62;
    --white:       #ffffff;
}

/* ── GLOBAL ── */
* { box-sizing: border-box; }

html, body, .stApp {
    background: var(--ivory) !important;
    font-family: 'Jost', sans-serif;
    color: var(--ink);
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #1c1410 0%, #3b1f17 60%, #6b2737 100%) !important;
    border-right: 1px solid rgba(201,168,76,0.3);
}
section[data-testid="stSidebar"] * {
    color: #f5ede0 !important;
    font-family: 'Jost', sans-serif;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: var(--gold-light) !important;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    border-radius: 8px !important;
    color: #f5ede0 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: var(--gold-light) !important; }

/* ── MAIN CONTENT AREA ── */
.main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1280px;
}

/* ── HERO HEADER ── */
.hero-wrapper::after {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.35);  /* dark overlay */
    z-index: 0;
}
.hero-wrapper * {
    position: relative;
    z-index: 1;
}
.hero-ornament {
    position: absolute;
    top: -20px; right: -20px;
    font-size: 11rem;
    opacity: 0.06;
    line-height: 1;
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'Jost', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 700;
    color: #fef3c7;  /* soft gold */
    text-shadow: 
        0 3px 15px rgba(0,0,0,0.8),
        0 0 10px rgba(201,168,76,0.6);
}
.hero-title em {
    font-style: italic;
    color: #ffd700;  /* bright gold */
    text-shadow: 
        0 0 12px rgba(255,215,0,0.8),
        0 0 25px rgba(255,215,0,0.5);
}
.hero-sub {
    font-size: 0.88rem;
    color: rgba(255,245,230,0.82);
    letter-spacing: 0.04em;
    font-weight: 300;
}
.hero-divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), transparent);
    margin: 1.2rem 0;
    border: none;
}

/* ── HERO BUTTONS ── */
.hero-btn-row {
    display: flex;
    gap: 0.9rem;
    margin-top: 1.6rem;
    flex-wrap: wrap;
}
.hero-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.6rem 1.4rem;
    border-radius: 50px;
    font-family: 'Jost', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.18s, box-shadow 0.18s, background 0.18s;
}
.hero-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
}
.hero-btn-primary {
    background: linear-gradient(135deg, #c9a84c, #e8c96a);
    color: #1c1410;
    border: none;
    box-shadow: 0 3px 14px rgba(201,168,76,0.45);
}
.hero-btn-outline {
    background: rgba(255,255,255,0.08);
    color: #fdf8f2;
    border: 1.5px solid rgba(255,255,255,0.35);
    backdrop-filter: blur(4px);
}
.hero-btn-outline:hover { background: rgba(255,255,255,0.16); }
.hero-btn-rose {
    background: linear-gradient(135deg, #c9826b, #e09a85);
    color: #ffffff;
    border: none;
    box-shadow: 0 3px 14px rgba(201,130,107,0.4);
}

/* ── KPI CARDS ── */
.kpi-row { display: flex; gap: 1.2rem; margin-bottom: 2rem; }
.kpi-card {
    flex: 1;
    background: var(--white);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    border: 1px solid rgba(201,168,76,0.2);
    box-shadow: 0 4px 24px var(--shadow);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(100,50,30,0.18);
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--rose));
    border-radius: 0 0 16px 16px;
}
.kpi-icon {
    font-size: 1.6rem;
    margin-bottom: 0.6rem;
    display: block;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 600;
    color: var(--ink);
    line-height: 1;
}
.kpi-value span { font-size: 1.1rem; color: var(--muted); font-weight: 300; }

/* ── SECTION HEADERS ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 2rem 0 1rem;
}
.section-head-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(201,168,76,0.5), transparent);
}
.section-head-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 400;
    color: var(--ink);
    white-space: nowrap;
}
.section-head-badge {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--rose-deep);
    background: var(--rose-light);
    padding: 3px 10px;
    border-radius: 20px;
}

/* ── CHART CARDS ── */
.chart-card {
    background: var(--white);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(201,168,76,0.15);
    box-shadow: 0 2px 20px var(--shadow);
    margin-bottom: 1.2rem;
}

/* ── DATA TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(201,168,76,0.2) !important;
}
[data-testid="stDataFrame"] table { font-family: 'Jost', sans-serif !important; }
[data-testid="stDataFrame"] th {
    background: #1c1410 !important;
    color: var(--gold-light) !important;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
[data-testid="stDataFrame"] tr:nth-child(even) td {
    background: var(--cream) !important;
}

/* ── SIDEBAR TITLE ── */
.sidebar-brand {
    text-align: center;
    padding: 1.6rem 1rem 1.2rem;
    border-bottom: 1px solid rgba(201,168,76,0.25);
    margin-bottom: 1.4rem;
}
.sidebar-brand-icon { font-size: 2.2rem; }
.sidebar-brand-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 400;
    color: #fdf8f2 !important;
    margin: 0.3rem 0 0.1rem;
    letter-spacing: 0.04em;
}
.sidebar-brand-sub {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(201,168,76,0.7) !important;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    border-top: 1px solid rgba(201,168,76,0.2);
}
.footer strong { color: var(--rose-deep); font-weight: 500; }

</style>
""", unsafe_allow_html=True)

# =======================
# 📂 LOAD DATA
# =======================
@st.cache_data
def load_data():
    return pd.read_csv("Indian_Weddings_.csv")

df = load_data()

# =======================
# 🔧 CLEANING
# =======================
df.columns = (
    df.columns
    .str.strip()
    .str.replace('/', '_')
    .str.replace(' ', '_')
)

for col in df.select_dtypes(include='object').columns:
    df[col] = (
        df[col]
        .str.replace(r'[/]', '', regex=True)
        .str.replace(r'\\xc2', '', regex=True)
        .str.strip()
        .str.title()
    )

df['Wedding_Type'] = df['Wedding_Type'].replace({
    'Destination Weddings': 'Destination Wedding',
    'Temple Weddings': 'Temple Wedding',
    'Farmhouse Weddings': 'Farmhouse Wedding'
})

# =======================
# 🎨 MATPLOTLIB THEME
# =======================
PALETTE_WARM = ['#c9826b', '#c9a84c', '#6b2737', '#d4a574', '#8b4c5a', '#e8c99a', '#a5614e', '#4a1c28']
PALETTE_GOLD = ['#c9a84c', '#e8d5a3', '#a5864a', '#f0e4b8', '#7a6430', '#d4ba7a']

plt.rcParams.update({
    'font.family': 'serif',
    'axes.facecolor': '#ffffff',
    'figure.facecolor': '#ffffff',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.bottom': False,
    'axes.grid': True,
    'grid.color': '#f0e8e0',
    'grid.linewidth': 0.7,
    'axes.labelcolor': '#7a6a62',
    'xtick.color': '#7a6a62',
    'ytick.color': '#7a6a62',
    'font.size': 10,
})

# =======================
# 🔍 SIDEBAR
# =======================
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-icon">💍</div>
    <div class="sidebar-brand-title">Wedding Analytics</div>
    <div class="sidebar-brand-sub">India · Insights</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("#### Filter Records")

wedding_type = st.sidebar.selectbox(
    "Wedding Type",
    ["All"] + sorted(df['Wedding_Type'].dropna().unique())
)
place = st.sidebar.selectbox(
    "Place",
    ["All"] + sorted(df['Place'].dropna().unique())
)
decor_cat = st.sidebar.selectbox(
    "Decor Category",
    ["All"] + sorted(df['Decor_Category'].dropna().unique())
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.72rem;color:rgba(245,237,224,0.45);text-align:center;letter-spacing:0.08em'>"
    "Data reflects Indian wedding trends<br>across multiple cities & types"
    "</div>",
    unsafe_allow_html=True
)

# =======================
# 📊 FILTER DATA
# =======================
filtered_df = df.copy()
if wedding_type != "All":
    filtered_df = filtered_df[filtered_df['Wedding_Type'] == wedding_type]
if place != "All":
    filtered_df = filtered_df[filtered_df['Place'] == place]
if decor_cat != "All":
    filtered_df = filtered_df[filtered_df['Decor_Category'] == decor_cat]

# =======================
# 🏠 HERO SECTION
# =======================
# Button state for scroll targeting
if 'scroll_to' not in st.session_state:
    st.session_state['scroll_to'] = None

st.markdown("""
<div class="hero-wrapper">
    <div class="hero-ornament">💍</div>
    <div class="hero-eyebrow">✦ Indian Wedding Trends</div>
    <h1 class="hero-title">Where <em>Data</em> Meets<br>Sacred Celebrations</h1>
    <hr class="hero-divider">
    <p class="hero-sub">Explore costs, decor patterns, and venue insights across India's most celebrated wedding styles</p>
    <div class="hero-btn-row">
        <span class="hero-btn hero-btn-primary">📊 View Charts</span>
        <span class="hero-btn hero-btn-rose">📋 Browse Data</span>
        <span class="hero-btn hero-btn-outline">💡 Cost Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Real Streamlit action buttons below hero
col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 4])
with col_b1:
    if st.button("📊 View Charts", key="btn_charts", use_container_width=True):
        st.session_state['scroll_to'] = 'charts'
with col_b2:
    if st.button("📋 Browse Data", key="btn_data", use_container_width=True):
        st.session_state['scroll_to'] = 'data'
with col_b3:
    if st.button("💡 Cost Insights", key="btn_insights", use_container_width=True):
        st.session_state['scroll_to'] = 'insights'

st.markdown("""
<style>
div[data-testid="column"] .stButton > button {
    background: linear-gradient(135deg, #c9a84c, #e8c96a);
    color: #1c1410 !important;
    border: none;
    border-radius: 50px;
    font-family: 'Jost', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    padding: 0.5rem 1rem;
    box-shadow: 0 3px 12px rgba(201,168,76,0.35);
    transition: transform 0.15s, box-shadow 0.15s;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #c9826b, #e09a85) !important;
    color: #fff !important;
    box-shadow: 0 3px 12px rgba(201,130,107,0.35);
}
div[data-testid="column"]:nth-child(3) .stButton > button {
    background: rgba(28,20,16,0.92) !important;
    color: #fdf8f2 !important;
    border: 1.5px solid rgba(201,168,76,0.5) !important;
}
div[data-testid="column"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.22);
}
</style>
""", unsafe_allow_html=True)

# =======================
# 📊 KPI CARDS
# =======================
avg_cost = filtered_df['Cost_of_Type'].mean() if len(filtered_df) > 0 else 0
max_cost = filtered_df['Cost_of_Type'].max() if len(filtered_df) > 0 else 0
num_types = filtered_df['Wedding_Type'].nunique()
num_places = filtered_df['Place'].nunique()

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <span class="kpi-icon">💒</span>
        <div class="kpi-label">Total Weddings</div>
        <div class="kpi-value">{len(filtered_df)}<span> records</span></div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">📍</span>
        <div class="kpi-label">Cities Covered</div>
        <div class="kpi-value">{num_places}<span> places</span></div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">💰</span>
        <div class="kpi-label">Average Cost</div>
        <div class="kpi-value">₹{round(avg_cost/100000, 2)}<span> L</span></div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">🎊</span>
        <div class="kpi-label">Wedding Styles</div>
        <div class="kpi-value">{num_types}<span> types</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# =======================
# 📄 DATA TABLE
# =======================
st.markdown('<div id="section-data"></div>', unsafe_allow_html=True)
if st.session_state.get('scroll_to') == 'data':
    st.markdown('<script>document.getElementById("section-data").scrollIntoView({behavior:"smooth"});</script>', unsafe_allow_html=True)

st.markdown("""
<div class="section-head">
    <span class="section-head-title">📋 Filtered Dataset</span>
    <div class="section-head-line"></div>
    <span class="section-head-badge">Live View</span>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df.style
        .background_gradient(subset=['Cost_of_Type'], cmap='YlOrBr', low=0.2)
        .format({'Cost_of_Type': '₹{:,.0f}'}),
    use_container_width=True,
    height=280
)

# =======================
# 📊 CHARTS — ROW 1
# =======================
st.markdown('<div id="section-charts"></div>', unsafe_allow_html=True)
if st.session_state.get('scroll_to') == 'charts':
    st.markdown('<script>document.getElementById("section-charts").scrollIntoView({behavior:"smooth"});</script>', unsafe_allow_html=True)

st.markdown("""
<div class="section-head">
    <span class="section-head-title">📊 Cost Analysis</span>
    <div class="section-head-line"></div>
    <span class="section-head-badge">By Category</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

# ── BAR CHART ──
with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Average Cost by Wedding Type**")

    wt_cost = (
        filtered_df.groupby('Wedding_Type')['Cost_of_Type']
        .mean()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(6.5, 4))
    bars = ax.barh(wt_cost.index, wt_cost.values, color=PALETTE_WARM[:len(wt_cost)],
                   height=0.6, edgecolor='none')

    for bar, val in zip(bars, wt_cost.values):
        ax.text(val + wt_cost.values.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f'₹{val:,.0f}', va='center', fontsize=8, color='#7a6a62')

    ax.set_xlabel('Average Cost (₹)', labelpad=8, fontsize=9)
    ax.set_title('Wedding Type vs. Cost', fontsize=11, fontweight='bold',
                 color='#1c1410', pad=12, loc='left')
    ax.tick_params(axis='y', length=0, labelsize=9)
    ax.tick_params(axis='x', length=0, labelsize=8)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1e5:.1f}L'))
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── PIE CHART ──
with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Top 5 Cities by Wedding Cost**")

    place_cost = (
        filtered_df.groupby('Place')['Cost_of_Type']
        .mean()
        .nlargest(5)
    )

    fig2, ax2 = plt.subplots(figsize=(6.5, 4))
    wedges, texts, autotexts = ax2.pie(
        place_cost.values,
        labels=place_cost.index,
        autopct='%1.1f%%',
        colors=PALETTE_GOLD[:len(place_cost)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 2.5},
        startangle=120,
        pctdistance=0.78
    )
    for t in texts: t.set_fontsize(9)
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color('#1c1410')
        at.set_fontweight('bold')

    ax2.set_title('Cost Distribution by City', fontsize=11, fontweight='bold',
                  color='#1c1410', pad=12, loc='left')
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =======================
# 📊 CHARTS — ROW 2
# =======================
col3, col4 = st.columns(2, gap="medium")

# ── HISTOGRAM ──
with col3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Cost Distribution**")

    fig3, ax3 = plt.subplots(figsize=(6.5, 4))
    sns.histplot(
        filtered_df['Cost_of_Type'],
        bins=12,
        kde=True,
        color='#c9826b',
        edgecolor='white',
        linewidth=0.6,
        ax=ax3,
        alpha=0.85
    )
    ax3.lines[0].set_color('#6b2737')
    ax3.lines[0].set_linewidth(2)
    ax3.set_xlabel('Cost (₹)', labelpad=8, fontsize=9)
    ax3.set_ylabel('Frequency', labelpad=8, fontsize=9)
    ax3.set_title('How Costs Spread Across Weddings', fontsize=11, fontweight='bold',
                  color='#1c1410', pad=12, loc='left')
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1e5:.1f}L'))
    ax3.tick_params(axis='both', length=0, labelsize=8)
    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── DECOR BOX / COUNT ──
with col4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Weddings by Decor Category**")

    if 'Decor_Category' in filtered_df.columns:
        decor_counts = filtered_df['Decor_Category'].value_counts().head(8)

        fig4, ax4 = plt.subplots(figsize=(6.5, 4))
        colors_d = PALETTE_WARM[:len(decor_counts)]
        bars4 = ax4.bar(
            range(len(decor_counts)),
            decor_counts.values,
            color=colors_d,
            edgecolor='none',
            width=0.6
        )
        ax4.set_xticks(range(len(decor_counts)))
        ax4.set_xticklabels(decor_counts.index, rotation=35, ha='right', fontsize=8)
        ax4.set_ylabel('Count', labelpad=8, fontsize=9)
        ax4.set_title('Decor Preference Overview', fontsize=11, fontweight='bold',
                      color='#1c1410', pad=12, loc='left')
        ax4.tick_params(axis='both', length=0, labelsize=8)

        for bar, val in zip(bars4, decor_counts.values):
            ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                     str(val), ha='center', fontsize=8, color='#7a6a62', fontweight='500')

        fig4.tight_layout()
        st.pyplot(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =======================
# 📊 FULL-WIDTH — BOXPLOT
# =======================
st.markdown('<div id="section-insights"></div>', unsafe_allow_html=True)
if st.session_state.get('scroll_to') == 'insights':
    st.markdown('<script>document.getElementById("section-insights").scrollIntoView({behavior:"smooth"});</script>', unsafe_allow_html=True)

st.markdown("""
<div class="section-head">
    <span class="section-head-title">📦 Cost Spread</span>
    <div class="section-head-line"></div>
    <span class="section-head-badge">By Wedding Type</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
fig5, ax5 = plt.subplots(figsize=(12, 4))

wt_order = filtered_df.groupby('Wedding_Type')['Cost_of_Type'].median().sort_values(ascending=False).index.tolist()

sns.boxplot(
    data=filtered_df,
    x='Wedding_Type',
    y='Cost_of_Type',
    order=wt_order,
    palette=PALETTE_WARM,
    width=0.45,
    linewidth=1.2,
    flierprops=dict(marker='o', markerfacecolor='#c9826b', markersize=4, alpha=0.5),
    ax=ax5
)
ax5.set_xlabel('Wedding Type', labelpad=8, fontsize=9)
ax5.set_ylabel('Cost (₹)', labelpad=8, fontsize=9)
ax5.set_title('Cost Range per Wedding Style — Median, Spread & Outliers', fontsize=11,
              fontweight='bold', color='#1c1410', pad=14, loc='left')
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1e5:.1f}L'))
ax5.tick_params(axis='both', length=0, labelsize=8)
plt.xticks(rotation=20, ha='right')
fig5.tight_layout()
st.pyplot(fig5, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =======================
# ❤️ FOOTER
# =======================
st.markdown("""
<div class="footer">
    ✦ &nbsp; Crafted with care by <strong>Atharvi</strong> &nbsp; · &nbsp; Indian Wedding Analytics Dashboard &nbsp; · &nbsp; Data-Driven Celebrations &nbsp; ✦
</div>
""", unsafe_allow_html=True)
