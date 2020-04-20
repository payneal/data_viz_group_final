import pycurl
import csv
import re
import stocks 
import requests

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

class StockDataImporter: 

    def __init__(self):
        self.headers = {}
        self.crumbValue =''
        self.buffer = BytesIO()
        self.encoding = 'iso-8859-1'
        self._set_cookie_header()
        self._set_crumb_value()
        self.stocks_info = stocks.all_stocks_info
        

    # private
    def _get_header_for_cookie(self, url):
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, self.buffer.write)
       # Set our header function.
        c.setopt(c.HEADERFUNCTION, self._grab_cookies_from_header)
        c.perform()
        c.close()
           
    def _grab_cookies_from_header(self, header_line):
        header_line = header_line.decode('iso-8859-1')
        if ':' not in header_line: return
        name, value = header_line.split(':', 1)
        name = name.strip()
        value = value.strip()
        name = name.lower()
        self.headers[name] = value
        
    def _get_cookie(self):
        if 'content-type' in self.headers:
            content_type = self.headers['content-type'].lower()
            match = re.search('charset=(\S+)', content_type)
            if match:
                self.encoding = match.group(1)
                print('Decoding using %s' % encoding)
    
    def _set_crumb_value(self): 
        body = self.buffer.getvalue()
        body = body.decode(self.encoding)
        p = re.compile(r'CrumbStore\":{\"crumb\":\"')
        mo1 = p.search(body)
        i = mo1.start()
        crumbValue= body[i+22:i+33]
        # print("here is crumbValue: " + crumbValue)
        self.crumbValue = crumbValue         

    def _set_cookie_header(self):
        url_for_cookie = "https://finance.yahoo.com/quote/AEX/history?p=AEX"
        # print("url for cookie: ")
        # print(url_for_cookie)
        self._get_header_for_cookie( url_for_cookie ) 
    
    def _grab_stock(self, info):

        url =("https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}").format(
            info["symbol"], info["start"], info['end'], self.crumbValue)
        # print("here is url: ")
        # print(url)
        headers = {"Cookie": self.headers['set-cookie']}
        req = requests.get(  url, headers=headers) 
        data = (req.text)
        data = data.splitlines()
        return data

    def _get_field_names(self, csv_data):
        new_data = []
        for x in csv_data:
            new_data.append(x.split(','))
        field_names = new_data[0]
        new_data.remove(new_data[0]) 
        data = self._format_data_for_csv(new_data)
        return field_names, data

    def _format_data_for_csv(self, new_data):

        # print ("here is new data: {}".format(new_data))
        data = []
        for x in new_data:
            data.append({
                'Date': x[0],
                'Open': x[1],
                "High": x[2],
                "Low":  x[3],
                "Close": x[4],
                "Adj Close": x[5],
                "Volume": x[6]
            })
        return data

    def _write_csv_stock_files(self, info, field_names, csv_data): 
        
        import os
        cwd = os.getcwd()
        del os
        file_location = cwd + "/../data/" + info['name'] + "/data.csv"
        with open(file_location, 'w', newline='') as file:
            writer= csv.DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            for x in csv_data:
                writer.writerow(x)

    # public
    def save_csv_stock_files(self):
        for info in self.stocks_info: 
            csv_data = self._grab_stock(info)
            field_names, csv_data  = self._get_field_names(csv_data)
            self._write_csv_stock_files(info, field_names, csv_data)


umm =  StockDataImporter()
umm.save_csv_stock_files()
print("done")
