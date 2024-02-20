# <u>Modèle Logique de Données de notre réseau ferroviaire</u>

___Tous les attributs sont NOT NULL par défaut.___

## <u>Définition d'une gare</u>

<span style="font-size:1.2em;"> - **Gare** (<u>#id : int</u>, nom : str, adresse : str, ville : str, zoneHoraire : str)</span>
>- **Avec UNIQUE (nom, adresse, ville).**

### _Relations avec Gare_
- **Taxi** (<u>#téléphone : str(10)</u>)
- **TransportPublic** (<u>#ligne : str</u>, desc : str)
- **Hotel** (<u>#id :int</u>, nom : str, adresse : str) 
- **Gare_Hotel** (<u>#gare => Gare.id, #hotel => Hotel.id</u>)
> ↑ Un hotel à proximité d'une gare.
- **Gare_TransPublic** (<u>#gare => Gare.id, #transport => TransportPublic.ligne</u>) 
> ↑ Transports public à proximité d'une gare.
- **Gare_Taxi** (<u>#gare => Gare.id, #taxi => Taxi.téléphone</u>)
> ↑ Taxi à proximité d'une gare.

<br>

## <u>Définition d'une ligne</u>
<span style="font-size:1.2em;"> - **Ligne** (<u>#id : int</u>, gare_départ => Gare.id, gare_arrivée => Gare.id) </span>

><b>Avec :
>- Gare_départ ≠ gare_arrivée,
>- UNIQUE (gare_départ, gare_arrivée). </b>

<br>

## <u>Définition d'un voyage</u>

<span style="font-size:1.2em;"> - **Voyage** (<u>#id : int</u>, début_période : date, fin_période : date, ligne => Ligne.id, type_train => TypeTrain.id) </span>
>- **Avec fin_période > début_période.** 

### _Relations avec Voyage_

- **TypeTrain** (<u>#id : int</u>, nom : str, nbr_places_max : int, première_classe : boolean, vitesse_max : int) 

- **Dessert_Hebdomadaire** (<u>#jour  : jour</u>) 
> ↑ _jour = {Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi, Dimanche}_

- **DateException** (<u>#jour : Date</u>)

- **Jour_Voyage** (<u>#voyage=> Voyage.id, #jour => DessertHebdomadaire.jour</u>)
- **Exception_Voyage** (<u>#voyage=> Voyage.id, #jour => DateException.jour</u>)


<br>

## <u>Définition d'un train</u>
<span style="font-size:1.2em;"> - **Train** (<u>#num : int</u>, type => TypeTrain.id) </span>

<br>

## <u>Définition d'un voyageur</u>

> Pour l'héritage avec Voyageur, on décide de faire un héritage par classe Mère avec un attribut type.

<span style="font-size:1.2em;"> - **Voyageur** (<u>#id : int</u>, nom : str, prénom : str, adresse : str, téléphone : str, type : str, num_carte : int, statut : str) </span>

><b>Avec :
>- type = {Régulier, Occasionnel),
>- Statut = {bronze, silver, gold, platine} et NULLABLE,
>- UNIQUE (num_carte) et NULLABLE,
>- NOT (type = Occasionnel AND num_carte AND statut), 
>- NOT (type = Régulier AND num_carte = NULL AND statut = NULL). </b>

<br>

## <u>Définition d'un billet</u>
<span style="font-size:1.2em;"> - **Billet** (<u>#id : int</u>, prix : numeric, moyen_paiment : str, assurance : boolean, voyageur => Voyageur.id) 

><b>Avec : 
> - moyen_paiment = {carte bleue, espèce, chèque},
> - Prix > 0€. </b>

<br>

## <u>Définition d'un trajet</u>
<span style="font-size:1.2em;"> - **Trajet**(<u>#id : int, #billet => Billet.id</u>, num_place : int, gare_départ => Dessert.gare, heure_départ => Dessert.heure_départ, gare_arrivée => Dessert.gare, heure_arrivée => Dessert.heure_arrivée, train => Train.num, durée : time) </span>

### _Relation avec Trajet_
- **Dessert** (<u>#voyage => Voyage.id, #gare => Gare.id</u>, heure_départ : Date, heure_arrivée : Date) 

><b>Avec :
> - heure_arrivée < heure_départ et gare_départ ≠ gare_arrivée, un train arrive dans une gare avant d'en partir dans la classe dessert
> - Durée = heure_arrivée - heure_départ > 0
(car heure_arrivée > heure_départ dans la classe trajet),
> - numPlace > 0. </b>

<br>

## <u>Conditions du MLD</u>
><b> Le ⊆ signifie "inclus dans".</b>

- Relation **1 : 1..N** entre Ligne et Voyage 
  - Projection (Ligne, id) = Projection (Voyage, ligne) 

<br>

- Relation **0..N : 1..7** entre Voyage et DateHebdomadaire
  - Projection (Voyage, id) = Projection (Exception_Voyage, voyage) 

<br>

- Relation Dessert **0..N : 2..N** entre Voyage et Gare
  - Projection (Voyage, id) = Projection (Dessert, voyage)
  - Projection (Jointure (Voyage, Ligne, Voyage.Ligne = Ligne.id), gare_départ) ⊆ Projection (Jointure (Dessert, Voyage, Voyage.id = Dessert.voyage), gare)
  - Projection (Jointure (Voyage, Ligne, Voyage.Ligne = Ligne.id), gare_arrivée) ⊆ Projection (Jointure (Dessert, Voyage, Voyage.id = Dessert.voyage), gare)

> <b>↑ Tous les voyages sont représentés dans la table Dessert et ils desservent au moins deux gares : la gare de départ et d'arrivée de la ligne à laquelle ils sont associés.</b>


- Relations **1 : 0..N** entre Trajet et Dessert
  - Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_départ), voyage) = Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_arrivée), voyage)
  - Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_départ), heure_départ) = Projection( Trajet, heure_départ)
  - Projection (Jointure (Trajet, Dessert, Dessert.gare = Trajet.gare_départ), heure_arrivée) = Projection( Trajet, heure_arrivée)
> <b>↑ La première condition fait que la gare de départ et d'arrivée dans trajet sont du même voyage.
>
> Les deux autres conditions servent à s'assurer que l'heure d'arrivée du trajet correspond à la gare d'arrivée, et pareil pour la gare et l'heure de départ. </b>

<br>

- Composition entre Trajet et Billet (⇔ Relation **1 : 1..N**)
  - Projection (Trajet, billet) = Projection (Billet, id)
