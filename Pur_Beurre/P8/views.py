""" imporation de render afin d'afficher le code HTML """
from django.shortcuts import render, redirect
from .forms import ConnexionForm, SearchForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse

import time
from .parse import Parsing
from .food_scrap import get_category

"""Couleur initial sans connexion"""
var_color = "Rooibos_chocolat"

def base(request):
    return render(request, 'P8/base.html', {"var_color": var_color})
""" Création de la vue pour les mentions légales """
def Legal_notice(request):
    return render(request, 'P8/Legal_Notice.html', {"var_color": var_color})

""" Création de la vue pour les resultats """
def results(request, tag):
    food = tag
    return render(request, 'P8/results.html', {"var_color": var_color, 'food':food})

def accueil(request):
    search_form = SearchForm(request.POST)

    if search_form.is_valid():
        search = search_form.cleaned_data["Recherche"]
        parse = Parsing(phrase=search, nb_letter=3)
        parse = parse.parser()
        print(parse)
        link_categorie = get_category(parse)
        print(link_categorie)
        return HttpResponseRedirect(reverse('results', args=(parse,)))
    else :
        search_form = SearchForm()
        print("On ne rentre pas dans le formulaire")

    return render(request, 'P8/home.html', {"var_color": var_color, 'search_form' : search_form})



def register(request):

    form = UserCreationForm(request.POST)

    if form.is_valid():
        print("ok compte (:")
        form.save()
        username = form.cleaned_data['username']
        messages.success(request, f'Votre compte {username} est crée')
        return redirect('/accueil')

    else :
        form = UserCreationForm()
        print("Echec")

    return render(request, 'P8/register.html', {'form':form, "var_color": var_color})



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
                var_color = "Biscuit_trempé"
                print("Var color devient {}".format(var_color))
                print("redirection accueil")
                return redirect('/accueil')
            else: # sinon une erreur sera affichée
                print("Else !")
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'P8/connect.html', {'form':form, "var_color": var_color})

def deconnexion(request):
    global var_color
    logout(request)
    var_color = "Rooibos_chocolat"
    print("déconnexion : var_color devient {}".format(var_color))
    time.sleep(2)
    print("redirection vers page d'accueil")
    return redirect('/accueil')

