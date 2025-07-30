# Text Classification Project

This project performs text classification on a given dataset. It includes data cleaning, preprocessing, feature engineering, model building, and evaluation. The code is designed to be robust and includes hyperparameter tuning to find the best models.

## Features

*   **Data Cleaning and Preprocessing:** The script cleans the text data by removing non-alphabetic characters, converting to lowercase, removing stopwords, and performing lemmatization.
*   **Feature Engineering:** Uses `TfidfVectorizer` to convert text data into numerical features.
*   **Model Building:** Implements and evaluates four different classification models:
    *   Random Forest
    *   Logistic Regression
    *   Support Vector Machine (SVM)
    *   Naive Bayes
*   **Hyperparameter Tuning:** Uses `GridSearchCV` to find the best hyperparameters for each model, optimizing for the weighted F1-score.
*   **Model Evaluation:** Evaluates models using:
    *   Accuracy, Precision, Recall, and F1-score
    *   Classification Reports
    *   Confusion Matrices
    *   Precision-Recall Curves
*   **Pipeline Implementation:** Encapsulates the vectorization and classification steps into a `scikit-learn` pipeline for a streamlined workflow.
*   **Model and Plot Saving:** Saves the best-trained models and all generated plots to an `outputs` directory.

## Project Structure

```
.
├── README.md
├── data.json
├── outputs
│   ├── models
│   │   ├── logistic_regression_model.joblib
│   │   ├── naive_bayes_model.joblib
│   │   ├── random_forest_model.joblib
│   │   └── svm_model.joblib
│   └── plots
│       ├── label_distribution_bar.png
│       ├── label_distribution_pie.png
│       ├── logistic_regression_confusion_matrix.png
│       ├── logistic_regression_precision_recall_curve.png
│       ├── model_evaluation_metrics.png
│       ├── naive_bayes_confusion_matrix.png
│       ├── naive_bayes_precision_recall_curve.png
│       ├── random_forest_confusion_matrix.png
│       ├── random_forest_precision_recall_curve.png
│       ├── svm_confusion_matrix.png
│       └── svm_precision_recall_curve.png
├── requirements.txt
└── text_classification.py
```

## Getting Started

### Prerequisites

You need to have Python 3 and the libraries listed in `requirements.txt` installed. You will also need to download the NLTK data for tokenization, stopwords, and lemmatization.

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd Text-Classification
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Download NLTK data:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

### Running the Script

1.  Ensure you have the `data.json` file in the same directory.
2.  Run the script:
    ```bash
    python text_classification.py
    ```

The script will train the models, save the best versions, and generate and save all the evaluation plots.
