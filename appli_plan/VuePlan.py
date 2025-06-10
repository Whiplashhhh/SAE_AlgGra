# Auteur:
#   Willem VANBAELINGHEM--DEZITTER - TPA
# création -> 09/06/2025
# dernière MAJ -> 09/06/2025

import sys
from PyQt6.QtWidgets import QApplication, QWidget, \
                            QGraphicsScene, QGraphicsView, QGraphicsItem, \
                            QGraphicsPixmapItem, QGraphicsRectItem, \
                            QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QPen, QPixmap, QColor
from PyQt6.QtCore import Qt

class SceneMagasin(QGraphicsScene):
    '''Class précisant les éléments de la scène graphique'''

    def __init__(self):
        '''Constructeur de la classe'''
        
        # appel au constructeur de la classe mère        
        super().__init__() 
        
        largeur_plan = 1000
        hauteur_plan = 1000
        
        
        # Chargement du plan
        pixmap = QPixmap(sys.path[0] + '/plan.jpg')
        pixmap = pixmap.scaled(largeur_plan, hauteur_plan, Qt.AspectRatioMode.KeepAspectRatio)
        
        self.plan = QGraphicsPixmapItem(pixmap)
        self.addItem(self.plan)
        
        larg = pixmap.width()
        haut = pixmap.height()
        self.setSceneRect(0, 0, larg, haut)

        
        # Quadrillage
        lignes, colonnes = 22, 32
        tailleX = larg / colonnes
        tailleY = haut / lignes
        for i in range(lignes):
            for j in range(colonnes):
                rect = QGraphicsRectItem(j*tailleX, i*tailleY, tailleX, tailleY)
                rect.setBrush(QBrush(Qt.GlobalColor.transparent))
                rect.setPen(Qt.GlobalColor.gray)
                rect.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
                self.addItem(rect)
                
class MagasinView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene_magasin = SceneMagasin()
        self.setScene(self.scene_magasin)
        # taille adaptée à la scène
        self.setFixedSize(int(self.scene_magasin.width()) + 5, int(self.scene_magasin.height()) + 5)
        

# --- main ------------------------------------------------------------------
if __name__ == "__main__":
    
    print(f' --- main --- ')
    # création d'une QApplication
    app = QApplication(sys.argv)

    view = MagasinView()
    
    view.show()

    # lancement de l'application
    sys.exit(app.exec())