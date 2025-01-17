import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

if __name__ == '__main__':
    # Keep Secrets separate
    from dotenv import load_dotenv
    from os import getenv
    load_dotenv('../.secrets')
    connection_string = getenv('DB_NAME')