from pymongo import MongoClient
import csv

client = MongoClient()
client = MongoClient('localhost',27017)
DB = client.MeteoWebScrapingDB
Collection = DB.Indicator

with open('data.csv','w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['id', 'ville', 'collect-date', 'meteo-date', 'temperature', 'temperature-ressentie', 'precipitations','probabilites', 'direction-vent', 'vitesse-vent'])
    for data in client.MeteoWebScrapingDB.Indicator.find():
        filewriter.writerow([str(data['_id']),str(data['ville']),str(data['current-date']),str(data['date']),str(data['temperature']),str(data['temperature-ressentie']),str(data['precipitations']),str(data['probabilités']),str(data['direction-vent']),str(data['vitesse-vent'])])
    print('Done!')