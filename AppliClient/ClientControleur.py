import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QListWidgetItem
from PyQt6.QtCore import Qt

from ClientVue import ClientVue
from ClientModel import ClientModel

class ClientControleur:
    def __init__(self):
        self.modele = ClientModel()
        self.vue = ClientVue()

        self.tous_les_produits = self.modele.get_tous_les_produits()

        self.vue.liste_categories.addItems(self.modele.get_categories())
        self.vue.liste_categories.itemClicked.connect(self.afficher_produits)
        self.vue.liste_produits.itemClicked.connect(self.ajouter_produit)
        self.vue.bouton_fermer.clicked.connect(self.effacer_liste)
        self.vue.bouton_sauvegarder.clicked.connect(self.sauvegarder)
        self.vue.bouton_charger.clicked.connect(self.charger)
        self.vue.bouton_aleatoire.clicked.connect(self.generer_aleatoire)
        self.vue.liste_sous_categories.itemClicked.connect(self.retirer_produit)
        self.vue.search_bar.textChanged.connect(self.filtrer_produits)
        self.vue.bouton_cest_parti.clicked.connect(self.lancer_chemin)

        self.vue.showMaximized()

    def afficher_produits(self, item):
        self.categorie_actuelle = item.text()
        produits = self.modele.get_produits_categorie(self.categorie_actuelle)
        self.update_liste_produits(produits)

    def update_liste_produits(self, produits):
        self.vue.liste_produits.clear()
        for produit in produits:
            widget_item = QListWidgetItem(f"+ {produit}")
            widget_item.setData(Qt.ItemDataRole.UserRole, produit)
            self.vue.liste_produits.addItem(widget_item)

    def filtrer_produits(self):
        texte = self.vue.search_bar.text().lower().strip()
        if not texte:
            self.vue.liste_produits.clear()
            return
        suggestions = [p for p in self.tous_les_produits if texte in p.lower()]
        self.update_liste_produits(suggestions)

    def ajouter_produit(self, item):
        produit = item.data(Qt.ItemDataRole.UserRole)
        self.modele.ajouter_produit(produit)
        self.mettre_a_jour_affichage_liste()

    def retirer_produit(self, item):
        texte = item.text()
        produit = texte[2:].split(" (")[0]
        self.modele.retirer_produit(produit)
        self.mettre_a_jour_affichage_liste()

    def mettre_a_jour_affichage_liste(self):
        self.vue.liste_sous_categories.clear()
        for produit, quantite in self.modele.get_liste_courses().items():
            self.vue.liste_sous_categories.addItem(f"- {produit} ({quantite})")
        total = sum(self.modele.get_liste_courses().values())
        self.vue.label_total.setText(f"Total articles : {total}")

    def effacer_liste(self):
        self.modele.effacer_liste()
        self.vue.liste_sous_categories.clear()
        self.vue.label_total.setText("Total articles : 0")

    def sauvegarder(self):
        fileName, _ = QFileDialog.getSaveFileName(self.vue, "Sauvegarder", "", "JSON Files (*.json)")
        if fileName:
            self.modele.sauvegarder_liste(fileName)

    def charger(self):
        fileName, _ = QFileDialog.getOpenFileName(self.vue, "Charger", "", "JSON Files (*.json)")
        if fileName:
            self.modele.charger_liste(fileName)
            self.mettre_a_jour_affichage_liste()

    def generer_aleatoire(self):
        self.modele.generer_liste_aleatoire()
        self.mettre_a_jour_affichage_liste()

    def lancer_chemin(self):
        liste_courses = list(self.modele.get_liste_courses().keys())
        if not liste_courses:
            return
        coords_produits = self.modele.get_coords_produits(liste_courses)
        chemin = self.modele.get_chemin("48,AL", liste_courses)
        self.vue.afficher_chemin(chemin, coords_produits)
