# File: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\crop-recommendation-ai\src\models\recommendation_model.py

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

class RecommendationModel:
    def __init__(self, soil_data):
        self.soil_data = soil_data
        self.model = GaussianNB()  # Focus on Naive Bayes
        self.best_model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()

    def train(self):
        X, y = self.soil_data.drop('label', axis=1), self.soil_data['label']
        y_encoded = self.label_encoder.fit_transform(y)
        X_scaled = self.scaler.fit_transform(X)  # Scale the data

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

        # Define hyperparameter grid for GaussianNB
        param_grid = {
            'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
        }

        # Use GridSearchCV for hyperparameter tuning
        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Set the best model
        self.best_model = grid_search.best_estimator_
        print(f'Best parameters: {grid_search.best_params_}')
        print(f'Best cross-validation score: {grid_search.best_score_}')

        # Evaluate on the test set
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
        
        # Scale the input features
        soil_features_scaled = self.scaler.transform([soil_features])
        
        # Get prediction probabilities
        probabilities = self.best_model.predict_proba(soil_features_scaled)[0]
        
        # Map probabilities to class labels
        class_labels = self.label_encoder.inverse_transform(range(len(probabilities)))
        predictions_with_confidence = {label: prob for label, prob in zip(class_labels, probabilities)}
        
        return predictions_with_confidence