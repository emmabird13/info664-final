import pandas as pd

with open('plre_books_data.json', encoding='utf-8') as json_file:
  df = pd.read_json(json_file)

df.to_csv('plre_books_data.csv', encoding='utf-8', index='FALSE')