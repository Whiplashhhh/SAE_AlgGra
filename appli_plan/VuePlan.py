# Auteur:
#   Willem VANBAELINGHEM--DEZITTER - TPA
# création -> 09/06/2025
# dernière MAJ -> 10/06/2025

import sys
from PyQt6.QtWidgets import QApplication, \
                            QGraphicsScene, QGraphicsView, \
                            QGraphicsPixmapItem, QGraphicsRectItem
from PyQt6.QtGui import QGuiApplication ,QBrush, QPixmap
from PyQt6.QtCore import Qt

class SceneMagasin(QGraphicsScene):
    '''Class précisant les éléments de la scène graphique'''

    def __init__(self):
        '''Constructeur de la classe'''
        
        # appel au constructeur de la classe mère        
        super().__init__() 
  
        #dimmension du plan      
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
        self.lignes, self.colonnes = 52, 52
        self.tailleX = larg / self.colonnes
        self.tailleY = haut / self.lignes
        self.rectangles = []
        for i in range(self.lignes):
            for j in range(self.colonnes):
                rect = QGraphicsRectItem(j*self.tailleX, i*self.tailleY, self.tailleX, self.tailleY)
                rect.setBrush(QBrush(Qt.GlobalColor.transparent))
                rect.setPen(Qt.GlobalColor.gray)
                rect.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
                self.addItem(rect)
                self.rectangles.append(rect)
                
    def majGrille(self, scale):
        '''Met à jour le quadrillage en fonction du facteur de zoom'''
        for i in range(self.lignes):
            for j in range(self.colonnes):
                rect = self.rectangles[i*self.colonnes + j]
                rect.setRect(j * self.tailleX * scale, 
                             i * self.tailleY * scale, 
                             self.tailleX * scale, 
                             self.tailleY * scale)
                
class MagasinView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene_magasin = SceneMagasin()
        self.setScene(self.scene_magasin)

        # Facteur de zoom
        self.echelle = 1.0
        
    
    def wheelEvent(self, event):
        '''Gestion du zoom avec la molette de la souris'''
        zoom_in = 1.25
        zoom_out = 0.8
        
        if event.angleDelta().y() > 0:  # Molette vers le haut 
            self.echelle *= zoom_in
        else:                           # Molette vers le bas
            self.echelle *= zoom_out
            
        self.resetTransform()
        self.scale(self.echelle, self.echelle)
            
        

# --- main ------------------------------------------------------------------
if __name__ == "__main__":
    
    print(f' --- main --- ')
    # création d'une QApplication
    app = QApplication(sys.argv)

    view = MagasinView()
    
    view.show()
    
    # Centrer la fenêtre au milieu de l'écran
    screen = QGuiApplication.primaryScreen().geometry()
    window = view.frameGeometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    view.move(x, y)

    # lancement de l'application
    sys.exit(app.exec())