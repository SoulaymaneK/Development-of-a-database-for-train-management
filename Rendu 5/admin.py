from affichage import *
from main import conn, cur


def menu_admin():
    print(
        "\n\033[35mVous êtes dans l'espace ADMIN. Choisissez le numéro de l'action que vous voulez effectuer (q pour quitter): ")
    print("========== AJOUT DE DONNÉES ==========")
    print("1. Ajouter une gare")
    print("2. Ajouter un taxi")
    print("3. Ajouter un hotel")
    print("4. Ajouter un transport public")
    print("5. Ajouter une ligne")
    print("6. Ajouter un type de train")
    print("7. Ajouter un train")
    print("8. Ajouter une date d'exception")
    print("9. Ajouter un voyage")
    print("10. Ajouter une desserte")
    print("=====================================\n")
    print("======== SUPPRESSION DE DONNÉES =======")
    print("11. Supprimer une gare")
    print("12. Supprimer une ligne")
    print("13. Supprimer un type de train")
    print("14. Supprimer un train")
    print("15. Supprimer un voyage")
    print("16. Supprimer un voyageur")
    print("17. Supprimer un billet")
    print("18. Supprimer une desserte")
    print("19. Supprimer un trajet")
    print("=====================================\n")
    print("======== CONSULTATION DE DONNÉES =======")
    print("20.Afficher les gares")
    print("21.Afficher les lignes")
    print("22.Afficher les trains")
    print("23.Afficher les voyages")
    print("24.Afficher les voyageurs")
    print("25.Afficher les billets")
    print("26.Afficher les dessertes")
    print("=====================================\033[0m\n")


def ajouter_gare():
    print("Entrez les informations de la nouvelle gare: ")
    nom = input("Nom : ")
    adresse = input("Adresse: ")
    ville = input("Ville : ")
    zonehoraire = input("Zone Horaire : ")
    sql = f"""SELECT * FROM Gare WHERE nom = '{nom}' AND adresse='{adresse}' AND ville='{ville}';"""
    cur.execute(sql)
    gare = cur.fetchone()
    if gare:
        print(f"La gare {gare[1]} située à {gare[2]} {gare[3]} existe déjà.")
    else:
        sql1 = f"""INSERT INTO Gare(nom,adresse,ville,zoneHoraire) VALUES ('{nom}','{adresse}','{ville}','{zonehoraire}');"""
        cur.execute(sql1)
        conn.commit()
        print("La gare a bien été ajoutée !")


def ajouter_taxi():
    print("Entrez les informations du taxi : ")
    telephone = input("Téléphone : ")
    sql = f"""SELECT * FROM Taxi WHERE telephone='{telephone}';"""
    cur.execute(sql)
    check_taxi = cur.fetchone()
    if not check_taxi:
        sql1 = f"""INSERT INTO Taxi(telephone) VALUES ('{telephone}');"""
        cur.execute(sql1)
        conn.commit()
        print("Le taxi a bien été ajouté.")
    else:
        print("Le taxi existe déjà !")


def ajouter_hotel():
    print("Entrez les informations de l'hôtel : ")
    nom = input("Nom : ")
    adresse = input("Adresse : ")
    sql = f"""SELECT * FROM Hotel WHERE nom='{nom}' AND adresse='{adresse}';"""
    cur.execute(sql)
    check_hotel = cur.fetchone()
    if not check_hotel:
        sql1 = f"""INSERT INTO Hotel(nom,adresse) VALUES ('{nom}','{adresse}');"""
        cur.execute(sql1)
        conn.commit()
        print("L'hôtel a bien été ajouté.")
    else:
        print("L'hôtel existe déjà !")


def ajouter_tp():
    print("Entrez les informations du transport public : ")
    ligne = input("Ligne : ")
    description = input("Description : ")
    sql = f"""SELECT * FROM TransportPublic WHERE ligne='{ligne}' AND description='{description}';"""
    cur.execute(sql)
    check_tp = cur.fetchone()
    if not check_tp:
        sql1 = f"""INSERT INTO TransportPublic(ligne,description) VALUES ('{ligne}','{description}');"""
        cur.execute(sql1)
        conn.commit()
        print("Le transport public a bien été ajouté.")
    else:
        print("Le transport public existe déjà !")


def ajouter_ligne():
    print("Choisissez les gare de départ et d'arrivée de la nouvelle ligne : ")
    sql = "SELECT * FROM Gare;"
    cur.execute(sql)
    liste_gare = cur.fetchall()
    if liste_gare:
        for gare in liste_gare:
            print(f"{gare[0]}. {gare[1]}")
        gare_d = int(input("Numéro de la gare de départ : "))
        gare_a = int(input("Numéro de la gare d'arrivée : "))
        sql2 = f"""SELECT * FROM Ligne WHERE gare_depart={gare_d} AND gare_arrive={gare_a};"""
        cur.execute(sql2)
        ligne = cur.fetchone()
        if not ligne and gare_d != gare_a:
            sql3 = f"""INSERT INTO Ligne(gare_depart,gare_arrive) VALUES ({gare_d},{gare_a});"""
            cur.execute(sql3)
            conn.commit()
            print("La nouvelle ligne à bien été ajoutée !")
        else:
            print("La ligne existe déjà !")
    else:
        print("Il n'existe pas encore de gare !")


def ajouter_type_train():
    print("Entrez les informations du nouveau type de train : ")
    nom = input("Nom : ")
    nbmax = int(input("Nombre de places maximum : "))
    premiere_classe = input("Possède-t-il la première classe (oui/non) : ")
    vmax = int(input("Vitesse max : "))
    if premiere_classe.lower() == "oui":
        premiere_classe = True
    else:
        premiere_classe = False
    sql = f"""SELECT * FROM TypeTrain WHERE nom='{nom}' AND nbr_places_max={nbmax} AND premiere_classe={premiere_classe} AND vitesse_max={vmax};"""
    cur.execute(sql)
    liste_trains = cur.fetchone()
    if not liste_trains:
        sql1 = f"""INSERT INTO TypeTrain (nom,nbr_places_max,premiere_classe,vitesse_max) VALUES ('{nom}',{nbmax},{premiere_classe},{vmax});"""
        cur.execute(sql1)
        conn.commit()
        print("L'ajout du nouveau type de train a bien été effectué.")
    else:
        print("Ce type de train existe déjà !")


def ajouter_train():
    print("Entrez le numéro du nouveau train : ")
    num = int(input("Num : "))
    print("Choisissez son type : ")
    sql = "SELECT * FROM TypeTrain;"
    cur.execute(sql)
    liste_type = cur.fetchall()
    if liste_type:
        for type in liste_type:
            print(
                f"{type[0]}. {type[1]}, {type[2]} places maximum, "
                f"première classe : {'disponible' if type[3] else 'indisponible'}, vitesse max : {type[4]}")
            type = int(input("Numéro du type : "))
            sql1 = f"""INSERT INTO Train(num,type) VALUES ({num},{type});"""
            cur.execute(sql1)
            conn.commit()
            print("Le nouveau train a bien été ajouté !")
    else:
        print("Créez d'abord un nouveau type de train !")


def ajouter_date_exception():
    date = input("Entrez la date d'exception (JJ/MM/AAAA): ")
    date = '/'.join(date.split('/')[::-1])
    sql = f"""SELECT * FROM DateException WHERE jour='{date}';"""
    cur.execute(sql)
    check_date = cur.fetchone()
    if not check_date:
        sql1 = f"""INSERT INTO DateException(jour) VALUES('{date}');"""
        cur.execute(sql1)
        conn.commit()
        print("La date a bien été ajoutée.")
    else:
        print("La date existe déjà !")


def ajouter_voyage():
    print("Entrez les informations du nouveau voyage : ")
    d_periode = input("Date de début de période (JJ/MM/AAAA): ")
    d_periode = '/'.join(d_periode.split('/')[::-1])
    f_periode = input("Date de fin de période (JJ/MM/AAAA) : ")
    f_periode = '/'.join(f_periode.split('/')[::-1])
    sql = "SELECT l.id,g1.nom as gare_depart,g2.nom as gare_arrive FROM Ligne l \
         INNER JOIN Gare g1 ON l.gare_depart=g1.id \
         INNER JOIN Gare g2 ON l.gare_arrive=g2.id;"
    cur.execute(sql)
    liste_ligne = cur.fetchall()
    sql1 = "SELECT * FROM TypeTrain;"
    cur.execute(sql1)
    liste_type = cur.fetchall()
    if liste_ligne and liste_type:
        print("Choisissez la ligne du nouveau voyage : ")
        for ligne in liste_ligne:
            print(f"{ligne[0]}. {ligne[1]} - {ligne[2]}")
        lvoyage = int(input("Numéro de la ligne : "))
        print("Choisissez le type de train du nouveau voyage : ")
        for type in liste_type:
            print(
                f"{type[0]}. {type[1]}, {type[2]} places maximum, Premiere classe : {type[3]}, Vitesse max : {type[4]}")
        tvoyage = int(input("Numéro du type : "))
        sql2 = f"""SELECT * FROM Voyage WHERE debut_periode='{d_periode}' AND fin_periode='{f_periode}' AND ligne={lvoyage} AND type_train={tvoyage};"""
        cur.execute(sql2)
        liste_voyage = cur.fetchone()
        if not liste_voyage:
            sql3 = f"""INSERT INTO Voyage(debut_periode,fin_periode,ligne,type_train) VALUES ('{d_periode}','{f_periode}',{lvoyage},{tvoyage});"""
            cur.execute(sql3)
            conn.commit()
            print("Le nouveau voyage a bien été ajoutée.")
        else:
            print("le voyage existe déjà !")
    else:
        print("Commencez par créer des types de train et des lignes !")


def ajouter_desserte():
    print("Choisissez le voyage auquel vous voulez ajouter une dessert : ")
    sql = "SELECT v.id,v.debut_periode,v.fin_periode,g1.nom,g2.nom,t.nom FROM Voyage v \
         INNER JOIN Ligne l ON v.ligne=l.id \
         INNER JOIN Gare g1 ON l.gare_depart=g1.id \
         INNER JOIN Gare g2 ON l.gare_arrive=g2.id \
         INNER JOIN TypeTrain t ON v.type_train = t.id \
         ORDER BY v.debut_periode DESC;"
    cur.execute(sql)
    liste_voyage = cur.fetchall()
    sql1 = "SELECT * FROM Gare;"
    cur.execute(sql1)
    liste_gare = cur.fetchall();
    if liste_voyage and liste_gare:
        for voyage in liste_voyage:
            print(f"{voyage[0]}. Du {voyage[1]} au {voyage[2]}, {voyage[3]} - {voyage[4]} en {voyage[5]}")
        voyage = int(input("Numéro du voyage : "))
        sql2 = f"""SELECT * FROM Voyage WHERE id={voyage};"""
        cur.execute(sql2)
        check_voyage = cur.fetchone()
        print("Choisissez la gare desservie : ")
        for gare in liste_gare:
            print(f"{gare[0]}. {gare[1]}")
        gare = int(input("Numéro de la gare à supprimer : "))
        sql3 = f"""SELECT * FROM Gare WHERE id={gare};"""
        cur.execute(sql3)
        check_gare = cur.fetchone()
        heure_arrive = input("Heure à laquelle le train entre en gare (HH:MM:SS) : ")
        heure_depart = input("Heure à laquelle le train quitte la gare (HH:MM:SS) : ")
        if check_voyage and check_gare:
            sql4 = f"""INSERT INTO DESSERT(voyage, gare, heure_depart, heure_arrive) VALUES ({voyage},{gare},'{heure_depart}','{heure_arrive}');"""
            cur.execute(sql4)
            conn.commit()
            print("La nouvelle desserte a bien été ajoutée.")
        else:
            print("Le voyage ou la gare sélectionnée n'existe pas !")
    else:
        print("Il n'existe pas de gare ou de voyage !")


def supprimer_gare():
    print("Choisissez la gare à supprimer : ")
    sql = "SELECT * FROM Gare;"
    cur.execute(sql)
    liste_gare = cur.fetchall()
    if liste_gare:
        for gare in liste_gare:
            print(f"{gare[0]}. {gare[1]}")
        gare = int(input("Numéro de la gare à supprimer : "))
        sql1 = f"""SELECT * FROM Gare WHERE id={gare};"""
        cur.execute(sql1)
        check_gare = cur.fetchone()
        if check_gare:
            sql2 = f"""DELETE FROM Gare WHERE id={gare};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression de la gare à bien été effectuée.\n")
        else:
            print("La gare n'existe pas !")
    else:
        print("Il n'existe pas de gare!")


def supprimer_ligne():
    print("Choisissez la ligne à supprimer : ")
    sql = "SELECT l.id,g1.nom as gare_depart,g2.nom as gare_arrive FROM Ligne l \
         INNER JOIN Gare g1 ON l.gare_depart=g1.id \
         INNER JOIN Gare g2 ON l.gare_arrive=g2.id;"
    cur.execute(sql)
    liste_ligne = cur.fetchall()
    if liste_ligne:
        for ligne in liste_ligne:
            print(f"{ligne[0]}. {ligne[1]} - {ligne[2]}")
        ligne = int(input("Numéro de la ligne à supprimer : "))
        sql1 = f"""SELECT * FROM Ligne WHERE id={ligne};"""
        cur.execute(sql1)
        check_ligne = cur.fetchone()
        if check_ligne:
            sql2 = f"""DELETE FROM Ligne WHERE id={ligne};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression de la ligne à bien été effectuée.\n")
        else:
            print("La ligne n'existe pas !\n")
    else:
        print("Il n'existe pas de ligne !\n")


def supprimer_type_train():
    print("Choisissez le type de train à supprimer : ")
    sql = "SELECT * FROM TypeTrain;"
    cur.execute(sql)
    liste_type = cur.fetchall()
    if liste_type:
        for type in liste_type:
            print(
                f"{type[0]}. {type[1]}, {type[2]} places maximum, "
                f"premiere classe : {'disponible' if type[3] else 'indisponible'}, vitesse max : {type[4]}")
        type = int(input("Numéro du type : "))
        sql1 = f"""SELECT * FROM TypeTrain WHERE id={type};"""
        cur.execute(sql1)
        check_type = cur.fetchone()
        if check_type:
            sql2 = f"""DELETE FROM TypeTrain WHERE id={type};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression du type de train à bien été effectuée.")
        else:
            print("Le type de train n'existe pas !")
    else:
        print("Il n'existe pas de type de train !")


def supprimer_train():
    print("Choisissez le type de train à supprimer : ")
    sql = "SELECT num FROM TypeTrain;"
    cur.execute(sql)
    liste_train = cur.fetchall()
    if liste_train:
        for train in liste_train:
            print(f"Numéro du train : {train[0]}")
        train = int(input("Numéro du train : "))
        sql1 = f"""SELECT * FROM Train WHERE num={train};"""
        cur.execute(sql1)
        check_train = cur.fetchone()
        if check_train:
            sql2 = f"""DELETE FROM TypeTrain WHERE id={train};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression du train à bien été effectuée.\n")
        else:
            print("Le train n'existe pas !\n")
    else:
        print("Il n'existe pas de train !\n")


def supprimer_voyage():
    print("Choisissez le voyage à supprimer : ")
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
        voyage = int(input("Numéro du voyage : "))
        sql1 = f"""SELECT * FROM Voyage WHERE id={voyage};"""
        cur.execute(sql1)
        check_voyage = cur.fetchone()
        if check_voyage:
            sql2 = f"""DELETE FROM Voyage WHERE id={voyage};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression du voyage à bien été effectuée.")
        else:
            print("Le voyage n'existe pas !")
    else:
        print("Il n'existe pas de voyage !")


def supprimer_voyageur_admin():
    if afficher_liste_voyageur():
        id_voyageur = int(input("Numéro du voyageur : "))
        sql1 = f"""SELECT * FROM voyageur WHERE id={id_voyageur};"""
        cur.execute(sql1)
        check_voyageur = cur.fetchone()
        if check_voyageur:
            sql1 = f"""DELETE FROM Voyageur WHERE id={check_voyageur[0]};"""
            cur.execute(sql1)
            conn.commit()
            print("Le voyageur a bien été supprimé.")
        else:
            print("Le voyageur n'existe pas !")


def supprimer_desserte():
    print("Choisissez la desserte à supprimer : ")
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
            print(f"{i}. Ligne : {d[2]} - {d[3]}. Dessert {d[4]}. Entrée du train en gare : {d[5]}, départ à {d[6]}.")
            i += 1
        desserte = int(input("Numéro de la desserte : "))
        if desserte > 0 and desserte <= i - 1:
            d = list_desserte[desserte - 1]
            sql1 = f"""DELETE FROM Dessert WHERE voyage={d[0]} AND gare={d[1]};"""
            cur.execute(sql1)
            conn.commit()
            print("La desserte a bien été supprimée. \n")
        else:
            print("La desserte n'existe pas !\n")
    else:
        print("Il n'existe pas de desserte ! \n")


def supprimer_billet():
    print("Choisissez le voyage à supprimer : ")
    sql = "SELECT b.*,g1.nom,b.trajet->>'heure_depart',g2.nom,b.trajet->>'heure_arrive',v.nom,v.prenom,b.trajet->>'date',b.trajet->>'num_place' FROM Billet b\
         INNER JOIN Voyageur v ON b.voyageur=v.id\
         INNER JOIN Gare g1 ON CAST(b.trajet->>'gare_depart' AS INTEGER)=g1.id \
         INNER JOIN Gare g2 ON CAST(b.trajet->>'gare_arrive' AS INTEGER) = g2.id;"
    cur.execute(sql)
    liste_billet = cur.fetchall()
    if liste_billet:
        for billet in liste_billet:
            print(
                f"{billet[0]}. {billet[5]} {billet[6]} - {billet[7]} {billet[8]} le {billet[11]}. {billet[9]} {billet[10]} siège n° {billet[12]}, {billet[1]} €")
        billet = int(input("Numéro du billet : "))
        sql1 = f"""SELECT * FROM Billet WHERE id={billet};"""
        cur.execute(sql1)
        check_billet = cur.fetchone()
        if check_billet:
            sql2 = f"""DELETE FROM Billet WHERE id={billet};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression du billet à bien été effectuée.")
        else:
            print("Le billet n'existe pas !")
    else:
        print("Il n'existe pas de billet !")


def supprimer_trajet(): # À REFAIRE
    print("Choisissez le trajet à supprimer : ")
    sql = "SELECT b.id,b.trajer->>'date',g1.nom,b.trajet->>'heure_depart',g2.nom,b.trajet->>'heure_arrive',tr.num FROM Billet b \
         INNER JOIN Gare g1 ON CAST(b.trajet->>'gare_depart' AS INTEGER)=g1.id \
         INNER JOIN Gare g2 ON CAST(b.trajet->>'gare_arrive' AS INTEGER)=g2.id \
         INNER JOIN Train tr ON b.trajet->>'trajet'=tr.num ;"
    cur.execute(sql)
    liste_trajet = cur.fetchall()
    if liste_trajet:
        for trajet in liste_trajet:
            print(f"{trajet[0]}. {trajet[2]} {trajet[3]} - {trajet[4]} {trajet[5]} le {trajet[2]}. Train n°{trajet[6]}")
        trajet = int(input("Numéro du trajet : "))
        sql1 = f"""SELECT * FROM Billet WHERE id={trajet};"""
        cur.execute(sql1)
        check_trajet = cur.fetchone()
        if check_trajet:
            sql2 = f"""DELETE FROM Billet WHERE id={trajet};"""
            cur.execute(sql2)
            conn.commit()
            print("La suppression du trajet à bien été effectuée.")
        else:
            print("Le trajet n'existe pas !")
    else:
        print("Il n'existe pas de trajet !")
