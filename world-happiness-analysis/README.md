# World Happiness Analysis

A comprehensive analysis of global happiness data using advanced statistical methods, machine learning, and interactive visualizations.

## 🌟 Overview

This project provides an in-depth analysis of the World Happiness Report data, exploring relationships between happiness scores and various socio-economic factors across countries and time periods. The analysis includes advanced statistical modeling, time series analysis, and interactive visualizations.

## 🚀 Features

- **Advanced Data Cleaning**: Robust preprocessing with outlier detection and missing value handling
- **Statistical Analysis**: Correlation analysis, regression modeling, and normality tests
- **Machine Learning**: Random Forest and Linear Regression models for happiness prediction
- **Interactive Visualizations**: Plotly-based charts, maps, and dashboards
- **Time Series Analysis**: Trend analysis and country-wise happiness trajectories
- **Automated Reporting**: Comprehensive HTML and JSON reports
- **GitHub Ready**: All plots and results saved as files for easy sharing

## 📊 Generated Visualizations

All visualizations are saved as interactive HTML files in the `outputs/plots/` directory:

- **Correlation Heatmap**: Interactive correlation matrix with annotations
- **Happiness Distribution**: Statistical distribution analysis with normal curve overlay
- **Top Countries Chart**: Bar chart of highest-performing countries
- **World Happiness Map**: Interactive choropleth map showing global happiness
- **Scatter Matrix**: Multi-variable relationship analysis
- **Time Series Analysis**: Happiness trends over time with confidence intervals

## 🛠️ Technologies Used

- **Python 3.8+**
- **Data Analysis**: Pandas, NumPy, SciPy
- **Machine Learning**: Scikit-learn, Statsmodels
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Statistical Analysis**: Advanced statistical tests and modeling
- **Jupyter Notebooks**: Interactive analysis environment

## 📂 Project Structure

```
world-happiness-analysis/
├── world_happiness_analysis.ipynb    # Main analysis notebook
├── happiness.csv                     # Input data
├── happiness_cleaned.csv            # Cleaned data output
├── requirements.txt                  # Python dependencies
├── .gitignore                       # Git ignore file
├── README.md                        # This file
└── outputs/                         # Generated outputs
    ├── plots/                       # Interactive HTML visualizations
    │   ├── correlation_heatmap.html
    │   ├── happiness_distribution.html
    │   ├── top_countries.html
    │   ├── world_happiness_map.html
    │   ├── scatter_matrix.html
    │   └── happiness_time_series.html
    ├── data/                        # Analysis results
    │   ├── happiness_cleaned.csv
    │   ├── exploration_results.json
    │   ├── statistical_analysis.json
    │   ├── time_series_analysis.json
    │   └── comprehensive_report.json
    └── analysis_report.html          # Main HTML report
```

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd world-happiness-analysis
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

5. **Open and run** `world_happiness_analysis.ipynb`

## 📈 Key Insights

The analysis reveals several important findings:

- **Data Quality**: Comprehensive cleaning ensures robust analysis
- **Global Trends**: Time series analysis shows happiness trends over years
- **Country Rankings**: Identification of top and bottom performing countries
- **Predictive Modeling**: Machine learning models achieve good prediction accuracy
- **Factor Analysis**: Key variables driving happiness scores

## 🎯 Analysis Highlights

### Statistical Analysis
- Descriptive statistics for all variables
- Correlation analysis with happiness scores
- Regression modeling (Linear and Random Forest)
- Feature importance analysis
- Normality testing

### Visualizations
- Interactive correlation heatmaps
- Global happiness choropleth maps
- Time series trend analysis
- Country performance rankings
- Multi-variable scatter matrices

### Reporting
- Automated HTML report generation
- JSON data exports for further analysis
- Comprehensive documentation

## 🔄 Reproducibility

All analysis is fully reproducible:
- Fixed random seeds for consistent results
- Comprehensive documentation
- Version-controlled dependencies
- Clear step-by-step notebook structure

## 📊 Sample Outputs

The analysis generates various outputs including:
- Interactive HTML visualizations viewable in any browser
- Statistical summaries and model results
- Cleaned datasets for further analysis
- Comprehensive reports with key findings

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs or issues
- Suggesting new features or analyses
- Improving documentation
- Adding new visualization types

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- World Happiness Report data providers
- Python data science community
- Plotly for interactive visualizations
- Contributors and maintainers

---

**Note**: Ensure you have the `happiness.csv` file in the project root directory before running the analysis.

For questions or support, please open an issue in the repository.
