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
        product = r.get('https://fr.openfoodfacts.org/api/v0/produit/{}.json'.format(CB_link))
        print(product)
        # On parcours le json pour récupérer le nom de la catégorie
        product_json = product.json()
        product_json = product_json['product']['categories_tags'][1]
        product_json = product_json[3:]
        print(product_json)
        # On configure l'url de la catégorie JSON
        category_json = "https://fr-en.openfoodfacts.org/category/{}/1.json".format(product_json)
        print(category_json)
        return category_json


class GetProductApi :


    def __init__(self, nb_product = 10, requête=""):
        self.nb_product = nb_product #Le nombre de produits
        self.requête = r.get(requête)

    def get(self):
        # Creation list for BDD
        url = []
        name = []
        ns = []
        link_pictures = []

        print("la requête retourne un code : {}".format(self.requête))
        json_category = self.requête.json()
        i = 0
        for data in json_category["products"]:

            # On récupère seulement les produits avec un nutriscore
            if data["nutrition_grades_tags"] != ['not-applicable']:
                try :
                    url.append((data["url"]))
                    name.append((data["product_name"]))
                    ns.append((data["nutrition_grades_tags"]))
                    if data["nutrition_grades_tags"] == ['not-applicable']:
                        print("nutriscore inexistant")
                    link_pictures.append((data["image_url"]))
                    i = i + 1
                    print(i)

                # On intercepte les produits sans images
                except KeyError:
                    print("un produit sans image; n°{}".format(i))
                    numéro = i
                    # On supprime à la volée les produits correspondants
                    del url[numéro]
                    del name[numéro]
                    del ns[numéro]
        print(url)
        print(name)
        print(ns)
        print(link_pictures)
        print("{} élément dans la liste".format(len(link_pictures)))


# On initialise l'instance de classe Scrapping_json
Nutella = Scrapping_json("Volvic")
Nutella.get_product_url()

liens = Nutella.get_json_categorie()

# On initialise l'instance de classe GetProductApi
substitut = GetProductApi(nb_product=10, requête=liens)
substitut.get()

