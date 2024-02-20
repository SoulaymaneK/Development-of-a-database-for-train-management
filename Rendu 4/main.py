"""
On a repartit en 3 l'usage de la couche applicative.
- On a tout d'abord des ADMIN qui s'occupent de créer chaque instance de la base de donnée (exceptée des voyageurs qui s'inscrivent eux-même) et
ont la possibilité de supprimer toutes données.
- On a ensuite créer des GESTIONNAIRE qui eux s'occupent de relier les différentes instances entres-elles. Par exemple relier des taxis avec des gares etc..
Ils n'ont aucun droit de suppression. Ils peuvent seulement relier des données ou modifier certaines données.
- Et on a ensuite créer des CLIENT qui peuvent créer, supprimer un compte, reserver, annuler, modifier des billets. Ils peuvent également consulter
quelques statistiques sur les différentes lignes, trajets, etc.. Et peuvent aussi rechercher des trajets, horaires de trains etc..

De plus, on a modifié la base de donnée en ajoutant des utilisateures de l'application. En effet, on a donc créer une table utilisateur permettant d'identifier
les utilisateurs avec leur login et leur mot de passe. On a donc ensuite créer en python des fonctions pour se creer un compte ou pour se login si on a déjà un compte.

Liste des login et mot de passe pour se connecter à l'application python : 

Pour l'admin (nom_utilisateur, mot_de_passe) : ('admin', 'admin123')

Pour le gestionnaire (nom_utilisateur, mot_de_passe) : ('gestionnaire', 'gestionnaire123') 

Pour les clients (nom_utilisateur, mot_de_passe) : ('client1', 'client123') 

"""
from admin import *
from gestionnaire import *
from client import *


def login():
    while True:
        username = input("Veuillez entrer votre nom d'utilisateur : ")
        password = input("Veuillez entrer votre mot de passe : ")
        cur.execute(f"SELECT * FROM Utilisateur WHERE nom_utilisateur='{username}' AND mot_de_passe='{password}'")
        user = cur.fetchone()
        if user is None:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")
        else:
            print("Connexion réussie !")
            role = user[3]
            if role == 'admin':
                admin()
            elif role == 'gestionnaire':
                gestionnaire()
            elif role == 'client':
                client(user)
            break


def creer_compte():
    print("Entrez les informations du nouveau utilisateur : ")
    while True:
        username = input("Nom d'utilisateur : ")
        sql = f"""SELECT * FROM Utilisateur WHERE nom_utilisateur='{username}';"""
        cur.execute(sql)
        user = cur.fetchone()
        if not user:
            password = input("Mot de passe : ")
            role = input("Choisissez votre rôle ('admin', 'gestionnaire', 'client') : ")
            liste_role = ['admin', 'gestionnaire', 'client']
            while not role in liste_role:
                role = input("Veuillez enter correctement votre rôle ('admin', 'gestionnaire', 'client') : ")
            sql1 = f"""INSERT INTO Utilisateur(nom_utilisateur,mot_de_passe,role) VALUES ('{username}','{password}','{role}') RETURNING id;"""
            cur.execute(sql1)
            user_id = cur.fetchone()[0]
            conn.commit()
            if role == 'client':
                ajouter_voyageur(user_id)
            break
        else:
            print("Ce nom d'utilisatuer est déjà pris.")


def admin():
    liste_choix = [f'{i}' for i in range(1, 27)]
    choix = ''
    while choix.lower() != 'q':
        menu_admin()
        choix = input("Votre choix : ")
        while not choix in liste_choix and choix.lower() != 'q':
            print("Veuillez entrez correctement votre choix, ", end=' ')
            choix = input("votre choix : ")
        if choix == '1':
            ajouter_gare()
        elif choix == '2':
            ajouter_taxi()
        elif choix == '3':
            ajouter_hotel()
        elif choix == '4':
            ajouter_tp()
        elif choix == '5':
            ajouter_ligne()
        elif choix == '6':
            ajouter_type_train()
        elif choix == '7':
            ajouter_train()
        elif choix == '8':
            ajouter_date_exception()
        elif choix == '9':
            ajouter_voyage()
        elif choix == '10':
            ajouter_desserte()
        elif choix == '11':
            supprimer_gare()
        elif choix == '12':
            supprimer_ligne()
        elif choix == '13':
            supprimer_type_train()
        elif choix == '14':
            supprimer_train()
        elif choix == '15':
            supprimer_voyage()
        elif choix == '16':
            supprimer_voyageur_admin()
        elif choix == '17':
            supprimer_billet()
        elif choix == '18':
            supprimer_desserte()
        elif choix == '19':
            supprimer_trajet()
        elif choix == '20':
            afficher_liste_gare()
        elif choix == '21':
            afficher_liste_ligne()
        elif choix == '22':
            afficher_liste_train()
        elif choix == '23':
            afficher_liste_voyage()
        elif choix == '24':
            afficher_liste_voyageur()
        elif choix == '25':
            afficher_liste_billets()
        elif choix == '26':
            afficher_liste_desserte()
        else:
            print("Vous avez quitté l'espace ADMIN !\n")


def gestionnaire():
    liste_choix = [f'{i}' for i in range(1, 11)]
    choix = ''
    while choix.lower() != 'q':
        menu_gestionnaire()
        choix = input("Votre choix : ")
        while not choix in liste_choix and choix.lower() != 'q':
            print("Veuillez entrez correctement votre choix, ", end=' ')
            choix = input("votre choix : ")
        if choix == '1':
            hotel_gare()
        elif choix == '2':
            tp_gare()
        elif choix == '3':
            taxi_gare()
        elif choix == '4':
            jour_voyage()
        elif choix == '5':
            exception_voyage()
        elif choix == '6':
            modifier_voyage()
        elif choix == '7':
            modifier_type_voyageur_gestionnaire()
        elif choix == '8':
            modifier_billet_assurance_gestionnaire()
        elif choix == '9':
            modifier_desserte()
        elif choix == '10':
            modifier_place_trajet()
        else:
            print("Vous avez quitté l'espace GESTIONNAIRE !\n")


def client(user):
    cur.execute("SELECT * FROM Voyageur WHERE utilisateur = %s", (user[0],))
    voyageur = cur.fetchone()

    print("\nBonjour, " + voyageur[2] + " " + voyageur[1] + " !")

    liste_choix = [f'{i}' for i in range(1, 13)]
    choix = ''
    while choix.lower() != 'q':
        menu_client()
        choix = input("Votre choix : ")
        while not choix in liste_choix and choix.lower() != 'q':
            print("Veuillez entrez correctement votre choix, ", end=' ')
            choix = input("votre choix : ")
        if choix == '1':
            consult_voyage()
        elif choix == '2':
            recherche_trajet()
        elif choix == '3':
            consult_trajet_voyageur(voyageur)
        elif choix == '4':
            nbvoyageur_ligne()
        elif choix == '5':
            nbvoyageur_train()
        elif choix == '6':
            affchier_info_voyageur(voyageur)
        elif choix == '7':
            modifier_type_voyageur_client(voyageur)
        elif choix == '8':
            reserver_billet(voyageur)
        elif choix == '9':
            annuler_billet(voyageur)
        elif choix == '10':
            modifier_date_trajet(voyageur)
        elif choix == '11':
            modifier_billet_assurance_client(voyageur)
        elif choix == '12':
            supprimer_voyageur(user)
            break
        else:
            print("Vous avez quitté l'espace CLIENT !\n")


def menu_utilisateur():
    while True:
        print("Bonjour, bienvenue à l'application !")
        print("\033[32m==========Login==========")
        print("1.Je me connecte")
        print("2.Créer un compte\033[0m")
        liste_choix = ["1", "2"]

        choix = input("Votre choix : (q pour quitter) : ")
        while not choix in liste_choix and choix.lower() != 'q':
            print("Veuillez entrez correctement votre choix, ", end=' ')
            choix = input("votre choix (q pour quitter) : ")
        if choix == '1':
            login()
        elif choix == '2':
            creer_compte()
        else:
            print("Au revoir !\n")
            break


menu_utilisateur()
