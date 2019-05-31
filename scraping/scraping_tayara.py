from time import sleep

import requests

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
    sleep(3)

cluster = Cluster(['127.0.0.1'])
#cluster = Cluster(idle_heartbeat_interval=10)
session = cluster.connect()

log.info("creating keyspace...")
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
    """ % KEYSPACE)
#
log.info("setting keyspace...")
session.set_keyspace(KEYSPACE)
#
log.info("creating table...")
session.execute("""
    CREATE TABLE IF NOT EXISTS annonce (
        marque text,
        modele text,
        kilometrage decimal,
        annee decimal,
        energie text,
        boite text,
        prix decimal,
        lien text,
        description text,
        titre text,
        puissance text,
        PRIMARY KEY (lien)
    )
    """)
#
# display product
def product(url):
    web_r = requests.get(url)
    web_soup = BeautifulSoup(web_r.text, 'html.parser')

    kilometrage = web_soup.findAll("div",{"class":"infos"})[0].findAll("li")[0].findAll("span")[0].get_text()
    kilometrage = kilometrage.replace('Km', '')
    kilometrage = kilometrage.replace('km', '')
    kilometrage = kilometrage.replace(' ', '')


    annee = web_soup.findAll("div",{"class":"infos"})[0].findAll("li")[1].findAll("span")[0].get_text()
    annee = annee[3:7]

    #energie = web_soup.findAll("div", {"class" : "technical-details"})[0].findAll("table")[1].findAll("td")[1].get_text()
    energie = web_soup.findAll("div", {"class" : "technical-details"})[0].findAll("table")[1].findAll("td")[0].get_text()
    energie = energie.lower()

    boite = web_soup.findAll("div", {"class" : "technical-details"})[0].findAll("table")[3].findAll("td")[0].get_text()
    boite = boite.lower()


    prix = web_soup.findAll("div", {"class" : "buttons"})[0].findAll("span")[0].get_text()
    prix = prix.replace('Prix', '')
    prix = prix.replace('DT','')
    prix = prix.replace(' ', '')

    description = web_soup.findAll("div", {"class" : "description"})[0].findAll("p")[0].get_text()

    titre = web_soup.findAll("div", {"class", "bloc-title"})[0].findAll("h3")[0].get_text()

    marque = titre.split(' ', 1)[0]
    modele = titre.split(' ', 1)[1]

    puissance = web_soup.findAll("div", {"class" : "technical-details"})[0].findAll("table")[2].findAll("td")[0].get_text()
    puissance = puissance.replace('CV', '')
    puissance = puissance.replace(' ', '')

   #prepared = session.prepare("""
   #    INSERT INTO annonce (marque, modele, kilometrage, annee, energie, boite, prix, lien, description, titre, puissance)
   #    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   #    """)

    #l#og.info("inserting row")
    #session.execute(prepared, (marque, modele, kilometrage, annee, energie, boite, prix, url, description, titre, puissance))

    print(marque +" "+ modele + " " + prix + "DT")


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
                link = "https://www.tayara.tn" + link
            else:
                link = url + link
        if link.startswith("https://www.tayara.tn") and not link.endswith("#"):
            if not link in links:
                links.append(link)
                if link.startswith("https://www.tayara.tn/listings/voitures-9"):
                    print("product : " + link)
                    product(link)
                    #sleepF()
                else:
                    print("not useful page : " + link)
            else:
                print("link exists : " + link)
        else:
            print("external : " + link)

        print(" ")
        print("---------------------------------------")
        print("---------------------------------------")
        print(" ")
        #sleepF()



page_scap("https://www.tayara.tn/c/v%C3%A9hicules/voitures")

