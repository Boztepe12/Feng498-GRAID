# File: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\crop-recommendation-ai\src\models\recommendation_model.py

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split, GridSearchCV

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.naive_bayes import GaussianNB



from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import numpy as np

class RecommendationModel:
    def __init__(self, soil_data):
        self.soil_data = soil_data
        self.model = GaussianNB()  
        self.best_model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()

    def train(self):
        self.soil_data = self.soil_data.drop('rainfall', axis=1)  # Drop rows with missing values
        X, y = self.soil_data.drop('label', axis=1), self.soil_data['label']
        
        # Fit the LabelEncoder with the labels
        self.label_encoder.fit(y)
        
        param_grid = {
            'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
        }

        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X, y)

        self.best_model = grid_search.best_estimator_
        print(f'Best parameters: {grid_search.best_params_}')
        print(f'Best cross-validation score: {grid_search.best_score_}')

    def predict(self, soil_features):
        if self.best_model is None:
            raise Exception("Model is not trained yet. Call train() before predict().")
        
        # Convert soil_features to a DataFrame with the same column names as the training data
        if isinstance(soil_features, list):
            soil_features = pd.DataFrame([soil_features], columns=self.soil_data.drop('label', axis=1).columns)
        elif isinstance(soil_features, np.ndarray):
            soil_features = pd.DataFrame(soil_features, columns=self.soil_data.drop('label', axis=1).columns)
        
        # Get probabilities for each class
        probabilities = self.best_model.predict_proba(soil_features)[0]  # Extract the first row
        print(probabilities)
        
        # Map probabilities to class labels
        class_labels = self.label_encoder.inverse_transform(range(len(probabilities)))
        predictions_with_confidence = {label: f"{round(prob * 100, 3)}%" for label, prob in zip(class_labels, probabilities) if round(prob * 100, 3) > 0.00}
        sorted_predictions = dict(sorted(predictions_with_confidence.items(), key=lambda item: float(item[1][:-1]), reverse=True))
        
        return sorted_predictions