import json
import numpy as np
import os
from collections import deque

class ClientModel:
    def __init__(self):
        self.charger_fichiers()
        self.liste_courses = {}

    def charger_fichiers(self):
        base_path = os.path.dirname(__file__)

        # Chargement des produits (avec sous-catégories multiples)
        with open(os.path.join(base_path, "produits_repartis_complet_final.json"), "r", encoding="utf-8") as f:
            self.produits_par_sous_categorie = json.load(f)

        # Chargement des positions des catégories
        with open(os.path.join(base_path, "positions_categories.json"), "r", encoding="utf-8") as f:
            self.positions_categories = json.load(f)

        # Génération d'une table produit → catégorie (normalisée)
        self.produit_to_categorie = {}
        for sous_cat, produits in self.produits_par_sous_categorie.items():
            # On nettoie le nom de la catégorie : exemple "Poissonnerie1" → "Poissonnerie"
            categorie = ''.join([i for i in sous_cat if not i.isdigit()]).strip()
            for produit in produits:
                self.produit_to_categorie[produit] = categorie

        # Liste des catégories globales (nettoyées)
        self.categories = list(set(self.produit_to_categorie.values()))

        # Chargement du graphe
        with open(os.path.join(base_path, "graphe.json"), "r", encoding="utf-8") as f:
            self.graphe = json.load(f)

    def get_categories(self):
        return self.categories

    def get_produits_categorie(self, categorie):
        produits = []
        for produit, cat in self.produit_to_categorie.items():
            if cat == categorie:
                produits.append(produit)
        return sorted(produits)

    def get_tous_les_produits(self):
        return sorted(list(self.produit_to_categorie.keys()))

    def ajouter_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses[produit] += 1
        else:
            self.liste_courses[produit] = 1

    def retirer_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses[produit] -= 1
            if self.liste_courses[produit] <= 0:
                del self.liste_courses[produit]

    def effacer_liste(self):
        self.liste_courses = {}

    def sauvegarder_liste(self, fichier):
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(self.liste_courses, f, indent=4)

    def charger_liste(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            self.liste_courses = json.load(f)

    def generer_liste_aleatoire(self):
        tout = self.get_tous_les_produits()
        tout = np.array(tout)
        n = min(10, len(tout))
        indices = np.random.choice(len(tout), size=n, replace=False)
        self.liste_courses = {}
        for i in indices:
            produit = tout[i]
            self.liste_courses[produit] = 1

    def get_liste_courses(self):
        return self.liste_courses

    def get_coords_produits(self, produits):
        coords = []
        for produit in produits:
            categorie = self.produit_to_categorie.get(produit)
            if categorie:
                coord = self.positions_categories.get(categorie)
                if coord:
                    coords.append(coord)
        return coords

    def dijkstra(self, depart):
        file = deque([[depart]])
        dico = {depart: (0, [depart])}

        while file:
            chemin = file.popleft()
            sommet = chemin[-1]
            voisins = self.graphe.get(sommet, [])
            for voisin in voisins:
                nouvelle_distance = dico[sommet][0] + 1
                nouveau_chemin = chemin + [voisin]
                if voisin not in dico or nouvelle_distance < dico[voisin][0]:
                    dico[voisin] = (nouvelle_distance, nouveau_chemin)
                    file.append(nouveau_chemin)
        return dico

    def get_chemin(self, depart, produits):
        coords_produits = self.get_coords_produits(produits)
        print("Coords produits trouvées :", coords_produits)  # pour debug
        chemin_final = []
        position_actuelle = depart
        produits_restants = coords_produits.copy()

        while produits_restants:
            dico_chemin = self.dijkstra(position_actuelle)
            prochain = min(produits_restants, key=lambda c: dico_chemin[c][0])
            chemin_final += dico_chemin[prochain][1][1:]
            position_actuelle = prochain
            produits_restants.remove(prochain)

        dico_retour = self.dijkstra(position_actuelle)
        chemin_final += dico_retour[depart][1][1:]
        return [depart] + chemin_final
