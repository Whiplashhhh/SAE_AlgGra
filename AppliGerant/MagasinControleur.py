# =================== CONTROLLER : MagasinControleur.py =====================
# Auteurs : Willem VANBAELINGHEM--DEZITTER, Alex FRANCOIS
# Rôle : S
# ===============ert d'interface entre la vue et le modèle, gère les actions utilisateur===========================================================

class MagasinControleur:
    """
    Le contrôleur fait le lien entre la vue (IHM) et le modèle (données).
    """
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue

    def get_produits_de_case(self, ligne, colonne):
        """
        Fonction appelé quand une case est cliqué, va donner à MagasinVue, la case, les produits et la catégorie de la case cliquée
        """
        if colonne < 26:#On transforme la colonne en lettre
            lettre_colonne = chr(ord('A') + colonne)
        else:
            lettre_colonne = 'A' + chr(ord('A') + (colonne - 26))
        key = f"{ligne+1},{lettre_colonne}"

        #Récupération des produits par catégorie
        categorie = self.modele.positions_categories.get(key, None)
        if categorie:
            produits = self.modele.produits_par_categories.get(categorie, [])
            return produits, key, categorie
        else:
            return [], key, None
        
    # Fonction pour ajouter un produits dans une catégorie
    def ajouter_produit(self, categorie, produit):
        self.modele.ajouter_produit(categorie, produit)

    def supprimer_produit(self, categorie, produit):
        self.modele.supprimer_produit(categorie, produit)

    #Reinitialise tous les produits
    def reset_produits(self):
        self.modele.reset_produits()

    def sauvegarder(self):
        self.modele.sauvegarder()