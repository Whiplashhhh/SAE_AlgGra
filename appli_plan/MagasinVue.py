import sys
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QScrollArea
from PyQt6.QtGui import QGuiApplication, QBrush, QPixmap, QFont, QColor, QPen
from PyQt6.QtCore import Qt
from MagasinModel import MagasinModel
from MagasinControleur import MagasinControleur

class CaseMagasin(QGraphicsRectItem):
    def __init__(self, x, y, width, height, ligne, colonne, modele, vue):
        super().__init__(x, y, width, height)
        self.ligne = ligne
        self.colonne = colonne
        self.modele = modele
        self.vue = vue
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
            self.vue.afficher_produits_case(produits)
        else:
            self.vue.afficher_produits_case([])

        
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
        self.scene_magasin = SceneMagasin(self.modele, self)
        self.view = QGraphicsView(self.scene_magasin)
        
        self.liste_produits_case = QListWidget()
        self.liste_produits_case.setFixedWidth(200)
        
        self.liste_globale = QListWidget()
        for categorie in self.modele.produits_par_categories:
            for produit in self.modele.produits_par_categories[categorie]:
                item = QListWidgetItem(produit)
                self.liste_globale.addItem(item)
        self.liste_globale.itemClicked.connect(self.afficher_produit_selectionne)
        
        layout_droit = QVBoxLayout()
        layout_droit.addWidget(QLabel("Produits de la case"))
        layout_droit.addWidget(self.liste_produits_case)
        layout_droit.addWidget(QLabel("Tous les produits"))
        layout_droit.addWidget(self.liste_globale)
        
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(layout_droit)
        self.setLayout(layout)
        self.setWindowTitle("MoliShop - Gerant ")
        self.resize(1400, 900)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MagasinVue()
    window.show()
    sys.exit(app.exec())
