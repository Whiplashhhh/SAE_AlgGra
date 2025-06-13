from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, 
    QGraphicsLineItem, QLineEdit
)
from PyQt6.QtGui import QPixmap, QPen
from PyQt6.QtCore import Qt, QPointF, QTimer

class ClientVue(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application 2 - Gestion de courses")
        self.resize(1400, 900)

        layout_principal = QHBoxLayout(self)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout_principal.addWidget(self.view, stretch=4)

        self.nb_colonnes = 52  # A -> AZ
        self.nb_lignes = 50

        self.charger_plan()

        zone_milieu = QVBoxLayout()
        self.label_produits = QLabel("Produits disponibles :")
        zone_milieu.addWidget(self.label_produits)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un produit...")
        zone_milieu.addWidget(self.search_bar)

        self.liste_produits = QListWidget()
        zone_milieu.addWidget(self.liste_produits)
        layout_principal.addLayout(zone_milieu, stretch=1)

        zone_droite = QVBoxLayout()
        self.label_categorie = QLabel("Catégories :")
        zone_droite.addWidget(self.label_categorie)
        self.liste_categories = QListWidget()
        zone_droite.addWidget(self.liste_categories)

        self.label_sous_categorie = QLabel("Liste de course :")
        zone_droite.addWidget(self.label_sous_categorie)
        self.liste_sous_categories = QListWidget()
        zone_droite.addWidget(self.liste_sous_categories)

        self.label_total = QLabel("Total articles : 0")
        zone_droite.addWidget(self.label_total)

        self.bouton_charger = QPushButton("Charger une liste de courses")
        self.bouton_fermer = QPushButton("Effacer la liste de courses")
        self.bouton_sauvegarder = QPushButton("Sauvegarder la liste de courses")
        self.bouton_cest_parti = QPushButton("C'est parti !")
        self.bouton_aleatoire = QPushButton("Créer une liste aléatoire")

        zone_droite.addWidget(self.bouton_charger)
        zone_droite.addWidget(self.bouton_fermer)
        zone_droite.addWidget(self.bouton_sauvegarder)
        zone_droite.addWidget(self.bouton_cest_parti)
        zone_droite.addWidget(self.bouton_aleatoire)

        layout_principal.addLayout(zone_droite, stretch=1)
        self.setLayout(layout_principal)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tracer_prochain_segment)
        self.index_segment = 0
        self.points = []

    def charger_plan(self):
        self.scene.clear()

        pixmap = QPixmap("plan.jpg")
        self.plan = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.plan)

        largeur = pixmap.width()
        hauteur = pixmap.height()

        self.view.setSceneRect(0, 0, largeur, hauteur)
        self.view.fitInView(0, 0, largeur, hauteur, Qt.AspectRatioMode.KeepAspectRatio)

        self.taille_case_x = largeur / self.nb_colonnes
        self.taille_case_y = hauteur / self.nb_lignes

    def afficher_chemin(self, chemin):
        print("Chemin reçu :", chemin)
        for item in self.scene.items():
            if isinstance(item, QGraphicsLineItem):
                self.scene.removeItem(item)

        self.pen = QPen(Qt.GlobalColor.red)
        self.pen.setWidth(4)
        self.points = []

        for coord in chemin:
            lig, col = coord.split(",")
            ligne = int(lig)
            col_idx = self.col_to_int(col)
            x = col_idx * self.taille_case_x + self.taille_case_x / 2
            y = (ligne - 1) * self.taille_case_y + self.taille_case_y / 2
            self.points.append(QPointF(x, y))
        self.index_segment = 0
        self.timer.start(100)

    def tracer_prochain_segment(self):
        if self.index_segment >= len(self.points) - 1:
            self.timer.stop()
            return

        p1 = self.points[self.index_segment]
        p2 = self.points[self.index_segment + 1]
        line = QGraphicsLineItem(p1.x(), p1.y(), p2.x(), p2.y())
        line.setPen(self.pen)
        self.scene.addItem(line)
        self.index_segment += 1

    def col_to_int(self, col_str):
        col_str = col_str.strip().upper()
        res = 0
        for c in col_str:
            res = res * 26 + (ord(c) - ord('A') + 1)
        return res - 1
