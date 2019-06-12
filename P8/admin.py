from django.contrib import admin
from .models import PRODUIT, CATEGORIES, SUBSTITUT, Profil
# Register your models here.

admin.site.register(PRODUIT)

admin.site.register(CATEGORIES)

admin.site.register(SUBSTITUT)

admin.site.register(Profil)