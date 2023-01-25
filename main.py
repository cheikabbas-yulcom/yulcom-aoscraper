# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 15:34:01 2022

@author: USER
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def joffres():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    URL = "https://joffres.net/recherche?domaine=Informatique+%26+D%C3%A9veloppement&localisation=&societe=&secteur=&prevision=0%2F1000000000&date_publication=&date_expiration=12%2F20%2F2022+-+01%2F31%2F2023&statut=Priv%C3%A9"
    page = requests.get(URL)

    # print(page.text)
    soup = BeautifulSoup(page.content, "html.parser")
    offres = soup.find_all("a", class_="job-title", href=True)
    localites = soup.find_all("small", "d-inline offre-localisation")
    dates_exp = soup.find_all("small", "expire-date text-success")
    dates_pub = soup.find_all("small", "societe to-hide-on-mobile")
    societes = soup.find_all("small", "societe")

    list_offres = []
    list_localite = []
    list_liens = []
    list_date_exp = []
    list_societe = []

    donnees = {}
    for offre in offres:
        list_offres.append(offre.text.strip())
    for offre in offres:
        list_liens.append(offre['href'])
    for localite in localites:
        list_localite.append(localite.text.strip())
    for date in dates_exp:
        list_date_exp.append(date.text.lstrip("Expire le\\r\\n").strip())
    for societe in societes:
        list_societe.append(societe.text.strip())

    donnees['Offres'] = list_offres
    donnees['Societes'] = list_societe[0:-1:2]
    donnees['Localites'] = list_localite
    donnees['DatePublication'] = list_societe[1:len(list_societe) + 1:2]
    donnees['DateExpiration'] = list_date_exp
    donnees['Liens'] = list_liens

    print(list_date_exp)

    data = pd.DataFrame.from_dict(donnees)
    return data


def undp():
    URL = "https://procurement-notices.undp.org/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    offres = soup.find_all("table", class_="standard cellborder")
    links = offres[0].find_all("a", href=True)
    links_list = []
    for link in links:
        links_list.append('https://procurement-notices.undp.org/' + str(link['href']))
    df = pd.read_html(str(offres[0]))
    data = df[0]
    data.drop(['Development Area', 'Development Area.1', 'Ref No', 'Procurement Process'], axis=1, inplace=True)
    data['links'] = links_list[8:]
    values = ["BURKINA FASO", "MALI", "NIGER", "MOROCCO", "TOGO", "SENEGAL", "COTE d'IVOIRE", "GUINEA", "BENIN"]
    data = data.loc[data['UNDP Country'].isin(values)]
    return data