# coding: utf-8

### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

### Idée originale! Qui pourrait être appliquée à l'ensemble des profs de l'UQAM :)
### Je pense que je vais tenter la chose dans un 2e script (correction-JHR-2.py)
### Ton script fonctionne bien jusqu'à la ligne 45 environ
### Voir mes commentaires ci-dessous pour la solution que je te propose

import csv
import requests
from bs4 import BeautifulSoup

url = "http://professeurs.uqam.ca/component/savrepertoireprofesseurs/professeurs?unite=DSPD0000&listLayouts=default"

dossier = "repertoire-ScPo-JHR.csv"

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
    print(lien) ### J'ai ajouté ce print pour suivre le travail du script au fur et à mesure qu'il moissonne des pages

# En analysant le répertoire des enseignants en science politique de l'UQAM, j'ai remarqué une tendance. Tous les « td » possédant la « class » « nom professeur » comportaient les url de chaque fiche descriptive des professeurs.
# J'ai ajouté « http://professeurs.uqam.ca » au début de chaque lien pour être en mesure de bien diriger le script sur la bonne page. 
    
    contenu2 = requests.get(lien, headers=entetes)
    page2 = BeautifulSoup(contenu2.text,"html.parser")

# Par la suite, j'ai appliqué la même formule qui permet d'obtenir les informations « html » d'une site web. 

    annuaire = []

# J'ai créé une liste nommée « fiche » pour pouvoir y insérer tous les éléments nécessaires que je veux afficher dans mon csv. 
    
    annuaire.append(lien) ### Excellent, car certains URLs contiennent le nom du, de la, prof; d'autres un code ésotérique

# Comme premier élément, j'insère les url que j'ai obtenus tantôt à titre de référence, si j'ai besoin de les utiliser plus tard. 
    
    ### Ci-dessous, tu fais une boucle dans quelque chose qui ne permet pas de faire une boucle.
    ### Je vais mettre tout ce bloc de code en commentaires

    # for infos in page2:
    #     donnees = page2.find("div", class_="col-md-5")
    #     print(donnees)
    #     donnees2 = page2.find("div", class_="col-md-6")
    #     if donnees in page2:
    #         annuaire.append(donnees.text, donnees2.text)
    #     else:
    #         annuaire.append(donnees2.text)

    ### Voici plutôt comment je m'y prendrais:

    ### D'abord, on prend le nom du, de la prof, ce qui est assez simple

    nom = page2.find("div", id="fiche").h1.text.strip()
    print(nom)
    annuaire.append(nom)

    ### Ensuite, je vais faire le choix de ne ramasser que les infos qui se trouvent en haut de la fiche
    ### À savoir, les infos de base, tout ce qui se trouve en haut des onglets
    ### Je constate qu'il y a deux cas possibles

    ### Premier cas, les fiches «simples» où il y a peu de détails; on y trouve toujours un <div> de classe "col-md-6"

    if page2.find("div", class_="col-md-6") in page2.find("div", id="fiche").find("div", class_="row"):
        
        ### Les infos qui nous intéressent sont incluses dans des balises <p>; on les met toutes dans une variable que je vais appeler «infos»
        infos = page2.find("div", class_="col-md-6").find_all("p")
        print(len(infos))

        ### Le premier de ces <p> contient le nom du département; on le ramasse
        dept = infos[0].text.strip()
        print(dept)
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
            # print(info)
            if poste.strong.text == "Poste":
                poste = poste.text.split(":")
                poste = poste[1].strip()
                break
            else:
                poste = ""
        annuaire.append(poste)
        for courriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if courriel.strong.text == "Courriel":
                courriel = courriel.text.split(":")
                courriel = courriel[1].strip()
                break
            else:
                courriel = ""
        annuaire.append(courriel)
        for autrecourriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if autrecourriel.strong.text == "Autre courriel":
                autrecourriel = autrecourriel.text.split(":")
                autrecourriel = autrecourriel[1].strip()
                break
            else:
                autrecourriel = ""
        annuaire.append(autrecourriel)
        for tel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if tel.strong.text == "Téléphone":
                tel = tel.text.split(":")
                tel = tel[1].strip()
                break
            else:
                tel = ""
        annuaire.append(tel)
        for autretel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if autretel.strong.text == "Autre téléphone":
                autretel = autretel.text.split(":")
                autretel = autretel[1].strip()
                break
            else:
                autretel = ""
        annuaire.append(autretel)
        for local in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if local.strong.text == "Local":
                local = local.text.split(":")
                local = local[1].strip()
                break
            else:
                local = ""
        annuaire.append(local)

        print(annuaire)
    
    ### 2e cas: les fiches plus complètes
    ### Elles contiennent deux <div> de classe «col-md-5»; on va les chercher toutes les deux

    else:
        colonnes = page2.find_all("div", class_="col-md-5")

        ### Pour la première colonne, je répète l'opération faite ci-haut
        infos = colonnes[0].find_all("p")
        print(len(infos))

        ### Le premier de ces <p> contient ici encore le nom du département; on le ramasse
        dept = infos[0].text.strip()
        print(dept)
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
            # print(info)
            if poste.strong.text == "Poste":
                poste = poste.text.split(":")
                poste = poste[1].strip()
                break
            else:
                poste = ""
        annuaire.append(poste)
        for courriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if courriel.strong.text == "Courriel":
                courriel = courriel.text.split(":")
                courriel = courriel[1].strip()
                break
            else:
                courriel = ""
        annuaire.append(courriel)
        for autrecourriel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if autrecourriel.strong.text == "Autre courriel":
                autrecourriel = autrecourriel.text.split(":")
                autrecourriel = autrecourriel[1].strip()
                break
            else:
                autrecourriel = ""
        annuaire.append(autrecourriel)
        for tel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if tel.strong.text == "Téléphone":
                tel = tel.text.split(":")
                tel = tel[1].strip()
                break
            else:
                tel = ""
        annuaire.append(tel)
        for autretel in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if autretel.strong.text == "Autre téléphone":
                autretel = autretel.text.split(":")
                autretel = autretel[1].strip()
                break
            else:
                autretel = ""
        annuaire.append(autretel)
        for local in infos[1:]: ### On exclut l'élément [0] d'infos, puisqu'on l'a déjà moissonné
            # print(info)
            if local.strong.text == "Local":
                local = local.text.split(":")
                local = local[1].strip()
                break
            else:
                local = ""
        annuaire.append(local)

        print(annuaire)

# J'ai voulu, après, créer une boucle qui me permet d'obtenir les informations sur chaque professeur. J'ai remarqué que dans certaines fiches, le « div » « class = cool-md-5 » me permet d'obtenir toutes les infos. Par contre, dans quelques fiches, ce « div » n'est pas présent et les informations se retrouvent plutôt dans le « div » « class = cool-md-6 ». Dans tous les cas, le « div » « class = cool-md-6 » contient des informations utiles, ce pourquoi je l'inscris dans la première condition puisque c'est nécessaire d'avoir les deux « div » lorsqu'ils sont tous les deux présents. 
# Je rencontre toutefois toujours le même problème. Chaque fiche, donc toutes les informations reliées à un professeur, s'affiche en quadruple. Malgré plusieurs tentatives pour régler le problème, je n'ai pas été en mesure de le faire. 

### Ici, le problème est simplement dû à l'indentation.
### Il fallait juste indenter le tout d'un coup à droite

    mastodonte = open(dossier,"a")
    chef = csv.writer(mastodonte)
    chef.writerow(annuaire)
            
# Encore une fois, j'ai appliqué la formule vue en classe pour créer un csv. Le seul problème, c'est que dans le fichier csv que je crée, il y a seulement la première ligne qui s'affiche. 

# Je recontre deux problèmes majeures. Dans un premier temps, j'obtiens toutes les informations quatre fois plutôt qu'une. Je pourrais le nettoyer dans un fichier csv, par exemple à l'aide d'excel, mais j'aurais préféré simplifier le tout et n'avoir qu'une seule série d'informations pour chaque professeur. 
# Mon deuxième problème touche la création du csv. Je ne suis pas en mesure d'obtenir toutes les lignes de ma boucle et je n'obtiens que les informations du dernier professeur. 
# Malgré plusieurs tentatives, je n'ai pas été en mesure de solutionner ces deux problèmes. 
