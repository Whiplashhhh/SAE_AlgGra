class File:
    def init(self, n):
        self.tab = []
    def enfiler(self, x):
        self.tab.append(x)
    def defiler(self):
        return self.tab.pop(0)
    def est_vide(self):
        return len(self.tab) == 0

def dijkstra(graphe: dict, depart: str, bk_liste: list = []) -> dict:
    """
    Renvoie un dico {sommet: (distance, chemin)}, depuis 'depart'
    :param graphe: {sommet: [voisins]}
    :param depart: str genre '48,AL'
    :param bk_liste: cases à éviter
    """
    file = File(len(graphe))
    file.enfiler([depart])

    dico = {depart: (0, [depart])}

    while not file.est_vide():
        chemin = file.defiler()
        sommet = chemin[-1]
        voisins = graphe.get(sommet, [])
        for voisin in voisins:
            if voisin in bk_liste:
                continue
            nouvelle_distance = dico[sommet][0] + 1  # distance = 1 à chaque fois (graphe simple)
            nouveau_chemin = list(chemin) + [voisin]
            if voisin not in dico:
                dico[voisin] = (nouvelle_distance, nouveau_chemin)
                file.enfiler(nouveau_chemin)
            else:
                if nouvelle_distance < dico[voisin][0]:
                    dico[voisin] = (nouvelle_distance, nouveau_chemin)
                    file.enfiler(nouveau_chemin)
    return dico