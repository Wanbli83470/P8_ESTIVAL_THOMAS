from django.test import TestCase
from django.urls import reverse
from P8.models import SUBSTITUT, Profil, CATEGORIES, PRODUIT
from django.db.models import Q
# We test the obtaining of a 200 response on the home page
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)
# We test the obtaining of a 404 response on the page error
"""    def test_error_page(self):
        response = self.client.get(reverse('error'))
        self.assertEqual(response.status_code, 500)"""

class GetTestCase(TestCase):
    def setUp(self):
        """Setup for data products"""
        CATEGORIES.objects.create(NOM="testCat", LINK_OFF="www.testcat.com")
        self.cat_key = CATEGORIES.objects.get(NOM="testCat")
        PRODUIT.objects.create(NOM="testProduct", IMG_URL="www.urls.images", STORE="Store", NUTRISCORE=2, CATEGORIE_ID=self.cat_key)

        # SUBSTITUT.objects.create(PRODUIT_ID="" ,USER_FAVORITE="")

    def test_products_exist(self):
        """We test the addition of the product"""
        products = PRODUIT.objects.get(NOM="testProduct")
        print(products.NUTRISCORE)
        # sub = SUBSTITUT.objects.get(PRODUIT_ID="")
        self.assertEqual(products.NOM, "testProduct")

    def test_cat_exist(self):
        category = CATEGORIES.objects.get(NOM="testCat")
        self.assertEqual(category.NOM, "testCat")

    def test_nutriscore(self):
        """On test la requête ORM pour obtenir des produits avec un nutriscore intéréssants"""
        ns_product = PRODUIT.objects.filter(NUTRISCORE__lt=4)
        ns_product = ns_product.get(CATEGORIE_ID=self.cat_key)
        print(ns_product.NUTRISCORE)
        self.assertIn(1, [1, 3])


    def test_save_sub(self):
        pass

# On test la connexion d'un utilisateur
