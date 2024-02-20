import psycopg2
from random import randint
from affichage import *

conn = psycopg2.connect("dbname='dbnf18p100' user='nf18p100' password='Kq9HTunusG5r' host='tuxa.sme.utc'")
# conn = psycopg2.connect("dbname='dbnf18p086' user='nf18p086' password='W847Stt3KWkl' host='tuxa.sme.utc'")
cur = conn.cursor()


def menu_gestionnaire():
    print(
        "\n\033[33mVous êtes dans l'espace GESTIONNAIRE. Choisissez le numéro de l'action que vous voulez effectuer (q pour quitter): ")
    print("==========AJOUT DE DONNEES==========")
    print("1.Relier un hotel à une gare")
    print("2.Relier un transport public à une gare")
    print("3.Relier un taxi à une gare")
    print("4.Associer une date hebdomadaire à un voyage")
    print("5.Associer une date exception à un voyage")
    print("=====================================")
    print("========MODIFICATION DE DONNEES=======")
    print("6.Modififer le jour d'un voyage")
    print("7.Modifier le type d'un voyageur")
    print("8.Modifier l'assurance d'un billet")
    print("9.Modifier les horaires d'une desserte")  # faire un ON UPDATE CASCADE pour modifier ausis pour le trajet
    print("10.Modifier le numéro de siège")
    print("=====================================\033[0m\n")


def taxi_gare():
    print("Choisissez la gare et le taxi : ")
    if afficher_liste_gare():
        gare = int(input("Numéro de la gare : "))
        if afficher_liste_taxi():
            taxi = input("Numéro du taxi : ")
            sql2 = f"""SELECT * FROM Gare_Taxi WHERE gare={gare} AND taxi='{taxi}';"""
            cur.execute(sql2)
            check_g_h = cur.fetchone()
            if not check_g_h:
                sql4 = f"""INSERT INTO Gare_Taxi(gare,taxi) VALUES({gare},'{taxi}');"""
                cur.execute(sql4)
                conn.commit()
                print("Le taxi a bien été relié à la gare")
            else:
                print("Le taxi est déjà enregistré prés de la gare")


def hotel_gare():
    print("Choisissez la gare et l'hotel : ")
    if afficher_liste_gare():
        gare = int(input("Numéro de la gare : "))
        if afficher_liste_hotel():
            hotel = int(input("Numéro de l'hotel : "))
            sql2 = f"""SELECT * FROM Gare_Hotel WHERE gare={gare} AND hotel={hotel};"""
            cur.execute(sql2)
            check_g_h = cur.fetchone()
            if not check_g_h:
                sql4 = f"""INSERT INTO Gare_Hotel(gare,hotel) VALUES({gare},{hotel});"""
                cur.execute(sql4)
                conn.commit()
                print("L'hotel a bien été relié à la gare")
            else:
                print("L'hotel est déjà enregistré prés de la gare")


def tp_gare():
    print("Choisissez la gare et l'hotel : ")
    if afficher_liste_gare():
        gare = int(input("Numéro de la gare : "))
        if afficher_liste_tp():
            ligne = input("Ligne du transport public : ")
            sql2 = f"""SELECT * FROM Gare_TransPublic WHERE gare={gare} AND transport={ligne};"""
            cur.execute(sql2)
            check_g_h = cur.fetchone()
            if not check_g_h:
                sql4 = f"""INSERT INTO Gare_TransPublic(gare,transport) VALUES({gare},'{ligne}');"""
                cur.execute(sql4)
                conn.commit()
                print("Le transport public a bien été relié à la gare")
            else:
                print("Le transport public est déjà enregistré prés de la gare")


def jour_voyage():
    liste_jour = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    print("Choisissez le voyage auquel vous voulez ajouter un jour : ")
    if afficher_liste_voyage():
        voyage = int(input("Numéro du voyage : "))
        sql1 = f"""SELECT * FROM Voyage WHERE id={voyage};"""
        cur.execute(sql1)
        check_voyage = cur.fetchone()
        jour = input("Entrez un jour de la semaine : ")
        while not jour in liste_jour:
            jour = input("Entrez un jour de la semaine : ")
        sql2 = f"""SELECT * FROM Jour_Voyage WHERE voyage={voyage} AND jour='{jour}';"""
        cur.execute(sql2)
        check_jv = cur.fetchone()
        if check_voyage and not check_jv:
            sql3 = f"""INSERT INTO Jour_Voyage(voyage,jour) VALUES ({voyage},'{jour}');"""
            cur.execute(sql3)
            conn.commit()
            print("Le jour a bien été associé au voayge.\n")
        else:
            print("le voyage n'existe pas ou est déjà relié à ce jour.\n")


def exception_voyage():
    sql1 = "SELECT * FROM DateException WHERE jour>=CURRENT_DATE ;"
    cur.execute(sql1)
    liste_dex = cur.fetchall()
    if liste_dex:
        print("Choisissez le voyage auquel vous voulez ajouter un jour : ")
        if afficher_liste_voyage():
            voyage = int(input("Numéro du voyage : "))
            sql1 = f"""SELECT * FROM Voyage WHERE id={voyage};"""
            cur.execute(sql1)
            check_voyage = cur.fetchone()
            for date in liste_dex:
                print(f"{date[0]}")
            date = int(input("Date (AAAA/MM/JJ) : "))
            sql1 = f"""SELECT * FROM DateException WHERE jour='{date}' AND;"""
            cur.execute(sql1)
            check_date = cur.fetchone()
            sql2 = f"""SELECT * FROM Exception_Voyage WHERE voyage={voyage} AND jour='{date}';"""
            cur.execute(sql2)
            check_ev = cur.fetchone()
            if check_voyage and check_date and not check_ev:
                sql3 = f"""INSERT INTO Exception_Voyage(voyage,jour) VALUES ({voyage},'{date}');"""
                cur.execute(sql3)
                conn.commit()
                print("La date a bien été associée au voyage.\n")
            else:
                print("Il n'y a pas de dateexception enregistrée pour plus tard.\n")
    else:
        print("Il n'existe pas de date excpetion ulterieure!\n")


def modifier_voyage():
    print("Choisissez le voyage dont vous voulez modifier la période : ")
    if afficher_liste_voyage():
        voyage = int(input("Numéro du voyage : "))
        sql1 = f"""SELECT * FROM Voyage WHERE id={voyage};"""
        cur.execute(sql1)
        check_voyage = cur.fetchone()
        if check_voyage:
            newd_periode = input("Entrez le debut de la nouvelle periode (AAAA/MM/JJ) : ")
            newf_periode = input("Entrez la fin de la nouvelle periode (AAAA/MM/JJ) : ")
            sql2 = f"""UPDATE Voyage SET debut_periode='{newd_periode}', fin_periode='{newf_periode}' WHERE id={voyage};"""
            cur.execute(sql2)
            conn.commit()
            print("La modification a bien été prise en compte. \n")
        else:
            print("Le voyage n'existe pas ! \n")


def modifier_type_voyageur_gestionnaire():
    liste_type = ['Occasionnel', 'Regulier']
    liste_statut = ['bronze', 'silver', 'gold', 'platine']
    print("Choisissez le voyageur dont vous voulez modifier le type : ")
    if afficher_liste_voyageur():
        id_voyageur = int(input("Numéro du voyageur : "))
        sql1 = f"""SELECT * FROM voyageur WHERE id={id_voyageur};"""
        cur.execute(sql1)
        check_voyageur = cur.fetchone()
        if check_voyageur:
            print(f"Type actuel du voyageur : {check_voyageur[5]}. Vous avez le choix entre Occasionnel et Regulier")
            newtype = input("Nouveau type : ")
            while not newtype in liste_type:
                newtype = input("Nouveau type : ")
            if newtype == 'Occasionnel':
                sql1 = f"""UPDATE Voyageur SET type='{newtype}',num_carte=NULL,statut=NULL WHERE id={check_voyageur[0]};"""
                cur.execute(sql1)
                conn.commit()
                print("La modification a bien été prise en compte.\n")
            elif newtype == 'Regulier':
                num_carte = input("Entrez son numéro de carte : ")
                statut = input("Entrez son statut ('bronze', 'silver', 'gold', 'platine') : ")
                while not statut in liste_statut:
                    statut = input("Entrez son statut ('bronze', 'silver', 'gold', 'platine') : ")
                sql2 = f"""UPDATE Voyageur SET type='{newtype}',num_carte={num_carte},statut='{statut}' WHERE id={check_voyageur[0]};"""
                cur.execute(sql2)
                conn.commit()
                print("La modification a bien été prise en compte.\n")
        else:
            print("Le voyageur n'existe pas ! \n")


def modifier_billet_assurance_gestionnaire():
    print("Choisissez le voyageur dont vous voulez modifier le billet : ")
    if afficher_liste_voyageur():
        id_voyageur = int(input("Numéro du voyageur : "))
        sql1 = f"""SELECT * FROM voyageur WHERE id={id_voyageur};"""
        cur.execute(sql1)
        voyageur = cur.fetchone()
        if voyageur:
            modifier_billet_assurance(voyageur)
        else:
            print("Le voyageur n'existe pas.")


def modifier_desserte():
    print("Choisissez la desserte à modifier : ")
    liste_desserte = afficher_liste_desserte()
    if liste_desserte:
        desserte = int(input("Numéro de la desserte : "))
        if 0 < desserte <= len(liste_desserte):
            d = liste_desserte[desserte - 1]
            new_h_arrive = input("Entrez la nouvelle heure d'entré en gare du train (HH:MM:SS) : ")
            new_h_depart = input("Entrez la nouvelle heure de depart en gare du train (HH:MM:SS) : ")
            sql1 = f"""UPDATE Dessert SET heure_arrive='{new_h_arrive}',heure_depart='{new_h_depart}' WHERE voyage={d[0]} AND gare={d[1]};"""
            cur.execute(sql1)
            conn.commit()
            print("La desserte a bien été modifiée. \n")
        else:
            print("La desserte n'existe pas !\n")
    else:
        print("Il n'existe pas de desserte ! \n")


def modifier_place_trajet():
    print("Choisissez le voyageur dont vous voulez modifier la place : ")
    if afficher_liste_voyageur():
        id_voyageur = int(input("Numéro du voyageur : "))
        sql1 = f"""SELECT * FROM voyageur WHERE id={id_voyageur};"""
        cur.execute(sql1)
        voyageur = cur.fetchone()
        if voyageur:
            if afficher_billet_voyageur(voyageur):
                billet = int(input("Numéro du billet : "))
                sql2 = f"""SELECT * FROM Billet WHERE id={billet};"""
                cur.execute(sql2)
                check_billet = cur.fetchone()
                if check_billet:
                    sql2 = f"""SELECT t.id,t.date,g1.nom,t.heure_depart,g2.nom,t.heure_arrive,t.train,t.num_place,tp.nbr_places_max FROM Trajet t \
                         INNER JOIN Gare g1 ON t.gare_depart=g1.id \
                         INNER JOIN Gare g2 ON t.gare_arrive=g2.id \
                         INNER JOIN Train tr ON t.train=tr.num \
                         INNER JOIN TypeTrain tp ON tr.type=tp.id \
                         WHERE t.billet={check_billet[0]};"""
                    cur.execute(sql2)
                    trajet = cur.fetchone()
                    if trajet:
                        print(
                            f"Pour le trajet : {trajet[2]} {trajet[3]} - {trajet[4]} {trajet[5]} le {trajet[1]}. Train n°{trajet[6]}.")
                        new_siege = int(input(
                            f"Vous êtes au siège n°{trajet[7]}. Entrez le nouveau numéro du siège (vous pouvez entrez-le même) : "))
                        if 0 < new_siege <= trajet[8]:
                            sql3 = f"""UPDATE Trajet SET num_place={new_siege} WHERE id={trajet[0]};"""
                            cur.execute(sql3)
                            conn.commit()
                            print("La modification a bien été prise en compte.\n")
                        else:
                            print("Désolé ce siège n'est pas disponible dans ce train.\n")
                    else:
                        print("Aucun trajet associé à ce billet.\n")
                else:
                    print("Le billet n'existe pas.\n")
            else:
                print("Le voyageur n'a aucun billet en cours.\n")
        else:
            print("Le voyageur n'existe pas.")
