# ====================== MODEL : MagasinModel.py ======================
# Auteurs : Willem VANBAELINGHEM--DEZITTER, Alex FRANCOIS
# Rôle : Gère toutes les données du projet (catégories, produits, positions, cases utiles)
# ====================================================================

import json

class MagasinModel:
    """
    Le modèle gère toutes les données et la logique associée.
    """
    def __init__(self, infos_projet):
        # infos_projet : dict contenant les chemins des fichiers et infos générales du projet
        self.infos_projet = infos_projet
        self.lignes = 52
        self.colonnes = 52

        # Chargement des données du projet
        self.positions_categories = self._charger_json(self.infos_projet["positions_categories"])
        self.produits_par_categories = self._charger_json(self.infos_projet["produits_par_categories"])
        self.cases_utiles = set(self._charger_json(self.infos_projet["cases_utiles"]).keys())

        # On retient le fichier où sauvegarder les produits
        self.fichier_produits = self.infos_projet["produits_par_categories"]

    def _charger_json(self, chemin):
        """
        Charge un fichier JSON et renvoie le contenu sous forme de dict.
        """
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Erreur : fichier {chemin} introuvable.")
            return {}

    def is_case_util(self, ligne, colonne):
        """
        Renvoie True si la case (ligne, colonne) est accessible/utile, False sinon.
        """
        coord = f"{ligne+1},{chr(ord('A')+colonne) if colonne < 26 else 'A'+chr(ord('A')+colonne-26)}"
        return coord in self.cases_utiles

    def get_produits_dans_case(self, ligne, colonne):
        """
        Renvoie la liste des produits pour une case précise (ligne, colonne).
        """
        key = f"{ligne+1},{chr(ord('A')+colonne) if colonne < 26 else 'A'+chr(ord('A')+colonne-26)}"
        categorie = self.positions_categories.get(key, None)
        if categorie:
            return self.produits_par_categories.get(categorie, [])
        return []

    def ajouter_produit(self, categorie, produit):
        """
        Ajoute un produit à une catégorie, évite les doublons.
        """
        if categorie in self.produits_par_categories:
            if produit not in self.produits_par_categories[categorie]:
                self.produits_par_categories[categorie].append(produit)
        else:
            self.produits_par_categories[categorie] = [produit]

    def supprimer_produit(self, categorie, produit):
        """
        Supprime un produit d'une catégorie s'il existe.
        """
        if categorie in self.produits_par_categories and produit in self.produits_par_categories[categorie]:
            self.produits_par_categories[categorie].remove(produit)

    def reset_produits(self):
        """
        Vide tous les produits placés dans le magasin.
        """
        for cat in self.produits_par_categories:
            self.produits_par_categories[cat] = []

    def sauvegarder(self):
        """
        Sauvegarde l'état actuel des produits par catégorie dans le fichier prévu.
        """
        try:
            with open(self.fichier_produits, "w", encoding="utf-8") as f:
                json.dump(self.produits_par_categories, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")