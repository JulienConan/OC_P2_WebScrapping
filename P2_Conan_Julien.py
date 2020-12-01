import requests
import urllib.request
import shutil
from bs4 import BeautifulSoup
import os 


url_main = "https://books.toscrape.com/"

liste_url_nb_page = []
liste_all_category_url = []

# Fonction permettant la récupération des urls des premères pages de chaque catégories de livre
def urlsCategoryandNbPageandName(url) :
	list_category_url = []
	response = requests.get(url) 								
	if response.ok :
		soup = BeautifulSoup(response.text, 'html.parser')							
		category = soup.find('div', {'class' :'side_categories'}).findAll('a')
		for i in category :
			url_cat = url + str(i['href'])
			list_category_url.append(url_cat)
	list_category_url.remove(list_category_url[0])

	for url_category in list_category_url :
		response = requests.get(url_category)						
		if response.ok :												
			soup = BeautifulSoup(response.text, 'html.parser')							
			try :
				page = str(soup.find('ul', {'class' : "pager"}).find('li', {'class' : 'current'}).text).rstrip("\n").rstrip(" ").rstrip("\n").rstrip(" ")
				page = int(page.split(" ")[-1])
			except :
				page = 1
			name_category = str(soup.find('h1').text)
		t = (url_category, page, name_category)
		liste_url_nb_page.append(t)
	return liste_url_nb_page

# Fonction permettant la récupération de toutes les urls d'une catgégorie
def allUrlsFromCatgeory(tuples) :
	list_page_category.append(tuples[0])
	if tuples[1] > 1 :
		for j in range(2,tuples[1]+1) :
			page_url = tuples[0].replace("index.html", "page-" + str(j) + ".html")
			list_page_category.append(page_url)
	return list_page_category

# Fonction permettant de récupérer les information voulues pour un livre
def book_scrapping(url) :
	book_element = {}
	response = requests.get(url) 														

	if response.ok :																	

		book_element = dict()															
		soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser") 							

		# Récupération de l'url de la page
		book_element['product_page_url'] = url

		# Récupération du titre du livre
		book_element['title'] = str(soup.title.text).replace(" | Books to Scrape - Sandbox", "").lstrip()
		
		data_list = soup.findAll('tr')
		for data in data_list :
			# Récupération du code UPC
			if data.find('th').text == 'UPC' :
				book_element['universal_product_code'] = data.find('td').text
			# Récupération du prix HT
			elif data.find('th').text == 'Price (excl. tax)' :
				book_element['price_including_tax'] = data.find('td').text.lstrip("Â£")
			# Récupération du prix TTC
			elif data.find('th').text == 'Price (incl. tax)' :
				book_element['price_excluding_tax'] = data.find('td').text.lstrip("Â£")
			# Récupération du stock disponible
			elif data.find('th').text == 'Availability' :
				available = ""
				for s in data.find('td').text :
					if s.isdigit() :
						available = available + s
				book_element['number_available'] = available

		# Récupération de la description du livre
		description = soup.find('div', {'id' : 'content_inner'}).findAll('p')
		book_element['product_description'] = str(description[3].text).replace(";", ",")

		# Récupération de la catégorie du livre
		category = soup.find('ul', {'class' : "breadcrumb"})
		for i in category :
			if str(i).find("/category/books/") > 0 :
				book_element['category'] = i.text.lstrip("\n").rstrip("\n")

		# Récupération du classement du livre
		article = soup.find('div', {'class' : "col-sm-6 product_main"}).findAll('p')
		for i in article :
			i = str(i)
			if i.find("star-rating") > 0 :
				i = i.split("\"")[1].lstrip("star-rating ")
				book_element['reviews_rating'] = i	

		# Récupération du l'url de l'image de la couverture du livre
		img_url = str(soup.find('div', { 'class' : 'item active'}).find("img"))
		img_url = url_main + img_url.split("\"")[3].lstrip('../')
		book_element['image_url'] = img_url
	return book_element

# Fonction permettant de récupérer toutes urls pour chaque livre de la page
def liste_book(url) :		
	liste_book_in_url = list()
	response = requests.get(url) 									

	if response.ok :
		soup = BeautifulSoup(response.text, 'html.parser')							
		category = soup.findAll('h3')
		for i in category :
			a= i.find('a')
			url_book =url_main + "catalogue/" + a['href'].lstrip('../')
			liste_book_in_url.append(url_book)
	return liste_book_in_url

def creationPathCategory(category) :
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
					'image_url']

		ligne_entetes = ";".join(entetes) + "\n"
		file.write(ligne_entetes)
	return file_cat, path_img

#def downloadBookImage(url, path) :


	
# Programme principale

list_url_category = urlsCategoryandNbPageandName(url_main)
print("Recherche des urls des catégories finie \n")


for i in list_url_category :
	list_page_category = []
	list_page_category = allUrlsFromCatgeory(i)
	print("Recherche de toutes les urls de la catégorie " + str(i[2]) + " finie\n")
	file_cat, path_img = creationPathCategory(str(i[2]))
	
	for j in list_page_category :
		list_url_book = liste_book(j)
		for k in list_url_book :
			with open(file_cat, 'a', encoding="utf-8") as file :
				infos = book_scrapping(k)
				print(infos)
				new_line = ";".join(infos.values()) + "\n"
				file.write(new_line)

			url_img = str(infos['image_url'])
			img_data = requests.get(url_img).content
			img_name = str(infos['title']).replace(" ", "_").replace(":", "").replace("/", "_").replace("\\", "").replace("\"","").replace("*", "_").replace("?", "_").replace(">", "_").replace("<", "_").replace("|", "_") + ".jpeg"
			if len(img_name) > 173 :
				img_name = img_name[:168] + ".jpeg"
			img_path = path_img + "/" + img_name
			urllib.request.urlretrieve(url_img, img_path)
