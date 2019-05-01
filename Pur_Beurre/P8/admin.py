from django.contrib import admin
from .models import Person, PRODUIT, CATEGORIES, SUBSTITUT
# Register your models here.
admin.site.register(Person)

admin.site.register(PRODUIT)

admin.site.register(CATEGORIES)

admin.site.register(SUBSTITUT)