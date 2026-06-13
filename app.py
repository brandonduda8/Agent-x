from transformers import pipeline

sentiment_pipeline = pipeline('sentiment-analysis')

# Example usage
text = "I love using AI to solve specific problems!"
result = sentiment_pipeline(text)
print(result)