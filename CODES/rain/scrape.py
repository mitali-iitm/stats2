f=open("codes.txt",'r')
codes=f.readlines()
f.close()
urls=[]


import requests
for code in codes:
	urls.append("https://worldweather.wmo.int/en/json/" + code.strip() + "_en.json" )
#-------------------------------------------------------------------
import csv
with open('weather.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["SN", "JAN", "FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"])
    i=0
    for url in urls:
    	resp=requests.get(url).json()["city"]["climate"]["climateMonth"]
    	row=[i]
    	i+=1
    	for month in range(12):
    		try:
    			row.append(resp[month]["rainfall"])
    		except:
    			row.append(0)
    	writer.writerow(row)
    	print(row)

#---------------------------------------------------------------------------