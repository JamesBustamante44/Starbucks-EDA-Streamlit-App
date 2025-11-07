import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Starbucks EDA", page_icon="☕", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ["Home", "Data Overview", "EDA"])

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_starbucks.csv")

df = load_data()

# Home Page
if section == "Home":
    st.title("☕ Starbucks Data EDA App")
    st.image("https://1000logos.net/wp-content/uploads/2017/08/Starbucks-Logo-768x432.png", width=300)
    st.write("""
    Welcome to the **Starbucks Drinks Exploratory Data Analysis (EDA) App**!  
    Browse through the app to discover insights on Starbucks beverages, their nutritional information, and more.
    """)
    st.balloons()

# Data Overview Page
elif section == "Data Overview":
    st.header("📋 Data Overview")
    st.write("Here is a preview of the Starbucks dataset used for analysis:")
    st.dataframe(df.head(10))
    
    st.subheader("Dataset Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Beverages", len(df))
    with col2:
        st.metric("Total Features", len(df.columns))
    with col3:
        st.metric("Categories", df['Beverage_category'].nunique())
    
    st.markdown("""
    **Dataset Columns:**
    - `Beverage_category`: Drink category (e.g., Coffee, Tea)
    - `Beverage`: Name of the beverage
    - `Beverage_prep`: Preparation style/size
    - `Calories`, `Total Fat (g)`, `Sugars (g)`, `Caffeine (mg)`, etc.: Nutritional values
    """)

# EDA Page
elif section == "EDA":
    st.header("🔍 Exploratory Data Analysis")
    
    # Histogram: Calories
    st.subheader("Calorie Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.histplot(df["Calories"], bins=30, ax=ax1, color="green", kde=True)
    ax1.set_xlabel("Calories")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)
    
    # Scatter Plot: Calories vs. Sugars
    st.subheader("Calories vs. Sugar Content")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x="Sugars (g)", y="Calories", data=df, ax=ax2, alpha=0.6)
    ax2.set_xlabel("Sugars (g)")
    ax2.set_ylabel("Calories")
    st.pyplot(fig2)
    
    # Box Plot: Caffeine Content by Category
    st.subheader("Caffeine Content by Beverage Category")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="Beverage_category", y="Caffeine (mg)", data=df, ax=ax3)
    plt.xticks(rotation=45, ha='right')
    ax3.set_xlabel("Beverage Category")
    ax3.set_ylabel("Caffeine (mg)")
    plt.tight_layout()
    st.pyplot(fig3)
    
    # Bar Chart: Average Calories per Category
    st.subheader("Average Calories by Beverage Category")
    avg_cals = df.groupby("Beverage_category")["Calories"].mean().sort_values(ascending=False)
    st.bar_chart(avg_cals)
    
    # Additional: Correlation Heatmap
    st.subheader("Correlation Heatmap")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    corr_matrix = df[numeric_cols].corr()
    fig4, ax4 = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax4)
    st.pyplot(fig4)
