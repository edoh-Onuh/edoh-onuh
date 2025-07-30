# Diabetes Prediction Analysis

This project uses a Jupyter Notebook to analyze the Pima Indians Diabetes Database. The primary goal is to build and evaluate several machine learning models to predict whether a patient has diabetes based on certain diagnostic measurements.

## Features

*   **Exploratory Data Analysis (EDA):** The notebook includes a comprehensive EDA section with visualizations to understand the data's characteristics and the relationships between different features.
*   **Data Preprocessing:** It demonstrates how to handle physiologically impossible zero values by replacing them with NaN and then imputing them using a robust pipeline.
*   **Model Training:** Three different classification models are trained:
    *   Logistic Regression
    *   Decision Tree
    *   Random Forest
*   **Model Evaluation:** The models are evaluated using various metrics, including:
    *   Classification Reports (Precision, Recall, F1-score)
    *   AUC-ROC Curves
    *   Precision-Recall Curves
*   **Pipeline Implementation:** The entire workflow, from preprocessing to model training, is encapsulated in a `scikit-learn` pipeline to ensure a robust and reproducible process.

## Getting Started

### Prerequisites

You need to have Python 3 and the libraries listed in `requirements.txt` installed.

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd <project-directory>
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Notebook

1.  Ensure you have the `diabetes_dataset.csv` file in the same directory. The data can be sourced from [Kaggle](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database).
2.  Launch Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
3.  Open the `diabtes_prediction.ipynb` file and run the cells.

## Project Structure

```
.
├── README.md
├── diabtes_prediction.ipynb
├── outputs
│   └── plots
│       ├── correlation_matrix.png
│       ├── histograms.png
│       ├── outcome_distribution.png
│       ├── precision_recall_curve.png
│       └── roc_curve.png
└── requirements.txt
```

## Results

The analysis concludes that the **Random Forest** model is the best-performing model for this dataset, achieving the highest accuracy and AUC score.
