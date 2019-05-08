import requests as r
from bs4 import BeautifulSoup as b
import unicodedata
import re
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

    def get_json_categorie(self):
        # On récupère le code barre du produit
        print(self.link_product)
        CB_link = re.findall("([0-9]+)", self.link_product)
        CB_link = str(CB_link)
        print(CB_link)
        # On requête l'api du produit
        category = r.get('https://fr.openfoodfacts.org/api/v0/produit/{}.json'.format(CB_link))
        print(category)
        # On parcours le json pour récupérer le nom de la catégorie
        category_json = category.json()
        category_json = category_json['product']['categories_tags'][0]
        category_json = category_json[3:]
        print(category_json)


# On initialise l'instance de classe
Nutella = Scrapping_json("Nutella")
Nutella.get_product_url()
Nutella.get_json_categorie()
