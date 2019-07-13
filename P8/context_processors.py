from .models import CATEGORIES, SUBSTITUT, PRODUIT

def ma_var(a):
    ma_var = "Une chaine avec le context-processor"
    return {'ma_var': ma_var}

def nb_products(request):
    if str(request.user) != "AnonymousUser":
        sub_id = SUBSTITUT.objects.filter(USER_FAVORITE=request.user).values_list('PRODUIT_ID', flat=True)
        sub_id = list(sub_id)
        print(type(sub_id))
        nb_products = len(sub_id)

    else:
        nb_products = 0

    return {'nb_products': nb_products}



