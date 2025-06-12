import json

class MagasinModel:
    def __init__(self, fichier_positions, fichier_produits):
        self.positions_categories = self.charger_json(fichier_positions)
        self.produits_par_categories = self.charger_json(fichier_produits)
        self.fichier_produits = fichier_produits

    def charger_json(self, chemin):
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def sauvegarder(self):
        with open(self.fichier_produits, 'w', encoding='utf-8') as f:
            json.dump(self.produits_par_categories, f, indent=4, ensure_ascii=False)

    def get_categorie(self, coord):
        return self.positions_categories.get(coord, None)

    def get_produits(self, categorie):
        return self.produits_par_categories.get(categorie, [])

    def ajouter_produit(self, categorie, produit):
        self.produits_par_categories.setdefault(categorie, [])
        if produit not in self.produits_par_categories[categorie]:
            self.produits_par_categories[categorie].append(produit)

    def supprimer_produit(self, categorie, produit):
        if categorie in self.produits_par_categories:
            if produit in self.produits_par_categories[categorie]:
                self.produits_par_categories[categorie].remove(produit)
