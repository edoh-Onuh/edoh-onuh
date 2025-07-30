import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_recall_curve, auc
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
import warnings
from sklearn.exceptions import UndefinedMetricWarning
import joblib
import os

# Create directories for outputs
os.makedirs('outputs/models', exist_ok=True)
os.makedirs('outputs/plots', exist_ok=True)

# Load the dataset
df = pd.read_json('Text-Classification/data.json', convert_dates=['date'])

# Data Cleaning and Preprocessing
df = df[['text', 'label_name']].dropna().drop_duplicates()

# Check Data Information
df.info()

# Check Dataset Description
df.describe()

# Check Dataset Shape
df.shape

# Checking Null Values
df.isnull().sum()

# Define a function for text preprocessing
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove non-alphabetic characters and convert to lowercase
    tokens = [word.lower() for word in tokens if word.isalpha()]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    
    # Remove additional non-alphabetic characters using regex
    preprocessed_text = re.sub(r'[^a-zA-Z\s]', '', preprocessed_text)
    
    return preprocessed_text

# Apply preprocessing to the text data
df['processed_text'] = df['text'].apply(preprocess_text)

# Create a pipeline for vectorization and modeling
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000)),
    ('clf', OneVsRestClassifier(LogisticRegression(solver='liblinear'))) # Placeholder classifier
])

# Data Partitioning
X_train, X_test, y_train, y_test = train_test_split(df['processed_text'], df['label_name'], test_size=0.2, random_state=42, stratify=df['label_name'])

# Suppress UndefinedMetricWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Model Building, Hyperparameter Tuning, and Evaluation
models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'Logistic Regression': LogisticRegression(solver='liblinear'),
    'SVM': SVC(probability=True, random_state=42),
    'Naive Bayes': MultinomialNB()
}

param_grids = {
    'Random Forest': {
        'clf__estimator__n_estimators': [100, 200],
        'clf__estimator__class_weight': ['balanced']
    },
    'Logistic Regression': {
        'clf__estimator__C': [0.1, 1, 10],
        'clf__estimator__class_weight': ['balanced']
    },
    'SVM': {
        'clf__estimator__C': [0.1, 1, 10],
        'clf__estimator__gamma': ['scale', 'auto'],
        'clf__estimator__class_weight': ['balanced']
    },
    'Naive Bayes': {
        'clf__estimator__alpha': [0.1, 0.5, 1.0]
    }
}

evaluations = {}  # Dictionary to store evaluation metrics

for name, model in models.items():
    print(f"Training and evaluating {name}...")
    
    # Create a specific pipeline for the current model
    current_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000)),
        ('clf', OneVsRestClassifier(model))
    ])
    
    # Perform Grid Search for hyperparameter tuning
    grid_search = GridSearchCV(current_pipeline, param_grid=param_grids[name], cv=3, n_jobs=-1, scoring='f1_weighted')
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    
    # Predict on test data
    y_pred = best_model.predict(X_test)
    
    # Calculate accuracy
    accuracy = best_model.score(X_test, y_test)
    
    # Generate classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Store evaluation metrics
    evaluations[name] = {
        'Accuracy': accuracy, 
        'Precision': report['weighted avg']['precision'], 
        'Recall': report['weighted avg']['recall'],
        'F1-score': report['weighted avg']['f1-score']
    }
    
    # Print the report
    print(f"{name} Classifier Accuracy: {accuracy}")
    print(f"Best parameters for {name}: {grid_search.best_params_}")
    print(f"{name} Classifier Report:\n{classification_report(y_test, y_pred)}")
    
    # Save the best model
    joblib.dump(best_model, f'outputs/models/{name.lower().replace(" ", "_")}_model.joblib')
    
    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    cm_fig = ff.create_annotated_heatmap(z=cm, x=list(best_model.classes_), y=list(best_model.classes_), colorscale='Blues')
    cm_fig.update_layout(
        title=f'{name} Confusion Matrix',
        xaxis_title='Predicted Label',
        yaxis_title='True Label'
    )
    cm_fig.write_image(f'outputs/plots/{name.lower().replace(" ", "_")}_confusion_matrix.png')
    cm_fig.show()
    
    # Generate precision-recall curve for each class
    y_test_bin = label_binarize(y_test, classes=best_model.classes_)
    y_scores = best_model.predict_proba(X_test)
    
    pr_fig = go.Figure()
    
    for i, class_name in enumerate(best_model.classes_):
        precision, recall, _ = precision_recall_curve(y_test_bin[:, i], y_scores[:, i])
        pr_auc = auc(recall, precision)
        pr_fig.add_trace(go.Scatter(x=recall, y=precision, mode='lines', name=f'Class {class_name} (area = {pr_auc:.2f})'))
    
    pr_fig.update_layout(
        title=f'{name} Precision-Recall Curve',
        xaxis_title='Recall',
        yaxis_title='Precision'
    )
    pr_fig.write_image(f'outputs/plots/{name.lower().replace(" ", "_")}_precision_recall_curve.png')
    pr_fig.show()

# Interactive Visualization
label_counts = df['label_name'].value_counts().reset_index()
label_counts.columns = ['label_name', 'Count']
fig = px.bar(label_counts, x='label_name', y='Count', title='Distribution of Labels')
fig.write_image('outputs/plots/label_distribution_bar.png')
fig.show()

# Interactive Pie Chart 
label_distribution = y_test.value_counts().reset_index()
label_distribution.columns = ['label_name', 'Count']
fig = px.pie(label_distribution, values='Count', names='label_name', title='Distribution of Labels in Test Set')
fig.write_image('outputs/plots/label_distribution_pie.png')
fig.show()

# Model evaluation metrics using Plotly
model_names = list(evaluations.keys())
accuracy_values = [metrics['Accuracy'] for metrics in evaluations.values()]
precision_values = [metrics['Precision'] for metrics in evaluations.values()]
recall_values = [metrics['Recall'] for metrics in evaluations.values()]
f1_values = [metrics['F1-score'] for metrics in evaluations.values()]

fig = go.Figure()
fig.add_trace(go.Bar(x=model_names, y=accuracy_values, name='Accuracy', marker_color='blue'))
fig.add_trace(go.Bar(x=model_names, y=precision_values, name='Precision', marker_color='orange'))
fig.add_trace(go.Bar(x=model_names, y=recall_values, name='Recall', marker_color='green'))
fig.add_trace(go.Bar(x=model_names, y=f1_values, name='F1-score', marker_color='red'))

fig.update_layout(
    title='Model Evaluation Metrics',
    xaxis_title='Model',
    yaxis_title='Metric Value',
    barmode='group'
)
fig.write_image('outputs/plots/model_evaluation_metrics.png')
fig.show()
