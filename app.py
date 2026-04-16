import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Title
st.title("💍 Wedding Data Analysis Dashboard")

# Load data
df = pd.read_csv("Indian_Weddings_.csv")

# =======================
# 🔧 CLEANING
# =======================

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace('/', '_')
    .str.replace(' ', '_')
)

# Clean all text columns
for col in df.select_dtypes(include='object').columns:
    df[col] = (
        df[col]
        .str.replace(r'[/]', '', regex=True)      # remove ///
        .str.replace(r'\\xc2', '', regex=True)    # remove xc2
        .str.strip()                              # remove spaces
        .str.title()                              # proper format
    )

# Fix specific values
df['Wedding_Type'] = df['Wedding_Type'].replace({
    'Destination Weddings': 'Destination Wedding',
    'Temple Weddings': 'Temple Wedding',
    'Farmhouse Weddings': 'Farmhouse Wedding'
})

# =======================
# 🔍 SIDEBAR FILTERS
# =======================

st.sidebar.header("🔍 Filter Data")

wedding_type = st.sidebar.selectbox(
    "Select Wedding Type",
    ["All"] + sorted(df['Wedding_Type'].dropna().unique())
)

place = st.sidebar.selectbox(
    "Select Place",
    ["All"] + sorted(df['Place'].dropna().unique())
)

decor_cat = st.sidebar.selectbox(
    "Select Decor Category",
    ["All"] + sorted(df['Decor_Category'].dropna().unique())
)

# =======================
# 📊 FILTER LOGIC
# =======================

filtered_df = df.copy()

if wedding_type != "All":
    filtered_df = filtered_df[filtered_df['Wedding_Type'] == wedding_type]

if place != "All":
    filtered_df = filtered_df[filtered_df['Place'] == place]

if decor_cat != "All":
    filtered_df = filtered_df[filtered_df['Decor_Category'] == decor_cat]

# =======================
# 📄 SHOW DATA
# =======================

st.subheader("📄 Filtered Data")
st.write(filtered_df)

# =======================
# 📊 BAR PLOT
# =======================

st.subheader("📊 Average Cost by Wedding Type")

wt_cost = df.groupby('Wedding_Type')['Cost_of_Type'].mean().sort_values(ascending=False)

fig, ax = plt.subplots()
wt_cost.plot(kind='bar', ax=ax)
plt.xticks(rotation=45)
plt.title("Average Cost by Wedding Type")
st.pyplot(fig)

# =======================
# 🥧 PIE CHART
# =======================

st.subheader("🥧 Top 5 Cost Distribution by Place")

place_cost = df.groupby('Place')['Cost_of_Type'].mean().nlargest(5)

fig2, ax2 = plt.subplots()
place_cost.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
plt.ylabel('')
st.pyplot(fig2)

# =======================
# 📊 HISTOGRAM
# =======================

st.subheader("📊 Cost Distribution")

fig3, ax3 = plt.subplots()
sb.histplot(df['Cost_of_Type'], bins=10, kde=True, ax=ax3)
st.pyplot(fig3)

# =======================
# ❤️ FOOTER
# =======================

st.write("Created by Atharvi 💙")
