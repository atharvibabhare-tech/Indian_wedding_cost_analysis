import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =======================

# ⚙️ PAGE CONFIG

# =======================

st.set_page_config(page_title="Wedding Dashboard", layout="wide")

# =======================

# 🎨 DARK BLUE THEME

# =======================

st.markdown(""" <style>
.stApp {
background: linear-gradient(to right, #0f172a, #1e3a8a);
color: white;
}
h1, h2, h3 {
color: white;
} </style>
""", unsafe_allow_html=True)

# =======================

# 🎯 TITLE

# =======================

st.title("💍 Wedding Data Analysis Dashboard")
st.markdown("Elegant insights into wedding trends and costs")

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
.str.replace('/', '*')
.str.replace(' ', '*')
)

for col in df.select_dtypes(include='object').columns:
df[col] = (
df[col]
.str.replace(r'[/]', '', regex=True)
.str.replace(r'\xc2', '', regex=True)
.str.strip()
.str.title()
)

df['Wedding_Type'] = df['Wedding_Type'].replace({
'Destination Weddings': 'Destination Wedding',
'Temple Weddings': 'Temple Wedding',
'Farmhouse Weddings': 'Farmhouse Wedding'
})

# =======================

# 🔍 SIDEBAR FILTERS

# =======================

st.sidebar.title("🔍 Filters")

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

# 📊 KPI CARDS

# =======================

col1, col2, col3 = st.columns(3)

col1.markdown(f"""

<div style="background-color:#1e293b;padding:15px;border-radius:10px;text-align:center">
<h4>💒 Total Weddings</h4>
<h2>{len(filtered_df)}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""

<div style="background-color:#1e293b;padding:15px;border-radius:10px;text-align:center">
<h4>📍 Places</h4>
<h2>{filtered_df['Place'].nunique()}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""

<div style="background-color:#1e293b;padding:15px;border-radius:10px;text-align:center">
<h4>💰 Avg Cost</h4>
<h2>{round(filtered_df['Cost_of_Type'].mean(),2)}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =======================

# 📄 DATA TABLE

# =======================

st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

# =======================

# 📊 CHARTS

# =======================

col1, col2 = st.columns(2)

# BAR CHART

with col1:
st.subheader("📊 Avg Cost by Wedding Type")

```
wt_cost = (
    filtered_df.groupby('Wedding_Type')['Cost_of_Type']
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots()
wt_cost.plot(
    kind='bar',
    color='#1d4ed8',
    edgecolor='white',
    ax=ax
)

plt.xticks(rotation=45)
plt.title("Average Cost by Wedding Type", fontweight='bold')
st.pyplot(fig)
```

# PIE CHART

with col2:
st.subheader("🥧 Top 5 Cost by Place")

```
place_cost = (
    filtered_df.groupby('Place')['Cost_of_Type']
    .mean()
    .nlargest(5)
)

fig2, ax2 = plt.subplots()
place_cost.plot(
    kind='pie',
    autopct='%1.1f%%',
    colormap='Blues',
    wedgeprops={'edgecolor':'white'}
)

plt.ylabel('')
plt.title("Top 5 Places by Cost", fontweight='bold')
st.pyplot(fig2)
```

# =======================

# 📊 HISTOGRAM

# =======================

st.subheader("📊 Cost Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(
filtered_df['Cost_of_Type'],
bins=10,
kde=True,
color='#3b82f6'
)

plt.title("Cost Distribution", fontweight='bold')
st.pyplot(fig3)

# =======================

# ❤️ FOOTER

# =======================

st.markdown("---")
st.markdown("👩‍💻 Created by **Atharvi** 💙")
