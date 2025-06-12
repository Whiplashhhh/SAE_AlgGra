import json

class MagasinModel:
    def __init__(self, fichier_cases_utiles, fichier_positions, fichier_produits, largeur_plan=1000, hauteur_plan=1000):
        self.largeur_plan = largeur_plan
        self.hauteur_plan = hauteur_plan
        self.lignes = 52
        self.colonnes = 52
        self.tailleX = largeur_plan / self.colonnes
        self.tailleY = hauteur_plan / self.lignes

        self.cases_utiles = self.load_cases_utiles(fichier_cases_utiles)
        self.positions_categories = self.charger_positions(fichier_positions)
        self.produits_par_categories = self.charger_produits(fichier_produits)

    def load_cases_utiles(self, fichier_cases_utiles):
        try:
            with open(fichier_cases_utiles, "r", encoding="utf-8") as f:
                data = json.load(f)
            return set(data.keys())
        except FileNotFoundError:
            print(f"Erreur : fichier {fichier_cases_utiles} introuvable.")
            return set()

    def charger_positions(self, fichier_positions):
        try:
            with open(fichier_positions, "r", encoding="utf-8") as fichier:
                data = json.load(fichier)
                
                return data
        except FileNotFoundError:
            print(f"Erreur : fichier {fichier_positions} introuvable.")
            return {}

    def charger_produits(self, fichier_produits):
        try:
            with open(fichier_produits, "r", encoding="utf-8") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            print(f"Erreur : fichier {fichier_produits} introuvable.")
            return {}

    def is_case_util(self, ligne, colonne):
        coord = f"{ligne+1},{chr(ord('A') + colonne) if colonne < 26 else 'A' + chr(ord('A') + (colonne - 26))}"
        return coord in self.cases_utiles

    def get_produits_dans_case(self, colonne_str, ligne):
        cle = f"{colonne_str},{ligne}"
        categorie = self.positions_categories.get(cle, None)
        if categorie:
            return self.produits_par_categories.get(categorie, [])
        else:
            return []

    def afficher_produits_case(self, key):
        if key in self.positions_categories:
            categorie = self.positions_categories[key]
            produits = self.produits_par_categories.get(categorie, [])
            print(f"Produits dans la case {key} : {produits}")
        else:
            print(f"Aucun produit dans la case {key}")