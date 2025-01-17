import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv

load_dotenv('../.secrets')
db_precon = getenv('pre_conn')
DB_name = getenv('DB_NAME')

connection_string = f"{db_precon}{DB_name}"
engine = create_engine(connection_string)

query = """SELECT comments.sentiment FROM youtube_local.comments, channels
where channels.channel_name = 'guvi';"""

df = pd.read_sql(query, engine)
print(df.head())
engine.dispose()


sns.set(style="whitegrid", palette="muted", font_scale=1.2)

plt.figure(figsize=(10, 6))

sns.boxplot(y='sentiment', data=df, color='lightgreen')
plt.title("Box Plot of Sentiment Scores")
plt.ylabel("Sentiment Score")
plt.tight_layout()
plt.show()

sns.histplot(data=df, x='sentiment', kde=True, bins=30, color='skyblue')
plt.title("Distribution of Sentiment Scores")
plt.xlabel("Sentiment Score")
plt.ylabel("Frequency")
plt.show()

sns.violinplot(y='sentiment', data=df, color='orange')
plt.title("Violin Plot of Compound Sentiment Scores")
plt.ylabel("Compound Sentiment Score")
plt.show()

df['sentiment_category'] = pd.cut(df['sentiment'], bins=[-1, -0.05, 0.05, 1], labels=['Negative', 'Neutral', 'Positive'])
sentiment_counts = df['sentiment_category'].value_counts()

sentiment_counts.plot(kind='pie', autopct='%1.1f%%', colors=['red', 'gray', 'green'], startangle=140)
plt.title("Proportion of Sentiment Categories")
plt.ylabel('')  # Hides the y-label
plt.show()

