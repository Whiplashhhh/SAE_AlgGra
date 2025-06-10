# Auteur:
#   Willem Vanbaelinghem--Dezitter - TPA
#   Alex François - TPA
# création -> 09/06/2025
# dernière MAJ -> 10/06/2025

import sys
from PyQt6.QtWidgets import QApplication, \
                            QGraphicsScene, QGraphicsView, \
                            QGraphicsPixmapItem, QGraphicsRectItem, \
                            QGraphicsTextItem, QMessageBox
from PyQt6.QtGui import QGuiApplication,QBrush, QPixmap, QFont
from PyQt6.QtCore import Qt

class CaseMagasin(QGraphicsRectItem):
    def __init__(self, x, y, width, height,ligne,colonne):
        super().__init__(x, y, width, height)
        self.ligne = ligne
        self.colonne = colonne
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.setPen(Qt.GlobalColor.gray)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        
    def mousePressEvent(self, event):
        colonne = self.colonne
        if colonne < 26:
            lettre_colonne = chr(ord('A') + colonne)
        else:
            lettre_colonne = 'A' + chr(ord('A') + (colonne - 26))
        print(f"Case sélectionnée: Ligne {self.ligne+1}, Colonne {lettre_colonne}")
        # msg= QMessageBox()
        # msg.setText(f"Case sélectionnée: Ligne {self.ligne+1}, Colonne {lettre_colonne}")
        # msg.exec()
        super().mousePressEvent(event)

class SceneMagasin(QGraphicsScene):
    '''Class précisant les éléments de la scène graphique'''
    def __init__(self):
        '''Constructeur de la classe'''
        super().__init__()

        # dimension du plan
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
        # Ajouter les labels pour les coordonnées
        self.add_grid_labels(larg, haut, self.lignes, self.colonnes)
        self.tailleX = larg / self.colonnes
        self.tailleY = haut / self.lignes
        self.rectangles = []  # Liste pour stocker les rectangles du quadrillage
        for i in range(self.lignes):
            for j in range(self.colonnes):
                rect = CaseMagasin(j*self.tailleX, i*self.tailleY, self.tailleX, self.tailleY, i, j)
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
                


    def add_grid_labels(self, width, height, lignes, colonnes):
        #Ajoute les labels de coordonnée
        font = QFont("Arial", 8)
        # Labels de colonnes (A, B, C, ...)
        for j in range(colonnes):
            label_char = chr(ord('A') + (j % 26))
            # Si plus de 26 colonnes, alors on pase à AA
            if j >= 26:
                label_char = 'A' + chr(ord('A') + (j - 26))
                label_str = 'A' + chr(ord('A') + (j - 26))
            else:
                label_str = chr(ord('A') + j)

            label = QGraphicsTextItem(label_str)
            label.setFont(font)
            x = j * (width / colonnes)
            y = -15  # au-dessus de la première ligne
            label_width = label.boundingRect().width()
            label.setPos(x + (width / colonnes) / 2 - label_width / 2, y)
            self.addItem(label)
        
        # Labels de lignes (1, 2, 3, ...)
        for i in range(lignes):
            label = QGraphicsTextItem(str(i + 1))
            label.setFont(font)
            x = -15  # à gauche de la première colonne
            y = i * (height / lignes)
            label_height = label.boundingRect().height()
            label.setPos(x, y + (height / lignes) / 2 - label_height / 2)
            self.addItem(label)
            

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
