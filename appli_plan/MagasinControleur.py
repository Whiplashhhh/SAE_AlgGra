# Auteurs:
#   Willem VANBAELINGHEM--DEZITTER - TPA
# date création: 10/06/2025
# dernière maj: 12/06/2025

class MagasinControleur:
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue

    def get_produits_de_case(self, ligne, colonne):
        if colonne < 26:
            lettre_colonne = chr(ord('A') + colonne)
        else:
            lettre_colonne = 'A' + chr(ord('A') + (colonne - 26))
        key = f"{ligne+1},{lettre_colonne}"

        categorie = self.modele.positions_categories.get(key, None)
        if categorie:
            produits = self.modele.produits_par_categories.get(categorie, [])
            return produits, key, categorie
        else:
            return [], key, None

    def ajouter_produit(self, categorie, produit):
        self.modele.ajouter_produit(categorie, produit)

    def supprimer_produit(self, categorie, produit):
        self.modele.supprimer_produit(categorie, produit)

    def sauvegarder(self):
        self.modele.sauvegarder()