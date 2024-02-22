import csv 
import json
from datetime import datetime


with open('times.csv','r',newline='') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # print(header_row)
    hours = []
    for row in reader:
        time = datetime.strptime(row[1], '%a, %d %b %Y %H:%M:%S %z') #takes string to date
        hour = time.strftime("%d") 
        hours.append(hour)

with open('hours.csv', 'w',newline='') as g:
    writer = csv.writer(g, delimiter=',')
    for hour in hours:
        writer.writerow(hour)

        