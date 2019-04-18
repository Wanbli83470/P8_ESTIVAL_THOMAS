""" imporation de render afin d'afficher le code HTML """
from django.shortcuts import render
from .forms import ConnexionForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

var_color = "text-danger"
""" Création de la vue pour les mentions légales """
def Legal_notice(request):
    var_color = "text-danger"
    return render(request, 'P8/Legal_Notice.html', {"var_color": var_color})

""" Création de la vue pour les resultats """
def results(request):
    return render(request, 'P8/results.html')
# Create your views here.

from django.contrib.auth import authenticate, login

def connexion(request):
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
            else: # sinon une erreur sera affichée
                print("Else !")
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'P8/connect.html', locals())

def deconnexion(request):
    logout(request)
    return render(request, 'P8/home.html')