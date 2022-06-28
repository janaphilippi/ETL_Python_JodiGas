'''This program utilized the 3.9.7 python's version. 
The objective of this task was to create a python script that outputted one valid JSON series per line, that contained data provided by 
a dataset in JODI-Gas World Database, based on the realization of the Jodi-Gas Questionnaire in different countries. The criteria for the 
set's organization, here in this program, was based on the page 33 of the Jodi-Gas manual (https://www.jodidata.org/_resources/files/downloads/manuals/jodi-gas-manual.pdf) 
where I quote: 

"This check involves comparing the data point of the latest month to that of the preceding months and/or to the data point of the 
same month in the previous year (which is normally the most useful comparison when data show a strong seasonal trend, as natural gas 
data often do)."

So, based on the advice provided by the manual, I chose to group the data per single months of different years, so it can be used to 
compare seasonal trends, per different countries, the kind of energy production, of flow and of units (because we can't compare apples 
to bananas). The result is very granular, but it implies in facilitation on applications and regrouping the data.'''

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import csv
import datetime
import json


def dateIso8601(period):
    date_time_obj = datetime.datetime.strptime(period, '%Y-%m').date()
    date_time = str(date_time_obj)
    return date_time

resp = urlopen("https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip")
zipfile = ZipFile(BytesIO(resp.read()))
file_name_list = zipfile.namelist()
zipfile.extractall()
   
for item in file_name_list:
    with open('{}'.format(item),'r', newline = '') as file:
        csvreader = csv.reader(file)
        data_csv = list(csvreader)
data_csv.pop(0)

series_dict = {}

for row in data_csv:
    row[1] = row[1].split('-')
    series_id = datetime.datetime.strptime(row[1][1], "%m").strftime("%B") + "\\" + row[0] +"\\" + row[2] + "\\" + row[3] + "\\" + row[4]
    if series_id not in list(series_dict.keys()):
        series_dict[series_id] = { "series_id":series_id,
                                  "points":[],
                                  "fields":{
                                      "country":row[0],
                                      "energy_product":row[2],
                                      "flow_breakdown":row[3],
                                      "unit_measure":row[4],
                                      "assessment_code":row[6]    
                                  }
                                }      
    list_d_p = [dateIso8601(row[1][0] + '-' + row[1][1]), float(row[5])]
    series_dict[series_id]["points"].append(list_d_p)

for i in series_dict.values():
    jsonString = json.dumps(i)
    print(jsonString)
 
