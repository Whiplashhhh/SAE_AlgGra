import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel
from PyQt6.QtGui import QPixmap, QPolygon
from PyQt6.QtCore import QPoint, QSize, QRect
from PyQt6.QtCore import Qt



class Exemple3(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Surfaces cliquables')
        self.setGeometry(100, 100, 400,400)
        
        self.plan = QPixmap(sys.path[0] + "/paysage.jpg")
        self.plan.scaledToWidth(400)
        self.pixmap_label = QLabel()
        self.pixmap_label.setPixmap(self.plan.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatio))
        self.pixmap_label.setMinimumWidth(400)

        # signal
        self.pixmap_label.mousePressEvent = self.img_click

        # création des surfaces
        surface_1 = QPolygon(QRect(0, 0, 200, 200))
        surface_2 = QPolygon() << QPoint(200, 0) << QPoint(400, 0) << QPoint(400, 200) << QPoint(200, 200)
        surface_3 = QPolygon() << QPoint(0, 200) << QPoint(200, 200) << QPoint(200, 400) << QPoint(0, 400)

        # dictionnaire référençant les surfaces et les slots associés
        self.surfaces = {
            1 : {
                'polygone': surface_1,
                'func': self.func1
            },
            2 : {
                'polygone': surface_2,
                'func': self.func2
            },
            3 : {
                'polygone': surface_3,
                'func': self.func3
            },
            4 : {
                'polygone': None,
                'func': self.funcNone
            }
        }

        # définition du layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.pixmap_label)
        self.setLayout(layout)

        self.show()



    def resize(self)-> None:
        self.pixmap_label.resize(self.size())
        self.pixmap_label.setPixmap(self.plan.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatio))

    
    def resizeEvent(self, event)-> None:
        self.resize()
        super().resizeEvent(event)


    def img_click(self, event)-> None:
        pos = event.pos()
        n = 1

        while n < 4 and not self.surfaces[n]['polygone'].containsPoint(pos, Qt.FillRule.OddEvenFill):
            n += 1
            
        self.surfaces[n]['func']()
        

    # fonctions appelées après clic
    def func1(self) -> None :
        print('première surface')


    def func2(self) -> None :
        print('deuxième surface')

    
    def func3(self) -> None :
        print('troisième surface')


    def funcNone(self) -> None :
        print('pas de surface cliquable')



# --- main ------------------------------------------------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    f = Exemple3()
    
    sys.exit(app.exec())