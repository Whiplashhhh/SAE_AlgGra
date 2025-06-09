import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, \
                            QLabel, QPushButton, QWidget, QComboBox

from PyQt6.QtCore import Qt, QAbstractItemModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem



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


class ComboCheck(QComboBox) :

    def __init__(self):
        super().__init__()
        self.setModel(QStandardItemModel())
        self.view().pressed.connect(self.handleItemPressed)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if index.row() != 0:
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)

    
class Exemple2(QWidget) :

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Exemple')
        self.setFixedSize(500, 600)
        
        self.layoutCombo: QHBoxLayout = QHBoxLayout()
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bouton: QPushButton = QPushButton('Bouton à cliquer')
        self.bouton.setMaximumSize(200, 20)
        self.bouton.clicked.connect(self.affichage)

        self.combo: QComboBox = QComboBox()
        self.combo.addItems(['Liste de produits', '  ☐ produit1', '  ☐ produit2', '  ☐ produit3'])
        self.combo.activated.connect(self.caseCombo)

        self.combo2 : QComboBox = ComboCheck()
        self.combo2.addItem('Liste de produits')
        for i in range(1, 4):
            self.combo2.addItem('  produit' + str(i))
            item = self.combo2.model().item(i, 0)
            item.setCheckState(Qt.CheckState.Unchecked)
        
        self.label: QLabelDemo = QLabelDemo()
        self.label.setFixedSize(150, 50)

        self.layoutCombo.addWidget(self.combo)
        self.layoutCombo.addSpacing(30)
        self.layoutCombo.addWidget(self.combo2)        
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addSpacing(100)
        self.layout.addLayout(self.layoutCombo)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.bouton)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(100)

        self.setMouseTracking(True)
        
        self.show()


    def caseCombo(self, indice) -> None:
        texte:str = self.combo.itemText(indice)
        if texte[2] == '☐':
            self.combo.setItemText(indice, '  ☑' + texte[3:])
        elif texte[2] == '☑':
            self.combo.setItemText(indice, '  ☐' + texte[3:])


    def mousePressEvent(self, event) -> None :
        print('Position :', event.position().x(), event.position().y())


    def mouseMoveEvent(self, event) -> None :
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