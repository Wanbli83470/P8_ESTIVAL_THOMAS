""" imporation de render afin d'afficher le code HTML """
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .forms import ConnexionForm, SearchForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
import time
from .parse import Parsing
from .food_scrap import ScrappingJson, GetProductApi, DetailScrapping
from .models import CATEGORIES, SUBSTITUT, PRODUIT

"""Color without connection"""
var_color = "Rooibos_chocolat"   # Defined the theme color


def base(request):
    """We use the render module of Django to display the html page and pass variables in parameter"""
    search_form = SearchForm()
    return render(request, 'P8/base.html', {"var_color": var_color, "search_form": search_form})


def Legal_notice(request):
    search_form = SearchForm()
    return render(request, 'P8/Legal_Notice.html', {"var_color": var_color, 'search_form': search_form})


def results(request, parse, name_categorie):
    search_form = SearchForm()
    parse = parse
    name_categorie = name_categorie
    # Recovery of already saved products to avoid duplication
    if str(request.user) != "AnonymousUser":  # Condition to ensure that a user is well connected
        print("User =", request.user)
        sub_id = SUBSTITUT.objects.filter(USER_FAVORITE=request.user).values_list('PRODUIT_ID', flat=True)
        sub_id = list(sub_id)  # list of products already saved
    else:
        sub_id = []

    cat_key = CATEGORIES.objects.get(NOM=name_categorie)  # Recovering category ID
    product = PRODUIT.objects.filter(Q(CATEGORIE_ID=cat_key) & Q(NUTRISCORE__lt=4))  # Obtaining products of a category with nutriscore less than 4

    return render(request, 'P8/results.html', {"var_color": var_color, 'parse': parse, 'product': product, "sub_id": sub_id, "search_form": search_form})


def accueil(request):
    search_form = SearchForm(request.POST)

    if search_form.is_valid():
        search = search_form.cleaned_data["Recherche"]

        # Parse function
        parse = Parsing(phrase=search, nb_letter=3)
        parse = parse.parser()
        print(parse)

        """" Obtention de la catégorie"""

        # We use ScrappingJson to get a product link
        products = ScrappingJson(parse)
        products.get_product_url()

        # We recover links of similar categories
        link_categorie = products.get_json_categorie()
        name_categorie = link_categorie[1]
        link_categorie = link_categorie[0]

        # We fill out temporary lists of products
        substitut = GetProductApi(max_pages=5, requête=link_categorie)
        substitut = substitut.get()
        substitut_url = substitut[0]
        substitut_name = substitut[1]
        substitut_nutriscore = substitut[2]
        substitut_pictures = substitut[3]

        # BDD registration of the category if nonexistent
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

        # Product database registration

        # 1 Counting the number of products
        nb_products = len(substitut_pictures)
        print("on propose : {} produits".format(nb_products))

        # 2 Foreign key recovery of the product
        key_cat = CATEGORIES.objects.get(NOM=name_categorie)

        # 3 Product insertion loop
        i = 0

        if test_cat == True:
            while i < nb_products:
                products = PRODUIT(NOM=substitut_name[i], PRODUIT_URL=substitut_url[i], STORE="Le store", NUTRISCORE=substitut_nutriscore[i], CATEGORIE_ID=key_cat, IMG_URL=substitut_pictures[i])
                products.save()
                i = i + 1
                print("i vaut : {}".format(i))

        # Redirect to the results page with the product name
        return HttpResponseRedirect(reverse('results', args=(parse, name_categorie)))

    else:
        search_form = SearchForm()
        print("On ne rentre pas dans le formulaire")

    return render(request, 'P8/home.html', {"var_color": var_color, 'search_form': search_form})


def details(request, id):
    search_form = SearchForm()

    food = PRODUIT.objects.get(id=id)  # Product ID recovery
    food_link = food.PRODUIT_URL  # Url recovery of the product

    link_ns = DetailScrapping(link=food_link)  # Initialization DetalScrapping class for additional information
    img_ns = link_ns.link_ns()  # Retrieving the image of the nutriscore

    value100g = link_ns.value_100g()
    titles = value100g[0]  # Subtitle recovery
    value100g = value100g[1]  # Recovery of nutritional values

    return render(request, 'P8/food_details.html', {"var_color": var_color, "food": food, 'search_form': search_form, "img_ns": img_ns, "value100g": value100g, "titles": titles})


def save(request, pk):
    """Using get_or_create to save only new items in the database"""
    food = PRODUIT.objects.get(pk=pk)
    test_save_product = SUBSTITUT.objects.get_or_create(PRODUIT_ID=food, USER_FAVORITE=request.user)
    print(test_save_product)
    return render(request, 'P8/home.html', {"var_color": var_color})


def register(request):
    search_form = SearchForm()

    form = UserCreationForm(request.POST)  # We post the registration form
    if form.is_valid():  # if correct data, the user is saved.
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
            user = authenticate(username=username, password=password)  # Verification of user input

            if user:
                login(request, user)
                var_color = "Biscuit_trempé"  # Changing the theme color
                print("Var color devient {}".format(var_color))
                return redirect('/accueil')
            else:
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'P8/connect.html', {'form': form, "var_color": var_color, 'error': error,})


def deconnexion(request):
    global var_color
    logout(request)  # Using the django logout
    var_color = "Rooibos_chocolat"  # Changing the theme color
    print("déconnexion : var_color devient {}".format(var_color))
    time.sleep(2)
    print("redirection vers page d'accueil")
    return redirect('/accueil')


def espace(request):
    search_form = SearchForm()
    return render(request, 'P8/espace.html', {"var_color": var_color, 'search_form': search_form})


def user_products(request):
    search_form = SearchForm()
    # Using request to view the logged in user
    print("utilisateur connecté : {}".format(request.user))
    # Establish a list of user's product ids
    sub_id = SUBSTITUT.objects.filter(USER_FAVORITE=request.user).values_list('PRODUIT_ID', flat=True)
    sub_id = list(sub_id)
    print(type(sub_id))
    # Recover all products with "Objects.all"
    product = PRODUIT.objects.all()
    return render(request, 'P8/user_products.html', {"var_color": var_color, 'sub_id': sub_id, 'product': product, 'search_form': search_form})

# Gestion des pages d'erreurs

# HTTP Error 400
def server_error(request):
    return render(request, 'P8/500.html', {"var_color": var_color})