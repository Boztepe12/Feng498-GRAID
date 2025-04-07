class RecommendationService:
    def __init__(self, model):
        self.model = model

    def train(self):
        self.model.train()

    def predict(self, soil_features):
        return self.model.predict(soil_features)

    