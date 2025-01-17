"""
Nltk_downloading.py
This program to analyze the extracted comment and load the comment to the SQL server.
"""
import nltk
import logging
import os
from config_and_auxiliary import locate_log
from nltk.sentiment import SentimentIntensityAnalyzer

log_file = locate_log('app', "nltk_sentiment.log")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_file)])
logger = logging.getLogger("NLTK_Sentiment")

# setting ltk_data folder optional.
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)


class CommentAnalyzer:
    def __init__(self):
        try:
            # Check for VADER lexicon
            nltk.data.find('sentiment/vader_lexicon.zip')
            logger.info("VADER lexicon already downloaded.")
        except LookupError:
            # Download VADER lexicon if not found
            nltk.download('vader_lexicon')
            logger.info("VADER lexicon downloaded successfully.")
        self.sia = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, comment_string) -> dict | None:
        """
        Analyze the sentiment and returns the result as dict itself.
        @param comment_string: input string
        @return: dict as output
        """
        if not comment_string.strip():
            logger.warning("Empty comment string received.")
            return None
        sentiment_score = self.sia.polarity_scores(comment_string)
        return sentiment_score

    @staticmethod
    def sentiment_type(sentiment_score: dict) -> str:
        """
        Returns the sentiment_type for compound in given dict.
        @param sentiment_score: compound number from sentiment score.
        @return:
        """
        compound_score = sentiment_score['compound']
        if compound_score > 0.05:
            sentiment_type = 'positive'
        elif compound_score < -0.05:
            sentiment_type = 'negative'
        else:
            sentiment_type = 'neutral'
        return sentiment_type


if __name__ == "__main__":
    analyzer = CommentAnalyzer()
    example_comment = "This is a fantastic tool!"
    score = analyzer.analyze_sentiment(example_comment)
    if score:
        sentiment = CommentAnalyzer.sentiment_type(score)
        print(f"Sentiment: {sentiment}, Score: {score}")
