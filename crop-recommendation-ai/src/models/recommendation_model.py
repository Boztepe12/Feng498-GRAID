from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

class RecommendationModel:
    def __init__(self, soil_data):
        self.soil_data = soil_data
        self.models = {
            'RandomForest': RandomForestClassifier(),
            'SVM': SVC(),
            'DecisionTree': DecisionTreeClassifier(),
            'RandomForest_100': RandomForestClassifier(n_estimators=100),
            'SVM_rbf': SVC(kernel='rbf'),
            'SVM_linear': SVC(kernel='linear'),
            'SVM_poly': SVC(kernel='poly'),
            'SVM_sigmoid': SVC(kernel='sigmoid'),
            'DecisionTree_100': DecisionTreeClassifier(max_depth=100)
            

        }
        self.best_model = None

    def train(self):
        X, y = self.soil_data.drop('crop', axis=1), self.soil_data['crop']
        best_score = 0

        for name, model in self.models.items():
            scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
            mean_score = scores.mean()
            print(f'{name} Accuracy: {mean_score}')

            if mean_score > best_score:
                best_score = mean_score
                self.best_model = model

        self.best_model.fit(X, y)
        print(f'Best model: {self.best_model}')

    def predict(self, soil_features):
        if self.best_model is None:
            raise Exception("Model is not trained yet. Call train() before predict().")
        return self.best_model.predict([soil_features])