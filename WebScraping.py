import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import pandas as pd

"""
Programme de WebScraping et d'insertion en BDD du site lameteoagricole.net
"""

client = MongoClient()
client = MongoClient('localhost', 27017)

DB = client.WebScrapingTestDB
Collection = DB.Indicator

prefecture = []

def getPrefecture():
    page = requests.get('https://fr.wikipedia.org/wiki/Liste_des_préfectures_de_France')
    soup = BeautifulSoup(page.text, 'html.parser')
    body_text = soup.find('center')
    tableBody = body_text.find('tbody')
    tableRow = tableBody.findAll('tr')
    for line in tableRow[1:]:
        codepostale = line.find('th').text[:-2]
        ville = line.findAll('a')[1].text
        if (codepostale not in ['971','972','973','974','976']):
            list = [ville,codepostale]
            prefecture.append(list)

getPrefecture()

villes = []
dates = []
ensoleillements = []
temperatures = []
temperatures_resentie = []
precipitations = []
probabilites = []
direction_vent = []
vitesse = []
vitesse_rafale = []
humidites = []
nebulosites = []

def getUrl(ville, codepostal, page):
    url = "https://www.lameteoagricole.net/meteo-heure-par-heure/" + str(ville) +"-" + str(codepostal) + "000-j"+str(page)+".html"
    return url

def extract_info(ville, codepostal):
    for i in range (2,4):
        page = requests.get(getUrl(ville, codepostal,i))
        soup = BeautifulSoup(page.text, 'html.parser')
        body_text = soup.find("div", attrs={'class': 'col-lg-8 col-xxl-9'})

        # Obtenir la ville:
        header = body_text.find("div", attrs={'class': 'table-outter-header'})
        ville = header.find("span", attrs={'class': 'fs-5 p-5'})

        # Obtenir le tableau d'informations:
        indicTable = body_text.find("table", attrs={'id': 'heures-table'})
        # Obtenir les dates/heures:
        indicDates = indicTable.find('tr')
        Dates = indicDates.findAll('th')
        for date in Dates:
            date = date.findAll('span')
            dates.append(date[0].text + " " + date[1].text + " " + date[2].text)

        # Obtenir les indicateurs:
        indicRowBody = indicTable.find('tbody')
        indicRow = indicRowBody.findAll('td')
        for indic in indicRow:
            villes.append(ville.text)
            indicDiv = indic.findAll('div', attrs={'class': 'd-flex flex-column mb-3 showDetailsBtn'})

            # Ensoleillement:
            sunshine = indicDiv[0].find('span', attrs='forModal')
            ensoleillements.append(sunshine.text)

            # Températures:
            temp = indicDiv[1].find('span', attrs='fw-bold fs-4 text-warning')
            temperatures.append(temp.text[:-1])  # [:-1] pour retirer le °
            tempR = indicDiv[1].find('span', attrs='fs-5 text-secondary noModal')
            temperatures_resentie.append(tempR.text[:-1])  # [:-1] pour retirer le °

            # Précipitations & probabilités:
            prec = indicDiv[2].find('span', attrs='fw-bold')
            precipitations.append(prec.text)
            prob = indicDiv[2].find('span', attrs='small text-shade-3 noModal')
            probabilites.append(prob.text[:-1])  # [:-1] pour retirer le %

            # Vents (Direction, Vitesse, Vitesse Rafale):
            dir = indicDiv[3].find('span', attrs='small')
            direction_vent.append(dir.text)
            vitesseVent = indicDiv[3].find('span', attrs='fw-bold')
            vitesse.append(vitesseVent.text)
            vitessesVent = indicDiv[3].findAll('span')
            vitesse_rafale.append(vitessesVent[7].text[:-5])

            # Humidités:
            humidite = indicDiv[4].find('span', attrs='fw-bold')
            humidites.append(humidite.text)

            # Nébulosités:
            nebulosite = indicDiv[5].find('span', attrs='fw-bold')
            nebulosites.append(nebulosite.text)
        Record = {
            "ville": villes[-1],
            "current-date": datetime.datetime.utcnow(),
            "date": dates[-1],
            "ensoleillement": ensoleillements[-1],
            "temperature": temperatures[-1],
            "temperature-ressentie": temperatures_resentie[-1],
            "precipitations": precipitations[-1],
            "probabilités": probabilites[-1],
            "direction-vent": direction_vent[-1],
            "vitesse-vent": vitesse[-1],
            "vitesse-rafale": vitesse_rafale[-1],
            "humitide": humidites[-1],
            "nebulosite": nebulosites[-1]
        }
        record_id = DB.Indicator.insert_one(Record)
        print(record_id)

#extract_info("Nîmes",30)


for list in prefecture:
    print(list[0], list[1])
    if list[1] == "2A":
        extract_info("", 20)
    elif list[1] == "2B":
        extract_info("",20200)
    elif int(list[1]) == 54:
        extract_info("Nancy",54100)
    elif int(list[1]) == 97:
        pass
    else :
        extract_info(list[0], list[1])
    print(len(villes))


"""print(villes)
print(dates)
print(ensoleillements)
print(temperatures)
print(temperatures_resentie)
print(precipitations)
print(probabilites)
print(direction_vent)
print(vitesse)
print(vitesse_rafale)
print(humidites)
print(nebulosites)"""