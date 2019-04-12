""" imporation de render afin d'afficher le code HTML """
from django.shortcuts import render

""" Création de la vue pour les mentions légales """
def Legal_notice(request):
    return render(request, 'P8/Legal_Notice.html')

""" Création de la vue pour les mentions légales """

# Create your views here.
