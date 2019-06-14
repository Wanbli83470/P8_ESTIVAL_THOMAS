from django.test import TestCase
from django.urls import reverse

# On test l'obtention d'une réponse 200 sur la page d'accueil
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)

# On test la connexion d'un utilisateur

# On test d'obtenir un produit avec nutriscore inférieur à 4

# On test qu'une catégorie est ajoutée lors d'une requête

