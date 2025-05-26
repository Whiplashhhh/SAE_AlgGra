import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, \
                            QLabel, QPushButton, QWidget, QComboBox

from PyQt6.QtCore import Qt



class QLabelDemo(QLabel) :
    
    def __init__(self):
        super().__init__()

        self.__histoire: list = []
        
        self.setText('Je suis un label')
        self.setAutoFillBackground(True)
        self.setFrameStyle(3)
        self.setMouseTracking(True)


    def getHistory(self) -> list :
        return self.__histoire
        

    def mouseMoveEvent(self, event) -> None :
        if self.__histoire == [] or self.__histoire[0] != 'survol':
            print('je survole')
            self.__histoire = ['survol'] + self.__histoire


    def enterEvent(self, event) -> None :
        print('je rentre')
        self.__histoire = ['entrée'] + self.__histoire


    def leaveEvent(self, event) -> None :
        print('je sors')
        self.__histoire = ['sortie'] + self.__histoire


   
class Exemple2(QWidget) :

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Exemple')
        self.setFixedSize(500, 500)
        
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bouton: QPushButton = QPushButton('Bouton à cliquer')
        self.bouton.setMaximumSize(200, 20)
        self.bouton.clicked.connect(self.affichage)

        self.combo: QComboBox = QComboBox()
        self.combo.addItems(['☐ produit1', '☐ produit2', '☐ produit3'])
        self.combo.activated.connect(self.caseCombo)

        self.label: QLabelDemo = QLabelDemo()
        self.label.setFixedSize(150, 50)
        
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.combo)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.bouton)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(100)

        self.setMouseTracking(True)
        
        self.show()


    def caseCombo(self, indice) -> None:
        texte:str = self.combo.itemText(indice)
        if texte[0] == '☐':
            self.combo.setItemText(indice, '☑' + texte[1:])
        else:
            self.combo.setItemText(indice, '☐' + texte[1:])


    def mousePressEvent(self, event) -> None :
        print('Position :', event.position().x(), event.position().y())


    def keyPressEvent(self, event) -> None :
        if event.modifiers() and Qt.Modifier.CTRL :
            if event.key() == Qt.Key.Key_A:
                print('Touche CTRL + A')


    def affichage(self) -> None :
        print(self.label.getHistory())
        

    # def closeEvent(self, event) -> None:         # A éviter
    #     event.ignore()



# --- main -----------------------------------------------------------------
if __name__ == '__main__':

    app = QApplication(sys.argv)

    main = Exemple2()
    
    sys.exit(app.exec())