
"""
Analyzer was pushed to new project.
2change
"""

import nltk
import json
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from concurrent.futures import ThreadPoolExecutor, as_completed
import seaborn as sns
import matplotlib.pyplot as plt


class AnalyserClass:
    def __init__(self, json_filename):
        self.filename = json_filename
        self.sentiment_data = {'details': [], 'neg': [], 'neu': [], 'pos': [], 'compound': []}
        if not nltk.downloader.Downloader().is_installed("vader_lexicon"):
            nltk.download('vader_lexicon')

    def read_json_file(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file '{self.filename}' does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file '{self.filename}' is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def analyze_comment(input_txt):
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(input_txt)
        return sentiment_scores

    def process_comments(self, comments_list):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.analyze_comment, text) for text in comments_list]
            for future in as_completed(futures):
                try:
                    data_dict = future.result()
                    for key in self.sentiment_data.keys():
                        self.sentiment_data[key].append(data_dict[key])
                except Exception as exc:
                    print(f'Generated an exception: {exc}')

    def plot_data(self):
        df = pd.DataFrame(self.sentiment_data)
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df[['neg', 'neu', 'pos', 'compound']])
        plt.title('Sentiment Analysis')
        plt.ylabel('Score')
        plt.xlabel('Sentiment')
        plt.show()

    def convert_and_process(self):
        result = self.read_json_file()
        first_key = next(iter(result))  # Channel name
        first_key_data = result[first_key]
        comment_texts = []

        for playlist in first_key_data['playlist']:
            for videos in playlist['videos']:
                for comments in videos[next(iter(videos))]['Comments']:
                    comment_text = videos[next(iter(videos))]['Comments'][comments]['Comment_Text']
                    comment_texts.append(comment_text)

        self.process_comments(comment_texts)


filename = "extracted_data/Sahi Siva-2024-06-02-14-54-06.json"
analyser = AnalyserClass(filename)
analyser.convert_and_process()
analyser.plot_data()
