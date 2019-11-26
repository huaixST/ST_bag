import os
import datetime
import pandas as pd
import numpy as np
from geopy.distance import lonlat, distance
import csv
from collections import Counter
import time

os.chdir('F:\9417 project1\StudentLife_Dataset\Inputs\sensing\wifi_location')
path ='F:\9417 project1\StudentLife_Dataset\Inputs\sensing\wifi_location'  
files =os.listdir(path) 
files.sort() 
s= []  
feature_dict={
                "location_total" : [],
                "location_kinds_average":[],
                #"location_inside":[],
                #"location_outside":[],
                "inside_avg":[]
                
          }

for file_ in files:
    if not  os.path.isdir(path +file_):
        f_name = str(file_)
        s.append(f_name)   

def timestamp2string(timeStamp):    
        d = datetime.datetime.fromtimestamp(timeStamp) 
        str1 = d.strftime("%Y-%m-%d")
        return str1
      
for k in s:
    print(k)
    content=[]
    with open (k) as ds:
        csv_file = csv.reader(ds)
        for row in csv_file:
              if row != []:
                    content.append(row)

        content_t = content[1:]
        time_days = set()
        days = set()
        BSSID_list = []
        kinds_average = 0
        inside_num = 0
        outside_num = 0
        inside_time = 0
        timestamp_list = []
        temp_compare = ''
        inside_period = []
        prev_day = 0
        for i in range(len(content_t)):
            day = timestamp2string(int(content_t[i][0]))
            days.add(day)
            nowDay = time.localtime(int(content_t[i][0])).tm_yday
            if content_t[i][1] != temp_compare:
                temp_compare = ''
                if len(timestamp_list) > 1:
                    inside_time = int(int(timestamp_list[-1]) - int(timestamp_list[0]))
                inside_period.append(inside_time)
                inside_time = 0
                timestamp_list = []

            if content_t[i][1].startswith('in'):
                if prev_day + 1 < nowDay:
                    temp_compare = ''
                    if len(timestamp_list) > 1:
                        inside_time = int(int(timestamp_list[-1]) - int(timestamp_list[0]))
                    inside_period.append(inside_time)
                    inside_time = 0
                    timestamp_list = []
                timestamp_list.append(content_t[i][0])
                temp_compare = content_t[i][1]
            else:
                temp_compare = ''
            prev_day = nowDay

        for i in range(len(content_t)):
            content_t[i][0]= timestamp2string(int(content_t[i][0]))
            time_days.add(content_t[i][0])
            BSSID_list.append(content_t[i][1])
            nowDay = time.localtime(int(content_t[i][0])).tm_yday
            
            
        sum = 0
        for s in inside_period:
            sum += s   
        result = Counter(BSSID_list)
        result_len = len(result)
        kinds_average = result_len/len(time_days)
        inside_avg = sum/len(time_days)
        feature_dict["location_total"].append(result_len)
        feature_dict["location_kinds_average"].append(kinds_average)
        feature_dict["inside_avg"].append(inside_avg)
       

pd.DataFrame(feature_dict).to_csv('wifi_location_data.csv')


