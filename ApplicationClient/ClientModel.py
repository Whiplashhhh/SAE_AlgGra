import json
import os
import numpy as np  

class ClientModel:
    def __init__(self):
        self.charger_fichiers()
        self.liste_courses = {}
        with open("position_produit.json", encoding="utf-8-sig") as f:
            self.produit_position = json.load(f)
        with open("graphe.json", encoding="utf-8-sig") as f:
            self.graphe = json.load(f)
        with open("sous_categorie_produits.json", encoding="utf-8-sig") as f:
            self.souscat_produits = json.load(f)
        # Liste des caisses
        self.caisses = [
            "44,AH", "44,AF", "44,AE", "44,AC", "44,AB",
            "44,Z", "44,Y", "44,W", "44,T", "44,S", "44,Q", "44,P", "44,O", "44,M"
        ]

    def charger_fichiers(self):
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, "produits_par_sous_catégori.json"), "r", encoding="utf-8") as f:
            self.sous_categories = json.load(f)
        with open(os.path.join(base_path, "produits_repartis_complet_final.json"), "r", encoding="utf-8") as f:
            self.produits_par_sous_categorie = json.load(f)
        self.categories = list(self.sous_categories.keys())

    def get_categories(self):
        return self.categories

    def get_produits_categorie(self, categorie):
        produits = []
        sous_cats = self.sous_categories.get(categorie, [])
        for sous_cat in sous_cats:
            produits.extend(self.produits_par_sous_categorie.get(sous_cat, []))
        return sorted(set(produits))

    def get_tous_les_produits(self):
        tous = []
        for cat in self.categories:
            tous.extend(self.get_produits_categorie(cat))
        return sorted(set(tous))

    def ajouter_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses[produit] += 1
        else:
            self.liste_courses[produit] = 1

    def retirer_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses[produit] -= 1
            if self.liste_courses[produit] <= 0:
                del self.liste_courses[produit]

    def effacer_liste(self):
        self.liste_courses = {}

    def sauvegarder_liste(self, fichier):
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(self.liste_courses, f, indent=4)

    def charger_liste(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            self.liste_courses = json.load(f)

    def generer_liste_aleatoire(self):
        tout = self.get_tous_les_produits()
        tout = np.array(tout)
        n = min(10, len(tout))
        indices = np.random.choice(len(tout), size=n, replace=False)
        self.liste_courses = {}
        for i in indices:
            produit = tout[i]
            self.liste_courses[produit] = 1

    def get_liste_courses(self):
        return self.liste_courses
    
    def get_coords_produits(self, produits):
        # Renvoie la liste des coordonnées sous forme de string "ligne,colonne"
        res = []
        for prod in produits:
            for souscat, plist in self.souscat_produits.items():
                if prod in plist:
                    for k, v in self.produit_position.items():
                        if v == souscat:
                            res.append(k)
                            break
        return res

    def get_chemin(self, depart, produits, dijkstra):
        # Récupère les coordonnées des produits à prendre
        points_a_visiter = self.get_coords_produits(produits)
        if not points_a_visiter:
            return []

        chemin_total = [depart]
        courant = depart
        a_faire = points_a_visiter.copy()
        
        # On fait un algo nearest neighbor (on va tjrs au plus proche suivant)
        while a_faire:
            best_dist = float('inf')
            best_pt = None
            best_chemin = []
            for pt in a_faire:
                res = dijkstra(self._format_graphe(), courant)
                if pt in res and res[pt][0] < best_dist:
                    best_dist = res[pt][0]
                    best_pt = pt
                    best_chemin = res[pt][1]
            if not best_pt:
                break  # Impossible d’aller à la suite
            # On ajoute le chemin (sans dupliquer la position courante)
            chemin_total += best_chemin[1:]
            courant = best_pt
            a_faire.remove(best_pt)
        
        # À la fin, va à la caisse la plus proche
        best_caisse = None
        best_dist = float('inf')
        best_chemin = []
        res = dijkstra(self._format_graphe(), courant)
        for caisse in self.caisses:
            if caisse in res and res[caisse][0] < best_dist:
                best_dist = res[caisse][0]
                best_caisse = caisse
                best_chemin = res[caisse][1]
        if best_caisse:
            chemin_total += best_chemin[1:]
        return chemin_total

    def _format_graphe(self):
        # Formate le graphe json en format { case: {voisin: 1, ...}, ... }
        graphe = {}
        for case, voisins in self.graphe.items():
            if isinstance(voisins, list):
                graphe[case] = {v: 1 for v in voisins}
            else:
                graphe[case] = {v: 1 for v in voisins.keys()}
        return graphe
