import sys
import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QApplication
from ProjetInfos import ProjetInfos

class GestionProjet(QWidget):
    def __init__(self, callback_on_loaded):
        super().__init__()

        self.callback_on_loaded = callback_on_loaded
        self.setWindowTitle("Gestion de projet")
        self.layout = QVBoxLayout()

        self.bouton_creer = QPushButton("Créer un nouveau projet")
        self.bouton_creer.clicked.connect(self.creer_projet)
        self.layout.addWidget(self.bouton_creer)

        self.bouton_charger = QPushButton("Charger un projet existant")
        self.bouton_charger.clicked.connect(self.charger_projet)
        self.layout.addWidget(self.bouton_charger)

        self.setLayout(self.layout)

    def creer_projet(self):
        self.fenetre_creation = ProjetInfos(self.callback_creation_terminee)
        self.fenetre_creation.show()

    def callback_creation_terminee(self, infos_projet):
        self.callback_on_loaded(infos_projet)
        self.close()

    def charger_projet(self):
        fichier, _ = QFileDialog.getOpenFileName(self, "Charger un projet existant", "", "JSON (*.json)")
        if fichier:
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    infos_projet = json.load(f)
                self.callback_on_loaded(infos_projet)
                self.close()
            except:
                QMessageBox.critical(self, "Erreur", "Impossible de charger le fichier projet.")