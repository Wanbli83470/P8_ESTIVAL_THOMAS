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