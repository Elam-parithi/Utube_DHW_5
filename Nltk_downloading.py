"""
pip install nltk
pip install --upgrade nltk

"""
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine, Table, MetaData, select, insert
from sqlalchemy.orm import sessionmaker


print(nltk.__version__)

# Download NLTK data (only once)
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# MySQL's connection string
DB_URL = 'mysql+pymysql://guvi_user:1king#lanka@localhost:3306/youtube_db'

# Setup SQLAlchemy engine and session
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Reflect existing database tables
metadata = MetaData()
metadata.reflect(bind=engine)

# Fetch the 'comments' table and check/create the 'sentiment' table
comments_table = metadata.tables['comments']

# Define or create the 'sentiment' table
if 'sentiment' not in metadata.tables:
    from sqlalchemy import Column, Integer, String, Table

    sentiment_table = Table(
        'sentiment',
        metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('comment_id', Integer, nullable=False),
        Column('comment_string', String(1000), nullable=False),
        Column('sentiment', String(20), nullable=False)
    )
    sentiment_table.create(engine)
else:
    sentiment_table = metadata.tables['sentiment']

# Query to fetch comments
query = select(comments_table.c.id, comments_table.c.comment_text)
result = session.execute(query)

# Insert sentiment analysis results into the 'sentiment' table
for row in result:
    comment_id = row.id
    comment_text = row.comment_text

    # Perform sentiment analysis
    sentiment_score = sia.polarity_scores(comment_text)
    sentiment = 'positive' if sentiment_score['compound'] > 0.05 else 'negative' if sentiment_score[
                                                                                        'compound'] < -0.05 else 'neutral'

    # Prepare insert statement
    insert_stmt = insert(sentiment_table).values(
        comment_id=comment_id,
        comment_text=comment_text,
        sentiment=sentiment
    )
    session.execute(insert_stmt)

# Commit the transaction
session.commit()
session.close()

print("Sentiment analysis completed and results stored in the 'sentiment' table.")

