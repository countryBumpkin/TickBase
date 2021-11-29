import csv
import pandas as pd

csv_path = 'C:/Users/deepg/Documents/TickBase/mendeley_article_Babesiosis_12-07-2021.csv'

with open(csv_path, encoding='utf-8') as file:
    reader = csv.reader(file)

    for row in reader:
        print(row[2])
