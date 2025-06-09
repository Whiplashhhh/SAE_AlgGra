import sys
from PyQt6.QtWidgets import QApplication, QWidget, \
                            QGraphicsScene, QGraphicsView, QGraphicsItem, \
                            QGraphicsPixmapItem, QGraphicsRectItem, \
                            QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QPen, QPixmap, QColor
from PyQt6.QtCore import Qt


# --- class Scene: hérite de QGraphicScene -----------------------------------
class Scene(QGraphicsScene):
    '''Class précisant les éléments de la scène graphique'''

    def __init__(self):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__()

        self.setSceneRect(0., 0., 500., 500.)                  # coord. réelles

        # une image
        self.image = QGraphicsPixmapItem(QPixmap(sys.path[0] + '/paysage.jpg'))
        self.image.setPos(20, 300)
        
        # un peu de texte
        self.texte = self.addText("Hello")
        self.texte.setPos(200,20)
        
        # quelques brosses de couleur
        brosse1 = QBrush(Qt.GlobalColor.red)           # couleur de remplissage
        brosse2 = QBrush(Qt.GlobalColor.blue)          # (à la brosse)
        brosse3 = QBrush(QColor(127, 0, 127))

        # quelques crayons de couleur
        crayon1 = QPen(Qt.GlobalColor.cyan)            # couleur de tracé
        crayon1.setWidth(3)                            # (au crayon)
        crayon2 = QPen(Qt.GlobalColor.green)
        crayon2.setWidth(2)
        crayon3 = QPen(QColor(127, 0, 127))
        crayon3.setWidth(5)

        # un rectangle
        rectangle = QGraphicsRectItem(200, 50, 400, 100)
        # rectangle.setPos(50, 20)
        rectangle.setBrush(brosse1)
        rectangle.setPen(crayon1)
        rectangle.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        # une ellipse (ou cercle, ou disque)
        ellipse = QGraphicsEllipseItem(100, 100, 400, 300)
        ellipse.setPos(75, 30)
        ellipse.setBrush(brosse2)
        ellipse.setPen(crayon2)
        ellipse.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # un trait
        trait = QGraphicsLineItem(0, 0, 500, 500)
        trait.setPen(crayon3)

        # ajout des éléments
        self.addItem(self.image)
        self.addItem(ellipse)
        self.addItem(rectangle)
        self.addItem(trait)
        
        ellipse.setZValue(2)                       # Option : position relative
        rectangle.setZValue(3)                     # des éléments dans la scène
        trait.setZValue(1)

        
        

# --- class Rendu : hérite de QGraphicsView -----------------------------------
class Rendu(QGraphicsView):
    '''Class faisant le rendu de la scène décrite au-dessus'''

    def __init__(self):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__()
        
        scene = Scene()
        self.setScene(scene)
        # self.fitInView(0, 0, 500, 500)




# --- class Fenêtre : hérite de QWidget ---------------------------------------
class Fenetre(Rendu):
    '''Class faisant le rendu de la scène décrite au-dessus'''

    def __init__(self):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__()
        
        self.showMaximized()
        
        



# --- main ------------------------------------------------------------------
if __name__ == "__main__":
    
    print(f' --- main --- ')
    # création d'une QApplication
    app = QApplication(sys.argv)

    # creation d'un widget
    f = Fenetre()

    # lancement de l'application
    sys.exit(app.exec())