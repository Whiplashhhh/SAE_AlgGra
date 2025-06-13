# =========================== main.py ===========================
# Point d'entrée de l'application - lance toute l'IHM du projet
# ===============================================================

import sys
from PyQt6.QtWidgets import QApplication
from MagasinVue import MagasinVue

if __name__ == "__main__":
    app = QApplication(sys.argv)

    fenetre = MagasinVue()

    sys.exit(app.exec())