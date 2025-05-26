import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QApplication



class SignalTrace(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Repérage de signaux')

        self.btn1: QPushButton = QPushButton("Bouton 1")
        self.btn1.setProperty('Message', "Coucou, je suis le bouton 1. L'autre ne sert à rien")
        
        self.btn2: QPushButton = QPushButton("Bouton 2")
        self.btn2.setProperty('Message', "Ne cliquez pas sur l'autre bouton. Il dit nimp.")
        
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)
        
        self.widget_2_bouttons: QWidget = QWidget()
        self.widget_2_bouttons.setLayout(self.layout)

        self.setCentralWidget(self.widget_2_bouttons)

        # Signaux
        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)

        # activation de la barre de statut
        self.statusBar()

        self.show()


    def buttonClicked(self) -> None :
        emetteur: sender = self.sender()
        affichage: str = emetteur.text() + ' : ' + emetteur.property('Message')
        self.statusBar().showMessage(affichage)

    

# --- main --------------------------------------------------------------------
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    exemple: SignalTrace = SignalTrace()
    
    sys.exit(app.exec())