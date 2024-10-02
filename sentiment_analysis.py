from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment_vader(text):
    """
    Analyze the sentiment of the given text using VADER.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        float, str: Sentiment score and label (Positive, Negative, or Neutral).
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = analyzer.polarity_scores(text)
    sentiment_score = sentiment_dict['compound']
    sentiment_label = "Neutral"
    
    if sentiment_score >= 0.05:
        sentiment_label = "Positive"
    elif sentiment_score <= -0.05:
        sentiment_label = "Negative"
    
    return sentiment_score, sentiment_label
