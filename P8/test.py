from django.test import TestCase
from django.urls import reverse
from P8.models import SUBSTITUT, Profil, CATEGORIES, PRODUIT

# On test l'obtention d'une réponse 200 sur la page d'accueil
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)




class GetTestCase(TestCase):
    def setUp(self):
        """Setup for data products"""
        CATEGORIES.objects.create(NOM = "testCat", LINK_OFF = "www.testcat.com")
        cat_key = CATEGORIES.objects.get(NOM = "testCat")
        PRODUIT.objects.create(NOM = "testProduct", IMG_URL = "www.urls.images", STORE = "Store", NUTRISCORE = 2, CATEGORIE_ID =cat_key)

        SUBSTITUT.objects.create()

# On test l'ajout d'un produit
    def test_products_exist(self):
        products = PRODUIT.objects.get(NOM="testProduct")

# On test la connexion d'un utilisateur

# On test d'obtenir des produits avec un nutriscore inférieur à 4

# On test qu'une catégorie est ajoutée lors d'une requête

# On test la création d'un utilisateur

# On test l'ajout d'un produit substitut


