""" imporation de render afin d'afficher le code HTML """
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConnexionForm, SearchForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
import time
from .parse import Parsing
from .food_scrap import ScrappingJson, GetProductApi, DetailScrapping
from .models import CATEGORIES, SUBSTITUT, PRODUIT

"""Color without connection"""
var_color = "Rooibos_chocolat"


def base(request):
    return render(request, 'P8/base.html', {"var_color": var_color})


def Legal_notice(request):
    search_form = SearchForm()
    return render(request, 'P8/Legal_Notice.html', {"var_color": var_color, 'search_form': search_form})


def results(request, parse, name_categorie):
    parse = parse
    name_categorie = name_categorie
    #On récupère l'identifiant des produits déjà sauvegardés
    if str(request.user) != "AnonymousUser":
        print("User =", request.user)
        sub_id = SUBSTITUT.objects.filter(USER_FAVORITE=request.user).values_list('PRODUIT_ID', flat=True)
        sub_id = list(sub_id)
    else:
        sub_id = []

    cat_key = CATEGORIES.objects.get(NOM=name_categorie)
    product = PRODUIT.objects.filter(Q(CATEGORIE_ID=cat_key) & Q(NUTRISCORE__lt=4))

    return render(request, 'P8/results.html', {"var_color": var_color, 'parse': parse, 'product': product, "sub_id": sub_id})


def accueil(request):
    search_form = SearchForm(request.POST)

    if search_form.is_valid():
        search = search_form.cleaned_data["Recherche"]

        # Fonction de parse
        parse = Parsing(phrase=search, nb_letter=3)
        parse = parse.parser()
        print(parse)


        """" Obtention de la catégorie"""

        # On initialise l'instance de classe Scrapping_json
        products = ScrappingJson(parse)

        # On récupère le liens du produit
        products.get_product_url()

        # On récupère le liens de la catégorie json avec l'api
        link_categorie = products.get_json_categorie()
        name_categorie = link_categorie[1]
        link_categorie = link_categorie[0]

        # On initialise l'instance de classe GetProductApi
        substitut = GetProductApi(nb_product=10, requête=link_categorie)
        substitut = substitut.get()
        substitut_url = substitut[0]
        substitut_name = substitut[1]
        substitut_nutriscore = substitut[2]
        substitut_pictures = substitut[3]

        # Enregistrement en BDD de la catégorie si inexistante
        cat = CATEGORIES.objects.get_or_create(NOM=name_categorie, LINK_OFF=link_categorie)
        test_cat = False

        if True in cat:
            print("Catégorie Crée")
            test_cat = True
            print(test_cat)
        else:
            print("Catégorie Existante")
            test_cat = False
            print(test_cat)

        # Enregistrement en BDD des produits

        # 1 on compte le nombre de produits
        nb_products = len(substitut_pictures)
        print("on propose : {} produits".format(nb_products))

        # 2 On Récupère la clef étrangère de catégorie
        key_cat = CATEGORIES.objects.get(NOM=name_categorie)

        # 3 On boucle pour insérer les produits dans la BDD
        i = 0

        if test_cat == True:
            while i < nb_products:
                products = PRODUIT(NOM=substitut_name[i], PRODUIT_URL=substitut_url[i], STORE="Le store", NUTRISCORE=substitut_nutriscore[i], CATEGORIE_ID=key_cat, IMG_URL=substitut_pictures[i])
                products.save()
                i = i + 1
                print("i vaut : {}".format(i))


        # Redirection vers la page results avec le nom du produit
        return HttpResponseRedirect(reverse('results', args=(parse, name_categorie)))
    else:
        search_form = SearchForm()
        print("On ne rentre pas dans le formulaire")

    return render(request, 'P8/home.html', {"var_color": var_color, 'search_form': search_form})


def details(request, id):
    search_form = SearchForm()
    food = PRODUIT.objects.get(id=id)
    food_link = food.PRODUIT_URL
    link_ns = DetailScrapping(link=food_link)
    img_ns = link_ns.link_ns()
    value100g = link_ns.value_100g()
    titles = value100g[0]
    value100g = value100g[1]
    print(value100g)
    return render(request, 'P8/food_details.html', {"var_color": var_color, "food": food, 'search_form': search_form, "img_ns": img_ns, "value100g": value100g, "titles": titles})

def save(request, pk):
    food = PRODUIT.objects.get(pk=pk)
    test_save_product = SUBSTITUT.objects.get_or_create(PRODUIT_ID=food, USER_FAVORITE=request.user)
    print(test_save_product)
    return render(request, 'P8/home.html', {"var_color": var_color})

def register(request):
    search_form = SearchForm()
    form = UserCreationForm(request.POST)

    if form.is_valid():
        print("ok compte (:")
        form.save()
        username = form.cleaned_data['username']
        messages.success(request, f'Votre compte {username} est crée')
        return redirect('/accueil')

    else:
        form = UserCreationForm()
        print("Echec")

    return render(request, 'P8/register.html', {'form': form, "var_color": var_color, 'search_form': search_form})


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

    return render(request, 'P8/connect.html', {'form': form, "var_color": var_color})


def deconnexion(request):
    global var_color
    logout(request)
    var_color = "Rooibos_chocolat"
    print("déconnexion : var_color devient {}".format(var_color))
    time.sleep(2)
    print("redirection vers page d'accueil")
    return redirect('/accueil')


def espace(request):
    search_form = SearchForm()
    return render(request, 'P8/espace.html', {"var_color": var_color, 'search_form': search_form})


def user_products(request):
    search_form = SearchForm()
    # On utilise request pour voir l'utilisateur connecté
    print("utilisateur connecté : {}".format(request.user))
    # On recueil les identifiants de substituts de cet utilisateur
    sub_id = SUBSTITUT.objects.filter(USER_FAVORITE=request.user).values_list('PRODUIT_ID', flat=True)
    sub_id = list(sub_id)
    print(type(sub_id))
    # On récupère tous les produits
    product = PRODUIT.objects.all()
    return render(request, 'P8/user_products.html', {"var_color": var_color, 'sub_id': sub_id, 'product': product, 'search_form': search_form})
