from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    genre = models.CharField(max_length=5, default="Homme")
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
    IMG_URL = models.CharField(max_length=100)
    STORE = models.CharField(max_length=50)
    NUTRISCORE = models.IntegerField()
    CATEGORIE_ID = models.ForeignKey(CATEGORIES, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class SUBSTITUT(models.Model):
    PRODUIT_ID = models.ForeignKey(PRODUIT, on_delete=models.CASCADE)
    USER_FAVORITE = models.ForeignKey(User, on_delete=ChildProcessError)

    def __str__(self):
        return "enregistré par : {}".format(self.USER_FAVORITE)