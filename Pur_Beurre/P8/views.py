""" imporation de render afin d'afficher le code HTML """
from django.shortcuts import render
from .forms import ConnexionForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

"""Couleur initial sans connexion"""
var_color = "text-primary"


""" Création de la vue pour les mentions légales """
def Legal_notice(request):
    return render(request, 'P8/Legal_Notice.html', {"var_color": var_color})

""" Création de la vue pour les resultats """
def results(request):
    return render(request, 'P8/results.html')

def accueil(request):
    return render(request, 'P8/home.html')

from django.contrib.auth import authenticate, login

def connexion(request):
    global var_color
    error = False
    print("vue connexion")
    if request.method == "POST":
        print("Méthode POST ok")
        form = ConnexionForm(request.POST or None)
        if form.is_valid():
            print("form valide !")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                var_color = "text-warning"
                print("Var color devient rouge")
            else: # sinon une erreur sera affichée
                print("Else !")
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'P8/connect.html', locals(), {"var_color": var_color})

def deconnexion(request):
    global var_color
    var_color = "text-success"
    logout(request)
    return render(request, 'P8/home.html', {"var_color": var_color})