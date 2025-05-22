import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, make_scorer
import pandas as pd
from sklearn.naive_bayes import GaussianNB

# Example data (replace with your own dataset)
soil_data = pd.read_csv('backend-server/graid_api/graid_app/recommendation_ai/src/data/soil_data.csv')
soil_data = soil_data.drop('rainfall', axis=1)  
X = soil_data.drop('label', axis=1)  # Features
y = soil_data['label']  # Target variable

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "SVM": SVC(),
    "Naive Bayes": GaussianNB(),
    "Extra Trees": RandomForestClassifier(n_estimators=100, criterion='entropy'),
    "Decision Tree": RandomForestClassifier(n_estimators=1, criterion='gini', bootstrap=False),
    "K-Nearest Neighbors": SVC(kernel='linear', probability=True),
    "XGBoost": GradientBoostingClassifier(n_estimators=200, learning_rate=0.1),
    "AdaBoost": GradientBoostingClassifier(n_estimators=50, learning_rate=1.0, subsample=0.8),
    "Linear Discriminant Analysis": LogisticRegression(solver='liblinear'),
    "Bagging": RandomForestClassifier(n_estimators=50, bootstrap=True),
    "Support Vector (RBF)": SVC(kernel='rbf', probability=True),
    "CatBoost": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1),

}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}

best_accuracy = 0
best_f1 = 0
best_precision = 0
best_recall = 0
best_model_accuracy = None
best_model_f1 = None
best_model_precision = None
best_model_recall = None

for name, model in models.items():
    model_accuracy_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    model_f1_scores = cross_val_score(model, X, y, cv=cv, scoring='f1_macro')
    model_precision_scores = cross_val_score(
        model, X, y, cv=cv, scoring='precision_macro', error_score='raise'
    )
    model_recall_scores = cross_val_score(
        model, X, y, cv=cv, scoring='recall_macro', error_score='raise'
    )
    
    results[name] = model_accuracy_scores
    if model_accuracy_scores.mean() > best_accuracy:
        best_accuracy = model_accuracy_scores.mean()
        best_model_accuracy = model
    if model_f1_scores.mean() > best_f1:
        best_f1 = model_f1_scores.mean()
        best_model_f1 = model
    if model_precision_scores.mean() > best_precision:
        best_precision = model_precision_scores.mean()
        best_model_precision = model
    if model_recall_scores.mean() > best_recall:
        best_recall = model_recall_scores.mean()
        best_model_recall = model
    print(f"{name}: Mean F1 = {model_f1_scores.mean():.4f} | Std = {model_f1_scores.std():.4f}")
    print(f"{name}: Mean Precision = {model_precision_scores.mean():.4f} | Std = {model_precision_scores.std():.4f}")
    print(f"{name}: Mean Recall = {model_recall_scores.mean():.4f} | Std = {model_recall_scores.std():.4f}")
    print(f"{name}: Mean Accuracy = {model_accuracy_scores.mean():.4f} | Std = {model_accuracy_scores.std():.4f}")

# Optional: Display results as a table
df = pd.DataFrame(results)
print("\nCross-validation accuracy scores:")

print(df)

print("\nBest Models and Their Scores:")
print(f"Best Accuracy Model: {type(best_model_accuracy).__name__} | Score: {best_accuracy:.4f}")
print(f"Best F1 Model: {type(best_model_f1).__name__} | Score: {best_f1:.4f}")
print(f"Best Precision Model: {type(best_model_precision).__name__} | Score: {best_precision:.4f}")
print(f"Best Recall Model: {type(best_model_recall).__name__} | Score: {best_recall:.4f}")