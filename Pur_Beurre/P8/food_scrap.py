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

list_products = soup.select(".products")[0]
product_one = list_products.li
# print(product_one)
link_product_one = product_one.a
print(link_product_one)
# print("test = {}".format(test))

