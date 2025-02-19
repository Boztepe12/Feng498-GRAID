class RecommendationService:
    def __init__(self, model):
        self.model = model

    def get_recommendations(self, soil_data):
        predictions = self.model.predict(soil_data)
        recommendations = self._format_recommendations(predictions)
        return recommendations

    def _format_recommendations(self, predictions):
        formatted_recommendations = []
        for crop, probability in predictions.items():
            formatted_recommendations.append({
                'crop': crop,
                'probability': probability
            })
        return formatted_recommendations