import csv
import json
import os
import stocks 

cwd = os.getcwd()
del os

json_data = {}

for info in stocks.all_stocks_info: 
    csvFilePath = cwd + "/../data/" + info['name'] + "/data.csv"

    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)

        for rows in csvReader:
            
            if (rows['Date'] not in json_data): 
                json_data[rows['Date']] = {}
        
            json_data[rows['Date']][info['name']] = {
                "close": rows['Close'],
                "open": rows["Open"],
                "high": rows['High'],
                "low": rows['Low'],
                "adj_close": rows['Adj Close'],
                "volume": rows["Volume"]}

jsonFilePath= cwd +"/../data/stock_data.json"
with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(json_data, indent=4))
