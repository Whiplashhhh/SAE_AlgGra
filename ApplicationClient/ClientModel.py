import json

class ClientModel:
    def __init__(self):
        with open("position_produit.json", encoding="utf-8-sig") as f:
            self.case_souscat = json.load(f)
        with open("sous_categorie_produits.json", encoding="utf-8-sig") as f:
            self.souscat_produits = json.load(f)
        with open("graphe.json", encoding="utf-8") as f:
            raw = json.load(f)
            # Si raw est déjà {case: [voisins]}, alors...
            self.graphe = {k: {v: 1 for v in voisins} for k, voisins in raw.items()}

    def get_case_produit(self, produit):
        """Trouve la case où se trouve ce produit."""
        for souscat, prods in self.souscat_produits.items():
            if produit in prods:
                for case, sc in self.case_souscat.items():
                    if sc == souscat:
                        return case
        return None

    def get_chemin(self, depart, liste_produits, dijkstra_func):
        chemin_total = []
        case_actuelle = depart
        a_faire = liste_produits[:]
        deja_fait = set()
        while a_faire:
            meilleur = None
            best_dist = None
            best_path = None
            for prod in a_faire:
                case_prod = self.get_case_produit(prod)
                if case_prod is None or case_prod in deja_fait:
                    continue
                dico = dijkstra_func(self.graphe, case_actuelle)
                if case_prod in dico:
                    dist, path = dico[case_prod]
                    if best_dist is None or dist < best_dist:
                        meilleur = prod
                        best_dist = dist
                        best_path = path
            if meilleur is not None:
                if not chemin_total:
                    chemin_total += best_path
                else:
                    chemin_total += best_path[1:]  # évite doublons
                case_actuelle = self.get_case_produit(meilleur)
                deja_fait.add(case_actuelle)
                a_faire.remove(meilleur)
            else:
                a_faire.remove(meilleur)
        return chemin_total

