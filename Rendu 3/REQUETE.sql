/*Requête qui retourne la liste des voyages qui desservent deux gare. (Donc avec deux gares données) */

SELECT v.id as Voyage, g1.nom as Gare_depart, d1.heure_depart, g2.nom as Gare_arrivee, d2.heure_arrive, STRING_AGG(CAST(jv.jour AS VARCHAR), ', ') as Jours
FROM Voyage v
JOIN Dessert d1 ON v.id = d1.voyage
JOIN Gare g1 ON d1.gare = g1.id
JOIN Dessert d2 ON v.id = d2.voyage
JOIN Gare g2 ON d2.gare = g2.id
JOIN Jour_Voyage jv ON v.id = jv.voyage
WHERE g1.nom = 'Paris gare de Lyon' /*[Gare de départ]*/
AND g2.nom = 'Gare de Marseille' /*[Gare d'arrivée]*/
AND d1.heure_depart < d2.heure_arrive
GROUP BY v.id, g1.nom, d1.heure_depart, g2.nom, d2.heure_arrive
ORDER BY d1.heure_depart;


/*Requête qui retourne la liste des gares Desservies par un voyage quelconque ici le 3.
Cela permet aux voyageurs d'avoir le détail d'un trajet trouvé avec la requete précédente*/

SELECT Gare.nom, heure_arrive, heure_depart  FROM Dessert
INNER JOIN Voyage on Voyage.id = Dessert.voyage
INNER JOIN Gare on Dessert.gare = Gare.id
WHERE voyage.id = 3 /*[VOYAGE_ID]*/
ORDER BY heure_depart;

/*Requête qui retourne la liste des trajets d'un voyageur avec s'il y'a assurance ou non et la durée des trajets (on affiche également l'id du billet car on peut avoir plusieurs trajets sur 1 billet)*/

SELECT b.id as billet, t.date, g1.nom as Gare_depart,t.heure_depart, g2.nom as Gare_arrivee, t.heure_arrive, d.duree,
       CASE WHEN b.assurance = TRUE THEN 'Oui' ELSE 'Non' END AS assurance
FROM Billet b
INNER JOIN Trajet t ON b.id = t.id
INNER JOIN duree_trajet d ON d.id = t.id
JOIN Gare g1 ON t.gare_depart = g1.id
JOIN Gare g2 ON t.gare_arrive = g2.id
WHERE b.voyageur = 1 /*[ID_VOYAGEUR]*/
ORDER BY t.date;

/*Requête qui retourne le nombre de voyageur par Ligne, trié par ordre décroissant (pour savoir quels Lignes sont les plus populaires)*/

SELECT l.id as id_ligne, COUNT(*) as nombre_voyageurs
FROM Billet b
INNER JOIN Trajet t ON b.id = t.billet
INNER JOIN Voyage v ON t.voyage = v.id
INNER JOIN Ligne l ON v.ligne = l.id
GROUP BY l.id
ORDER BY nombre_voyageurs DESC;

/*Requête qui effectue la même chose que la précédente avec le nb de voyageur dans les trains.
Cela peut-être utile pour connaitre le nombre exact de passager et le taux de remplissage des trains.*/

SELECT t.train, COUNT(*) as nombre_voyageurs, nbr_places_max - COUNT(*) as nb_places_restantes
FROM Billet b
INNER JOIN Trajet t ON b.id = t.billet
INNER JOIN Train on t.train = train.num
INNER JOIN TypeTrain type ON Train.type = type.id
GROUP BY t.train, nbr_places_max
ORDER BY nombre_voyageurs DESC;
