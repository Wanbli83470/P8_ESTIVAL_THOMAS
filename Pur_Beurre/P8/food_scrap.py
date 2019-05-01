import requests as r
from bs4 import BeautifulSoup as b
import unicodedata

class get_data :
    def __init__(self):
        pass

def get_category(choice_product) :
    # On choisit un produit
    product = choice_product
    # On paramètre la requête avec le produit pour obtenir le html correspondant
    requête = r.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(product))

    # On récupère le contenu du code html
    html = requête.content

    # On récupère proprement le contenu
    soup = b(html, 'html.parser')

    # On récupère la liste des produits
    list_products = soup.select(".products")[0]
    product_one = list_products.li

    # On récupère une url
    nb = 0

    link_product = str
    for link in list_products.find_all('a'):
        while nb < 1:
            link_product = link.get('href')
            # print(link_product)
            nb += 1


    link_product_complete = "https://fr.openfoodfacts.org{}".format(link_product)
    # print(link_product_complete)

    """Etape 2 : Récupérer le nom de la catégorie."""

    cat_requête = r.get(link_product_complete)
    cat_html = cat_requête.content
    cat_soup = b(cat_html, 'html.parser')

    link_cat = cat_soup.select(".tag.well_known")[2]
    link_cat = link_cat.text
    # print("lien catégorie : {}".format(link_cat))

    """Etape 3 : parcourir le json de la catégorie"""

    # Traitement de link_cat en vue de l'url

    # Suppresion des caracètre accentués
    link_cat = link_cat.lower()

    # remplacement des espaces par un tiret
    link_cat = link_cat.replace(" ", "-")

    # Suppresion des accents
    link_cat = unicodedata.normalize('NFKD', link_cat).encode('ascii', 'ignore')
    link_cat = link_cat.decode('utf-8')
    # print(link_cat)
    url_cat_json = "https://fr-en.openfoodfacts.org/category/{}.json".format(link_cat)
    # print(url_cat_json)
    return url_cat_json