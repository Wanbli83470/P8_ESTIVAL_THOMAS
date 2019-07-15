import requests as r
from bs4 import BeautifulSoup as b
import unicodedata
import re
import json


class ScrappingJson:
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
        # get the product barcode
        print(self.link_product)
        CB_link = re.findall("([0-9]+)", self.link_product)
        CB_link = str(CB_link)
        print(CB_link)
        # On requête l'api du produit
        product = r.get('https://fr.openfoodfacts.org/api/v0/produit/{}.json'.format(CB_link))
        print(product)
        # We run the json to get the name of the category
        product_json = product.json()
        product_json = product_json['product']['categories_tags'][1]
        product_json = product_json[3:]
        print(product_json)
        # Configuring the url category in json
        category_json = "https://fr-en.openfoodfacts.org/category/{}/1.json".format(product_json)
        print(category_json)
        return category_json, product_json


class GetProductApi:
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

            # Filter produced with nutriscore

            if data["nutrition_grades_tags"] != ['not-applicable'] and data["nutrition_grades_tags"] != ['unknown'] :
                try :
                    url.append((data["url"]))

                    name.append((data["product_name"]))
                    ns.append((data["nutrition_grades_tags"][0]))
                    link_pictures.append((data["image_url"]))
                    i = i + 1


                #
                # Deleting products without images

                except KeyError:
                    print("un produit sans image; n°{}".format(i))
                    numéro = i

                    del url[numéro]
                    del name[numéro]
                    del ns[numéro]

        print(url)
        print(name)
        print(link_pictures)
        print(ns)

        # Convert number to letters
        for n, i in enumerate(ns):
            if i == 'a':
                ns[n] = 1

            elif i == 'b':
                ns[n] = 2

            elif i == 'c':
                ns[n] = 3

            elif i == 'd':

                ns[n] = 4
            elif i == 'e':
                ns[n] = 5

        print(ns)
        print("{} élément dans la liste".format(len(link_pictures)))
        return url, name, ns, link_pictures


class DetailScrapping:
    def __init__(self, link, soup=str):
        self.link = link
        requête = r.get(self.link)
        html = requête.content
        soup = b(html, 'html.parser')
        self.soup = soup

    def link_ns(self):
        img_ns = []
        for link in self.soup.findAll('img', attrs={'src': re.compile("^https://static.openfoodfacts.org/images/misc/nutriscore")}):
            img_ns = link.get('src')
            print(img_ns)

        return img_ns

    def value_100g(self):
        title = []
        value = []
        nb = 0

        for l in self.soup.findAll(id="nutrition_data_table"):

            for t in l.findAll("td", class_="nutriment_label"):

                title.append(t.text)
                nb = len(title)


            print(" \npassage aux valeurs \n")

            for v in l.findAll("td", class_="nutriment_value"):
                print(v)

                value.append(v.text[0])
                value = value[0:nb]

        print(title)
        print(value)
        return title
