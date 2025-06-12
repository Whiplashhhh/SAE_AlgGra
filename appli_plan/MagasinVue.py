# Auteurs:
#   Willem Vanbaelinghem--Dezitter - TPA
#   Alex François - TPA
# création -> 09/06/2025
# dernière MAJ -> 11/06/2025

import sys
import json
from PyQt6.QtWidgets import QApplication, \
                            QGraphicsScene, QGraphicsView, \
                            QGraphicsPixmapItem, QGraphicsRectItem, \
                            QGraphicsTextItem, QMessageBox
from PyQt6.QtGui import QGuiApplication,QBrush, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt
from MagasinModel import MagasinModel

class CaseMagasin(QGraphicsRectItem):
    def __init__(self, x, y, width, height,ligne,colonne,modele):
        super().__init__(x, y, width, height)
        self.ligne = ligne
        self.colonne = colonne
        self.modele = modele
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
        #print(f"Case sélectionnée: Ligne {self.ligne+1}, Colonne {lettre_colonne}")
        # msg= QMessageBox()
        # msg.setText(f"Case sélectionnée: Ligne {self.ligne+1}, Colonne {lettre_colonne}")
        # msg.exec()

        key = f"{self.ligne+1},{lettre_colonne}"
        #print(f"Case sélectionnée: Ligne {self.ligne+1}, Colonne {lettre_colonne} (clé: {key})")
        
        # Vérifie si la case est utile avant d'afficher les produits
        if self.modele.is_case_util(self.ligne, self.colonne):
            self.modele.afficher_produits_case(key)  # Utilise la clé correcte
        else:
            print(f"Case inutile : pas de produit à afficher.")
        super().mousePressEvent(event)

class SceneMagasin(QGraphicsScene):
    '''Class précisant les éléments de la scène graphique'''
    def __init__(self,modele):
        '''Constructeur de la classe'''
        super().__init__()
        self.modele = modele

        # Chargement du plan
        pixmap = QPixmap(sys.path[0] + '/plan.jpg')
        pixmap = pixmap.scaled(self.modele.largeur_plan, self.modele.hauteur_plan, Qt.AspectRatioMode.KeepAspectRatio)

        self.plan = QGraphicsPixmapItem(pixmap)
        self.addItem(self.plan)

        larg = pixmap.width()
        haut = pixmap.height()
        
        self.tailleX = larg / self.modele.colonnes
        self.tailleY = haut / self.modele.lignes
        
        self.add_grid_labels(larg, haut, self.modele.lignes, self.modele.colonnes)

        self.setSceneRect(-30, -30, larg+60, haut+60)

        # Quadrillage
        self.rectangles = []  # Liste pour stocker les rectangles du quadrillage
        for i in range(self.modele.lignes):
            for j in range(self.modele.colonnes):
                x = j * self.tailleX
                y = i * self.tailleY
                rect = CaseMagasin(x, y, self.tailleX, self.tailleY, i, j,self.modele)
                                
                if not self.modele.is_case_util(i, j):
                    rect.setBrush(QBrush(QColor(50, 50, 50, 100))) #gris transparent (cases inutiles)
                else:
                    rect.setBrush(QBrush(Qt.GlobalColor.transparent)) #cases utiles
                    
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
            y = -17  # au-dessus de la première ligne
            label_width = label.boundingRect().width()
            label.setPos(x + (width / colonnes) / 2 - label_width / 2, y)
            self.addItem(label)
        
        # Labels de lignes (1, 2, 3, ...)
        for i in range(lignes):
            label = QGraphicsTextItem(str(i + 1))
            label.setFont(font)
            x = -20  # à gauche de la première colonne
            y = i * (height / lignes)
            label_height = label.boundingRect().height()
            label.setPos(x, y + (height / lignes) / 2 - label_height / 2)
            self.addItem(label)
            

class MagasinVue(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.modele = MagasinModel("./graphe.json", "./positions_categories.json", "./produits_par_categories.json")

        self.scene_magasin = SceneMagasin(self.modele)
        self.setScene(self.scene_magasin)
        
        # fenêtre redimensionnable
        self.setMinimumSize(950, 700)
        
        # fit automatique
        self.fitInView(self.scene_magasin.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        # Facteur de zoom
        self.echelle = 1.0
        self.first_fit = True  # pour ne pas recalculer en boucle

    def resizeEvent(self, event):
        '''Ajuste la scène quand la fenêtre est redimensionnée (mais seulement au départ)'''
        if self.first_fit:
            self.fitInView(self.scene_magasin.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.echelle = self.transform().m11()  # on récupère le facteur appliqué
            self.first_fit = False
        super().resizeEvent(event)
        
    
    def wheelEvent(self, event):
        '''Gestion du zoom avec la molette de la souris'''
        zoom_in = 1.1
        zoom_out = 0.9
        
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

    view = MagasinVue()
    view.show()
    
    # Centrer la fenêtre au milieu de l'écran
    screen = QGuiApplication.primaryScreen().geometry()
    window = view.frameGeometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    view.move(x, y)

    # lancement de l'application
    sys.exit(app.exec())
