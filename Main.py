import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox, QLineEdit

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lancement de l'application")
        self.resize(325, 100)

        layout = QVBoxLayout()

        label = QLabel("Sélectionne ton mode :")
        layout.addWidget(label)

        bouton_gerant = QPushButton("Mode Gérant")
        bouton_gerant.clicked.connect(self.lancer_gerant)
        layout.addWidget(bouton_gerant)

        bouton_client = QPushButton("Mode Client")
        bouton_client.clicked.connect(self.lancer_client)
        layout.addWidget(bouton_client)

        self.setLayout(layout)

    def lancer_gerant(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Mot de passe")
        dialog.setLabelText("Entre le mot de passe :")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)  # Affiche des ***
        ok = dialog.exec()
        mot_de_passe = dialog.textValue()
        if ok:
            if mot_de_passe == "VinsurVin":
                subprocess.Popen([sys.executable, "AppliGerant/Main_Gerant.py"])
                self.close()
            else:
                QMessageBox.critical(self, "Erreur", "Mot de passe incorrect !")

    def lancer_client(self):
        # On lance le script Main_Client.py
        subprocess.Popen([sys.executable, "AppliClient/Main_Client.py"])
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec())
