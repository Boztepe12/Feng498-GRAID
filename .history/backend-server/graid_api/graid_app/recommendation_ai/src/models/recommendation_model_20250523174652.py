# File: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\crop-recommendation-ai\src\models\recommendation_model.py

from sklearn.model_selection import  GridSearchCV


from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import numpy as np

class RecommendationModel:
    def __init__(self, soil_data):
        self.soil_data = soil_data
        self.model = RandomForestClassifier()  
        self.best_model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()

    def train(self):
        self.soil_data = self.soil_data.drop('rainfall', axis=1).drop('humidity',axis = 1)  # Drop rows with missing values
        X, y = self.soil_data.drop('label', axis=1), self.soil_data['label']
        
        # Fit the LabelEncoder with the labels
        self.label_encoder.fit(y)
        
        param_grid = {
            'n_estimators': [200],
            'max_depth': [10],
            'min_samples_split': [2],
            'min_samples_leaf': [1],
            
        }

        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X, y)

        self.best_model = grid_search.best_estimator_
        print(f'Best parameters: {grid_search.best_params_}')
        print(f'Best cross-validation score: {grid_search.best_score_}')

    def predict(self, soil_features):
        if self.best_model is None:
            raise Exception("Model is not trained yet.")

        # Convert soil_features to a DataFrame with the same column names as the training data
        if isinstance(soil_features, list):
            soil_features = pd.DataFrame([soil_features], columns=self.soil_data.drop('label', axis=1).columns)
        elif isinstance(soil_features, np.ndarray):
            soil_features = pd.DataFrame(soil_features, columns=self.soil_data.drop('label', axis=1).columns)

        # Get raw probabilities
        raw_probabilities = self.best_model.predict_proba(soil_features)[0]

        # Add smoothing to avoid 0% or 100% outputs
        epsilon = 1e-6
        smoothed_probs = (raw_probabilities + epsilon) / (raw_probabilities.sum() + epsilon * len(raw_probabilities))

        # Map smoothed probabilities to class labels
        class_labels = self.label_encoder.inverse_transform(np.arange(len(smoothed_probs)))
        predictions_with_confidence = {
            label: f"{round(prob * 100, 0)}%" 
            for label, prob in zip(class_labels, smoothed_probs)
        }

        # Sort by descending confidence
        sorted_predictions = dict(sorted(
            predictions_with_confidence.items(), 
            key=lambda item: float(item[1][:-1]), 
            reverse=True
        ))

        print("Smoothed probabilities:", smoothed_probs)
        print("Input features:\n", soil_features)
        print("Sorted predictions:\n", sorted_predictions)

        return sorted_predictions