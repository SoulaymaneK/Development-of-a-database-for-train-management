import psycopg2
from random import randint
from affichage import *

conn = psycopg2.connect("dbname='dbnf18p100' user='nf18p100' password='Kq9HTunusG5r' host='tuxa.sme.utc'")
# conn = psycopg2.connect("dbname='dbnf18p086' user='nf18p086' password='W847Stt3KWkl' host='tuxa.sme.utc'")
cur = conn.cursor()


def menu_client():
    print(
        "\n\033[34mVous êtes dans l'espace CLIENT. Choisissez le numéro de l'action que vous voulez effectuer (q pour quitter): ")
    print("==========CONSULTER DES DONNEES==========")
    print("1.Consulter les différents voyages entre deux gares")
    print("2.Chercher un trajet")
    print("3.Consulter vos trajets")
    print("4.Consulter le nombre de voyageur sur une ligne")
    print("5.Consulter le nombre de voyageur dans un train")
    print("=====================================")
    print("========ESPACE CLIENT=======")
    print("6.Afficher vos informations")
    print("7.Modifier votre statut")
    print("8.Réserver un billet")
    print("9.Annuler une réservation")
    print("10.Modifier la date d'une reservation")
    print("11.Modifier l'assurance d'un billet")
    print("12.Supprimer votre compte")
    print("=====================================\033[0m\n")


def consult_voyage():
    if afficher_liste_gare():
        gared = input("Entrez la gare de depart : ")
        garea = input("Entrez la gare d'arrivée : ")
        sql1 = f"""SELECT v.id as Voyage, g1.nom as Gare_depart, d1.heure_depart, g2.nom as Gare_arrivee, d2.heure_arrive, STRING_AGG(CAST(jv.jour AS VARCHAR), ', ') as Jours
            FROM Voyage v
            JOIN Dessert d1 ON v.id = d1.voyage
            JOIN Gare g1 ON d1.gare = g1.id
            JOIN Dessert d2 ON v.id = d2.voyage
            JOIN Gare g2 ON d2.gare = g2.id
            JOIN Jour_Voyage jv ON v.id = jv.voyage
            WHERE g1.nom = '{gared}'
            AND g2.nom = '{garea}'
            AND d1.heure_depart < d2.heure_arrive
            GROUP BY v.id, g1.nom, d1.heure_depart, g2.nom, d2.heure_arrive
            ORDER BY voyage,d1.heure_depart;
            """
        cur.execute(sql1)
        liste_voyage = cur.fetchall()
        if not liste_voyage:
            print(f"Il n'y a pas de voyage prévu entre {gared} et {garea}")
        else:
            for voyage in liste_voyage:
                print(
                    f"Voyage prévu le {voyage[5]} au débpart de {voyage[1]} à {voyage[2]} et à l'arrivé de {voyage[3]} à {voyage[4]}")


def recherche_trajet():
    villed = input("Entrez une ville de départ : ")
    villea = input(("Entrez une ville d'arrive : "))
    prixmin = float(input("Entrez un prix min : "))
    prixmax = float(input("Entrez un prix max : "))
    sql = f"""
        SELECT t.id,t.date,g1.nom as gare_depart,t.heure_depart,g2.nom as gare_arrive,t.heure_arrive,b.prix
        FROM Trajet t
        INNER JOIN Gare g1 ON t.gare_depart=g1.id
        INNER JOIN Gare g2 ON t.gare_arrive=g2.id
        INNER JOIN Billet b ON t.billet=b.id
        WHERE g1.ville = '{villed}' AND g2.ville = '{villea}' AND b.prix>={prixmin} AND b.prix<={prixmax} AND t.date>=CURRENT_DATE
        ORDER BY t.date;
        """
    cur.execute(sql)
    liste_trajet = cur.fetchall()
    if liste_trajet:
        print()
        for trajet in liste_trajet:
            print(
                f"Trajet {trajet[0]} prévu le {trajet[1]}. {trajet[2]} à {trajet[3]} - {trajet[4]} à {trajet[5]}. {trajet[6]}€")
    else:
        print("\nIl n'existe pas de trajet, essayer de changer les filtres de la recherche.")


def consult_trajet_voyageur(voyageur):
    sql2 = f"""SELECT b.id as billet, t.date, g1.nom as Gare_depart,t.heure_depart, g2.nom as Gare_arrivee, t.heure_arrive, d.duree,
        CASE WHEN b.assurance = TRUE THEN 'Oui' ELSE 'Non' END AS assurance
        FROM Billet b
        INNER JOIN Trajet t ON b.id = t.id
        INNER JOIN duree_trajet d ON d.id = t.id
        JOIN Gare g1 ON t.gare_depart = g1.id
        JOIN Gare g2 ON t.gare_arrive = g2.id
        WHERE b.voyageur = {voyageur[0]}
        ORDER BY t.date;
        """
    cur.execute(sql2)
    liste_trajet = cur.fetchall()
    if not liste_trajet:
        print(f"le voyageur {voyageur[1]} {voyageur[2]} n'est enregistré qar aucun trajet !")
    else:
        for trajet in liste_trajet:
            print(
                f"Trajet prévu le {trajet[1]} au départ de {trajet[2]} à {trajet[3]} et à l'arrivée de {trajet[4]} à {trajet[5]} pour une durée totale de {trajet[6]}.")


def nbvoyageur_ligne():
    liste_ligne = afficher_liste_ligne()
    if liste_ligne:
        id_ligne = int(input("\nEntrez le numéro de la ligne pour consulter son nombre de voyageur : "))
        sql1 = f"""
            SELECT l.id as id_ligne, COUNT(*) as nombre_voyageurs
            FROM Billet b
            INNER JOIN Trajet t ON b.id = t.billet
            INNER JOIN Voyage v ON t.voyage = v.id
            INNER JOIN Ligne l ON v.ligne = l.id
            WHERE l.id = {id_ligne}
            GROUP BY l.id
            ORDER BY nombre_voyageurs DESC;
            """
        cur.execute(sql1)
        nb_voyageur = cur.fetchone()
        for ligne in liste_ligne:
            if ligne[0] == nb_voyageur[0]:
                print(f"\nLa ligne {ligne[0]}, {ligne[1]} - {ligne[2]} comporte {nb_voyageur[1]} voyageur(s).")
    else:
        print("Il n'existe pas encore de ligne.")


def nbvoyageur_train():
    if afficher_liste_train():
        num_train = int(input("Entrez le numéro du train dont vous voulez consulter son nombre de voyageur : "))
        sql = f"""
            SELECT t.train, COUNT(*) as nombre_voyageurs, nbr_places_max - COUNT(*) as nb_places_restantes
            FROM Billet b
            INNER JOIN Trajet t ON b.id = t.billet
            INNER JOIN Train on t.train = train.num
            INNER JOIN TypeTrain type ON Train.type = type.id
            WHERE Train.num = {num_train}
            GROUP BY t.train, nbr_places_max
            ORDER BY nombre_voyageurs DESC;
            """
        cur.execute(sql)
        train = cur.fetchone()
        if train:
            print(f"Le Train n°{train[0]} comporte {train[1]} voyageur(s). Il reste encore {train[2]} places disponibles.")
        else:
            print("Le train n'existe pas !")


def ajouter_voyageur(user_id):
    # les voyageurs sont occasionenels par defaut lors de leur inscription
    print("Entres les informations du nouveau voyageur : ")
    nom = input("Nom : ")
    prenom = input("Prenom : ")
    adresse = input("Adresse : ")
    telephone = input("Telephone : ")
    sql = f"""SELECT * FROM Voyageur WHERE nom='{nom}' AND prenom='{prenom}' AND adresse='{adresse}' AND telephone='{telephone}';"""
    cur.execute(sql)
    voyageur = cur.fetchone()
    if not voyageur:
        sql1 = f"""INSERT INTO Voyageur(nom,prenom,adresse,telephone,type,num_carte,statut,utilisateur) VALUES ('{nom}','{prenom}','{adresse}','{telephone}','Occasionnel',NULL,NULL,'{user_id}') RETURNING id;"""
        cur.execute(sql1)
        voyageur = cur.fetchone()[0]
        print(voyageur)
        conn.commit()
        print("Votre compte a bien été créer.\n")
    else:
        print("Ces données sont déjà associées à un compte.")


def affchier_info_voyageur(voyageur):
    print("Votre information de voyageur :")
    print("Nom : " + voyageur[1])
    print("Prénom : " + voyageur[2])
    print("Adresse : " + voyageur[3])
    print("Téléphone : " + voyageur[4])
    print("Type de voyageur : " + voyageur[5])
    if voyageur[6]:
        print("Numéro de carte : " + str(voyageur[6]))
        print("Statut : " + voyageur[7])


def modifier_type_voyageur_client(voyageur):
    liste_type = ['Occasionnel', 'Regulier']
    liste_statut = ['bronze', 'silver', 'gold', 'platine']
    print(f"Type actuel du voyageur : {voyageur[5]}. Vous avez le choix entre Occasionnel et Regulier")
    newtype = input("Nouveau type : ")
    while not newtype in liste_type:
        newtype = input("Nouveau type : ")
    if newtype == 'Occasionnel':
        sql1 = f"""UPDATE Voyageur SET type='{newtype}',num_carte=NULL,statut=NULL WHERE id={voyageur[0]};"""
        cur.execute(sql1)
        conn.commit()
        print("La modification a bien été prise en compte.\n")
    elif newtype == 'Regulier':
        num_carte = input("Entrez son numéro de carte : ")
        statut = input("Entrez son statut ('bronze', 'silver', 'gold', 'platine') : ")
        while not statut in liste_statut:
            statut = input("Entrez son statut ('bronze', 'silver', 'gold', 'platine') : ")
        sql2 = f"""UPDATE Voyageur SET type='{newtype}',num_carte={num_carte},statut='{statut}' WHERE id={voyageur[0]};"""
        cur.execute(sql2)
        conn.commit()
        print("La modification a bien été prise en compte.\n")


def reserver_billet(voyageur):
    print("Choisissez un voyage : ")
    if afficher_liste_voyage():
        voyage = int(input("Numéro du voyage : "))
        sql1 = f"""SELECT * FROM Voyage WHERE id={voyage};"""
        cur.execute(sql1)
        check_voyage = cur.fetchone()
        if check_voyage:
            print("Chosissez une desserte du voyage : ")
            sql2 = f"""SELECT DISTINCT v.id as voyage, g1.nom as Gare_depart, d1.heure_depart, g2.nom as Gare_arrivee, d2.heure_arrive, v.type_train,g1.id,g2.id, STRING_AGG(CAST(jv.jour AS VARCHAR), ', ') as Jours
                FROM Voyage v
                JOIN Dessert d1 ON v.id = d1.voyage
                JOIN Gare g1 ON d1.gare = g1.id
                JOIN Dessert d2 ON v.id = d2.voyage
                JOIN Gare g2 ON d2.gare = g2.id
                JOIN Jour_Voyage jv ON v.id = jv.voyage
                WHERE v.id=1
                AND d1.heure_depart < d2.heure_arrive
                GROUP BY v.id, g1.nom, d1.heure_depart, g2.nom, d2.heure_arrive,g1.id,g2.id
                ORDER BY voyage,d1.heure_depart;"""
            cur.execute(sql2)
            liste_desserte = cur.fetchall()
            if liste_desserte:
                i = 1
                for d in liste_desserte:
                    print(f"{i}. {d[1]} {d[2]} - {d[3]} {d[4]}")
                    i += 1
                dessert = int(input("Numéro de la desserte : "))
                date = input(
                    "Entrez la date de votre voyage (AAAA/MM/JJ) : ")  # francehment je calcule pas si la date tombe pil poil avec les jours du voyages
                if 0 < dessert <= i:
                    dessert = liste_desserte[dessert - 1]
                    if voyageur:
                        prix = randint(0, 250)  # on s'en fou
                        moyen_paiement = input("Moyen paiement ('carte bleue', 'espece', 'cheque') : ")
                        assurance = input("Assurance (oui/non) : ")
                        if assurance.lower() == 'oui':
                            assurance = True
                        else:
                            assurance = False
                        try:
                            sql4 = f"""INSERT INTO Billet(prix,moyen_paiement,assurance,voyageur) VALUES ({prix},'{moyen_paiement}',{assurance},{voyageur[0]})"""
                            cur.execute(sql4)
                            conn.commit()
                        except Exception as e:
                            print("Erreur lors de la création du billet :", e)
                            conn.rollback()

                        place = int(input("Choisissez un numéro de place : "))
                        sql5 = f"""SELECT num FROM Train WHERE type={dessert[5]};"""
                        cur.execute(sql5)
                        train = cur.fetchone()
                        if train:
                            sql6 = f"""SELECT id FROM Billet WHERE prix={prix} AND moyen_paiement = '{moyen_paiement}' AND assurance = {assurance} AND voyageur={voyageur[0]}"""
                            cur.execute(sql6)
                            billet = cur.fetchone()
                            try:
                                sql7 = f"""INSERT INTO Trajet(voyage,date,billet,num_place,gare_depart,heure_depart,gare_arrive,heure_arrive,train) VALUES\
                                          ({dessert[0]},'{date}',{billet[0]},{place},{dessert[6]},'{dessert[2]}',{dessert[7]},'{dessert[4]}',{train[0]})"""
                                cur.execute(sql7)
                                conn.commit()
                                print("Le trajet a bien été créer.\n")
                            except Exception as e:
                                print("Erreur lors de la création du trajet :", e)
                                conn.rollback()
                        else:
                            print("Il n'existe pas de train.\n")
                    else:
                        print("Le voyageur n'existe pas. Commencez par vous créer un compte.\n")
                else:
                    print("Cette desserte n'existe pas.\n")
            else:
                print("Il n'existe aucune desserte pour ce voyage.\n")
        else:
            print("Ce voyage n'existe pas.\n")

def annuler_billet(voyageur):
    if voyageur:
        print("Choisissez la réservation à annulé : ")
        sql = f"""SELECT b.*,g1.nom,t.heure_depart,g2.nom,t.heure_arrive,t.date,t.num_place FROM Billet b\
             INNER JOIN Trajet t ON t.billet= b.id\
             INNER JOIN Gare g1 ON t.gare_depart =g1.id \
             INNER JOIN Gare g2 ON t.gare_arrive = g2.id \
             WHERE b.voyageur={voyageur[0]} AND t.date>=CURRENT_DATE ;"""
        cur.execute(sql)
        liste_billet = cur.fetchall()
        if liste_billet:
            for billet in liste_billet:
                print(
                    f"{billet[0]}. {billet[5]} {billet[6]} - {billet[7]} {billet[8]} le {billet[9]}. siège n° {billet[10]}, {billet[1]} €")
            billet = int(input("Numéro du billet : "))
            sql1 = f"""SELECT * FROM Billet WHERE id={billet};"""
            cur.execute(sql1)
            check_billet = cur.fetchone()
            if check_billet:
                sql2 = f"""DELETE FROM Billet WHERE id={billet};"""
                cur.execute(sql2)
                conn.commit()
                print("Votres réservation a bien été annulée.\n")
            else:
                print("Le billet n'existe pas !\n")
        else:
            print("Vous n'avez pas de reservation en cours!\n")
    else:
        print("Ce voyageur ne possede pas de compte.\n")


def modifier_date_trajet(voyageur):
    print("Choisissez la réservation dont vous voulez modifier la date : ")
    sql = f"""SELECT b.*,g1.nom,t.heure_depart,g2.nom,t.heure_arrive,t.date,t.num_place FROM Billet b\
               INNER JOIN Trajet t ON t.billet= b.id\
               INNER JOIN Gare g1 ON t.gare_depart =g1.id \
               INNER JOIN Gare g2 ON t.gare_arrive = g2.id \
               WHERE b.voyageur={voyageur[0]} AND t.date>=CURRENT_DATE ;"""
    cur.execute(sql)
    liste_billet = cur.fetchall()
    if liste_billet:
        for billet in liste_billet:
            print(
                f"{billet[0]}. {billet[5]} {billet[6]} - {billet[7]} {billet[8]} le {billet[9]}. siège n° {billet[10]}, {billet[1]} €")
        billet = int(input("Numéro du billet : "))
        sql1 = f"""SELECT * FROM Billet WHERE id={billet};"""
        cur.execute(sql1)
        check_billet = cur.fetchone()
        if check_billet:
            newd = input("Nouvelle date (AAAA/MM/JJ) : ")
            sql1 = f"""UPDATE Trajet SET date='{newd}' WHERE billet={billet};"""
            cur.execute(sql1)
            conn.commit()
            print("La modification a bien été prise en compte.\n")
        else:
            print("le billet n'existe pas.\n")
    else:
        print("Vous n'avez pas de trajet ulterieurement.\n")


def modifier_billet_assurance_client(voyageur):
    modifier_billet_assurance(voyageur)


def supprimer_voyageur(user):
    sql1 = f"""DELETE FROM utilisateur WHERE id={user[0]};"""
    cur.execute(sql1)
    conn.commit()
    print("Votre compte a bien été supprimé. \n")
