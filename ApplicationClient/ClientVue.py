import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QListWidgetItem, QGraphicsScene, QGraphicsView,
    QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPolygonItem, QMessageBox,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPen, QColor, QPolygonF
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtCore import QTimer

from ClientModel import ClientModel
from algo_chemin import dijkstra

class ClientVue(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAE Supérette - Parcours optimal")
        self.resize(1500, 900)
        self.model = ClientModel()

        layout_principal = QHBoxLayout(self)

        # Partie plan
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

        # Partie droite (liste + bouton)
        zone_droite = QVBoxLayout()
        self.liste_produits = QListWidget()
        self.liste_produits.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.charge_tous_les_produits()
        zone_droite.addWidget(self.liste_produits, stretch=1)
        zone_droite.addSpacerItem(QSpacerItem(10, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
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
            self.draw_path(chemin, liste_produits)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du calcul du chemin : {e}")

    def draw_path(self, chemin, liste_produits):
        # Supprime anciens traits et flèches
        for item in self.scene.items():
            if isinstance(item, (QGraphicsLineItem, QGraphicsPolygonItem)):
                self.scene.removeItem(item)
        # On pré-calcule les points à dessiner
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

        # --- Animation : dessin segment par segment avec QTimer
        self._animation_index = 0
        self._animation_points = points
        self._animation_pen = QPen(Qt.GlobalColor.red)
        self._animation_pen.setWidth(8)
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(lambda: self._draw_next_segment(liste_produits))
        self._animation_timer.start(60)  # Vitesse en ms (genre 60 = fluide et pas trop lent)

    def _draw_next_segment(self, liste_produits):
        idx = self._animation_index
        points = self._animation_points
        pen = self._animation_pen
        if idx < len(points) - 1:
            line = QGraphicsLineItem(points[idx].x(), points[idx].y(), points[idx + 1].x(), points[idx + 1].y())
            line.setPen(pen)
            line.setZValue(3)
            self.scene.addItem(line)
            self._animation_index += 1
        else:
            # Fin animation, ajoute les flèches sur les produits
            self._animation_timer.stop()
            coords_produits = self.model.get_coords_produits(liste_produits)
            for coord in coords_produits:
                try:
                    ligne, colonne = coord.split(",")
                    ligne = int(ligne)
                    col_idx = self.col_to_int(colonne)
                    x = (col_idx + 0.5) * self.taille_case_x
                    y = (ligne - 0.5) * self.taille_case_y
                    point = QPointF(x, y)
                    self.draw_arrow(point)
                except Exception as e:
                    print(f"Erreur flèche coordonnée {coord} : {e}")


    def draw_arrow(self, point):
        taille = min(self.taille_case_x, self.taille_case_y) / 2.2
        dx = taille / 2
        arrow = QPolygonF([
            QPointF(point.x() - dx, point.y() - taille/2),
            QPointF(point.x() + dx, point.y() - taille/2),
            QPointF(point.x(), point.y() + taille/2)
        ])
        arrow_item = QGraphicsPolygonItem(arrow)
        arrow_item.setBrush(Qt.GlobalColor.red)
        arrow_item.setPen(QPen(Qt.GlobalColor.black, 1))
        arrow_item.setZValue(10)
        self.scene.addItem(arrow_item)

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
