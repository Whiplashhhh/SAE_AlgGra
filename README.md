- Thomas TEITEN
- Alex FRANCOIS
- Romain THEOBALD
- Willem VANBAELINGHEM—DEZITTER

## Compte rendu 10/06/2025

Romain : Création du modèle de l’application client
Thomas : Création du fichier « algo_chemin » pour la gestion du plus court chemin pour l’application client
Willem : Gestion du zoom, Affichage du plan avec cadrillage
Alex : Ajout des coordonnées sur le cadrillage et case cliquable avec l’affichage de ses coordonnées.


## Compte rendu 11/06/2025

Romain : Création du fichier « Liste_Produits » et fichier pour la position des articles sur le plan en fonction de leur sous-catégorie.
Thomas : Modification « Liste_Produits » en sous-catégorie pour le placement des produits sur le plan et créationd’un fichier avec les catégories et leurs sous-catégories. 
Willem : Ajout de fonctionnalités pour l’application gérant (zoom du plan…), création d’un modèle pour l’application gérant. Fichier pour la position des articles sur le plan en fonction de leur sous-catégorie.
Alex : Modification « Vue_plan » pour inclure les produits sur les cases, et création du fichier pour la position des produits en fonction de leur sous catégorie.


## Compte rendu 12/06/2025

Romain : Création de l’interface pour l’application Client (Vue, Modèle, Controleur).
Thomas : Création du système qui dessine le chemin sur le plan du magasin avec l’algorithme de dijkstra.
Willem : Système de création de projet pour l’application gérant, Modification de l’interface de l’application gérant pour y inclure l’ajout et la suppression de produits.
Alex : Finition pour le fichier sur la position des produits, Modification dans MagasinVue et MagasinModel


## Compte rendu 13/06/2025

Romain : Assemblage de l’interface Application client et du système de dessin sur le plan et ajout de la fonctionnalité pour effacer le dessin en cliquant sur effacer la liste
Thomas : Assemblage de l’interface Application client et du système de dessin sur le plan.
Willem : Merge des deux applications dans la branche main et gestion des erreurs… Création d’un mot de passe pour entrer sur l’application gérant
Alex : Menu pour lancer l’une des deux applications, Création de commentaires


## Dépendances

pip install PyQt6, numpy


## Description

Ce projet est une application de gestion de magasin développée en Python avec PyQt6.  
L'application permet de :

- Gérer les informations d’un magasin (nom, auteur, adresse...)
- Visualiser un plan du magasin et y associer des produits à des emplacements précis
- Générer des parcours optimaux pour récupérer les produits d'une liste
- Gérer plusieurs projets, enregistrer/charger des configurations et supprimer des projets

## Utilisation

Pour lancer l'application :
```bash
python main.py
```
#### MOT DE PASSE DE L'APPLI GÉRANT : VinsurVin

### Cette commande lance un menu qui permet à l'utilisateur de choisir entre l'application Gérant et l'application Client.

## Fonctionnalités

Application Gérant :

- Mot de passe pour sécuriser l'application gérant.

- Zone de texte pour choisir le nom du projet.
- Zone de texte pour choisir l'auteur.
- Zone de texte pour choisir le nom et une autre pour l'adresse du magasin.

- Un premier bouton permet d'ajouter au projet une image du plan du magasin.
- Un deuxième bouton permet de valider et de créer le projet.
- Le dernier bouton permet de charger un projet déjà existant que l'utilisateur a déjà sauvegardé.

Application Client :

- La partie gauche correspond au plan du magasin.
- Lorsque l'on clique sur une catégorie, la liste des produits de celle-ci apparaît dans produits disponibles. Il est possible de rechercher un produit dans la barre de recherche.
- Lorsque l'on clique sur un produit, il est ajouté à la liste de courses et met à jour le nombre d'articles.

- Les boutons permettent de charger une liste de courses, l'effacer et la sauvegarder.
- Il est possible d'en créer une avec des articles choisis aléatoirement.
- Le bouton "C'est parti !" permet de lancer le dessin du chemin. Ce chemin est fait avec l'algorithme de dijkstra pour trouver le chemin le plus court entre les points.

## Ce que nous aurions aimé faire si nous avions eu plus de temps

- Nous aurions aimé implanter un système de prix pour chaque article afin d'avoir le coût final de notre liste de courses en plus du chemin.
- faire une grille ajustable avec un système qui reconnait automatiquement le rayon présent sur une case
- améliorer le côté grapique en optimisant les placements des widgets
- ajouter la possibilité de déplacer soi-même les widgets 
- ajouter la possibilité de changer de thème (clair, sombre)
- faire une barre de menu qui aurait regroupé les bouton de sauvegarde ou de charge
