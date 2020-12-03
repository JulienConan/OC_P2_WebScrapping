import requests
import shutil
from bs4 import BeautifulSoup
import os 
import re


URL_MAIN = "https://books.toscrape.com/"


def createSoupObject(url) :
	"""Fonction pour créer l'objet soup permettant le scrapping"""
	response = requests.get(url) 								
	if response.ok :
		soup = BeautifulSoup(response.content, 'html.parser')
	return soup

def urlsCategoryandNbPageandName(url) :
	"""Fonction récupérant les urls des premères pages de chaque catégories de livre"""
	list_category_url = []
	liste_url_nb_page_name = []
	soup = createSoupObject(url)			
	category = soup.find('div', {'class' :'side_categories'}).findAll('a')

	for i in category :
		url_cat = url + str(i['href'])
		list_category_url.append(url_cat)
	list_category_url.remove(list_category_url[0])
	
	for url_category in list_category_url :
		cat_infos = nbpageName(url_category)
		liste_url_nb_page_name.append(cat_infos)

	return liste_url_nb_page_name

def nbpageName(url) :
	"""Fonction récupérant les nombres de pages et le nom de chaque catégorie"""
	soup = createSoupObject(url)
	try :
		page = soup.find('li', {'class' : 'current'}).text.strip()
		page = int(page.split(" ")[-1])
	except :
		page = 1
	name_category = str(soup.find('h1').text)
	liste = (url, page, name_category)
	return liste

def allUrlsFromCatgeory(tuples) :
	"""Fonction permettant la récupération de toutes les urls d'une catégorie"""
	list_page_category.append(tuples[0])
	if tuples[1] > 1 :
		for j in range(2,tuples[1]+1) :
			page_url = tuples[0].replace("index.html", "page-" + str(j) + ".html")
			list_page_category.append(page_url)
	return list_page_category

def bookScrapping(url) :
	"""Fonction permettant de récupérer les information voulues pour un livre"""
	book_element = {}
	soup = createSoupObject(url)

	book_element['product_page_url'] = url
	book_element['universal_product_code'] = soup.find('td').text
	book_element['title'] = title = soup.find('li', { 'class' : 'active'}).text
	book_element['price_including_tax'] = soup.findAll('tr')[3].find('td').text
	book_element['price_excluding_tax'] = soup.findAll('tr')[2].find('td').text
	available = soup.findAll('tr')[5].find('td').text
	book_element['number_available'] = "".join(re.findall("[0-9]", available))
	book_element['product_description'] = soup.findAll('meta')[2]['content'].replace(";",",").strip()
	book_element['category'] = soup.findAll('li')[2].text.strip().replace(" ", "_")
	book_element['reviews_rating'] = soup.find('div', {'class' : "col-sm-6 product_main"}).findAll('p')[2]['class'][1]
	img_url = soup.img['src']
	book_element['image_url'] = URL_MAIN + img_url.strip("../")
	book_element['image_files'] = book_element['title'].replace(" ", "_").replace(":", "").replace("/", "_").replace("\\", "").replace("\"","").replace("*", "_").replace("?", "_").replace(">", "_").replace("<", "_").replace("|", "_") + ".jpeg"
	return book_element

def liste_book(url) :		
	"""Fonction permettant de récupérer toutes urls pour chaque livre de la page"""
	liste_book_in_url = list()
	soup =createSoupObject(url)							
	category = soup.findAll('h3')
	for i in category :
		a= i.find('a')
		url_book =URL_MAIN + "catalogue/" + a['href'].lstrip('../')
		liste_book_in_url.append(url_book)
	return liste_book_in_url

def creationPathCategory(category) :
	"""Fonction de création d'un dossier contenant le fichier .csv avec les entêtes,
	ainsi qu'un dossier images qui contiendra les images des livres"""
	category = category.replace(" ", "_")
	path_img = category + "/images"
	if os.path.exists(category) :
		shutil.rmtree(category)

	os.mkdir(category)
	os.mkdir(path_img)
	file_cat = category + "/" + category + ".csv"
	with open(file_cat, 'w') as file :
		entetes = ['product_page_url',
					'universal_product_code',
					'title',
					'price_including_tax',
					'price_excluding_tax',
					'number_available',
					'product_description',
					'category',
					'reviews_rating',
					'image_url',
					'image_name']

		ligne_entetes = ";".join(entetes) + "\n"
		file.write(ligne_entetes)
	return file_cat, path_img

def imgDownload(infos) :
	""" Fonction de téléchargement de l'image """
	requete = requests.get(infos['image_url'])
	path_file = infos['category'] + "/images/" + infos['image_files']
	if len(path_file) > 179:
				path_file = path_file[:178]
	if requete.ok :
		with open(path_file, 'wb') as f:
			f.write(requete.content)

#///////////////// Programme principale/////////////////////

list_url_category = urlsCategoryandNbPageandName(URL_MAIN)

for i in list_url_category :
	list_page_category = []
	list_page_category = allUrlsFromCatgeory(i)
	file_cat, path_img = creationPathCategory(str(i[2]))
	
	for j in list_page_category :
		list_url_book = liste_book(j)
		datas = ""
		for k in list_url_book :
			infos = bookScrapping(k)
			datas += ";".join(infos.values()) + "\n" 
			imgDownload(infos)

		with open(file_cat, 'a', encoding="utf-8") as file :
			file.write(datas)	