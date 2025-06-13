# =================== CONTROLLER : MagasinControleur.py =====================
# Auteurs : Romain Théobald, Thomas Teiten
# Rôle : Gére toutes les données du client et charge les fichiers nécessaires
# ==========================================================================
import json
import sys
import numpy as np
import os
from collections import deque

class ClientModel:
    def __init__(self):
        self.charger_fichiers()
        self.liste_courses = {}
        #Liste des caisses de fin de parcours
        self.caisses = [
            "44,AH", "44,AF", "44,AE", "44,AC", "44,AB",
            "44,Z", "44,Y", "44,W", "44,T", "44,S", "44,Q", "44,P", "44,O", "44,M"
        ]

    def charger_fichiers(self):
        base_path = sys.path[0]
        json_dir = os.path.join(base_path, "..", "json") 

        json_dir = os.path.abspath(json_dir)

        #Ouverture des fichiers JSON nécessaires 
        with open(os.path.join(json_dir, "categorie.json"), "r", encoding="utf-8-sig") as f:
            self.sous_categories = json.load(f)
        with open(os.path.join(json_dir, "produits_par_categories.json"), "r", encoding="utf-8-sig") as f:
            self.produits_par_sous_categorie = json.load(f)
        with open(os.path.join(json_dir, "positions_categories.json"), "r", encoding="utf-8-sig") as f:
            self.positions = json.load(f)
        with open(os.path.join(json_dir, "graphe.json"), "r", encoding="utf-8-sig") as f:
            self.graphe = json.load(f)
        self.categories = list(self.sous_categories.keys())

    #Donne la liste de toutes les catgéories
    def get_categories(self):
        return self.categories

    #Tous les produits d'une catégories 
    def get_produits_categorie(self, categorie):
        produits = []
        sous_cats = self.sous_categories.get(categorie, [])
        for sous_cat in sous_cats:
            produits.extend(self.produits_par_sous_categorie.get(sous_cat, []))
        return sorted(set(produits)) #Sert à obtenir une liste triée sans doublons

    #Tous les produits du magasin
    def get_tous_les_produits(self):
        tous = []
        for cat in self.categories:
            tous.extend(self.get_produits_categorie(cat))
        return sorted(set(tous))

    #Ajoute les produits à la liste de courses
    def ajouter_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses[produit] += 1
        else:
            self.liste_courses[produit] = 1

    #Retire les produits à la liste de courses
    def retirer_produit(self, produit):
        if produit in self.liste_courses:
            self.liste_courses[produit] -= 1
            if self.liste_courses[produit] <= 0:
                del self.liste_courses[produit]

    #Vide la liste de courses
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
        indices = np.random.choice(len(tout), size=n, replace=False)#Utilisation de numpy pour la liste aléatoire
        self.liste_courses = {}
        for i in indices:
            produit = tout[i]
            self.liste_courses[produit] = 1

    def get_liste_courses(self):
        return self.liste_courses

    #Chemin avec passage par sous-catégorie/positions

    #Donne les coordonnées des produits que l'on doit aller chercher dans le magasin
    def get_coords_produits(self, produits):
        coords = []
        produits_trouves = []
        for produit in produits:
            sous_cat_trouvee = None
            for sous_cat, liste_produits in self.produits_par_sous_categorie.items():
                if produit == sous_cat or produit in liste_produits:
                    sous_cat_trouvee = sous_cat
                    break
            if sous_cat_trouvee:
                for coord, sous_cat in self.positions.items():
                    if coord not in self.graphe:
                        continue  # On ignore les cases innaccssibles
                    if isinstance(sous_cat, list):
                        if sous_cat_trouvee in sous_cat:
                            coords.append(coord)
                            produits_trouves.append(produit)
                            break
                    else:
                        if sous_cat_trouvee == sous_cat:
                            coords.append(coord)
                            produits_trouves.append(produit)
                            break
        return coords

    #Algo de Dijkstra qui va permettre de calculer le chemin le plus court depuis un point donné
    def dijkstra(self, depart):
        file = deque([[depart]]) #Chemin à explorer
        dico = {depart: (0, [depart])} #Dico gardant les distances
        while file:
            chemin = file.popleft()
            sommet = chemin[-1]
            voisins = self.graphe.get(sommet, [])
            for voisin in voisins:
                nouvelle_distance = dico[sommet][0] + 1
                nouveau_chemin = chemin + [voisin]
                if voisin not in dico or nouvelle_distance < dico[voisin][0]:
                    dico[voisin] = (nouvelle_distance, nouveau_chemin)
                    file.append(nouveau_chemin)
        return dico

    #Va générer le chemin otpimal pour récupérer les produits jusqu'à la fin(les caisses)
    def get_chemin(self, depart, produits):
        coords_produits = self.get_coords_produits(produits)
        if not coords_produits:
            return [depart]
        chemin_final = []
        position_actuelle = depart
        produits_restants = coords_produits.copy()
        #On cherche ici le produit le plus proche à chaque fois
        while produits_restants:
            dico_chemin = self.dijkstra(position_actuelle)
            accessibles = [c for c in produits_restants if c in dico_chemin]
            if not accessibles:
                break
            prochain = min(accessibles, key=lambda c: dico_chemin[c][0])
            chemin_final += dico_chemin[prochain][1][1:]
            position_actuelle = prochain
            produits_restants.remove(prochain)

        # Aller à la caisse la plus proche atteignable
        dico_caisse = self.dijkstra(position_actuelle)
        caisses_accessibles = [c for c in self.caisses if c in dico_caisse]
        if caisses_accessibles:
            caisse_plus_proche = min(caisses_accessibles, key=lambda c: dico_caisse[c][0])
            chemin_final += dico_caisse[caisse_plus_proche][1][1:]

        return [depart] + chemin_final
