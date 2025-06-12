import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QListWidgetItem, QGraphicsScene, QGraphicsView,
    QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsRectItem, QMessageBox,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPen, QColor
from PyQt6.QtCore import Qt, QPointF

from ClientModel import ClientModel
from algo_chemin import dijkstra

class ClientVue(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAE Supérette - Parcours optimal")
        self.resize(1500, 900)
        self.model = ClientModel()

        layout_principal = QHBoxLayout(self)

        # --- Partie plan ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout_principal.addWidget(self.view, stretch=3)
        self.plan_pixmap = QPixmap("plan.jpg")
        self.plan_item = QGraphicsPixmapItem(self.plan_pixmap)
        self.scene.addItem(self.plan_item)
        self.scene.setSceneRect(self.plan_item.boundingRect())
        self.view.setSceneRect(self.plan_item.boundingRect())
        self.view.fitInView(self.plan_item, Qt.AspectRatioMode.KeepAspectRatio)

        with open("graphe.json", encoding="utf-8") as f:
            self.graphe = json.load(f)
            self.cases_utiles = list(self.graphe.keys())

        self.nb_colonnes = 52
        self.nb_lignes = 52
        self.taille_case_x = self.plan_pixmap.width() / self.nb_colonnes
        self.taille_case_y = self.plan_pixmap.height() / self.nb_lignes
        self.draw_grille()

        # --- Partie droite (liste + bouton) ---
        zone_droite = QVBoxLayout()
        # 1. Liste des produits (prend toute la hauteur possible)
        self.liste_produits = QListWidget()
        self.liste_produits.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.charge_tous_les_produits()
        zone_droite.addWidget(self.liste_produits, stretch=1)
        # 2. Espaceur (pousse le bouton en bas)
        zone_droite.addSpacerItem(QSpacerItem(10, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # 3. Bouton bien large
        self.bouton_chemin = QPushButton("Calculer mon chemin !")
        self.bouton_chemin.setMinimumHeight(50)
        self.bouton_chemin.setStyleSheet("font-size:20px; font-weight:bold;")
        zone_droite.addWidget(self.bouton_chemin)
        layout_principal.addLayout(zone_droite, stretch=1)
        self.setLayout(layout_principal)

        self.bouton_chemin.clicked.connect(self.calculer_chemin)

    def charge_tous_les_produits(self):
        produits = []
        for _, prods in self.model.souscat_produits.items():
            produits += prods
        produits = sorted(set(produits))
        for prod in produits:
            item = QListWidgetItem(prod)
            self.liste_produits.addItem(item)

    def draw_grille(self):
        for coord in self.cases_utiles:
            lig, col = coord.split(",")
            lig_idx = int(lig) - 1
            col_idx = self.col_to_int(col)
            x = col_idx * self.taille_case_x
            y = lig_idx * self.taille_case_y
            rect = QGraphicsRectItem(x, y, self.taille_case_x, self.taille_case_y)
            rect.setPen(QPen(Qt.GlobalColor.gray, 1))
            rect.setBrush(QColor(255, 255, 255, 60))
            rect.setZValue(1)
            self.scene.addItem(rect)

    def calculer_chemin(self):
        selection = self.liste_produits.selectedItems()
        if not selection:
            QMessageBox.warning(self, "Oups", "Sélectionne au moins un produit !")
            return
        liste_produits = [item.text() for item in selection]
        try:
            chemin = self.model.get_chemin("48,AL", liste_produits, dijkstra)
            if not chemin:
                QMessageBox.warning(self, "Erreur", "Aucun chemin trouvé !")
                return
            self.draw_path(chemin)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du calcul du chemin : {e}")

    def draw_path(self, chemin):
        for item in self.scene.items():
            if isinstance(item, QGraphicsLineItem):
                self.scene.removeItem(item)
        points = []
        for coord in chemin:
            try:
                ligne, colonne = coord.split(",")
                ligne = int(ligne)
                col_idx = self.col_to_int(colonne)
                x = (col_idx + 0.5) * self.taille_case_x
                y = (ligne - 0.5) * self.taille_case_y
                points.append(QPointF(x, y))
            except Exception as e:
                print(f"Erreur coordonnée : {coord} --> {e}")
        if len(points) < 2:
            return
        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(2)
        for i in range(len(points) - 1):
            line = QGraphicsLineItem(points[i].x(), points[i].y(), points[i+1].x(), points[i+1].y())
            line.setPen(pen)
            self.scene.addItem(line)

    def col_to_int(self, col_str):
        col_str = col_str.strip().upper()
        res = 0
        for c in col_str:
            res = res * 26 + (ord(c) - ord('A') + 1)
        return res - 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ClientVue()
    fenetre.show()
    sys.exit(app.exec())
