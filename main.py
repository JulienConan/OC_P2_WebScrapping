import requests
import shutil
from bs4 import BeautifulSoup
import os
import re


URL_MAIN = "https://books.toscrape.com/"


def create_soup(url: str):
    """Création de l'objet soup permettant le scrapping"""
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
    return soup


def urls_categories(url: str):
    """Récupération des urls des premères pages de chaque catégorie de livre"""
    list_urls_categories = []
    soup = create_soup(url)
    categories = soup.find("div", {"class": "side_categories"}).findAll("a")
    for category in categories:
        url_category = url + str(category["href"])
        list_urls_categories.append(url_category)
    list_urls_categories.remove(list_urls_categories[0])
    return list_urls_categories


def book_scrapping(url: str):
    """Récupération des informations voulues pour un livre"""
    book_element = {}
    soup = create_soup(url)
    trs = soup.findAll("tr")
    book_element["product_page_url"] = url
    book_element["universal_product_code"] = soup.find("td").text
    book_element["title"] = soup.find("li", {"class": "active"}).text
    book_element["price_including_tax"] = trs[3].find("td").text
    book_element["price_excluding_tax"] = trs[2].find("td").text
    available = trs[5].find("td").text
    book_element["number_available"] = "".join(re.findall("[0-9]", available))
    book_element["product_description"] = (
        soup.findAll("meta")[2]["content"].replace(";", ",").strip()
    )
    book_element["category"] = soup.findAll("li")[2].text.strip().replace(" ", "_")
    book_element["reviews_rating"] = soup.find("p", {"class": "star-rating"})["class"][
        1
    ]
    img_url = soup.img["src"]
    book_element["image_url"] = URL_MAIN + img_url.strip("../")
    book_element["image_files"] = (
        book_element["title"]
        .replace(" ", "_")
        .replace(":", "")
        .replace("/", "_")
        .replace("\\", "")
        .replace('"', "")
        .replace("*", "_")
        .replace("?", "_")
        .replace(">", "_")
        .replace("<", "_")
        .replace("|", "_")
        + ".jpeg"
    )
    return book_element


def list_books(url: str):
    """Fonction permettant de récupérer toutes urls pour chaque livre de la page"""
    list_books_in_url = list()
    soup = create_soup(url)
    category = soup.findAll("h3")
    for i in category:
        a = i.find("a")
        url_book = URL_MAIN + "catalogue/" + a["href"].lstrip("../")
        list_books_in_url.append(url_book)

    next_page = soup.find("li", {"class": "next"})
    if next_page != None:
        list_books_in_url += list_books(
            url.rsplit("/", 1)[0] + "/" + next_page.find("a")["href"]
        )
    return list_books_in_url


def create_path_category(category: str):
    """Création d'un dossier dans lequel se situera
    le fichier .csv avec les entêtes, ainsi qu'un
    dossier images qui contiendra les images des livres"""
    path_img = category + "/images"
    if os.path.exists(category):
        shutil.rmtree(category)
    os.mkdir(category)
    os.mkdir(path_img)
    file_cat = category + "/" + category + ".csv"
    with open(file_cat, "w") as file:
        entetes = [
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "reviews_rating",
            "image_url",
            "image_name",
        ]
        ligne_entetes = ";".join(entetes) + "\n"
        file.write(ligne_entetes)
    return file_cat, path_img


def img_download(infos: dict, category_folder: str):
    """ Fonction de téléchargement de l'image """
    requete = requests.get(infos["image_url"])
    path_file = category_folder + "/images/" + infos["image_files"]
    if len(path_file) > 179:
        path_file = path_file[:178]
    if requete.ok:
        with open(path_file, "wb") as f:
            f.write(requete.content)


# ///////////////// Programme principale/////////////////////

list_categories_urls = urls_categories(URL_MAIN)

for category in list_categories_urls:
    category_name = re.sub(r"[0-9_]", "", category.split("/")[-2])
    file_cat, path_img = create_path_category(category_name)
    list_books_urls = list_books(category)
    datas = ""
    for book_url in list_books_urls:
        infos = book_scrapping(book_url)
        datas += ";".join(infos.values()) + "\n"
        img_download(infos, category_name)

    with open(file_cat, "a", encoding="utf-8") as file:
        file.write(datas)
