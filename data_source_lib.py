
import pandas as pd
from datetime import datetime, timedelta
import requests as re
import json
import urllib as ur
from enum import Enum
import tqdm
from IPython.display import clear_output
import numpy as np
import time



class fundamentals(Enum):
    income = "income-statement"
    cash = "cash-flow-statement"
    balance = "balance-sheet-statement"

class get_fundamentals():
    
    def __init__(self, ticker, fun, output ="table"):
        if not isinstance(fun, fundamentals):
            raise "should input a instance of fundamentals"
        self.ticker = ticker.upper()
        self.fun = fun
        self.output = "table"
        self.result = {}


            
    def data_bulk_output(self):
       
        
        if self.output == "table":
            
            return self.result
          
        
    def get_fundamentals_data(self):
        trial=0
        while trial < 3:
            try:
                profile="https://financialmodelingprep.com/api/financials/{}/{}".format(self.fun.value,self.ticker)

                temp = re.get(profile,verify=False).text

                temp=temp.replace("\n","")

                temp = temp.replace("<pre>","")

                temp= json.loads(temp)

                temp = pd.DataFrame(temp[self.ticker])

                self.result[self.ticker] =temp

                return temp
            
            except Exception as e:
                print e
                trial+=1
            
        
class get_stock_data():
    
     def __init__(self,tic_list, output="table", **kwargs):
        self.arg_list = {"freq": 'minutes',"start_date": datetime.now()-timedelta(days =256),\
                    "end_date":datetime.now(), "day_range": 256, "file_name":""}
        
        self.tic_list = tic_list
        self.output = output
        self.arg_list["start_date"] 
        
        
        for key , arg in kwargs.iteritems():
            
            if key in ["freq","start_date","end_date"]:
                self.arg_list[key]=arg
            
            if key in ["timeframe"]:
                self.arg_list[key]=arg
                self.arg_list["start_date"] = datetime.now()-timedelta(days =arg)
    
        self.error = []
    
     def data_output(self):
       
        
        if self.output == "table":
            
            return self.result
    
        if self.output == "file":
            self.result.to_csv(self.arg_list["file_name"])
     
        

    
     def get_ondemand_data(self, interval = 1):
            
            self.result = pd.DataFrame()
            
            for i in tqdm.tqdm(range(len(self.tic_list))):
                trial = 0
                i = self.tic_list[i].upper()
                while trial <3:
                    try:
                        api_key = '95b5894daf3abced33fe48e7f265315e'
                        start_date=self.arg_list["start_date"].strftime("%Y%m%d%H%M%S")
                        end_date=self.arg_list["end_date"].strftime("%Y%m%d%H%M%S")
                        # This is the required format for datetimes to access the API

                        api_url = 'http://marketdata.websol.barchart.com/getHistory.csv?' + \
                                                'key={}&symbol={}&type={}&startDate={}&endDate={}&interval={}'\
                                                 .format(api_key, i, self.arg_list["freq"], start_date,end_date,interval)

                        temp = pd.read_csv(api_url, parse_dates=['timestamp'])
                        temp.set_index('timestamp', inplace=True)



                        #index= pd.MultiIndex.from_product([[i],temp.index])
                        #temp=pd.DataFrame(data=temp.values,index=index,columns=temp.columns)

                        self.result = self.result.append(temp)
                        clear_output()
                        print "Finished", i
                        
                        #time.sleep(5)
                        trial=3

                    except Exception as e:
                        print e
                        print "error occorded in getting data for ", i
                        trial +=1
                        time.sleep(10)
                        if trial == 3:
                            self.error.append([i,'get_ondemand'])
            
            self.result = self.result.reset_index()
            self.result["close"] = self.result["Close"]
            self.result = self.result.rename(columns={'symbol':'Ticker','timestamp':"TimeStamp","high":"High","low":"Low","open":"Open","volume":"Volume"})
            self.result["Return"]=( self.result.Close.diff(1)/self.result.Close)
            
            return self.data_output()
           
     def get_quandl_data(self, interval = 1):
            
            self.result = pd.DataFrame()
            
            for i in tqdm.tqdm(range(len(self.tic_list))):
                trial = 0
                i = self.tic_list[i].upper()
                while trial <3:
                    try:
                        api_key = 'scyebx61MMZzsK4yPcch'
                        start_date=self.arg_list["start_date"].strftime("%Y%m%d%H%M%S")
                        end_date=self.arg_list["end_date"].strftime("%Y%m%d%H%M%S")
                        # This is the required format for datetimes to access the API

                        api_url = "https://www.quandl.com/api/v3/datasets/" +\
                                    "EOD/{}?start_date={}&end_date={}&api_key={}"\
                                                 .format(i,start_date,end_date,api_key)

                        temp  = re.get(api_url,verify=False)
                        
                        print "query result code: " + str(temp.status_code)

                        temp = temp.text

                        temp = json.loads(temp)

                        temp = pd.DataFrame(temp)

                        temp = pd.DataFrame(temp.loc["data"][0],columns=temp.loc["column_names"][0])

                        temp["Ticker"] =i
                        
                        temp.set_index('Date', inplace=True)
                        
                        self.result = self.result.append(temp)

                        #index= pd.MultiIndex.from_product([[i],temp.index])
                        #temp=pd.DataFrame(data=temp.values,index=index,columns=temp.columns)

                        clear_output()
                        print "Finished", i
                        
                        #time.sleep(5)
                        trial=3

                    except Exception as e:
                        print e
                        print "error occorded in getting data for ", i
                        trial +=1
                        time.sleep(10)
                        if trial == 3:
                            self.error.append([i,'get_ondemand'])
            self.result = self.result.reset_index()
            self.result = self.result[["Ticker","Date","Adj_High","Adj_Low","Adj_Close","Adj_Open","Adj_Volume"]]
            self.result = self.result.rename(columns={'Date':"TimeStamp","Adj_High":"High","Adj_Low":"Low","Adj_Open":"Open","Adj_Volume":"Volume","Adj_Close":"Close"})
            self.result["Return"]=( self.result.Close.diff(1)/self.result.Close)
            
            return self.data_output()       
            
     def get_quote(self):
        
        self.result = pd.DataFrame()
        
        for i in tqdm.tqdm(range(len(self.tic_list))):
            i = self.tic_list[i].upper()

        profile="https://financialmodelingprep.com/api/company/price/{}".format(i)

        temp = re.get(profile, verify=False).text

        temp=self.result.replace("\n","")

        temp = self.result.replace("<pre>","")

        temp= json.loads(result)

        temp = pd.DataFrame(result).transpose()
        
        self.result = self.result.append(temp)
        
        self.data_output()
            
            
         
        
    
                 
    