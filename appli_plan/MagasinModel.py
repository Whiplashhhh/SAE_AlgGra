import json

class MagasinModel:
    def __init__(self, json_file, largeur_plan=1000, hauteur_plan=1000):
        self.largeur_plan = largeur_plan
        self.hauteur_plan = hauteur_plan
        self.lignes = 52
        self.colonnes = 52
        self.tailleX = largeur_plan / self.colonnes
        self.tailleY = hauteur_plan / self.lignes
        self.cases_utiles = self.load_cases_utiles(json_file)

    def load_cases_utiles(self, json_file):
        '''Charge les cases utiles depuis un fichier JSON'''
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
            return set(data.keys())
        except FileNotFoundError:
            print(f"Erreur : fichier {json_file} introuvable.")
            return set()

    def get_case_coordinates(self, ligne, colonne):
        '''Retourne les coordonnées d'une case'''
        x = colonne * self.tailleX
        y = ligne * self.tailleY
        return x, y, self.tailleX, self.tailleY

    def is_case_util(self, ligne, colonne):
        '''Vérifie si une case est utile'''
        coord = f"{ligne+1},{chr(ord('A') + colonne) if colonne < 26 else 'A' + chr(ord('A') + colonne - 26)}"
        return coord in self.cases_utiles