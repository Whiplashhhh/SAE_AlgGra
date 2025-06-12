import sys
import json
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QGuiApplication, QBrush, QPixmap, QFont, QColor, QPen
from PyQt6.QtCore import Qt
from MagasinModel import MagasinModel

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
        colonne = self.colonne
        if colonne < 26:
            lettre_colonne = chr(ord('A') + colonne)
        else:
            lettre_colonne = 'A' + chr(ord('A') + (colonne - 26))
        
        key = f"{self.ligne+1},{lettre_colonne}"
        
        if self.modele.is_case_util(self.ligne, self.colonne):
            categorie = self.modele.positions_categories.get(key, None)
            if categorie:
                produits = self.modele.produits_par_categories.get(categorie, [])
            else:
                produits = []
            self.parent_vue.afficher_produits_case(produits)
        else:
            self.parent_vue.afficher_produits_case([])
        
        super().mousePressEvent(event)

class SceneMagasin(QGraphicsScene):
    def __init__(self, modele, parent_vue):
        super().__init__()
        self.modele = modele
        self.parent_vue = parent_vue
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
                rect = CaseMagasin(x, y, self.tailleX, self.tailleY, i, j, self.modele, self.parent_vue)
                if not self.modele.is_case_util(i, j):
                    rect.setBrush(QBrush(QColor(50, 50, 50, 100)))
                self.addItem(rect)
                self.rectangles.append(rect)
        
        self.croix_items = []

    def afficher_croix(self, liste_cases):
        for croix in self.croix_items:
            self.removeItem(croix)
        self.croix_items.clear()

        for case_str in liste_cases:
            ligne, colonne = case_str.split(',')
            ligne = int(ligne)-1
            if len(colonne) == 1:
                colonne_num = ord(colonne)-ord('A')
            else:
                colonne_num = 26 + ord(colonne[1]) - ord('A')

            x = colonne_num * self.tailleX
            y = ligne * self.tailleY

            croix1 = self.addLine(x, y, x+self.tailleX, y+self.tailleY, QPen(Qt.GlobalColor.red, 2))
            croix2 = self.addLine(x, y+self.tailleY, x+self.tailleX, y, QPen(Qt.GlobalColor.red, 2))
            self.croix_items.extend([croix1, croix2])

class MagasinVue(QWidget):
    def __init__(self):
        super().__init__()
        self.modele = MagasinModel("./graphe.json", "./positions_categories.json", "./produits_par_categories.json")
        self.scene_magasin = SceneMagasin(self.modele, self)
        self.view = QGraphicsView(self.scene_magasin)
        
        self.liste_produits_case = QListWidget()
        self.liste_produits_case.setFixedWidth(200)
        
        self.liste_categories = QListWidget()
        self.liste_produits_global = QListWidget()

        with open("./catégorie.json", "r", encoding="utf-8") as f:
            self.mapping_familles = json.load(f)

        for famille in sorted(self.mapping_familles.keys()):
            item = QListWidgetItem(famille)
            self.liste_categories.addItem(item)
        self.liste_categories.itemClicked.connect(self.afficher_produits_de_famille)
        self.liste_produits_global.itemClicked.connect(self.afficher_produit_selectionne)

        layout_droit = QVBoxLayout()
        layout_droit.addWidget(QLabel("Produits de la case"))
        layout_droit.addWidget(self.liste_produits_case)
        layout_droit.addWidget(QLabel("Grandes Catégories"))
        layout_droit.addWidget(self.liste_categories)
        layout_droit.addWidget(QLabel("Produits de la catégorie"))
        layout_droit.addWidget(self.liste_produits_global)
        
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(layout_droit)
        self.setLayout(layout)
        self.setWindowTitle("Magasin avec grandes catégories")
        self.resize(1500, 900)

    def afficher_produits_case(self, produits):
        self.liste_produits_case.clear()
        if produits:
            for prod in produits:
                self.liste_produits_case.addItem(prod)
        else:
            self.liste_produits_case.addItem("Aucun produit")

    def afficher_produits_de_famille(self, item):
        self.liste_produits_global.clear()
        famille = item.text()
        produits = []
        for sous_categorie in self.mapping_familles[famille]:
            produits += self.modele.produits_par_categories.get(sous_categorie, [])
        for prod in sorted(produits):
            self.liste_produits_global.addItem(prod)

    def afficher_produit_selectionne(self, item):
        produit = item.text()
        cases_a_afficher = []
        for case, categorie in self.modele.positions_categories.items():
            produits_possibles = self.modele.produits_par_categories.get(categorie, [])
            if produit in produits_possibles:
                cases_a_afficher.append(case)
        self.scene_magasin.afficher_croix(cases_a_afficher)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MagasinVue()
    window.show()
    sys.exit(app.exec())