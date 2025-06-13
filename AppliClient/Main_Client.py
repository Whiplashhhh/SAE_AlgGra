# =========================== main.py ===========================
# Point d'entrée de l'application - lance toute l'IHM du projet
# ===============================================================

import sys
from PyQt6.QtWidgets import QApplication
from ClientControleur import ClientControleur

if __name__ == "__main__":
    app = QApplication(sys.argv)

    fenetre = ClientControleur()

    sys.exit(app.exec())