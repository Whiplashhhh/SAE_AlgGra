# ======================= VIEW : MagasinVue.py ========================
# Auteurs : Willem VANBAELINGHEM--DEZITTER, Alex FRANCOIS
# Rôle : Interface graphique utilisateur (IHM), aucune logique métier ici
# =====================================================================

import json
import os
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QListWidgetItem, QPushButton, QLineEdit, QMessageBox, QGraphicsView, QGraphicsScene, 
                             QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem)
from PyQt6.QtGui import QBrush, QPixmap, QFont, QColor, QPen
from PyQt6.QtCore import Qt
from MagasinModel import MagasinModel
from MagasinControleur import MagasinControleur
from Infos import Infos

class CaseMagasin(QGraphicsRectItem):
    """
    Une case du magasin, cliquable dans la scène.
    """
    def __init__(self, x, y, width, height, ligne, colonne, modele, parent_vue):
        super().__init__(x, y, width, height)
        self.ligne = ligne
        self.colonne = colonne
        self.modele = modele
        self.parent_vue = parent_vue
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.setPen(Qt.GlobalColor.gray)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        self.parent_vue.case_cliquee(self.ligne, self.colonne)
        super().mousePressEvent(event)

class SceneMagasin(QGraphicsScene):
    """
    La scène graphique qui affiche le plan et les cases.
    """
    def __init__(self, modele, vue):
        super().__init__()
        self.modele = modele
        self.vue = vue
        # Affiche le plan d'après le chemin du projet
        pixmap = QPixmap(self.modele.infos_projet["plan_magasin"])
        larg, haut = pixmap.width(), pixmap.height()
        pixmap = pixmap.scaled(larg, haut, Qt.AspectRatioMode.KeepAspectRatio)
        self.plan = QGraphicsPixmapItem(pixmap)
        self.addItem(self.plan)
        self.tailleX = larg / self.modele.colonnes
        self.tailleY = haut / self.modele.lignes
        self.setSceneRect(-30, -30, larg+60, haut+60)
        # Affichage du quadrillage
        for i in range(self.modele.lignes):
            for j in range(self.modele.colonnes):
                x = j * self.tailleX
                y = i * self.tailleY
                rect = CaseMagasin(x, y, self.tailleX, self.tailleY, i, j, self.modele, self.vue)
                if not self.modele.is_case_util(i, j):
                    rect.setBrush(QBrush(QColor(50, 50, 50, 100)))
                self.addItem(rect)
        # Affichage coordonnées
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        for j in range(self.modele.colonnes):
            x = j * self.tailleX + self.tailleX / 2 - 20
            texte = chr(ord('A') + j) if j < 26 else 'A' + chr(ord('A') + (j-26))
            item = QGraphicsTextItem(texte)
            item.setFont(font)
            item.setPos(x, -40)
            self.addItem(item)
        for i in range(self.modele.lignes):
            y = i * self.tailleY + self.tailleY / 2 - 15
            item = QGraphicsTextItem(str(i+1))
            item.setFont(font)
            item.setPos(-40, y)
            self.addItem(item)

    # Méthode pour afficher une croix sur une ou plusieurs cases (bonus pour affichage)
    def afficher_croix(self, liste_cases):
        if hasattr(self, 'croix_items'):
            for croix in self.croix_items:
                self.removeItem(croix)
            self.croix_items.clear()
        else:
            self.croix_items = []
        for case_str in liste_cases:
            ligne, colonne = case_str.split(',')
            ligne = int(ligne)-1
            colonne_num = (ord(colonne)-ord('A')) if len(colonne) == 1 else 26+ord(colonne[1])-ord('A')
            x = colonne_num * self.tailleX
            y = ligne * self.tailleY
            croix1 = self.addLine(x, y, x+self.tailleX, y+self.tailleY, QPen(Qt.GlobalColor.red, 2))
            croix2 = self.addLine(x, y+self.tailleY, x+self.tailleX, y, QPen(Qt.GlobalColor.red, 2))
            self.croix_items.extend([croix1, croix2])


class MagasinVue(QWidget):
    """
    La vue principale de l'application (IHM).
    """
    def __init__(self):
        super().__init__()
        self.selection_projet()

    def selection_projet(self):
        """Lance la boîte de dialogue pour créer/charger un projet."""
        self.dialog = Infos(self.on_infos_projet_valide)
        self.dialog.show()

    def on_infos_projet_valide(self, infos_projet):
        """Initialise l'IHM après création/chargement du projet."""
        self.infos_projet = infos_projet
        self.setup_ui()

    def setup_ui(self):
        # === Création du modèle et du contrôleur ===
        self.modele = MagasinModel(self.infos_projet)
        self.controleur = MagasinControleur(self.modele, self)
        self.scene_magasin = SceneMagasin(self.modele, self)
        self.view = QGraphicsView(self.scene_magasin)
        self.view.fitInView(self.scene_magasin.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Widgets principaux à droite ===
        self.label_coordonnees = QLabel("Aucune case sélectionnée")

        # Liste des produits de la case sélectionnée
        self.liste_produits_case = QListWidget()
        self.liste_produits_case.setFixedWidth(200)

        # Ajout/suppression produit sur la case
        self.input_produit = QLineEdit()
        self.bouton_ajout = QPushButton("Ajouter produit")
        self.bouton_supprimer = QPushButton("Supprimer produit")
        self.bouton_ajout.clicked.connect(self.ajouter_produit_case)
        self.bouton_supprimer.clicked.connect(self.supprimer_produit_case)

        # Réinitialisation de tous les produits
        self.bouton_reset = QPushButton("Réinitialiser tous les produits")
        self.bouton_reset.clicked.connect(self.reset_produits)

        # Suppression du projet (optionnel)
        self.bouton_supprimer_projet = QPushButton("Supprimer le projet (IRRÉVERSIBLE)")
        self.bouton_supprimer_projet.clicked.connect(self.supprimer_projet)

        # Bloc grandes catégories
        with open("./categorie.json", "r", encoding="utf-8") as f:
            self.mapping_familles = json.load(f)

        self.liste_categories = QListWidget()
        for famille in sorted(self.mapping_familles.keys()):
            item = QListWidgetItem(famille)
            self.liste_categories.addItem(item)
        self.liste_categories.itemClicked.connect(self.afficher_produits_de_famille)

        # Bloc produits de la grande catégorie sélectionnée
        self.liste_produits_global = QListWidget()
        self.liste_produits_global.itemClicked.connect(self.afficher_produit_selectionne)

        # === Organisation des widgets à droite ===
        layout_droit = QVBoxLayout()
        layout_droit.addWidget(self.bouton_supprimer_projet)
        layout_droit.addWidget(self.bouton_reset)
        layout_droit.addWidget(self.label_coordonnees)

        # --- Bloc produits de la case (gauche du bloc) + boutons ajout/suppression (droite du bloc) ---
        case_layout = QHBoxLayout()
        case_left = QVBoxLayout()
        case_left.addWidget(QLabel("Produits de la case"))
        case_left.addWidget(self.liste_produits_case)
        case_layout.addLayout(case_left)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(QLabel("Ajouter un produit :"))
        buttons_layout.addWidget(self.input_produit)
        buttons_layout.addWidget(self.bouton_ajout)
        buttons_layout.addWidget(self.bouton_supprimer)
        case_layout.addLayout(buttons_layout)

        layout_droit.addLayout(case_layout)

        # Bloc grandes catégories
        layout_droit.addWidget(QLabel("Grandes Catégories"))
        layout_droit.addWidget(self.liste_categories)

        # Bloc produits de la catégorie
        layout_droit.addWidget(QLabel("Produits de la catégorie"))
        layout_droit.addWidget(self.liste_produits_global)

        # === Agencement global ===
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        # Pour limiter la taille de la partie droite, comme dans ton ancien code :
        widget_droit = QWidget()
        widget_droit.setLayout(layout_droit)
        widget_droit.setMaximumWidth(350)
        layout.addWidget(widget_droit)
        self.setLayout(layout)
        self.setWindowTitle("MoliShop - Gérant")
        self.showMaximized()

        self.case_actuelle = None
        self.categorie_actuelle = None

    # ------------- Méthodes logiques (ne changent pas) ----------------
    def case_cliquee(self, ligne, colonne):
        produits, key, categorie = self.controleur.get_produits_de_case(ligne, colonne)
        self.case_actuelle = key
        self.categorie_actuelle = categorie
        self.label_coordonnees.setText(f"Case : {key}")
        self.afficher_produits_case(produits)

    def afficher_produits_case(self, produits):
        self.liste_produits_case.clear()
        if produits:
            for prod in produits:
                self.liste_produits_case.addItem(prod)
        else:
            self.liste_produits_case.addItem("Aucun produit")

    def ajouter_produit_case(self):
        if self.case_actuelle and self.categorie_actuelle:
            nouveau_produit = self.input_produit.text().strip()
            if nouveau_produit:
                self.controleur.ajouter_produit(self.categorie_actuelle, nouveau_produit)
                self.controleur.sauvegarder()
                self.case_cliquee(*self._parse_case(self.case_actuelle))
                self.input_produit.clear()

    def supprimer_produit_case(self):
        selected = self.liste_produits_case.currentItem()
        if selected and self.case_actuelle and self.categorie_actuelle:
            produit = selected.text()
            if produit != "Aucun produit":
                self.controleur.supprimer_produit(self.categorie_actuelle, produit)
                self.controleur.sauvegarder()
                self.case_cliquee(*self._parse_case(self.case_actuelle))

    def reset_produits(self):
        reply = QMessageBox.question(self, "Confirmation", "Tout réinitialiser ?")
        if reply == QMessageBox.StandardButton.Yes:
            self.controleur.reset_produits()
            self.controleur.sauvegarder()
            self.case_cliquee(0, 0)

    def supprimer_projet(self):
        reply = QMessageBox.question(self, "Suppression du projet",
                                    "Attention, cette action va SUPPRIMER TOUS les fichiers du projet. Voulez-vous continuer ?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        erreurs = []
        # Liste des chemins à supprimer
        chemins = [
            self.infos_projet.get("produits_par_categories"),
            os.path.join(os.path.dirname(self.infos_projet.get("produits_par_categories")), f"{self.infos_projet.get('nom_projet')}.json")
        ]

        for chemin in chemins:
            # Pour éviter de supprimer un plan générique utilisé ailleurs, on pourrait ajouter un test sur le chemin ou demander confirmation pour l’image
            if chemin and os.path.exists(chemin):
                try:
                    os.remove(chemin)
                except Exception as e:
                    erreurs.append(f"{chemin} : {e}")

        if erreurs:
            QMessageBox.warning(self, "Suppression partielle", "Certains fichiers n'ont pas pu être supprimés :\n" + "\n".join(erreurs))
        else:
            QMessageBox.information(self, "Suppression réussie", "Le projet a bien été supprimé.")

        # Ferme la fenêtre principale et rouvre la sélection de projet (clean)
        self.close()
        self.selection_projet()

    def afficher_produits_de_famille(self, item):
        famille = item.text()
        self.liste_produits_global.clear()
        for sous_categorie in self.mapping_familles[famille]:
            produits = self.modele.produits_par_categories.get(sous_categorie, [])
            for produit in produits:
                self.liste_produits_global.addItem(produit)

    def afficher_produit_selectionne(self, item):
        produit = item.text()
        # Affichage croix sur toutes les cases où il y a ce produit
        liste_cases = []
        for case, categorie in self.modele.positions_categories.items():
            produits_possibles = self.modele.produits_par_categories.get(categorie, [])
            if produit in produits_possibles:
                liste_cases.append(case)
        if liste_cases:
            self.scene_magasin.afficher_croix(liste_cases)

    def _parse_case(self, key):
        """Transforme une clé '4,B' en tuple (3,1)."""
        ligne_str, colonne_str = key.split(',')
        ligne = int(ligne_str) - 1
        if len(colonne_str) == 1:
            colonne = ord(colonne_str) - ord('A')
        else:
            colonne = 26 + ord(colonne_str[1]) - ord('A')
        return (ligne, colonne)