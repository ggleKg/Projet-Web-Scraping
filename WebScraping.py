import requests
from bs4 import BeautifulSoup
import pandas as pd

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

def getUrl(codepostal):
    url = "https://meteofrance.com/previsions-meteo-france/" + str(codepostal)
    return url

#def extract_info(city, codepostal):
page = requests.get('https://www.lameteoagricole.net/meteo-heure-par-heure/Al%C3%A8s-30100-j1.html')
soup = BeautifulSoup(page.text, 'html.parser')
body_text = soup.find("div", attrs={'class': 'col-lg-8 col-xxl-9'})

#Obtenir la ville:
header = body_text.find("div", attrs={'class': 'table-outter-header'})
ville = header.find("span", attrs={'class': 'fs-5 p-5'})

#Obtenir le tableau d'informations:
indicTable = body_text.find("table", attrs={'id': 'heures-table'})

#Obtenir les dates/heures:
indicDates = indicTable.find('tr')
Dates = indicDates.findAll('th')
for date in Dates:
    date = date.findAll('span')
    dates.append(date[0].text + " " + date[1].text + " " + date[2].text)
    #print(date[0].text + " " + date[1].text + " " + date[2].text)

#Obtenir les indicateurs:
indicRowBody = indicTable.find('tbody')
indicRow = indicRowBody.findAll('td')
for indic in indicRow:
    villes.append(ville.text)
    indicDiv = indic.findAll('div', attrs={'class': 'd-flex flex-column mb-3 showDetailsBtn'})
    #Ensoleillement:
    sunshine = indicDiv[0].find('span', attrs = 'forModal')
    ensoleillements.append(sunshine.text)
    #Températures:
    temp = indicDiv[1].find('span', attrs = 'fw-bold fs-4 text-warning')
    temperatures.append(temp.text[:-1]) # [:-1] pour retirer le °
    tempR = indicDiv[1].find('span', attrs = 'fs-5 text-secondary noModal')
    temperatures_resentie.append(tempR.text[:-1]) # [:-1] pour retirer le °
    #Précipitations & probabilités:
    prec = indicDiv[2].find('span', attrs = 'fw-bold')
    precipitations.append(prec.text)
    prob = indicDiv[2].find('span', attrs = 'small text-shade-3 noModal')
    probabilites.append(prob.text[:-1]) # [:-1] pour retirer le %
    #Vents (Direction, Vitesse, Vitesse Rafale):
    dir = indicDiv[3].find('span', attrs = 'small')
    direction_vent.append(dir.text)
    vitesseVent = indicDiv[3].find('span', attrs = 'fw-bold')
    vitesse.append(vitesseVent.text)
    vitessesVent = indicDiv[3].findAll('span')
    vitesse_rafale.append(vitessesVent[7].text[:-5])
    #Humidités:
    humidite = indicDiv[4].find('span', attrs = 'fw-bold')
    humidites.append(humidite.text)
    #Nébulosités:
    nebulosite = indicDiv[5].find('span', attrs = 'fw-bold')
    nebulosites.append(nebulosite.text)


print(villes)
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
print(nebulosites)