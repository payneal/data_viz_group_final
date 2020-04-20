import json
import os
import csv
from datetime import date, timedelta
cwd = os.getcwd()
del os

stock_data_json  = cwd + "/../data/stock_data.json"
change_json = {}

with open( stock_data_json) as f:
    data = json.load(f)


# print( data["2015-01-22"]["AEX"])

one= None
two = None
all_stocks =  [ 
    'AEX',
    'ATX',
    'BEL_20',
    # 'BIST_100',
    'Bovespa',
    'BSE_Sensex',
    'CAC40',
    'CSE',
    'DAX_PERFORMANCE-INDEX',
    "Dow_30",
    # "Euro_Stoxx_50",
    "EURONEXT_100",
    "HANG_SENG_INDEX",
    "IBEX_35",
    "IDX_Composite",
    "KOSPI_Composite_Index",
    "MOEX_Russia_Index",
    "Nasdaq",
    "Nifty_50",
    "IPC_MEXICO",
    "MERVAL",
    "Nikkei_225",
    "Russell_2000",
    "SP_500",
    "SP_NZX_50_INDEX_GROSS",
    "SP_TSX_Composite_index",
    "SMI",
    # "SSE",
    # "TA_35",
    # "Taiwan_Weighted"
] 

all_dates = []

sdate = date(2015, 1, 22)   # start date
edate = date(2020, 3, 16)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    all_dates.append(day.strftime('%Y-%m-%d'))


previous_date = None


# for date in all_dates:
for date in data:
    if date not in change_json:
        change_json[date] = {}
    
    for stock in all_stocks:
        if stock not in change_json[date]:
            if previous_date is None:
                change_json[date][stock] =  None
            else:
                try: 
                    one = float(data[previous_date][stock]['close'])
                    two = float(data[date][stock]["close"])
                    change_json[date][stock] =  (two-one)/one
                except:
                    #print("on this stock: " + stock + " this date: "+ date+" had issue")
                    change_json[date][stock] =  0
    
    previous_date = date
    if date == edate.strftime('%Y-%m-%d'):
        break;


#print("what is this?")
# print(change_json)

# Writing json file
with open( cwd + "/../data/change_percent.json", "w") as outfile: 
    outfile.write(json.dumps(change_json, indent = 4))

csv_change_json = []

for x in change_json:
    umm = change_json[x]
    umm['DATE'] = x
    csv_change_json.append(umm)

#print("csv line one")
#print(csv_change_json[0])

csv_cols = all_stocks
csv_cols.insert(0, "DATE")


#print ("csv coloms: {}".format( csv_cols))

file_location = cwd+ "/../data/change_percent.csv"
with open(file_location, "w", newline="")  as file:
    writer= csv.DictWriter(file, fieldnames = csv_cols)
    writer.writeheader()
    for x in csv_change_json:
        writer.writerow(x)



# print(change_json)
