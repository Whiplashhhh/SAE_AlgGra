import json

class MagasinModele:
    def __init__(self, fichier_positions, fichier_produits):
        self.test_positions_categories = {}
        self.test_produits_par_categories = {}
        self.charger_positions(fichier_positions)
        self.charger_produits(fichier_produits)

    def charger_positions(self, fichier_positions):
        """Charge les positions avec les catégories depuis un fichier JSON."""
        with open(fichier_positions, 'r', encoding='utf-8') as fichier:
            self.test_positions_categories = json.load(fichier)

    def charger_produits(self, fichier_produits):
        """Charge la liste des produits par catégorie depuis un fichier JSON."""
        with open(fichier_produits, 'r', encoding='utf-8') as fichier:
            self.test_produits_par_categories = json.load(fichier)

    def get_produits_dans_case(self, colonne_str, ligne):
        """Retourne la liste des produits de la catégorie présente dans la case."""
        cle = f"{colonne_str},{ligne}"
        categorie = self.test_positions_categories.get(cle, None)
        if categorie:
            return self.test_produits_par_categories.get(categorie, [])
        else:
            return []

    def afficher_produits_case(self, colonne_str, ligne):
        """Affiche les produits d'une case pour tester."""
        produits = self.get_produits_dans_case(colonne_str, ligne)
        if produits:
            print(f"Produits dans la case {colonne_str}{ligne} ({self.test_positions_categories[f'{colonne_str},{ligne}']}): {', '.join(produits)}")
        else:
            print(f"Aucun produit dans la case {colonne_str}{ligne}")
