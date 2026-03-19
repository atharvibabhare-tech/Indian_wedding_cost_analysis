import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Title
st.title("💍 Wedding Data Analysis Dashboard")

# Load data
df = pd.read_csv("wedding.csv")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

wedding_type = st.sidebar.selectbox("Select Wedding Type", df['Wedding_Type'].unique())
place = st.sidebar.selectbox("Select Place", df['Place'].unique())
decor_cat = st.sidebar.selectbox("Select Decor Category", df['Decor_Category'].unique())

# Filtered data
filtered_df = df[
    (df['Wedding_Type'] == wedding_type) &
    (df['Place'] == place) &
    (df['Decor_Category'] == decor_cat)
]

# Show data
st.subheader("📄 Filtered Data")
st.write(filtered_df)

# Bar Plot
st.subheader("📊 Average Cost by Wedding Type")
wt_cost = df.groupby('Wedding_Type')['Cost_of_Type'].mean()

fig, ax = plt.subplots()
wt_cost.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
plt.xticks(rotation=45)
plt.title("Average Cost by Wedding Type")
st.pyplot(fig)

# Pie Chart
st.subheader("🥧 Cost Distribution by Place")
place_cost = df.groupby('Place')['Cost_of_Type'].mean().nlargest(5)

fig2, ax2 = plt.subplots()
place_cost.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax2)
plt.ylabel('')
st.pyplot(fig2)

# Histogram
st.subheader("📊 Cost Distribution")
fig3, ax3 = plt.subplots()
sb.histplot(df['Cost_of_Type'], bins=10, kde=True, color='blue', ax=ax3)
st.pyplot(fig3)

# Footer
st.write("Created by Atharvi")
