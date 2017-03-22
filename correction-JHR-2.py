# coding: utf-8

### Ce scrit prend l'idée de Jean Balthazard et l'applique à l'ensemble des profs de l'UQAM

import csv
import requests
from bs4 import BeautifulSoup

url = "http://professeurs.uqam.ca/listeunite"

dossier = "repertoire-uqam-complet-JHR.csv"

entetes = {
    "User-Agent" : "JH Roy - Excercice pour cours de journalisme informatique", 
    "From" : "roy.jean-hugues@uqam.ca"
    }
    
contenu = requests.get(url,headers=entetes)
page = BeautifulSoup(contenu.text,"html.parser")

nbProfs = 0

for departement in page.find("div", id="contenu").find_all("li"):
    print("\n"+"#"*80)
    print(departement.text.strip())
    # print(departement.a["href"])
    lien = "http://professeurs.uqam.ca" + departement.a["href"]

    contenu2 = requests.get(lien, headers=entetes)
    page2 = BeautifulSoup(contenu2.text,"html.parser")

    profs = len(page2.find_all("td", class_="nom_professeur"))
    # print(profs)

    if profs > 0:

        for prof in page2.find_all("td", class_="nom_professeur"):

            nbProfs += 1

            annuaire = []
            # print(prof.text.strip())
            lien2 = "http://professeurs.uqam.ca" + prof.a["href"]

            contenu3 = requests.get(lien2, headers=entetes)
            page3 = BeautifulSoup(contenu3.text,"html.parser")

            nom = page3.find("div", id="fiche").h1.text.strip()
            print("\n"+"-"*30)
            print("Prof. " + nom + " (" + lien2 + ")\nest le #" + str(nbProfs) + " qu'on ramasse")
            annuaire.append(nom)

            if page3.find("div", class_="col-md-6") in page3.find("div", id="fiche").find("div", class_="row"):
    
                ### Les infos qui nous intéressent sont incluses dans des balises <p>; on les met toutes dans une variable que je vais appeler «infos»
                infos = page3.find("div", class_="col-md-6").find_all("p")
                # print(len(infos))

                ### Le premier de ces <p> contient le nom du département; on le ramasse
                dept = infos[0].text.strip()
                # print(dept)
                annuaire.append(dept)

                ### Ensuite, le nombre d'infos varie. Après avoir consulté la fiche de plusieurs collègues, je constate qu'il y a 7 autres informations possibles
                ### Pour chacune des infos qu'on attend, on va faire une boucle qui va la chercher dans chacun des <p> qu'on a déjà ramassés
                ### Si l'info est là, on l'ajoute à la liste «annuaire» et on arrête de chercher en faisant un «break», sinon on met du vide ("")

                for fac in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if fac.strong.text == "Faculté":
                        fac = fac.text.split(":")
                        fac = fac[1].strip()
                        break
                    else:
                        fac = ""
                annuaire.append(fac)
                for poste in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if poste.strong.text == "Poste":
                        poste = poste.text.split(":")
                        poste = poste[1].strip()
                        break
                    else:
                        poste = ""
                annuaire.append(poste)
                for courriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if courriel.strong.text == "Courriel":
                        courriel = courriel.text.split(":")
                        courriel = courriel[1].strip()
                        break
                    else:
                        courriel = ""
                annuaire.append(courriel)
                for autrecourriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if autrecourriel.strong.text == "Autre courriel":
                        autrecourriel = autrecourriel.text.split(":")
                        autrecourriel = autrecourriel[1].strip()
                        break
                    else:
                        autrecourriel = ""
                annuaire.append(autrecourriel)
                for tel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if tel.strong.text == "Téléphone":
                        tel = tel.text.split(":")
                        tel = tel[1].strip()
                        break
                    else:
                        tel = ""
                annuaire.append(tel)
                for autretel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if autretel.strong.text == "Autre téléphone":
                        autretel = autretel.text.split(":")
                        autretel = autretel[1].strip()
                        break
                    else:
                        autretel = ""
                annuaire.append(autretel)
                for local in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if local.strong.text == "Local":
                        local = local.text.split(":")
                        local = local[1].strip()
                        break
                    else:
                        local = ""
                annuaire.append(local)

                print(annuaire)

            else:
                colonnes = page3.find_all("div", class_="col-md-5")

                ### Pour la première colonne, je répète l'opération faite ci-haut
                infos = colonnes[0].find_all("p")
                # print(len(infos))

                ### Le premier de ces <p> contient le nom du département; on le ramasse
                dept = infos[0].text.strip()
                # print(dept)
                annuaire.append(dept)

                ### Ensuite, le nombre d'infos varie. Après avoir consulté la fiche de plusieurs collègues, je constate qu'il y a 7 autres informations possibles
                ### Pour chacune des infos qu'on attend, on va faire une boucle qui va la chercher dans chacun des <p> qu'on a déjà ramassés
                ### Si l'info est là, on l'ajoute à la liste «annuaire» et on arrête de chercher en faisant un «break», sinon on met du vide ("")

                for fac in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    # print(info)
                    if fac.strong.text == "Faculté":
                        fac = fac.text.split(":")
                        fac = fac[1].strip()
                        break
                    else:
                        fac = ""
                annuaire.append(fac)
                for poste in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if poste.strong.text == "Poste":
                        poste = poste.text.split(":")
                        poste = poste[1].strip()
                        break
                    else:
                        poste = ""
                annuaire.append(poste)
                for courriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if courriel.strong.text == "Courriel":
                        courriel = courriel.text.split(":")
                        courriel = courriel[1].strip()
                        break
                    else:
                        courriel = ""
                annuaire.append(courriel)
                for autrecourriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if autrecourriel.strong.text == "Autre courriel":
                        autrecourriel = autrecourriel.text.split(":")
                        autrecourriel = autrecourriel[1].strip()
                        break
                    else:
                        autrecourriel = ""
                annuaire.append(autrecourriel)
                for tel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if tel.strong.text == "Téléphone":
                        tel = tel.text.split(":")
                        tel = tel[1].strip()
                        break
                    else:
                        tel = ""
                annuaire.append(tel)
                for autretel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if autretel.strong.text == "Autre téléphone":
                        autretel = autretel.text.split(":")
                        autretel = autretel[1].strip()
                        break
                    else:
                        autretel = ""
                annuaire.append(autretel)
                for local in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
                    if local.strong.text == "Local":
                        local = local.text.split(":")
                        local = local[1].strip()
                        break
                    else:
                        local = ""
                annuaire.append(local)

                print(annuaire)

            mastodonte = open(dossier,"a")
            chef = csv.writer(mastodonte)
            chef.writerow(annuaire)