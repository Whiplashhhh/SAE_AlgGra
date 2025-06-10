# Auteur:
#   Romain Théobald - TPB
# création -> 10/06/2025
# dernière MAJ -> 10/06/2025
import json
import numpy as np

class ModeleProduits:
    def __init__(self, chemin_json):
        self.chemin_json = chemin_json
        self.categories = []
        self.produits = {}
        self.liste_course = []
        self.charger_donnees()

    def charger_json(self):
        """Recharge les données depuis le JSON."""
        self.charger_donnees()

    def ajouter_produit(self, produit):
        """Ajoute un produit à la liste de course s'il n'y est pas déjà."""
        if produit not in self.liste_course:
            self.liste_course.append(produit)

    def retirer_produit(self, produit):
        """Retire un produit de la liste de course s'il y est."""
        if produit in self.liste_course:
            self.liste_course.remove(produit)

    def get_liste_course(self):
        """Retourne la liste des produits de la liste de course."""
        return self.liste_course

    def charger_liste_course(self):
        """Affiche la liste de course sous forme de tableau (liste de tuples index, produit)."""
        return list(enumerate(self.liste_course, 1))

    def get_positions(self):
        """Retourne les positions (indices) des produits dans la liste de course."""
        return {produit: idx for idx, produit in enumerate(self.liste_course)}
