DROP TABLE IF EXISTS Gare,Taxi,TransportPublic,Hotel,Gare_Hotel,Gare_TransPublic,Gare_Taxi,Ligne,TypeTrain,
    Voyage,Dessert_Hebdomadaire,DateException,Jour_Voyage,Exception_Voyage,Train,Voyageur,Billet,Dessert,Trajet,Utilisateur CASCADE;

DROP TYPE IF EXISTS Jour,Statut,Type_voyageur,Moyen_paiement,Role_utilisateur;

DROP VIEW IF EXISTS Ligne_Voyage,Voyage_Date,voyage_ids,dessert_voyage_ids,voyage_ids_intersect,voyage_ligne_depart_gares,dessert_voyage_gares,
    valid_depart_gares,voyage_ligne_arrivee_gares,valid_arrivee_gares,Trajet_voyage_depart,Trajet_voyage_arrivee,Trajet_voyage_correspondant,
    check_voyage_trajet,trajet_heure_depart,trajet_heure_arrivee,Trajet_Billet CASCADE;

CREATE TABLE Gare
(
    id          SERIAL,
    nom         VARCHAR(30) NOT NULL,
    adresse     VARCHAR     NOT NULL,
    ville       VARCHAR(30) NOT NULL,
    zoneHoraire VARCHAR(30) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nom, adresse, ville)
);

CREATE TABLE Taxi
(
    telephone VARCHAR(10) PRIMARY KEY
);

CREATE TABLE TransportPublic
(
    ligne       VARCHAR,
    description VARCHAR NOT NULL,
    PRIMARY KEY (ligne)
);

CREATE TABLE Hotel
(
    id      SERIAL,
    nom     VARCHAR NOT NULL,
    adresse VARCHAR NOT NULL,
    UNIQUE (nom, adresse),
    PRIMARY KEY (id)
);

CREATE TABLE Gare_Hotel
(
    gare  INTEGER,
    hotel INTEGER,
    FOREIGN KEY (gare) REFERENCES Gare (id) ON DELETE CASCADE,
    FOREIGN KEY (hotel) REFERENCES Hotel (id) ON DELETE CASCADE,
    PRIMARY KEY (gare, hotel)
);

CREATE TABLE Gare_TransPublic
(
    gare      INTEGER,
    transport VARCHAR,
    FOREIGN KEY (gare) REFERENCES Gare (id) ON DELETE CASCADE,
    FOREIGN KEY (transport) REFERENCES TransportPublic (ligne) ON DELETE CASCADE,
    PRIMARY KEY (gare, transport)
);

CREATE TABLE Gare_Taxi
(
    gare INTEGER,
    taxi VARCHAR(10),
    FOREIGN KEY (gare) REFERENCES Gare (id) ON DELETE CASCADE,
    FOREIGN KEY (taxi) REFERENCES Taxi (telephone) ON DELETE CASCADE,
    PRIMARY KEY (gare, taxi)
);

CREATE TABLE Ligne
(
    id          SERIAL,
    gare_depart INTEGER NOT NULL,
    gare_arrive INTEGER NOT NULL,
    FOREIGN KEY (gare_depart) REFERENCES Gare (id) ON DELETE CASCADE,
    FOREIGN KEY (gare_arrive) REFERENCES Gare (id) ON DELETE CASCADE,
    PRIMARY KEY (id),
    CHECK (gare_depart != gare_arrive),
    UNIQUE (gare_depart, gare_arrive)
);

CREATE TABLE TypeTrain
(
    id              SERIAL,
    nom             VARCHAR(30) NOT NULL,
    nbr_places_max  INTEGER     NOT NULL,
    premiere_classe BOOLEAN,
    vitesse_max     INTEGER     NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Voyage
(
    id            SERIAL,
    debut_periode DATE    NOT NULL,
    fin_periode   DATE    NOT NULL,
    ligne         INTEGER NOT NULL,
    type_train    INTEGER NOT NULL,
    FOREIGN KEY (ligne) REFERENCES Ligne (id) ON DELETE CASCADE,
    FOREIGN KEY (type_train) REFERENCES TypeTrain (id) ON DELETE CASCADE,
    PRIMARY KEY (id),
    CHECK (fin_periode > debut_periode)
);

CREATE TYPE Jour AS ENUM ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche');

CREATE TABLE Dessert_Hebdomadaire
(
    jour Jour PRIMARY KEY
);

CREATE TABLE DateException
(
    jour DATE PRIMARY KEY
);

CREATE TABLE Jour_Voyage
(
    voyage INTEGER,
    jour   Jour,
    FOREIGN KEY (voyage) REFERENCES Voyage (id) ON DELETE CASCADE,
    FOREIGN KEY (jour) REFERENCES Dessert_Hebdomadaire (jour) ON DELETE CASCADE,
    PRIMARY KEY (voyage, jour)
);

CREATE TABLE Exception_Voyage
(
    voyage INTEGER,
    jour   DATE,
    FOREIGN KEY (voyage) REFERENCES Voyage (id) ON DELETE CASCADE,
    FOREIGN KEY (jour) REFERENCES DateException (jour) ON DELETE CASCADE,
    PRIMARY KEY (voyage, jour)
);

CREATE TABLE Train
(
    num  INTEGER,
    type INTEGER NOT NULL,
    FOREIGN KEY (type) REFERENCES TypeTrain (id) ON DELETE CASCADE,
    PRIMARY KEY (num)
);

CREATE TYPE Statut AS ENUM ('bronze', 'silver', 'gold', 'platine');
CREATE TYPE Type_voyageur AS ENUM ('Regulier', 'Occasionnel');

CREATE TYPE Role_utilisateur AS ENUM ('admin', 'gestionnaire', 'client');

CREATE TABLE Utilisateur
(
    id              SERIAL,
    nom_utilisateur VARCHAR UNIQUE   NOT NULL,
    mot_de_passe    VARCHAR          NOT NULL,
    role            Role_utilisateur NOT NULL,
    PRIMARY KEY (id)
);

CREATE FUNCTION is_client(id_utilisateur INTEGER) RETURNS BOOLEAN AS
$$
BEGIN
    RETURN EXISTS(SELECT 1 FROM Utilisateur WHERE id = id_utilisateur AND role = 'client');
END;
$$ LANGUAGE plpgsql;

CREATE TABLE Voyageur
(
    id          SERIAL,
    nom         VARCHAR        NOT NULL,
    prenom      VARCHAR        NOT NULL,
    adresse     VARCHAR        NOT NULL,
    telephone   VARCHAR        NOT NULL,
    type        Type_voyageur  NOT NULL,
    num_carte   INTEGER UNIQUE NULL,
    statut      Statut         NULL,
    utilisateur INTEGER UNIQUE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (utilisateur) REFERENCES Utilisateur (id) ON DELETE CASCADE,
    CHECK (NOT (type = 'Occasionnel' AND num_carte is NOT NULL AND statut is not NULL)),
    CHECK (NOT (type = 'Regulier' AND num_carte is NULL AND statut is NULL)),
    CHECK (is_client(utilisateur))
);



CREATE TYPE Moyen_paiement AS ENUM ('carte bleue', 'espece', 'cheque');

CREATE TABLE Billet
(
    id             SERIAL,
    prix           NUMERIC        NOT NULL CHECK (prix > 0),
    moyen_paiement Moyen_paiement NOT NULL,
    assurance      BOOLEAN,
    voyageur       INTEGER        NOT NULL,
    FOREIGN KEY (voyageur) REFERENCES Voyageur (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

CREATE TABLE Dessert
(
    voyage       INTEGER,
    gare         INTEGER,
    heure_arrive TIME NOT NULL,
    heure_depart TIME NOT NULL,
    FOREIGN KEY (voyage) REFERENCES Voyage (id) ON DELETE CASCADE,
    FOREIGN KEY (gare) REFERENCES Gare (id) ON DELETE CASCADE,
    PRIMARY KEY (voyage, gare),
    CHECK (heure_arrive < heure_depart),
    UNIQUE (voyage, gare, heure_depart),
    UNIQUE (voyage, gare, heure_arrive)
);


CREATE TABLE Trajet
(
    id           SERIAL,
    voyage       INTEGER,
    date         DATE CHECK (date > CURRENT_DATE),
    billet       INTEGER,
    num_place    INTEGER NOT NULL CHECK (num_place > 0),
    gare_depart  INTEGER NOT NULL,
    heure_depart TIME    NOT NULL,
    gare_arrive  INTEGER NOT NULL,
    heure_arrive TIME    NOT NULL,
    train        INTEGER NOT NULL,
    FOREIGN KEY (voyage, gare_depart, heure_depart) REFERENCES Dessert (voyage, gare, heure_depart) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (voyage, gare_arrive, heure_arrive) REFERENCES Dessert (voyage, gare, heure_arrive) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (billet) REFERENCES Billet (id) ON DELETE CASCADE,
    FOREIGN KEY (train) REFERENCES Train (num) ON DELETE CASCADE,
    PRIMARY KEY (id, billet),
    CHECK (gare_depart != gare_arrive)
);

/*========================================================================================================*/

/*CREATION DES VIEW POUR LES CONTRAINTES RELATIONNELLES*/

/*==========================================================*/

/*
Calcule de la durée des trajets
*/
CREATE VIEW Duree_Trajet AS
SELECT id, heure_arrive - heure_depart AS duree
FROM Trajet;

/*Relation 1 : 1..N entre Ligne et Voyage
Projection (Ligne, id) = Projection (Voyage, ligne)
*/
CREATE VIEW Ligne_Voyage AS
SELECT l.id as id_ligne, v.*
FROM Ligne as l
         INNER JOIN Voyage as v
                    ON l.id = v.ligne;

/*==========================================================*/

/*Relation 0..N : 1..7 entre Voyage et DateHebdomadaire
Projection (Voyage, id) = Projection (Exception_Voyage, voyage)
 */
CREATE VIEW Voyage_Date AS
SELECT v.id, d.jour, d.voyage
FROM Voyage as v
         INNER JOIN Jour_Voyage d
                    ON v.id = d.voyage;

/*==========================================================*/

/*Projection (Voyage, id) = Projection (Dessert, voyage)*/

/*première projection*/
CREATE VIEW voyage_ids AS
SELECT id
FROM Voyage;

/*deuxième projection*/
CREATE VIEW dessert_voyage_ids AS
SELECT DISTINCT voyage
FROM Dessert;

/*égalité des deux*/
CREATE VIEW voyage_ids_intersect AS
SELECT id
FROM voyage_ids
INTERSECT/*jointure naturelle*/
SELECT voyage
FROM dessert_voyage_ids;

/*==========================================================*/

/*Relation Dessert 0..N : 2..N entre Voyage et Gare
Projection (Jointure (Voyage, Ligne, Voyage.Ligne = Ligne.id), gare_départ) ⊆
  Projection (Jointure (Dessert, Voyage, Voyage.id = Dessert.voyage), gare)
 */

/*première jointure*/
CREATE VIEW voyage_ligne_depart_gares AS
SELECT Voyage.id, Ligne.gare_depart AS gare
FROM Voyage
         INNER JOIN Ligne ON Voyage.ligne = Ligne.id;

/*deuxième jointure*/
CREATE VIEW dessert_voyage_gares AS
SELECT Dessert.voyage, Dessert.gare
FROM Dessert
         INNER JOIN Voyage ON Voyage.id = Dessert.voyage;

/*resultat des projections. On utilisera cette table pour verifier si les contraintes relationnelles sont respectées*/
CREATE VIEW valid_depart_gares AS
SELECT voyage_ligne_depart_gares.id, voyage_ligne_depart_gares.gare
FROM voyage_ligne_depart_gares
         INNER JOIN dessert_voyage_gares ON voyage_ligne_depart_gares.id = dessert_voyage_gares.voyage
    AND voyage_ligne_depart_gares.gare = dessert_voyage_gares.gare;

/*==========================================================*/

/*Projection (Jointure (Voyage, Ligne, Voyage.Ligne = Ligne.id), gare_arrivée) ⊆
  Projection (Jointure (Dessert, Voyage, Voyage.id = Dessert.voyage), gare)
 */

/*première jointure*/
CREATE VIEW voyage_ligne_arrivee_gares AS
SELECT Voyage.id, Ligne.gare_arrive AS gare
FROM Voyage
         INNER JOIN Ligne ON Voyage.ligne = Ligne.id;

/*la deuxième jointure est la même qu'en haut*/

/*resultat des projections. On utilisera cette table pour verifier si les contraintes relationnelles sont respectées*/
CREATE VIEW valid_arrivee_gares AS
SELECT voyage_ligne_arrivee_gares.id, voyage_ligne_arrivee_gares.gare
FROM voyage_ligne_arrivee_gares
         INNER JOIN dessert_voyage_gares ON voyage_ligne_arrivee_gares.id = dessert_voyage_gares.voyage
    AND voyage_ligne_arrivee_gares.gare = dessert_voyage_gares.gare;


/*==========================================================*/

/*Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_départ), voyage) =
  Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_arrivée), voyage)
*/

/*on relève les voyage depuis trajet selon gare de depart*/
CREATE VIEW Trajet_voyage_depart AS
SELECT Trajet.voyage
FROM Trajet
         INNER JOIN Dessert ON Dessert.voyage = Trajet.voyage AND Dessert.gare = Trajet.gare_depart;

/*on relève les voyages depuis trajet selon gare d'arrive*/
CREATE VIEW Trajet_voyage_arrivee AS
SELECT Trajet.voyage
FROM Trajet
         INNER JOIN Dessert ON Dessert.voyage = Trajet.voyage AND Dessert.gare = Trajet.gare_arrive;

/*on joint les même voyages selons les 2 précédentes vues*/
CREATE VIEW Trajet_voyage_correspondant AS
SELECT DISTINCT Trajet_voyage_depart.voyage
FROM Trajet_voyage_depart
         INNER JOIN Trajet_voyage_arrivee ON Trajet_voyage_depart.voyage = Trajet_voyage_arrivee.voyage;

/*Cette méthode regroupe directement les voyages avec des gare d'arrive et gare de depart selon leur trajet, cela evite de faire deux vues. On choisira par la suite.

CREATE VIEW trajet_voyage_depart_arrivee AS
  SELECT t.voyage
  FROM Trajet t
  JOIN Dessert d1 ON t.voyage = d1.voyage AND t.gare_depart = d1.gare AND t.heure_depart = d1.heure_depart
  JOIN Dessert d2 ON t.voyage = d2.voyage AND t.gare_arrive = d2.gare AND t.heure_arrive = d2.heure_arrive
  GROUP BY t.voyage
  HAVING COUNT(DISTINCT d1.gare) = COUNT(DISTINCT d2.gare);

En regroupant les résultats par voyage, la vue vérifie ensuite si le nombre de gares de départ distinctes correspond
  au nombre de gares d'arrivée distinctes pour chaque voyage. Si oui, cela signifie que le voyage relie une gare de départ unique
  à une gare d'arrivée unique (ou à un ensemble de gares d'arrivée identiques), ce qui est conforme aux contraintes de la table
  Trajet.
*/

/*tester l'égalité des projections, si la vue est null alors il n'y a pas de problème*/
CREATE VIEW check_voyage_trajet AS
SELECT *
FROM Trajet_voyage_correspondant
EXCEPT
SELECT *
FROM (SELECT Trajet.voyage
      FROM Trajet
               INNER JOIN Dessert ON Dessert.voyage = Trajet.voyage AND Dessert.gare = Trajet.gare_arrive) t;

/*==========================================================*/

/*Relations 1 : 0..N entre Trajet et Dessert
Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_départ), heure_départ) =
  Projection( Trajet, heure_départ)
 */

CREATE VIEW trajet_heure_depart AS
SELECT t.heure_depart
FROM Trajet t
         INNER JOIN Dessert d ON t.voyage = d.voyage AND t.gare_depart = d.gare AND t.heure_depart = d.heure_depart;

/*==========================================================*/

/*Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_départ), heure_arrivée)
  = Projection( Trajet, heure_arrivée)
 */

CREATE VIEW trajet_heure_arrivee AS
SELECT t.heure_arrive
FROM Trajet t
         INNER JOIN Dessert d ON t.voyage = d.voyage AND t.gare_arrive = d.gare AND t.heure_arrive = d.heure_arrive;

/*==========================================================*/

/*Composition entre Trajet et Billet (⇔ Relation 1 : 1..N)
  Projection (Trajet, billet) = Projection (Billet, id)
 */
CREATE VIEW Trajet_Billet AS
SELECT Trajet.id AS trajet_id, Billet.id AS billet_id
FROM Trajet
         INNER JOIN Billet ON Trajet.billet = Billet.id;
