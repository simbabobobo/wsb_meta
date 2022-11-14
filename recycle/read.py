import pandas as pd
import os
import csv

base_path = os.path.dirname(os.path.dirname(__file__))
input_path = os.path.join(base_path, 'results', 'ceshi.csv')

csv_reader = csv.reader(open(input_path))
pm=[]
for line in csv_reader:
    pm.append(line)

for i in pm:
    i[1]= float(i[1])
print(pm)
