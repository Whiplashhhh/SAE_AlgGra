import json
import numpy as np
import os

class ClientModel:
    def __init__(self):
        self.charger_fichiers()
        self.liste_courses = {}

    def charger_fichiers(self):
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, "produits_par_sous_catégori.json"), "r", encoding="utf-8") as f:
            self.sous_categories = json.load(f)
        with open(os.path.join(base_path, "produits_repartis_complet_final.json"), "r", encoding="utf-8") as f:
            self.produits_par_sous_categorie = json.load(f)
        self.categories = list(self.sous_categories.keys())

    def get_categories(self):
        return self.categories

    def get_produits_categorie(self, categorie):
        produits = []
        sous_cats = self.sous_categories.get(categorie, [])
        for sous_cat in sous_cats:
            produits.extend(self.produits_par_sous_categorie.get(sous_cat, []))
        return sorted(set(produits))

    def get_tous_les_produits(self):
        tous = []
        for cat in self.categories:
            tous.extend(self.get_produits_categorie(cat))
        return sorted(set(tous))

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
