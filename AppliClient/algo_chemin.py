class File:
    def __init__(self):
        self.tab = []
    def enfiler(self, x):
        self.tab.append(x)
    def defiler(self):
        return self.tab.pop(0)
    def est_vide(self):
        return len(self.tab) == 0

def dijkstra(graphe: dict, depart: str, bk_liste: list = []) -> dict:
    file = File()
    file.enfiler([depart])

    dico = {depart: (0, [depart])}

    while not file.est_vide():
        chemin = file.defiler()
        sommet = chemin[-1]
        voisins = graphe.get(sommet, {})
        for voisin, distance in voisins.items():
            if voisin in bk_liste:
                continue
            nouvelle_distance = dico[sommet][0] + distance
            nouveau_chemin = list(chemin) + [voisin]
            if voisin not in dico:
                dico[voisin] = (nouvelle_distance, nouveau_chemin)
                file.enfiler(nouveau_chemin)
            else:
                if nouvelle_distance < dico[voisin][0]:
                    dico[voisin] = (nouvelle_distance, nouveau_chemin)
                    file.enfiler(nouveau_chemin)
    return dico
