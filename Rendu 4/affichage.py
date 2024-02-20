import psycopg2

conn = psycopg2.connect("dbname='dbnf18p100' user='nf18p100' password='Kq9HTunusG5r' host='tuxa.sme.utc'")
# conn = psycopg2.connect("dbname='dbnf18p086' user='nf18p086' password='W847Stt3KWkl' host='tuxa.sme.utc'")
cur = conn.cursor()


def afficher_liste_voyageur():
    sql = "SELECT * FROM voyageur;"
    cur.execute(sql)
    liste_voyageur = cur.fetchall()
    if liste_voyageur:
        for voyageur in liste_voyageur:
            print(
                f"{voyageur[0]}. {voyageur[1]} {voyageur[2]}, Téléphone : {voyageur[4]}, Type : {voyageur[5]}{', Numéro de carte:' + str(voyageur[6]) + ' ' if voyageur[6] is not None else ''}{', Statut:' + str(voyageur[7]) + ' ' if voyageur[7] is not None else ''}")
        return liste_voyageur
    else:
        return None


def afficher_billet_voyageur(voyageur):
    sql1 = f"""SELECT b.*,g1.nom,t.heure_depart,g2.nom,t.heure_arrive,t.date,t.num_place FROM Billet b
                       INNER JOIN Trajet t ON t.billet= b.id\
                       INNER JOIN Gare g1 ON t.gare_depart =g1.id \
                       INNER JOIN Gare g2 ON t.gare_arrive = g2.id
                       WHERE b.voyageur={voyageur[0]};"""
    cur.execute(sql1)
    liste_billet = cur.fetchall()
    if liste_billet:
        for b in liste_billet:
            print(f"{b[0]}. {b[5]} {b[6]} - {b[7]} {b[8]} le {b[9]}, place n°{b[10]}. {b[1]}€ , Assurance : {b[3]}")
        return liste_billet
    else:
        print("Il n'existe pas de billet ! \n")
        return None


def afficher_liste_billets():
    if afficher_liste_voyageur():
        id_voyageur = int(input("Numéro du voyageur : "))
        sql1 = f"""SELECT * FROM voyageur WHERE id={id_voyageur};"""
        cur.execute(sql1)
        voyageur = cur.fetchone()
        if voyageur:
            return afficher_billet_voyageur(voyageur)
        else:
            print("Le voyageur n'existé pas")
            return None

def afficher_liste_desserte():
    sql = "SELECT d.voyage,d.gare,g1.nom,g2.nom,g3.nom, d.heure_arrive, d.heure_depart FROM Dessert d \
               INNER JOIN Voyage v ON d.voyage = v.id \
               INNER JOIN Ligne l ON v.ligne=l.id \
               INNER JOIN Gare g1 ON l.gare_depart=g1.id \
               INNER JOIN Gare g2 ON l.gare_arrive=g2.id \
               INNER JOIN Gare g3 ON d.gare = g3.id \
               INNER JOIN TypeTrain t ON v.type_train = t.id \
               ORDER BY d.voyage;"
    cur.execute(sql)
    list_desserte = cur.fetchall()
    if list_desserte:
        i = 1
        for d in list_desserte:
            print(f"{i}. Ligne : {d[2]} - {d[3]}. Dessert {d[4]}. Entrée du train en gare : {d[5]}, depart à {d[6]}.")
            i += 1
        return list_desserte
    else:
        print("Il n'existe pas de desserte ! \n")
        return None

def afficher_liste_voyage():
    sql = "SELECT v.id,v.debut_periode,v.fin_periode,g1.nom,g2.nom,t.nom FROM Voyage v \
               INNER JOIN Ligne l ON v.ligne=l.id \
               INNER JOIN Gare g1 ON l.gare_depart=g1.id \
               INNER JOIN Gare g2 ON l.gare_arrive=g2.id \
               INNER JOIN TypeTrain t ON v.type_train = t.id \
               ORDER BY v.debut_periode DESC;"
    cur.execute(sql)
    liste_voyage = cur.fetchall()
    if liste_voyage:
        for voyage in liste_voyage:
            print(f"{voyage[0]}. Du {voyage[1]} au {voyage[2]}, {voyage[3]} - {voyage[4]} en {voyage[5]}")
        return liste_voyage
    else:
        print("Il n'existe pas de voyage ! \n")
        return None


def afficher_liste_gare():
    sql = "SELECT * FROM Gare;"
    cur.execute(sql)
    liste_gare = cur.fetchall()
    if liste_gare:
        for gare in liste_gare:
            print(f"{gare[0]}. {gare[1]}")
        return liste_gare
    else:
        print("Il n'existe pas de gare")
        return None

def afficher_liste_taxi():
    sql1 = "SELECT * FROM Taxi;"
    cur.execute(sql1)
    liste_taxi = cur.fetchall()
    if liste_taxi:
        for taxi in liste_taxi:
            print(f"Numéro taxi : {taxi[0]}")
        return liste_taxi
    else:
        print("Il n'existe pas de taxi")
        return None


def afficher_liste_hotel():
    sql1 = "SELECT * FROM Hotel;"
    cur.execute(sql1)
    liste_hotel = cur.fetchall()
    if liste_hotel:
        for hotel in liste_hotel:
            print(f"{hotel[0]}. {hotel[1]}, {hotel[2]}")
        return liste_hotel
    else:
        print("Il n'existe pas de hotel")
        return None


def afficher_liste_tp():
    sql1 = "SELECT * FROM TransportPublic;"
    cur.execute(sql1)
    liste_tp = cur.fetchall()
    if liste_tp:
        for tp in liste_tp:
            print(f"{tp[0]}. {tp[1]}")
        return liste_tp
    else:
        print("Il n'existe pas de transport public")
        return None


def afficher_liste_ligne():
    sql = """SELECT l.id,g.nom,g2.nom FROM Ligne l INNER JOIN Gare g ON l.gare_depart = g.id INNER JOIN Gare g2 ON l.gare_arrive = g2.id;"""
    cur.execute(sql)
    liste_ligne = cur.fetchall()
    if liste_ligne:
        for ligne in liste_ligne:
            print(f"{ligne[0]}. {ligne[1]} - {ligne[2]}")
        return liste_ligne
    else:
        print("Il n'existe pas de ligne")
        return None


def afficher_liste_train():
    sql = """SELECT t.num, t2.nom, t2.nbr_places_max, t2.premiere_classe, t2.vitesse_max FROM Train t JOIN typetrain t2 on t.type = t2.id;"""
    cur.execute(sql)
    liste_train = cur.fetchall()
    if liste_train:
        for train in liste_train:
            print(
                f"{train[0]}. Type : {train[1]}, Nombre de places: {train[2]}, Classes disponibles : {'première et seconde' if train[3] else 'seulement seconde'}, Vitesse maximale : {train[4]}")
        return liste_train
    else:
        print("Il n'existe pas de train")
        return None

def modifier_billet_assurance(voyageur):
    afficher_billet_voyageur(voyageur)
    billet = int(input("Numéro du billet : "))
    sql2 = f"""SELECT * FROM Billet WHERE id={billet};"""
    cur.execute(sql2)
    check_billet = cur.fetchone()
    if check_billet:
        if check_billet[3] == True:
            choix = input("Une assurance est pris pour ce billet. Voulez vous changer (oui/non) ? ")
            if choix.lower() == 'oui':
                sql3 = f"""UPDATE Billet SET assurance=FALSE WHERE id={billet};"""
                cur.execute(sql3)
                conn.commit()
                print("La modification a bien été prise en compte.\n")
            else:
                print("Aucune modification n'a été effectuée.\n")
        else:
            choix = input(
                "Vous n'avez pas décidé de prendre une assurance sur votre billet. Voulez vous changer (oui/non) ? ")
            if choix.lower() == 'oui':
                sql4 = f"""UPDATE Billet SET assurance=TRUE WHERE id={billet};"""
                cur.execute(sql4)
                conn.commit()
                print("La modification a bien été prise en compte.\n")
            else:
                print("Aucune modification n'a été effectuée.\n")


def modifier_billet_place(voyageur):
    afficher_billet_voyageur(voyageur)
    billet = int(input("Numéro du billet : "))
    sql2 = f"""SELECT * FROM Billet WHERE id={billet};"""
    cur.execute(sql2)
    check_billet = cur.fetchone()
    if check_billet:
        if check_billet[3] == True:
            choix = input("Une assurance est pris pour ce billet. Voulez vous changer (oui/non) ? ")
            if choix.lower() == 'oui':
                sql3 = f"""UPDATE Billet SET assurance=FALSE WHERE id={billet};"""
                cur.execute(sql3)
                conn.commit()
                print("La modification a bien été prise en compte.\n")
            else:
                print("Aucune modification n'a été effectuée.\n")
        else:
            choix = input(
                "Vous n'avez pas décidé de prendre une assurance sur votre billet. Voulez vous changer (oui/non) ? ")
            if choix.lower() == 'oui':
                sql4 = f"""UPDATE Billet SET assurance=TRUE WHERE id={billet};"""
                cur.execute(sql4)
                conn.commit()
                print("La modification a bien été prise en compte.\n")
            else:
                print("Aucune modification n'a été effectuée.\n")
