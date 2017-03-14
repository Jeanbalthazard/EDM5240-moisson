# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

url = "http://professeurs.uqam.ca/component/savrepertoireprofesseurs/professeurs?unite=DSPD0000&listLayouts=default"

dossier = "repertoire-uqam.csv"

entetes = {
    "User-Agent" : "Jean Balthazard - requête pour un cours journalistique", 
    "From" : "balthazardjean@gmail.com"
    }
    
contenu = requests.get(url,headers=entetes)

page = BeautifulSoup(contenu.text,"html.parser")

# Le début respecte les étapes vues en classe pour aller chercher l'information sur un site web. J'ai modifié le nom des variables, mais j'ai respecté la structure enseignée.

n = 0

for ligne in page.find_all("td", class_="nom_professeur"):
    lien = "http://professeurs.uqam.ca" + ligne.a["href"]

# En analysant le répertoire des enseignants en science politique de l'UQAM, j'ai remarqué une tendance. Tous les « td » possédant la « class » « nom professeur » comportaient les url de chaque fiche descriptive des professeurs.
# J'ai ajouté « http://professeurs.uqam.ca » au début de chaque lien pour être en mesure de bien diriger le script sur la bonne page. 
    
    contenu2 = requests.get(lien, headers=entetes)
    page2 = BeautifulSoup(contenu2.text,"html.parser")

# Par la suite, j'ai appliqué la même formule qui permet d'obtenir les informations « html » d'une site web. 

    annuaire = []

# J'ai créé une liste nommée « fiche » pour pouvoir y insérer tous les éléments nécessaires que je veux afficher dans mon csv. 
    
    annuaire.append(lien)

# Comme premier élément, j'insère les url que j'ai obtenus tantôt à titre de référence, si j'ai besoin de les utiliser plus tard. 
    
    for infos in page2:
        donnees = page2.find("div", class_="col-md-5")
        donnees2 = page2.find("div", class_="col-md-6")
        if donnees in page2:
            annuaire.append(donnees.text, donnees2.text)
        else:
            annuaire.append(donnees2.text)

print(annuaire)
            
# J'ai voulu, après, créer une boucle qui me permet d'obtenir les informations sur chaque professeur. J'ai remarqué que dans certaines fiches, le « div » « class = cool-md-5 » me permet d'obtenir toutes les infos. Par contre, dans quelques fiches, ce « div » n'est pas présent et les informations se retrouvent plutôt dans le « div » « class = cool-md-6 ». Dans tous les cas, le « div » « class = cool-md-6 » contient des informations utiles, ce pourquoi je l'inscris dans la première condition puisque c'est nécessaire d'avoir les deux « div » lorsqu'ils sont tous les deux présents. 
# Je rencontre toutefois toujours le même problème. Chaque fiche, donc toutes les informations reliées à un professeur, s'affiche en quadruple. Malgré plusieurs tentatives pour régler le problème, je n'ai pas été en mesure de le faire. 

mastodonte = open(dossier,"a")
chef = csv.writer(mastodonte)
chef.writerow(annuaire)
            
# Encore une fois, j'ai appliqué la formule vue en classe pour créer un csv. Le seul problème, c'est que dans le fichier csv que je crée, il y a seulement la première ligne qui s'affiche. 

# Je recontre deux problèmes majeures. Dans un premier temps, j'obtiens toutes les informations quatre fois plutôt qu'une. Je pourrais le nettoyer dans un fichier csv, par exemple à l'aide d'excel, mais j'aurais préféré simplifier le tout et n'avoir qu'une seule série d'informations pour chaque professeur. 
# Mon deuxième problème touche la création du csv. Je ne suis pas en mesure d'obtenir toutes les lignes de ma boucle et je n'obtiens que les informations du dernier professeur. 
# Malgré plusieurs tentatives, je n'ai pas été en mesure de solutionner ces deux problèmes. 
