import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =======================
# ⚙️ PAGE CONFIG
# =======================
st.set_page_config(page_title="Wedding Dashboard", layout="wide")

# =======================
# 🎯 TITLE
# =======================
st.title("💍 Wedding Data Analysis Dashboard")
st.markdown("Analyze wedding trends, costs, and preferences across India")

# =======================
# 📂 LOAD DATA
# =======================
@st.cache_data
def load_data():
    df = pd.read_csv("Indian_Weddings_.csv")
    return df

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
# 🔍 SIDEBAR
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

col1.metric("💒 Total Weddings", len(filtered_df))
col2.metric("📍 Unique Places", filtered_df['Place'].nunique())
col3.metric("💰 Avg Cost", round(filtered_df['Cost_of_Type'].mean(), 2))

st.markdown("---")

# =======================
# 📄 DATA TABLE
# =======================
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

# =======================
# 📊 CHARTS (SIDE BY SIDE)
# =======================
col1, col2 = st.columns(2)

# BAR CHART
with col1:
    st.subheader("📊 Avg Cost by Wedding Type")

    wt_cost = (
        filtered_df.groupby('Wedding_Type')['Cost_of_Type']
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()
    wt_cost.plot(
        kind='bar',
        color='#2e7d32',
        edgecolor='black',
        ax=ax
    )

    plt.xticks(rotation=45)
    plt.title("Average Cost by Wedding Type", fontweight='bold')
    st.pyplot(fig)

# PIE CHART
with col2:
    st.subheader("🥧 Top 5 Cost by Place")

    place_cost = (
        filtered_df.groupby('Place')['Cost_of_Type']
        .mean()
        .nlargest(5)
    )

    fig2, ax2 = plt.subplots()
    place_cost.plot(
        kind='pie',
        autopct='%1.1f%%',
        colormap='Greens',
        wedgeprops={'edgecolor':'white'}
    )

    plt.ylabel('')
    plt.title("Top 5 Places by Cost", fontweight='bold')
    st.pyplot(fig2)

# =======================
# 📊 HISTOGRAM
# =======================
st.subheader("📊 Cost Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(
    filtered_df['Cost_of_Type'],
    bins=10,
    kde=True,
    color='#43a047'
)

plt.title("Cost Distribution", fontweight='bold')
st.pyplot(fig3)

# =======================
# ❤️ FOOTER
# =======================
st.markdown("---")
st.markdown("👩‍💻 Created by **Atharvi** 💙")
