import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QFileDialog, QLabel, QListWidgetItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MagasinVue2(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application 2 - Gestion de courses")
        self.resize(1200, 800)

        # Layout principal horizontal
        layout_principal = QHBoxLayout(self)

        # Zone centrale : le plan
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout_principal.addWidget(self.view, stretch=3)

        self.charger_plan()

        # Zone droite : gestion des catégories & produits
        zone_droite = QVBoxLayout()

        self.label_categorie = QLabel("Catégories :")
        zone_droite.addWidget(self.label_categorie)

        self.liste_categories = QListWidget()
        zone_droite.addWidget(self.liste_categories)

        self.label_sous_categorie = QLabel("Sous-catégorie / Produits :")
        zone_droite.addWidget(self.label_sous_categorie)

        self.liste_sous_categories = QListWidget()
        zone_droite.addWidget(self.liste_sous_categories)

        # Boutons
        self.bouton_charger = QPushButton("Charger une liste de courses")
        self.bouton_fermer = QPushButton("Fermer la liste de courses")
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

        # Charge les vraies catégories depuis le fichier JSON directement
        self.charger_categories_json()

    def charger_plan(self):
        pixmap = QPixmap("plan.jpg")
        self.plan = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.plan)
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def charger_categories_json(self):
        with open("produits_repartis_complet_final.json", "r", encoding="utf-8") as f:
            self.produits_par_categorie = json.load(f)
        categories = list(self.produits_par_categorie.keys())
        self.liste_categories.addItems(categories)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MagasinVue2()
    fenetre.show()
    sys.exit(app.exec())
