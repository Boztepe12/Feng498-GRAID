class RecommendationService:
    def __init__(self, model):
        self.model = model

    def train(self):
        self.model.train()

    