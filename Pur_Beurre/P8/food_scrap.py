import requests as r
from bs4 import BeautifulSoup as b
import unicodedata
import json


class Scrapping_json :
    def __init__(self, product):
        self.product = product

    def get_product_url(self, link_product=""):
        self.link_product = link_product
        requête = r.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(self.product))
        html = requête.content
        soup = b(html, 'html.parser')
        list_products = soup.select(".products")[0]
        product_one = list_products.li

        # On récupère une url
        nb = 0

        for link in list_products.find_all('a'):
            while nb < 1:
                self.link_product = link.get('href')
                # print(link_product)
                nb += 1

        return self.link_product


    def get_categorie_url(self, link_cat = ""):
        self.link_cat = link_cat

        print("on rentre dans get_categorie_url")

        link_product_complete = "https://fr.openfoodfacts.org{}".format(self.link_product)
        print(link_product_complete)
        cat_requête = r.get(link_product_complete)
        cat_html = cat_requête.content
        cat_soup = b(cat_html, 'html.parser')
        self.link_cat = cat_soup.select(".tag.well_known")[2]
        self.link_cat = self.link_cat.text

        print("lien catégorie : {}".format(self.link_cat))
        return self.link_cat


    def get_json_categorie(self, link_cat = ""):
        self.link_cat = link_cat
        print("\nOn rentre dans get_json_categorie \n")
        # Traitement de link_cat en vue de l'url

        # Suppresion des caracètre accentués
        self.link_cat = self.link_cat.lower()
        # remplacement des espaces par un tiret
        self.link_cat = self.link_cat.replace(" ", "-")

        # Suppresion des accents
        self.link_cat = unicodedata.normalize('NFKD', self.link_cat).encode('ascii', 'ignore')
        self.link_cat = self.link_cat.decode('utf-8')

        url_cat_json = "https://fr-en.openfoodfacts.org/category/{}.json".format(self.link_cat)

        return url_cat_json



# # On initialise l'instance de classe
# Nutella = Scrapping_json("Nutella")
#
# Nutella.get_product_url()
#
# MA_CATÉGORIE = Nutella.get_categorie_url()
#
# JSON = Nutella.get_json_categorie(link_cat=MA_CATÉGORIE)
# print(JSON)

category = r.get('https://fr.openfoodfacts.org/api/v0/produit/3564700007341.json')
print(category)

category_json = category.json()
category_json = category_json['product']['categories_tags'][0]
category_json = category_json[3:]
print(category_json)