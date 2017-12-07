import json
import csv

json_data = open('sample.json')
d = json.load(json_data)

csv_data = open('data.csv', 'w')

csvwriter = csv.writer(csv_data)

k = 'haha'
csvwriter.writerow(k)

csv_data.close()