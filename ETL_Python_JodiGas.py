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
to bananas). The result is very granular, but it implies in facilitation on applications and regrouping the data. '''

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

def extractDataFromCsvList(data, column):
    name = []
    for row in data:
        if row[column] not in name:
            name.append(row[column])
    name.pop(0)
    return name

resp = urlopen("https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip")
zipfile = ZipFile(BytesIO(resp.read()))
file_name_list = zipfile.namelist()
zipfile.extractall()
   
for item in file_name_list:
    with open('{}'.format(item),'r', newline = '') as file:
        csvreader = csv.reader(file)
        data_csv = list(csvreader)

data_no_header = []
for row in data_csv:
    data_no_header.append(row)
data_no_header.pop(0)

month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
area_list = extractDataFromCsvList(data_csv, 0)
energy_product = extractDataFromCsvList(data_csv, 2)
flow_breakdown = extractDataFromCsvList(data_csv, 3)
unit_measure = extractDataFromCsvList(data_csv, 4)

for row in data_no_header:
    row[1] = row[1].split('-')


for u in unit_measure:
    for f in flow_breakdown:
        for p in energy_product:
            for country in area_list:
                for m in month:
                    list_date_points = []
                    assesment_code = 0
                    for data in data_no_header:
                        if data[0] == country and data[1][1] == m and data[2] == p and data[3] == f and data[4] == u:
                            list_d_p = [dateIso8601(data[1][0] + '-' + data [1][1]), float(data[5])]
                            list_date_points.append(list_d_p)
                            assesment_code = data[6]
                    
                    series_dict = { "series_id":datetime.datetime.strptime(m, "%m").strftime("%B") + "\\" + country +\
                                  "\\" + p + "\\" + f + "\\" + u,
                                  "points":list_date_points,
                                  "fields":{
                                      "country":country,
                                      "energy_product":p,
                                      "flow_breakdown":f,
                                      "unit_measure":u,
                                      "assessment_code":assesment_code     
                                  }
                                }                          
                    if series_dict["points"] != []:
                        jsonString = json.dumps(series_dict)
                        print(jsonString)