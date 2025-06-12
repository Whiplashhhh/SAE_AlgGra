import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QApplication

class Infos(QWidget):
    def __init__(self, callback_on_save):
        super().__init__()

        self.callback_on_save = callback_on_save
        self.setWindowTitle("Création d'un nouveau projet")
        self.layout = QVBoxLayout()

        self.champs = {}

        # Demande classique des infos projet
        for label_text in ["Nom du projet", "Auteur", "Nom du magasin", "Adresse du magasin"]:
            self.layout.addWidget(QLabel(label_text))
            line_edit = QLineEdit()
            self.champs[label_text] = line_edit
            self.layout.addWidget(line_edit)

        # Date auto
        self.date_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.layout.addWidget(QLabel(f"Date de création : {self.date_creation}"))

        # Choix du plan (image uniquement)
        self.bouton_plan = QPushButton("Choisir le plan du magasin (image)")
        self.bouton_plan.clicked.connect(self.choisir_plan)
        self.layout.addWidget(self.bouton_plan)
        self.chemin_plan = ""

        # Bouton valider
        self.bouton_valider = QPushButton("Créer le projet")
        self.bouton_valider.clicked.connect(self.valider)
        self.layout.addWidget(self.bouton_valider)

        self.setLayout(self.layout)

    def choisir_plan(self):
        fichier, _ = QFileDialog.getOpenFileName(self, "Choisir le plan du magasin", "", "Images (*.jpg *.png)")
        if fichier:
            self.chemin_plan = fichier

    def valider(self):
        nom_projet = self.champs["Nom du projet"].text().strip()

        if not nom_projet:
            QMessageBox.warning(self, "Erreur", "Le nom du projet est obligatoire.")
            return

        if not self.chemin_plan:
            QMessageBox.warning(self, "Erreur", "Vous devez choisir un plan de magasin.")
            return

        # On construit le projet.json avec les chemins auto générés
        dossier_projet = QFileDialog.getExistingDirectory(self, "Choisir le dossier de sauvegarde du projet")

        if not dossier_projet:
            return

        chemin_positions = os.path.join(dossier_projet, "positions_categories.json")
        chemin_produits = os.path.join(dossier_projet, f"produits_par_categories_{nom_projet}.json")

        # Copie du fichier positions_categories fixe
        if not os.path.exists(chemin_positions):
            # on suppose que ton fichier positions_categories est à la racine de ton projet actuel
            chemin_positions_source = os.path.join(os.getcwd(), "positions_categories.json")
            if os.path.exists(chemin_positions_source):
                with open(chemin_positions_source, "r", encoding="utf-8") as src, open(chemin_positions, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            else:
                QMessageBox.critical(self, "Erreur", "Le fichier positions_categories.json de base est introuvable.")
                return

        # Création du fichier produits_par_categories vide
        if not os.path.exists(chemin_produits):
            with open(chemin_produits, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)

        infos_projet = {
            "nom_projet": nom_projet,
            "auteur": self.champs["Auteur"].text(),
            "nom_magasin": self.champs["Nom du magasin"].text(),
            "adresse_magasin": self.champs["Adresse du magasin"].text(),
            "date_creation": self.date_creation,
            "plan_magasin": self.chemin_plan,
            "positions_categories": chemin_positions,
            "produits_par_categories": chemin_produits
        }

        # On sauvegarde le projet.json
        chemin_projet = os.path.join(dossier_projet, f"{nom_projet}.json")
        with open(chemin_projet, "w", encoding="utf-8") as f:
            json.dump(infos_projet, f, indent=4, ensure_ascii=False)

        self.callback_on_save(infos_projet)
        self.close()

# === test indépendant (à supprimer après intégration) ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Infos(lambda infos: print(infos))
    f.show()
    sys.exit(app.exec())