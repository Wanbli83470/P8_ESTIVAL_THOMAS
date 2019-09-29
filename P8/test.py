from django.test import TestCase, Client
from django.urls import reverse
from P8.models import SUBSTITUT, Profil, CATEGORIES, PRODUIT
from django.contrib.auth.models import User
from Pur_Beurre.wsgi import *
from django.db.models import Q


class GetTestCase(TestCase):
    def setUp(self):
        """Setup for data products"""
        CATEGORIES.objects.create(NOM="testCat", LINK_OFF="www.testcat.com")
        self.cat_key = CATEGORIES.objects.get(NOM="testCat")
        PRODUIT.objects.create(NOM="testProduct", IMG_URL="www.urls.images", STORE="Store", NUTRISCORE=2, CATEGORIE_ID=self.cat_key)
        PRODUIT.objects.create(NOM="testProduct2", IMG_URL="www.urls.images", STORE="Store", NUTRISCORE=4, CATEGORIE_ID=self.cat_key)
        # SUBSTITUT.objects.create(PRODUIT_ID="" ,USER_FAVORITE="")

    def test_save_products(self):
        """We test the addition of the product"""
        products = PRODUIT.objects.get(NOM="testProduct")
        print(products.NUTRISCORE)
        self.assertEqual(products.NOM, "testProduct")

    def test_save_category(self):
        """We test the backup of a category in BDD"""
        category = CATEGORIES.objects.get(NOM="testCat")
        self.assertEqual(category.NOM, "testCat")

    def test_min_nutriscore(self):
        """We test the ORM query with filter"""
        ns_product = PRODUIT.objects.filter(NUTRISCORE__lt=4)
        ns_product = ns_product.get(CATEGORIE_ID=self.cat_key)
        print(ns_product.NUTRISCORE)
        self.assertIn(1, [1, 3])


class CodeHttp(TestCase):

    def setUp(self):
        self.c = Client()
    def test_page_200(self):
        """We test the obtaining of a 200 response on the home page"""
        response = self.c.get("/accueil")
        self.assertEqual(response.status_code, 200)

    def test_page_404(self):
        """We test the obtaining of a 404 response on the page error"""
        response = self.c.get("/adressess/")
        self.assertEqual(response.status_code, 404)
