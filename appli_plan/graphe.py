import json

def generate_graphe():
    colonnes = [chr(c) for c in range(ord('A'), ord('Z') + 1)] + ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY']
    colonnes.remove('A')  # Suppression de la colonne A
    lignes = list(range(1, 49))  # 1 à 48
    graphe = {}

    for l in lignes:
        for c in colonnes:
            voisins = []
            if l > 1:
                voisins.append(f"{l-1},{c}")
            if l < 48:
                voisins.append(f"{l+1},{c}")
            i = colonnes.index(c)
            if i > 0:
                voisins.append(f"{l},{colonnes[i-1]}")
            if i < len(colonnes)-1:
                voisins.append(f"{l},{colonnes[i+1]}")
            graphe[f"{l},{c}"] = voisins

    return graphe

graphe = generate_graphe()
with open("graphe.json", "w") as f:
    json.dump(graphe, f, indent=2)
