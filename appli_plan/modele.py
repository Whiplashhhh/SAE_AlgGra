# comment affecter à une case les produits contenus
import sys
import json
import os
from PyQt6.QtWidgets import QMessageBox

class MagasinModele:
    """Gestion des catégories et de l'affectation des produits aux cases."""

    def __init__(self, chemin_json: str):
        # Charge les produits par catégorie depuis le JSON
        with open(chemin_json, encoding="utf-8") as f:
            self.categories = json.load(f)
        # Dictionnaire (ligne, colonne) -> [produits]
        self.cases: dict[tuple[int, int], list[str]] = {}

    # --- méthodes d'affectation ------------------------------------------------
    def affecter_produits(self, ligne: int, colonne: int, produits: list[str]):
        self.cases[(ligne, colonne)] = produits

    def ajouter_produit(self, ligne: int, colonne: int, produit: str):
        self.cases.setdefault((ligne, colonne), []).append(produit)

    # --- méthodes de consultation ---------------------------------------------
    def get_produits(self, ligne: int, colonne: int) -> list[str]:
        return self.cases.get((ligne, colonne), [])

    def get_categories(self) -> list[str]:
        return list(self.categories.keys())

    def get_produits_categorie(self, categorie: str) -> list[str]:
        return self.categories.get(categorie, [])

    # --- affichage -------------------------------------------------------------
    def afficher_produits_case(self, ligne: int, colonne: int):
        produits = self.get_produits(ligne, colonne)
        if produits:
            texte = (
                f"Produits dans la case (Ligne {ligne + 1}, Colonne {colonne + 1}) :\n"
                + "\n".join(produits)
            )
        else:
            texte = (
                f"Aucun produit dans la case (Ligne {ligne + 1}, Colonne {colonne + 1})."
            )
        msg = QMessageBox()
        msg.setWindowTitle("Produits de la case")
        msg.setText(texte)
        msg.exec()


# Exemple d'utilisation :
if __name__ == "__main__":
    chemin = os.path.join(os.path.dirname(__file__), "..", "Liste_produits", "liste_produits.json")
    chemin = os.path.abspath(chemin)
    modele = MagasinModele(chemin)
    # Affecter des produits à la case (0, 0)
    modele.affecter_produits(0, 0, ["Ail", "Oignons"])
    # Ajouter un produit à la case (0, 0)
    modele.ajouter_produit(0, 0, "Carotte")
    # Afficher les produits de la case (0, 0)
    print(modele.get_produits(0, 0))
    # Afficher les catégories
    print(modele.get_categories())
    # Afficher les produits d'une catégorie
    print(modele.get_produits_categorie("Légumes"))