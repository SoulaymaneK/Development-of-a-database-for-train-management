# D4_G3 - Projet NF18



## Gestion des trains

Votre client est une société de chemins de fer, qui souhaite mettre en place un système pour gérer ses gares, ses trains, ses lignes de trains et ses billets. Les gares ont un nom, une adresse, une ville, et une zone horaire (GMT). Il est possible que plusieurs gares aient le même nom. Cependant, les noms des gares d'une même ville sont tous différents.

Les trains sont caractérisés par un numéro et un type (TGV, TER, etc.), ce dernier conditionnant le nombre de places maximal dans le train, les classes disponibles (première et seconde ou seulement seconde), sa vitesse maximale, etc.

La société gère des lignes de trains qui relient une gare de départ à une gare terminus. Sur chaque ligne sont programmés un ou plusieurs voyages. A un voyage sont associées des heures de départ et d'arrivée dans chaque gare qu'il dessert, en sachant qu'il ne s'arrête pas forcément dans toutes les gares de la ligne. Les voyages sont programmés de manière périodique selon un calendrier hebdomadaire (par exemple, on programme un train Paris-Compiègne à 10 heures du matin, chaque jour sauf le dimanche, sur la période du 01/02/2018 au 20/04/2018). Néanmoins, il est possible d'avoir des dates d'exception (jours fériés par exemple) où on supprime/ajoute des voyages. Les voyages d'une même ligne sont assurés par un type de train spécifique.

La réservation de billet est faite par un voyageur, dont on veut garder le nom, prénom, adresse, numéro de téléphone, et le moyen de paiement utilisé pour le billet (carte bleue, espèce, chèque, etc.). Un billet peut être composé de plusieurs trajets. Le billet comporte pour chaque trajet une gare et une heure de départ, une gare et une heure d'arrivée, une durée, ainsi que le numéro de train et le numéro de place. Qui plus est, il est possible de prendre avec le billet une assurance pour pouvoir l'annuler ou modifier les dates gratuitement, autrement, la modification n'est pas possible et 20% du prix du billet est retenu lors l'annulation. Lors de la réservation du billet, le système de réservation peut proposer des adresses d'hôtels à proximité de la gare d'arrivée du voyageur, ainsi que des taxis ou encore des informations sur les transports publics.

Il existe deux types de voyageurs : les voyageurs occasionnels et les voyageurs réguliers, qui ont une carte numérotée et un statut (bronze, silver, gold, platine...).

## Objectifs

La société de chemin de fer vous demande de mettre en place une base de données et un système de gestion qui permet :

• De gérer les gares, les lignes de trains, les trains et leurs itinéraires ;

• Aux clients, de consulter les horaires des trains et chercher des trajets en fonction des villes de
départ et d'arrivée, des dates du voyage, et de facteurs de prix (prix minimum ou maximum) ;

• Aux clients, de réserver des billets, d'annuler leurs réservations ou de les modifier (au plus tard
le jour du départ) ;

• D'obtenir des statistiques sur le fonctionnement de la société : taux de remplissage des trains,
gares les plus fréquentées, les lignes les plus empruntées, etc.
