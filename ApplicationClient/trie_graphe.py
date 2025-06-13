import json

# --- Fichiers à adapter si besoin ---
fichier_graphe = "graphe.json"
fichier_positions = "position_produit.json"
fichier_graphe_modifie = "graphe_sans_rayons.json"

# 1. Charger le graphe
with open(fichier_graphe, "r", encoding="utf-8-sig") as f:
    graphe = json.load(f)

# 2. Charger la liste des cases-rayons (toutes les positions produits)
with open(fichier_positions, "r", encoding="utf-8-sig") as f:
    positions_rayons = set(json.load(f).keys())

# 3. Supprimer du graphe toutes les cases-rayons
for case in list(graphe.keys()):
    if case in positions_rayons:
        del graphe[case]
    else:
        # Supprimer aussi les liens vers les cases-rayons
        graphe[case] = [v for v in graphe[case] if v not in positions_rayons]

# 4. Enregistrer le nouveau graphe modifié
with open(fichier_graphe_modifie, "w", encoding="utf-8-sig") as f:
    json.dump(graphe, f, indent=2)

print(f"Le graphe modifié a été enregistré dans : {fichier_graphe_modifie}")
