import json
import numpy as np

class MagasinModel2:
    def __init__(self):
        self.charger_graphe()
        self.charger_positions()
        self.charger_produits()
        self.liste_courses = []

    def charger_graphe(self):
        with open("graphe.json", "r", encoding="utf-8") as f:
            self.graphe = json.load(f)

    def charger_positions(self):
        with open("positions_categories.json", "r", encoding="utf-8") as f:
            self.positions = json.load(f)

    def charger_produits(self):
        with open("produits_repartis_complet_final.json", "r", encoding="utf-8") as f:
            self.produits_par_categorie = json.load(f)

    def get_categories(self):
        return list(self.produits_par_categorie.keys())

    def get_produits_categorie(self, categorie):
        return self.produits_par_categorie[categorie]

    def ajouter_produit(self, produit):
        if produit not in self.liste_courses:
            self.liste_courses.append(produit)

    def retirer_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses.remove(produit)

    def sauvegarder_liste(self, chemin_fichier):
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(self.liste_courses, f, indent=4)

    def charger_liste(self, chemin_fichier):
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            self.liste_courses = json.load(f)

    def generer_liste_aleatoire(self, n=10):
        tout = []
        for produits in self.produits_par_categorie.values():
            tout.extend(produits)
        tout = np.array(tout)
        if len(tout) <= n:
            self.liste_courses = tout.tolist()
        else:
            indices = np.random.choice(len(tout), size=n, replace=False)
            self.liste_courses = tout[indices].tolist()

    def get_position_produit(self, produit):
        for case, categorie in self.positions.items():
            if produit in self.produits_par_categorie.get(categorie, []):
                return case

