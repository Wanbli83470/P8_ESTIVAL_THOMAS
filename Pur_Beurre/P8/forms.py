from django import forms

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class SearchForm(forms.Form):
    Recherche = forms.CharField(label="Recherche", max_length=50, help_text='Saisissez simplement un nom de produit svp.')

    def clean_search(self):
        print("on test la saisie du formulaire")
        data = self.cleaned_data['Recherche']
        print(data)
        if "pizza" in data:
            raise forms.ValidationError("On ne veut pas entendre parler de pizza !")
        else :
            print("champs valide")
        return data  # Ne pas oublier de renvoyer le contenu du champ traité