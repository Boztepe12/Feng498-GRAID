# File: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\crop-recommendation-ai\src\models\recommendation_model.py

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
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
        self.models = {
            'RandomForest': RandomForestClassifier(),
            'SVM': SVC(),
            'DecisionTree': DecisionTreeClassifier(),
            'XGBoost': XGBClassifier(),
            'KNN': KNeighborsClassifier(),
            'LogisticRegression': LogisticRegression(max_iter=1000),  # Increased max_iter
            'NaiveBayes': GaussianNB(),
            'AdaBoost': AdaBoostClassifier(),
            'GradientBoosting': GradientBoostingClassifier(),
            'BaggingClassifier': BaggingClassifier(),
            'ExtraTreesClassifier': ExtraTreesClassifier(),
            'MLPClassifier': MLPClassifier(max_iter=1000)  # Increased max_iter
        }
        self.best_model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()

    def train(self):
        X, y = self.soil_data.drop('label', axis=1), self.soil_data['label']
        y_encoded = self.label_encoder.fit_transform(y)
        X_scaled = self.scaler.fit_transform(X)  # Scale the data

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

        best_score = 0

        # Use StratifiedKFold for cross-validation
        skf = StratifiedKFold(n_splits=5)

        for name, model in self.models.items():
            scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='accuracy')
            mean_score = scores.mean()
            print(f'{name} Mean Cross-Validation Score: {mean_score}')

            if mean_score > best_score:
                best_score = mean_score
                self.best_model = model

        self.best_model.fit(X_train, y_train)  # Use training data
        print(f'Best model: {self.best_model}, Best Score: {best_score}')

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
        soil_features_scaled = self.scaler.transform([soil_features])  # Scale the input features
        prediction_encoded = self.best_model.predict(soil_features_scaled)
        prediction = self.label_encoder.inverse_transform(prediction_encoded)
        return prediction