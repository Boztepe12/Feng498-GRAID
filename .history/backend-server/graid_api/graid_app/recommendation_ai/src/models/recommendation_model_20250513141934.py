# File: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\crop-recommendation-ai\src\models\recommendation_model.py

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split, GridSearchCV

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.naive_bayes import GaussianNB



from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

class RecommendationModel:
    def __init__(self, soil_data):
        self.soil_data = soil_data
        self.model = GaussianNB()  
        self.best_model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()

    def train(self):
        
        # self.soil_data = self.soil_data.drop('rainfall',axis=1)  # Drop rows with missing values
        X, y = self.soil_data
        y_encoded = self.label_encoder.fit_transform(y)
        X_scaled = self.scaler.fit_transform(X)  

        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

        
        param_grid = {
            'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
        }

        
        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        
        self.best_model = grid_search.best_estimator_
        print(f'Best parameters: {grid_search.best_params_}')
        print(f'Best cross-validation score: {grid_search.best_score_}')

        
        self.evaluate(X_test, y_test)

    def evaluate(self, X_test, y_test):
        if self.best_model is None:
            raise Exception("Model is not trained yet. Call train() before evaluate().")
        
        y_pred = self.best_model.predict(X_test)  # Use test data
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='macro')
        recall = recall_score(y_test, y_pred, average='macro')
        f1 = f1_score(y_test, y_pred, average='macro')

        print(f'Accuracy: {accuracy}')
        print(f'Precision: {precision}')
        print(f'Recall: {recall}')
        print(f'F1 Score: {f1}')

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    def predict(self, soil_features):
        if self.best_model is None:
            raise Exception("Model is not trained yet. Call train() before predict().")
        
        # Ensure soil_features is a DataFrame with the same column names as the training data
        if not isinstance(soil_features, pd.DataFrame):
            soil_features = pd.DataFrame([soil_features], columns=self.soil_data.drop('label', axis=1).columns)
        
        # Scale the features
        soil_features_scaled = self.scaler.transform(soil_features)
        
        # Get probabilities for each class
        probabilities = self.best_model.predict_proba(soil_features_scaled)[0]
        
        # Map probabilities to class labels
        class_labels = self.label_encoder.inverse_transform(range(len(probabilities)))
        predictions_with_confidence = {label: f"{round(prob * 100, 3)}%" for label, prob in zip(class_labels, probabilities) if round(prob * 100, 3) > 0.00}
        sorted_predictions = dict(sorted(predictions_with_confidence.items(), key=lambda item: item[1], reverse=True))
        


        return sorted_predictions       