### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

### Idée originale.
### Dans les faits, la majorité du moissonnage qui se fait sur le web
### Se fait sur des sites commerciaux, comme celui-ci.
### C'est un exercice intéressant pour apprendre le moissonnage.

### D'autant que les sites commerciaux implantent différents moyens pour rendre le moissonnage très difficile
### Ce site, notamment, change régulièremetn les URL pour afficher son contenu
### Ce qui fait que ce qui fonctionne à un moment donné, ne fonctionne plus après un certain temps
### J'ai passé plusieurs heures sur ce site et ce n'est pas impossible de le moissonner,
### Mais c'est un travail pour lequel je n'ai malheureusement pas de temps.
### Pour s'attaquer à un site commercial, il faut qu'il y ait un intérêt public

### J'ai laissé un des CSV qui a été produits au cours de l'une de mes tentatives

# coding: utf-8 

#Ce script vise à référencer les produits Zara. 

import csv 
import requests 
from bs4 import BeautifulSoup

# url = "http://www.zara.com/ca/fr/homme-c358523.html"

### Je vais plutôt démarrer de la page d'accueil:
url = "http://www.zara.com/ca/fr/"

fichier = "produitszara-JHR.csv"

entetes = {
	# "User-Agent":"Samuel Maurin Bonte",
	'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1',
	# "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36",
	'Cookie':'web_version=STANDARD; storepath=ca/fr; optimizelyEndUserId=oeu1490006067624r0.6780998269343408; WC_cookiesMsg=1; optimizelySegments=%7B%22188049923%22%3A%22false%22%2C%22188080683%22%3A%22direct%22%2C%22188117527%22%3A%22none%22%2C%22188127138%22%3A%22gc%22%2C%22236998896%22%3A%22true%22%7D; optimizelyBuckets=%7B%7D; socControl=http%3A%2F%2Fwww.zara.com; _ga=GA1.2.819801244.1490006068; RT="sl=0&ss=1490006065908&tt=0&obo=0&sh=&dm=zara.com&si=78d0fd15-3d5c-4336-9a3e-81e82279c614&bcn=%2F%2F6b148a64.mpstat.us%2F&ld=1490014550958&r=http%3A%2F%2Fwww.zara.com%2Fca%2Ffr%2F&ul=1490012806383"'
	# "From":"sammaurin21@gmail.com" #affiche un message d'erreur 
}

contenu1 = requests.get(url, headers=entetes, allow_redirects=False)
# print(contenu1.url)
# print(contenu1.status_code)
# print(contenu1.history)
# contenu1 = requests.get(url)
page = BeautifulSoup(contenu1.text, "html.parser")

### Ce bloc de code, qui sert à produire un fichier CSV contenant nos résultats, doit être placé plus bas
# f = open(fichier,"a")    
# final = csv.writer(f)
# final.writerow(["Nom produit","Prix","Url"])

# for ligne in page.find_all("a"):
	# print(ligne)
	# print(page.find("a")["href"])

# i = 0

### Premier étage, on va chercher les liens vers les grandes sections du site
for section in page.find("li", class_="_category-link-wrapper     ").find_all("a", class_="_category-link"):        # boucle 1 
	# print(section["href"])
	print(section.text)

### Bonne construction des hyperliens pour aller vers le "2e étage" du site
### Sauf que le début est plus court
	# debut = "http://www.zara.com/ca/fr/"
	# debut = "http:"
	debut = ""
	hyperlien = debut + section["href"]
	print(hyperlien)

### Dans chaque section, ensuite, on va chercher les infos sur les produits

	contenu2 = requests.get(hyperlien, headers=entetes)
	# contenu2 = requests.get(hyperlien)
	# print(contenu2.url)
	# print(contenu2.status_code)
	# print(contenu2.history)
	page2 = BeautifulSoup(contenu2.text, "html.parser")

	try:

		for produit in page2.find("ul", class_="product-list").find_all("li", class_="product"):
			# prodURL = "http:" + produit.a["href"]
			prodURL = produit.a["href"]
			print("   >>> " + prodURL)

			if produit.find("div", class_="product-info") in produit:
				if produit.find("a", class_="name _item").text != "":
					# prodNom = produit.find("a", class_="name _item").text
					# print(prodNom)

					# prodImage = produit.find("div", class_="_product-grid-xmedia").find("img")["src"]
					# prodImage = "http:" + prodImage
					prodURL = produit.find("a", class_="item _item")["href"]
					prodURL = "http:" + prodURL
					print(prodURL)

### Et ici, on descend au «3e étage» pour accéder aux informations relatives à chacun des produits
					contenu3 = requests.get(prodURL, headers=entetes)
					# contenu3 = requests.get(prodURL)
					page3 = BeautifulSoup(contenu3.text, "html.parser")

					prodNom = page3.find("h1", class_="product-name").text
					prodNom = prodNom[:-7].strip()
					print(prodNom)
					prodPrix = page3.find("div", class_="right-container").find("div", class_="price").span.text
					print(prodPrix)
					prodDesc = page3.find("div", id="description").find("p", class_="description").text.strip()
					prodImage = page3.find("div", id="plain-image").find("img", class_="image-big")["src"]
					prodImage = "http:" + prodImage

### C'est ici qu'on peut inscrire les infos qu'on vient de trouver dans notre fichier CSV
					zara = [section.text,prodNom,prodPrix,prodDesc,prodImage,prodURL]
					print(zara) ### Affichage pour vérifier

				achille = open(fichier,"a")
				talon = csv.writer(achille)
				talon.writerow(zara)

	except:
		print("Aucun produit dans cette section")

# e = 0


# Je n'ai pas réussi à aller chercher le deuxième étage d'urls, les produits, qui amènent aux données recherchées.

#for produit in page.find_all("a")[1:]: # boucle 2
	# print(section["href"])

