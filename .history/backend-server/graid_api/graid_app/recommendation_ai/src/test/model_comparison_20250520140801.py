import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.naive_bayes import GaussianNB

# Example data (replace with your own dataset)
soil_data = pd.read_csv('graid_app/recommendation_ai/src/data/soil_data.csv')
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
    "Quadratic Discriminant Analysis": GaussianNB(var_smoothing=1e-9),
    "Bagging": RandomForestClassifier(n_estimators=50, bootstrap=True),
    "Support Vector (RBF)": SVC(kernel='rbf', probability=True),
    "CatBoost": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1),
    


}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}
best_model = None
best_score = 0


for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    results[name] = scores
    if scores.mean() > best_score:
        best_score = scores.mean()
        best_model = model
    print(f"{name}: Mean Accuracy = {scores.mean():.4f} | Std = {scores.std():.4f}")

# Optional: Display results as a table
df = pd.DataFrame(results)
print("\nCross-validation accuracy scores:")

print(f"\nBest model: {best_model.__class__.__name__} with accuracy: {best_score:.4f}")