# ☕ Starbucks-EDA-Streamlit-App

Exploratory Data Analysis of Starbucks beverages with interactive Streamlit dashboard

## 📋 Project Overview

This interactive web application provides comprehensive exploratory data analysis (EDA) of Starbucks beverages, including detailed nutritional information and visualizations. The app is built using Streamlit and offers an intuitive interface to explore various aspects of Starbucks drinks.

## ✨ Features

- **Home Page**: Welcome interface with project introduction
- **Data Overview**: Quick statistics and preview of the dataset
- **EDA Dashboard**: Interactive visualizations including:
  - Calorie distribution histogram
  - Calories vs. Sugar scatter plot
  - Caffeine content by beverage category
  - Average calories comparison
  - Correlation heatmap of nutritional values

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JamesBustamante44/Starbucks-EDA-Streamlit-App.git
cd Starbucks-EDA-Streamlit-App
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Add your data file:
   - Place `cleaned_starbucks.csv` in the root directory
   - The CSV should contain columns for beverage information and nutritional data

### Running the App

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 📊 Dataset

The app uses a cleaned Starbucks beverage dataset containing:
- Beverage category and name
- Preparation details
- Nutritional information (calories, fat, carbs, sugar, protein, etc.)
- Caffeine content
- Vitamin and mineral percentages

## 🛠️ Built With

- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **Matplotlib** - Data visualization
- **Seaborn** - Statistical graphics
- **NumPy** - Numerical computing

## 📂 Project Structure

```
Starbucks-EDA-Streamlit-App/
├── app.py                  # Main Streamlit application
├── cleaned_starbucks.csv   # Dataset (add this file)
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore file
```

## 📝 To-Do

- [ ] Upload `cleaned_starbucks.csv` data file
- [ ] Add more interactive filters
- [ ] Include downloadable reports
- [ ] Deploy to Streamlit Cloud

## 👤 Author

**James Bustamante**
- GitHub: [@JamesBustamante44](https://github.com/JamesBustamante44)

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Starbucks dataset for educational analysis
- Streamlit community for excellent documentation
