import requests as r
from bs4 import BeautifulSoup as b
# On choisit un produit
product = input("Enter le nom du produit : ")
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
        print(link_api)
        nb += 1


link_product