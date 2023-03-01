import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import pandas as pd

"""
Programme de Jérémy LUCAS, Amine HADDAD, Matthieu SFEIR et Oumaima
Programme de WebScraping et d'insertion sur BDD Mongo du site meteoblue.com
"""


"""
Ouverture BDD Local avec MongoDB
"""
client = MongoClient()
client = MongoClient('localhost', 27017)
DB = client.MeteoWebScrapingDB
Collection = DB.Indicator

"""
Ouvre le document 'prefecture.csv' contenant : Le nom de la préfécture ainsi que son code 
(utile pour le webscraping)
"""
prefectureData = pd.read_csv("prefecture.csv", sep=";")
prefectureDataFrame = pd.DataFrame(prefectureData)

"""Initialisation de listes pour stocker les Valeurs"""
villes = []
dates = []
temperatures = []
temperatures_resenties = []
precipitations = []
probabilites = []
direction_vent = []
vitesse = []

"""
Entrée : Nom de ville, Code de ville lié à Météoblue et le numéro de la page du jour
Sortie : URL de la page à Scraper
"""
def getUrl(ville, codeVille, page):
    url = "https://www.meteoblue.com/fr/meteo/semaine/"+str(ville)+"_france_"+str(codeVille)+"?day="+str(page)
    return url

"""
Entrée : Nom de ville et le code correspondant à cette ville
Sortie : Insertion dans les listes des Données WebScraper
"""
def extract_info(ville,codeVille):
    maxDay = 7 #Nombre max de jour à Scrap (1 à 7)
    for i in range (1,maxDay + 1):
        page = requests.get(getUrl(ville, codeVille, i))
        soup = BeautifulSoup(page.text, 'html.parser')

        #On avance jusqu'à arriver au Tableau de Données :
        wrapperMain = soup.find("div", attrs={'class': 'wrapper-main'})
        tabResults = wrapperMain.find("div", attrs={'class': 'tab-results'})
        tabWrapper = tabResults.find("div", attrs={'class': 'tab-wrapper'})
        tableValues = tabWrapper.findAll("tr")

        #Heures :
        times = tableValues[0]
        days = times.findAll('time')
        for day in days[1:]:
            dates.append(str(days[0].text) + " " + str(day.text[:2]) + ":" + str(day.text[2:]))

        #Températures :
        for temp in tableValues[2].findAll('td')[:-1]: #Une cellule en trop
            villes.append(ville)
            temperatures.append((temp.text)[:-1]) #On retire le symbole °

        #Températures Ressenties :
        for temp in tableValues[3].findAll('td')[:-1]:
            temperatures_resenties.append((temp.text)[:-1]) #On retire le symbole °

        #Direction du Vent :
        for dir_vent in tableValues[4].findAll('td')[:-1]:
            direction_vent.append(dir_vent.text)

        #Vitesse du Vent :
        for vitesse_vent in tableValues[5].findAll('td')[:-1]:
            vitesse.append((vitesse_vent.findAll('div')[2].text)[1:])

        #Précipitation :
        for precipitation in tableValues[6].findAll('td')[:-1]:
            precipitations.append((precipitation.findAll('div')[2].text)[1:-1])

        #Probabilités de Précipitation :
        for probPrec in tableValues[7].findAll('td')[:-1]:
            probabilites.append((probPrec.text)[2:-3])

"""
Entrée : Indice lié aux listes de Données
Sorties : Insertion dans MongoDB des données contenues dans les listes
"""
def insertDB(i):
    Record = {
        "ville": villes[i],
        "current-date": datetime.datetime.utcnow(),
        "date" : dates[i],
        "temperature": temperatures[i],
        "temperature-ressentie": temperatures_resenties[i],
        "precipitations": precipitations[i],
        "probabilités": probabilites[i],
        "direction-vent": direction_vent[i],
        "vitesse-vent": vitesse[i],
        }
    record_id = DB.Indicator.insert_one(Record)

#Convertion des données de préfectures en Liste pour l'usage du 'for' suivant
prefectureList = prefectureData.values.tolist()

"""
Extraction des données pour toutes les préféctures de france
"""
for prefecture in prefectureList:
    extract_info(prefecture[0], prefecture[1])

"""
Insertion des données dans une BDD MongoDB
"""
for i in range(len(villes)):
    insertDB(i)
    print(str(i+1) + "/" + str(len(villes)))

print("Done!")