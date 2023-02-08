import requests
from bs4 import BeautifulSoup
import pandas as pd

cities = []
dates = []

def getUrl(codepostal):
    url = "https://meteofrance.com/previsions-meteo-france/" + str(codepostal)
    return url

#def extract_info(city, codepostal):
page = requests.get('https://www.lameteoagricole.net/meteo-heure-par-heure/Rouen-35000-j1.html')
soup = BeautifulSoup(page.text, 'html.parser')
body_text = soup.find("div", attrs={'class': 'col-lg-8 col-xxl-9'})

#Obtenir la ville:
header = body_text.find("div", attrs={'class': 'table-outter-header'})
city = header.find("span", attrs={'class': 'fs-5 p-5'})
cities.append(city.text)

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
    indicDiv = indic.findAll('div', attrs={'class': 'd-flex flex-column mb-3 showDetailsBtn'})
    #print(indicDiv)
    for value in indicDiv:
        print(value)