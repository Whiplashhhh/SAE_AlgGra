class MagasinControleur:
    def __init__(self, modele):
        self.modele = modele

    def charger_produits_case(self, coord):
        categorie = self.modele.get_categorie(coord)
        if categorie:
            return self.modele.get_produits(categorie)
        return []

    def ajouter_produit_case(self, coord, produit):
        categorie = self.modele.get_categorie(coord)
        if categorie:
            self.modele.ajouter_produit(categorie, produit)
            return True
        return False

    def supprimer_produit_case(self, coord, produit):
        categorie = self.modele.get_categorie(coord)
        if categorie:
            self.modele.supprimer_produit(categorie, produit)
            return True
        return False

    def sauvegarder_modifications(self):
        self.modele.sauvegarder()
