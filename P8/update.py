import psycopg2
from food_scrap import GetProductApi
from mail_ import Mailing
import smtplib
import ssl
import datetime
HOST = "localhost"
USER = "wanbli"
PASSWORD = "jpmfmaemp73%"
DATABASE = "pur_beurre"

DATE_NOW = datetime.datetime.now()
DICT_DATE = {1:"Janvier", 2:"Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}

try:
    # Connect to an existing database
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cursor = conn.cursorsor()
    print(conn)
    print(">>> Connexion réussi")
    #Select substitut_id
    cursor.execute('SELECT "PRODUIT_ID_id", "id" FROM "P8_substitut"')
    substitut_id = set(dict((cursor.fetchall())))
    print(substitut_id)
    #SELECT MAX PRODUCTS
    nb_products_save = ('SELECT MAX("id") FROM "P8_produit"')
    cursor.execute(nb_products_save)
    nb_products_save = cursor.fetchone()[0]
    #Delete products dont save
    for i in range(1, nb_products_save+1):
        if i not in substitut_id:
            pysql = 'DELETE FROM "P8_produit" WHERE "id"=%s' % i
            cursor.execute(pysql, ())
            conn.commit()
        else:
            pass

    #Get url category
    cursor.execute('SELECT "NOM", "id" FROM "P8_categories"')
    url_category = dict(cursor.fetchall())
    print(url_category)
    conn.commit()
    MAX_ID = max(substitut_id)

    print("MAX_ID VAUT : " + str(MAX_ID))
    pysql = 'ALTER SEQUENCE "P8_produit_id_seq" RESTART WITH %s' % str(MAX_ID+1)
    cursor.execute(pysql, ())
    conn.commit()

    i = 0

    #Update with download new products
    for key, value in url_category.items():
        substitut = GetProductApi(max_pages=2, requête=key)
        substitut = substitut.get()
        substitut_url, substitut_name, substitut_nutriscore, substitut_pictures = substitut[0], substitut[1], substitut[2], substitut[3]
        substitut_len = len(substitut_name)
        while i < substitut_len:
            print("Insertion de : " + str(i))
            print("i vaut : {}".format(i))
            pysql = 'INSERT INTO "P8_produit" ("NOM", "PRODUIT_URL", "STORE", "NUTRISCORE", "CATEGORIE_ID_id", "IMG_URL") VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(pysql, (substitut_name[i], substitut_url[i], "Store", substitut_nutriscore[i], value, substitut_pictures[i]))
            i += 1

        print(key, value)
        print(i)
        conn.commit()
        i = 0
        # Close connection
    conn.close()
    print(conn)

    with open('/home/thomas/Bureau/rapport_update_P10.txt', 'a') as f:
        f.write(f"\nBase de données actualisée le : {DATE_NOW.day} {DICT_DATE[DATE_NOW.month]} {DATE_NOW.year}.")
    Mailing(true_false=1).test_mail()
except:
    with open('/home/thomas/Bureau/rapport_update_P10.txt', 'a') as f:
        f.write(f"\nEchec d'actualisation de la BDD le : {DATE_NOW.day} {DICT_DATE[DATE_NOW.month]} {DATE_NOW.year}.")
    Mailing(true_false=0).test_mail()
