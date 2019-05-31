from encodings.utf_16 import encode
from time import sleep
from decimal import *

import requests
import re

import logging

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


from cassandra.cluster import Cluster
from bs4 import BeautifulSoup



KEYSPACE = "testkeyspace"
links = []
skipLinks = ['https://www.automobile.tn/fr/occasion/recherche',
             'https://www.automobile.tn/fr/occasion/du-jour',
             'https://www.automobile.tn/fr/occasion/comparateur',
             'https://www.automobile.tn/fr/occasion/vendeurs-pro']


def sleepF():
    print("sleeping......")
    sleep(60)

cluster = Cluster(['127.0.0.1'])
#cluster = Cluster(idle_heartbeat_interval=10)
session = cluster.connect()

log.info("creating keyspace...")
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
    """ % KEYSPACE)

log.info("setting keyspace...")
session.set_keyspace(KEYSPACE)

log.info("creating table...")
session.execute("""
    CREATE TABLE IF NOT EXISTS annonce (
        marque text,
        modele text,
        kilometrage text,
        annee text,
        energie text,
        boite text,
        prix text,
        lien text,
        description text,
        titre text,
        puissance text,
        PRIMARY KEY (lien)
    )
    """)

session.execute("""
    CREATE TABLE IF NOT EXISTS skips (
        lien text,
        PRIMARY KEY (lien)
    )
    """)




# display product
def product(url):
    web_r = requests.get(url)
    web_soup = BeautifulSoup(web_r.text, 'html.parser')

    kilometrage = web_soup.findAll("td", {"width" : "150"})[1].get_text()
    kilometrage = re.sub("[^0-9]", "", kilometrage)
    print("kilometrage : " + "'"+kilometrage+"'")

    energie = web_soup.findAll("td", {"width" : "150"})[0].get_text()
    energie = energie.lower()
    print("energie : " + "'"+energie+"'")

    annee = ""
    boite = ""
    puissance = ""
    max = len(web_soup.findAll("td"))
    i = 0
    j = 0
    while i < max:
        text = web_soup.findAll("td")[i].get_text()
        text = text.replace(' ', '').replace('\n', '').replace('\r', '').replace('\r', '\xa0')

        if re.match(r"[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9]", text):
            if j < 3:
                annee = text
                annee = annee[6:10]
                annee = re.sub("[^0-9]", "", annee)
                j += 1

        if "canique" in text:
            boite = "mécanique"

        if "tomatique" in text:
            boite = "automatique"

        if len(text) < 14 and "CV" in text:
            puissance = text
            puissance = puissance.replace('CV', '')
            puissance = puissance.replace(' ', '')
            puissance = re.sub("[^0-9]", "", puissance)

        i += 1

    print("annee : " + "'" + annee + "'")
    print("boite : " + "'" + boite + "'")

    prix1 = web_soup.findAll("td", {"class" : "da_field_text"}, {"colspan", "3"})[2].get_text()
    prix1 = prix1.replace('Dinar Tunisien (TND)', '')
    prix1 = prix1.replace(' ', '').replace('\n', '').replace('\r', '')

    prix1 = re.sub("[^0-9]", "", prix1)


    prix2 = web_soup.findAll("td", {"class","da_field_text"})[3].get_text()
    prix2 = prix2.replace('Dinar Tunisien (TND)', '')
    prix2 = prix2.replace(' ', '').replace('\n', '').replace('\r', '')

    prix2 = re.sub("[^0-9]", "", prix2)

    if prix1.isdigit():
        prix = prix1
    else:
        prix = prix2

    print("prix : " + "'"+prix+"'")

    description = web_soup.findAll("td", {"class" : "da_field_text"}, {"colspan","3"})[3].get_text() + " " + web_soup.findAll("td", {"class" : "da_field_text"}, {"colspan","3"})[4].get_text()

    titre = web_soup.findAll("td", {"class" : "da_field_text"}, {"colspan", "3"})[0].get_text()

    marque = titre.split('  > ', 2)[1]
    modele = titre.split('  > ', 2)[2]
    print("marque : " + "'"+marque+"'")
    print("modele : " + "'"+modele+"'")

    print("puissance : " + "'"+puissance+"'")



    if kilometrage.isdigit():

        if annee.isdigit():

            if prix.isdigit():

                if puissance.isdigit():

                    #prepared = session.prepare("""
                    #    INSERT INTO annonce (marque, modele, kilometrage, annee, energie, boite, prix, lien, description, titre, puissance)
                    #    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    #    """)
                    #log.info("inserting row")
                    #session.execute(prepared, (marque, modele, kilometrage, annee, energie, boite, prix, url, description, titre, puissance))
                    #rows3 = session.execute("SELECT count(*) FROM annonce")
                    #print("annonces totale : " + str(rows3[0]))
                    print("OK")

                else:
                    print("error puissance : '" + puissance + "'")

            else:
                print("error prix : '" + prix + "'")

        else:
            print("error annee : '" + annee +"'")

    else:
        print("error kilometrage : '" + kilometrage +"'")

#product('http://www.tunisie-annonce.com/DetailsAnnonceAuto.asp?cod_ann=2936975')

# check page links, call display or recursive
def page_scap(url):
    global links
    global skipLinks
    web_r = requests.get(url)
    web_soup = BeautifulSoup(web_r.text, 'html.parser')

    for i in web_soup.findAll("a"):
        link = i["href"]
        if not link.startswith("http"):
            if link.startswith("/"):
                link = "http://www.tunisie-annonce.com" + link
            else:
                link = "http://www.tunisie-annonce.com/" + link
        if link.startswith("http://www.tunisie-annonce.com"):
            if not link in links:
                links.append(link)
                if link.startswith("http://www.tunisie-annonce.com/AnnoncesAuto.asp?rech_cod_cat="):
                    #print("scaping : " + link)
                    page_scap(link)
                elif link.startswith("http://www.tunisie-annonce.com/DetailsAnnonceAuto.asp?cod_ann="):
                    #print("product : " + link)
                    #rows1 = session.execute("SELECT * FROM annonce where lien = '"+link+"'")
                    #rows2 = session.execute("SELECT * FROM skips where lien = '"+link+"'")
                    #if not rows1 or not rows2:
                    product(link)
                    print(" ")
                    print("---------------------------------------")
                    print("---------------------------------------")
                    print(" ")
                    sleep(1)
                    #else:
                    #    print("exists in CASSANDRA -------------------------------------------------------------------------------")
                #else:
                    #print("not useful page : " + link)
            #else#:
            #    print("link exists : " + link)
        #else:
        #    print("external : " + link)

        #print(" ")
        #print("---------------------------------------")
        #print("---------------------------------------")
        #print(" ")



page_scap("http://www.tunisie-annonce.com/AnnoncesAuto.asp")
#product("http://www.tunisie-annonce.com/DetailsAnnonceAuto.asp?cod_ann=2984691")

