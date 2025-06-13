# Auteurs:
#   Willem VANBAELINGHEM--DEZITTER - TPA
#   Alex FRANCOIS - TPA
# date création: 010/06/2025
# dernière maj: 12/06/2025

import json

class MagasinModel:
    def __init__(self, infos_projet):
        self.infos_projet = infos_projet
    
        self.lignes = 52
        self.colonnes = 52
        
        self.fichier_produits = infos_projet["produits_par_categories"]

        # self.cases_utiles = self.load_cases_utiles(fichier_cases_utiles)
        self.positions_categories = self.charger_positions(infos_projet["positions_categories"])
        self.produits_par_categories = self.charger_produits(infos_projet["produits_par_categories"])
        self.cases_utiles = self.load_cases_utiles(infos_projet["cases_utiles"])

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
            
    def ajouter_produit(self, categorie, produit):
        if categorie in self.produits_par_categories:
            if produit not in self.produits_par_categories[categorie]:
                self.produits_par_categories[categorie].append(produit)
        else:
            self.produits_par_categories[categorie] = [produit]

    def supprimer_produit(self, categorie, produit):
        if categorie in self.produits_par_categories:
            if produit in self.produits_par_categories[categorie]:
                self.produits_par_categories[categorie].remove(produit)

    def sauvegarder(self):
        try:
            with open(self.fichier_produits, "w", encoding="utf-8") as fichier:
                json.dump(self.produits_par_categories, fichier, indent=4, ensure_ascii=False)
            print("Sauvegarde effectuée.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")