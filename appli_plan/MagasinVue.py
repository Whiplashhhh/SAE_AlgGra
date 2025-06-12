# Auteurs:
#   Willem VANBAELINGHEM--DEZITTER - TPA
#   Alex FRANCOIS - TPA
# date création: 09/06/2025
# dernière maj: 12/06/2025
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QListWidgetItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, 
                             QGraphicsRectItem, QGraphicsTextItem, QLabel, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QPushButton, QLineEdit, QMessageBox)
from PyQt6.QtGui import QGuiApplication, QBrush, QPixmap, QFont, QColor, QPen
from PyQt6.QtCore import Qt
from MagasinModel import MagasinModel
from MagasinControleur import MagasinControleur

class CaseMagasin(QGraphicsRectItem):
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
        #colonne = self.colonne
        # if colonne < 26:
        #     lettre_colonne = chr(ord('A') + colonne)
        # else:
        #     lettre_colonne = 'A' + chr(ord('A') + (colonne - 26))
        
        # key = f"{self.ligne+1},{lettre_colonne}"

        # if self.modele.is_case_util(self.ligne, self.colonne):
        #     categorie = self.modele.positions_categories.get(key, None)
        #     if categorie:
        #         produits = self.modele.produits_par_categories.get(categorie, [])
        #     else:
        #         produits = []
        #     self.vue.afficher_produits_case(produits)
        # else:
        #     self.vue.afficher_produits_case([])
        self.parent_vue.case_cliquee(self.ligne, self.colonne)
        
        super().mousePressEvent(event)

class SceneMagasin(QGraphicsScene):
    def __init__(self, modele, vue):
        super().__init__()
        self.modele = modele
        self.vue = vue
        pixmap = QPixmap(sys.path[0] + '/plan.jpg')
        pixmap = pixmap.scaled(self.modele.largeur_plan, self.modele.hauteur_plan, Qt.AspectRatioMode.KeepAspectRatio)
        self.plan = QGraphicsPixmapItem(pixmap)
        self.addItem(self.plan)
        
        larg = pixmap.width()
        haut = pixmap.height()
        self.tailleX = larg / self.modele.colonnes
        self.tailleY = haut / self.modele.lignes
        self.setSceneRect(-30, -30, larg+60, haut+60)
        self.rectangles = []
        for i in range(self.modele.lignes):
            for j in range(self.modele.colonnes):
                x = j * self.tailleX
                y = i * self.tailleY
                rect = CaseMagasin(x, y, self.tailleX, self.tailleY, i, j, self.modele, self.vue)
                if not self.modele.is_case_util(i, j):
                    rect.setBrush(QBrush(QColor(50, 50, 50, 100)))
                self.addItem(rect)
                self.rectangles.append(rect)
        
        self.croix = None
        
        #affichage des coordonnées
        font = QFont()
        font.setBold(True)
        for j in range(self.modele.colonnes):
            x = j * self.tailleX + self.tailleX / 2
            texte = chr(ord('A') + j) if j < 26 else 'A' + chr(ord('A') + (j-26))
            item = QGraphicsTextItem(texte)
            item.setFont(font)
            item.setPos(x, -25)
            self.addItem(item)

        for i in range(self.modele.lignes):
            y = i * self.tailleY + self.tailleY / 2
            item = QGraphicsTextItem(str(i+1))
            item.setFont(font)
            item.setPos(-25, y)
            self.addItem(item)
        
    def afficher_croix(self, case_str):
        if hasattr(self, 'croix1') and self.croix1:
            self.removeItem(self.croix1)
        if hasattr(self, 'croix2') and self.croix2:
            self.removeItem(self.croix2)

        ligne, colonne = case_str.split(',')
        ligne = int(ligne)-1
        if len(colonne) == 1:
            colonne_num = ord(colonne)-ord('A')
        else:
            colonne_num = 26 + ord(colonne[1]) - ord('A')

        x = colonne_num * self.tailleX
        y = ligne * self.tailleY

        self.croix1 = self.addLine(x, y, x+self.tailleX, y+self.tailleY, QPen(Qt.GlobalColor.red, 2))
        self.croix2 = self.addLine(x, y+self.tailleY, x+self.tailleX, y, QPen(Qt.GlobalColor.red, 2))

class MagasinVue(QWidget):
    def __init__(self):
        super().__init__()
        self.modele = MagasinModel("./graphe.json", "./positions_categories.json", "./produits_par_categories.json")
        self.controleur = MagasinControleur(self.modele, self)
        self.scene_magasin = SceneMagasin(self.modele, self)
        self.view = QGraphicsView(self.scene_magasin)
        
        self.liste_produits_case = QListWidget()
        self.liste_produits_case.setFixedWidth(200)
        
        self.label_coordonnees = QLabel("Aucune case sélectionnée")
        
        self.liste_globale = QListWidget()
        for categorie in self.modele.produits_par_categories:
            for produit in self.modele.produits_par_categories[categorie]:
                item = QListWidgetItem(produit)
                self.liste_globale.addItem(item)
        self.liste_globale.itemClicked.connect(self.afficher_produit_selectionne)
        
        self.input_produit = QLineEdit()
        self.bouton_ajout = QPushButton("Ajouter produit")
        self.bouton_supprimer = QPushButton("Supprimer produit")
        self.bouton_sauvegarde = QPushButton("Sauvegarder")
        
        self.bouton_ajout.clicked.connect(self.ajouter_produit_case)
        self.bouton_supprimer.clicked.connect(self.supprimer_produit_case)
        self.bouton_sauvegarde.clicked.connect(self.controleur.sauvegarder)
        
        layout_droit = QVBoxLayout()
        layout_droit.addWidget(self.label_coordonnees)
        layout_droit.addWidget(QLabel("Produits de la case"))
        layout_droit.addWidget(self.liste_produits_case)
        layout_droit.addWidget(QLabel("Ajouter un produit :"))
        layout_droit.addWidget(self.input_produit)
        layout_droit.addWidget(self.bouton_ajout)
        layout_droit.addWidget(self.bouton_supprimer)
        layout_droit.addWidget(self.bouton_sauvegarde)
        layout_droit.addWidget(QLabel("Tous les produits"))
        layout_droit.addWidget(self.liste_globale)
        
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(layout_droit)
        self.setLayout(layout)
        self.setWindowTitle("MoliShop - Gerant ")
        self.showMaximized()
        
        self.case_actuelle = None
        self.categorie_actuelle = None
        
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

    def afficher_produit_selectionne(self, item):
        produit = item.text()
        for case, categorie in self.modele.positions_categories.items():
            produits_possibles = self.modele.produits_par_categories.get(categorie, [])
            if produit in produits_possibles:
                self.scene_magasin.afficher_croix(case)
                break
    def ajouter_produit_case(self):
        if self.case_actuelle and self.categorie_actuelle:
            nouveau_produit = self.input_produit.text()
            if nouveau_produit:
                self.controleur.ajouter_produit(self.categorie_actuelle, nouveau_produit)
                self.case_cliquee(*self.parse_case(self.case_actuelle))
                self.input_produit.clear()

    def supprimer_produit_case(self):
        if self.case_actuelle and self.categorie_actuelle:
            item = self.liste_produits_case.currentItem()
            if item:
                produit = item.text()
                self.controleur.supprimer_produit(self.categorie_actuelle, produit)
                self.case_cliquee(*self.parse_case(self.case_actuelle))

    def parse_case(self, case_str):
        ligne, colonne = case_str.split(',')
        ligne = int(ligne)-1
        if len(colonne) == 1:
            colonne_num = ord(colonne)-ord('A')
        else:
            colonne_num = 26 + ord(colonne[1]) - ord('A')
        return ligne, colonne_num

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MagasinVue()
    window.show()
    sys.exit(app.exec())
