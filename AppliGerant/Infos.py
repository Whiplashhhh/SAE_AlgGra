# ========================= INFOS DIALOG : Infos.py ==========================
# Rôle : Fenêtre pour créer ou charger un projet (nom, auteur, plan, etc.)
# ============================================================================

import json
import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox

class Infos(QWidget):
    """
    Fenêtre pour saisir les infos du projet ou charger un projet existant
    """
    def __init__(self, callback_on_save):
        super().__init__()
        self.callback_on_save = callback_on_save
        self.setWindowTitle("Création d'un nouveau projet")
        self.layout = QVBoxLayout()
        self.champs = {}

        # Création des champs à remplir pour l'utilisateur
        for label_text in ["Nom du projet", "Auteur", "Nom du magasin", "Adresse du magasin"]:
            self.layout.addWidget(QLabel(label_text))
            line_edit = QLineEdit()
            self.champs[label_text] = line_edit
            self.layout.addWidget(line_edit)

        # Date automatique
        self.date_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.layout.addWidget(QLabel(f"Date de création : {self.date_creation}"))

        # Sélection du plan 
        self.bouton_plan = QPushButton("Choisir le plan du magasin (image)")
        self.bouton_plan.clicked.connect(self.choisir_plan)
        self.layout.addWidget(self.bouton_plan)
        self.chemin_plan = ""

        # Boutons de validation et de chargement projet
        self.bouton_valider = QPushButton("Créer le projet")
        self.bouton_valider.clicked.connect(self.valider)
        self.layout.addWidget(self.bouton_valider)

        self.bouton_charger = QPushButton("Charger un projet existant")
        self.bouton_charger.clicked.connect(self.charger_projet_existant)
        self.layout.addWidget(self.bouton_charger)

        self.setLayout(self.layout)

    def choisir_plan(self):
        """
        Choisit le plan du magasin (image)
        """
        fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir le plan du magasin",
            os.path.join(os.getcwd(), "Plans"),  # Définit le dossier Plan par défaut
            "Images (*.jpg *.png)"
        )        
        if fichier:
            self.chemin_plan = fichier

    def valider(self):
        """
        Crée un nouveau projet et les fichiers nécessaires
        """
        nom_projet = self.champs["Nom du projet"].text().strip()
        if not nom_projet:
            QMessageBox.warning(self, "Erreur", "Le nom du projet est obligatoire.")
            return
        if not self.chemin_plan:
            QMessageBox.warning(self, "Erreur", "Vous devez choisir un plan de magasin.")
            return

        # Le dossier de sauvegarde du projet sera toujours 'Projets/' 
        dossier_projet = os.path.join(os.getcwd(), "Projets")
        if not os.path.exists(dossier_projet):
            os.makedirs(dossier_projet)

        # Toujours utiliser Plans/plan.jpg, copie si besoin
        dossier_plans = os.path.join(os.getcwd(), "Plans")
        if not os.path.exists(dossier_plans):
            os.makedirs(dossier_plans)
            
        # On prend le chemin du plan
        chemin_plan = "Plans/plan.jpg"

        # Fichiers du projet : TOUJOURS dans json/
        chemin_positions = "json/positions_categories.json"
        chemin_produits = f"json/produits_par_categories_{nom_projet}.json"
        chemin_cases = "json/graphe.json"

        # Création fichier produits vide si pas déjà créé
        if not os.path.exists(os.path.join(os.getcwd(), chemin_produits)):
            with open(os.path.join(os.getcwd(), chemin_produits), "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)

        #Enregistrement du json projet
        infos_projet = {
            "nom_projet": nom_projet,
            "auteur": self.champs["Auteur"].text(),
            "nom_magasin": self.champs["Nom du magasin"].text(),
            "adresse_magasin": self.champs["Adresse du magasin"].text(),
            "date_creation": self.date_creation,
            "plan_magasin": chemin_plan,
            "positions_categories": chemin_positions,
            "produits_par_categories": chemin_produits,
            "cases_utiles": chemin_cases
        }
        chemin_projet = os.path.join(dossier_projet, f"{nom_projet}.json")
        with open(chemin_projet, "w", encoding="utf-8") as f:
            json.dump(infos_projet, f, indent=4, ensure_ascii=False)
        self.callback_on_save(infos_projet)
        self.close()

    def charger_projet_existant(self):
        """
        Charge un projet existant déjà créé
        """
        fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Charger un projet existant",
            os.path.join(os.getcwd(), "Projets"),  # Définit le dossier Projets par défaut
            "JSON (*.json)"
)
        if fichier:
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    infos_projet = json.load(f)
                self.callback_on_save(infos_projet)
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de charger le fichier projet.\n{e}")
