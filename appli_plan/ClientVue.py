from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QLineEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ClientVue(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application 2 - Gestion de courses")
        self.resize(1400, 900)

        layout_principal = QHBoxLayout(self)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout_principal.addWidget(self.view, stretch=4)
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

        # TOTAL ARTICLES placé juste sous la liste de course :
        self.label_total = QLabel("Total articles : 0")
        zone_droite.addWidget(self.label_total)

        self.bouton_charger = QPushButton("Charger une liste de courses")
        self.bouton_fermer = QPushButton("Effacer la liste de courses")
        self.bouton_sauvegarder = QPushButton("Sauvegarder la liste de courses")
        self.bouton_aleatoire = QPushButton("Créer une liste aléatoire")
        self.bouton_cest_parti = QPushButton("C'est parti !")

        zone_droite.addWidget(self.bouton_charger)
        zone_droite.addWidget(self.bouton_fermer)
        zone_droite.addWidget(self.bouton_sauvegarder)
        zone_droite.addWidget(self.bouton_cest_parti)
        zone_droite.addWidget(self.bouton_aleatoire)

        layout_principal.addLayout(zone_droite, stretch=1)
        self.setLayout(layout_principal)

    def charger_plan(self):
        pixmap = QPixmap("plan.jpg")
        self.plan = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.plan)
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.view.scale(1.3, 1.3)
