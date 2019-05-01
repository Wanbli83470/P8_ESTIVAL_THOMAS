from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=ChildProcessError)

    def __str__(self):
        return "Le profil de {0}".format(self.user.username)



class CATEGORIES(models.Model):
    NOM = models.CharField(max_length=80)
    LINK_OFF = models.CharField(max_length=80)

    def __str__(self):
        return "Catégorie : {}".format(self.NOM)

class PRODUIT(models.Model):
    NOM = models.CharField(max_length=200)
    PRODUIT_URL = models.CharField(max_length=200)
    STORE = models.CharField(max_length=50)
    NUTRISCORE = models.IntegerField()
    CATEGORIE_ID = models.ForeignKey(CATEGORIES, on_delete=models.CASCADE)

    def __str__(self):
        return "Produit : {}, nutriscore : {}".format(self.NOM, self.NUTRISCORE)

class SUBSTITUT(models.Model):
    NOM = models.CharField(max_length=200)
    STORE = models.CharField(max_length=50)
    SUBSTITUT_URL = models.CharField(max_length=200)
    DESCRIPTION = models.TextField()
    USER_FAVORITE = models.OneToOneField(User, on_delete=ChildProcessError)

    def __str__(self):
        return "Substitut : {}".format(self.NOM)