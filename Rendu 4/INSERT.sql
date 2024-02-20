/*Dans ce fichier on insert des données dans toutes les tables*/

insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Gare du Nord', 'rue de Paris', 'Paris', 'GMT+2');
insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Gare de Lille', 'rue de Lille', 'Lille', 'GMT+2');
insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Gare de Compiegne', 'rue de Compiegne', 'Compiegne', 'GMT+2');
insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Gare de Creil', 'rue de Creil', 'Creil', 'GMT+2');

insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Gare de Marseille', 'rue de Marseille', 'Marseille', 'GMT+2');
insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Paris gare de Lyon', 'rue de Paris', 'Paris', 'GMT+2');
insert into gare (nom,adresse,ville, zoneHoraire) VALUES ('Gare de Grenoble', 'rue de Grenoble', 'Grenoble', 'GMT+2');

insert into taxi (telephone) VALUES ('0675489030');
insert into taxi (telephone) VALUES ('0698637204');
insert into taxi (telephone) VALUES ('0719085803');

insert into TransportPublic (ligne, description) VALUES ('1', 'Metro 1');
insert into TransportPublic (ligne, description) VALUES ('172', 'Bus 172');

insert into hotel (nom, adresse) VALUES ('Hotel Mercure', 'rue de Paris');

insert into Gare_Taxi (gare, taxi) VALUES (1, '0675489030');
insert into Gare_Taxi (gare, taxi) VALUES (1, '0698637204');
insert into Gare_Taxi (gare, taxi) VALUES (5, '0719085803');
insert into Gare_TransPublic (gare, transport) VALUES (1,'1');
insert into Gare_TransPublic (gare, transport) VALUES (1,'172');
insert into Gare_Hotel (gare, hotel) VALUES (1, 1);

insert into Ligne (gare_depart, gare_arrive) VALUES (1, 2);
insert into Ligne (gare_depart, gare_arrive) VALUES (6, 5);

insert into TypeTrain (nom, nbr_places_max, premiere_classe, vitesse_max) VALUES ('TGV', 540, TRUE, 350);
insert into TypeTrain (nom, nbr_places_max, premiere_classe, vitesse_max) VALUES ('TER', 240, TRUE, 280);

insert into Voyage (debut_periode, fin_periode, ligne, type_train) VALUES ('2020/02/12', '2025/08/02', 1, 1);
insert into Voyage (debut_periode, fin_periode, ligne, type_train) VALUES ('2016/07/03', '2028/01/12', 2, 1);
insert into Voyage (debut_periode, fin_periode, ligne, type_train) VALUES ('2014/12/13', '2026/02/22', 2, 1);

/*Voyage 1 (Paris, Creil, Compiegne, Lille)*/

insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (1, 1, '08:00:00', '07:40:00');
insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (1, 4, '08:40:00', '08:35:00');
insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (1, 3, '09:00:00', '08:55:00');
insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (1, 2, '10:00:00', '09:30:00');

/*Voyage 2 (Paris, Marseille)*/

insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (2, 6, '11:00:00', '10:30:00');
insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (2, 5, '14:45:00', '14:10:00');

/*Voyage 3 (Paris, Grenoble, Marseille)*/

insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (3, 6, '06:00:00', '05:50:00');
insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (3, 7, '08:15:00', '08:00:00');
insert into Dessert (voyage, gare, heure_depart, heure_arrive) VALUES (3, 5, '09:35:00', '09:20:00');

insert into Dessert_Hebdomadaire (jour) VALUES ('Lundi');
insert into Dessert_Hebdomadaire (jour) VALUES ('Mardi');
insert into Dessert_Hebdomadaire (jour) VALUES ('Mercredi');
insert into Dessert_Hebdomadaire (jour) VALUES ('Jeudi');
insert into Dessert_Hebdomadaire (jour) VALUES ('Vendredi');
insert into Dessert_Hebdomadaire (jour) VALUES ('Dimanche');

insert into Jour_Voyage (voyage, jour) VALUES (1, 'Lundi');
insert into Jour_Voyage (voyage, jour) VALUES (1, 'Dimanche');
insert into Jour_Voyage (voyage, jour) VALUES (2, 'Jeudi');
insert into Jour_Voyage (voyage, jour) VALUES (2, 'Mardi');
insert into Jour_Voyage (voyage, jour) VALUES (3, 'Mercredi');
insert into Jour_Voyage (voyage, jour) VALUES (3, 'Vendredi');

insert into DateException (jour) VALUES ('2023/05/01');
insert into DateException (jour) VALUES ('2023/05/08');

insert into Exception_Voyage (voyage, jour) VALUES (1, '2023/05/01');
insert into Exception_Voyage (voyage, jour) VALUES (1, '2023/05/08');

insert into Train (num, type) VALUES (1876, 1);
insert into Train (num, type) VALUES (7250, 1);
insert into Train (num, type) VALUES (5238, 2);

INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, role) VALUES ('admin', 'admin123', 'admin');
INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, role) VALUES ('gestionnaire', 'gestionnaire123', 'gestionnaire');
INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, role) VALUES ('client1', 'client123', 'client');
INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, role) VALUES ('client2', 'client123', 'client');
INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, role) VALUES ('client3', 'client123', 'client');
INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, role) VALUES ('client4', 'client123', 'client');

insert into Voyageur (nom, prenom, adresse, telephone, type,utilisateur) VALUES ('Jean', 'Dupont', 'rue des potiers', '0765325678', 'Occasionnel',3);
insert into Voyageur (nom, prenom, adresse, telephone, type, num_carte, statut,utilisateur) VALUES ('Michelle', 'Hernandez', 'rue des fleurs', '0953678497', 'Regulier', 192873,'platine',4);
INSERT INTO Voyageur (nom, prenom, adresse, telephone, type, num_carte, statut,utilisateur) VALUES ('Martin', 'Marie', '456 Avenue des Champs-Élysées, Paris', '0145678901', 'Regulier', 123456, 'bronze',5);
INSERT INTO Voyageur (nom, prenom, adresse, telephone, type,utilisateur) VALUES ('Garcia', 'Pedro', '789 Rue du Bac, Paris', '0123456789', 'Occasionnel',6);

insert into Billet (prix, moyen_paiement, assurance, voyageur) VALUES (50, 'carte bleue', FALSE, 1);
insert into Billet (prix, moyen_paiement, assurance, voyageur) VALUES (140, 'carte bleue', FALSE, 1);
insert into Billet (prix, moyen_paiement, assurance, voyageur) VALUES (20, 'carte bleue', TRUE, 2);

/*Trajet du voyageur 1 Paris Lille*/

insert into Trajet (voyage, billet, date, num_place, gare_depart, heure_depart, gare_arrive, heure_arrive, train)
  VALUES (1, 1,'2023/09/10', 35, 1, '08:00:00', 2, '09:30:00', 1876);

/*Trajet du voyageur 1 Paris Grenoble*/

insert into Trajet (voyage, billet, date, num_place, gare_depart, heure_depart, gare_arrive, heure_arrive, train)
  VALUES (3, 2,'2023/09/14', 42, 6, '06:00:00', 7, '08:00:00', 7250);

/*Trajet du voyageur 2 Paris Marseille*/

insert into Trajet (voyage, billet, date, num_place, gare_depart, heure_depart, gare_arrive, heure_arrive, train)
  VALUES (2, 3,'2023/05/20', 21, 6, '11:00:00', 5, '14:10:00', 5238);
