
import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ]);

HAUTEUR = TBL.shape [1]
LARGEUR = TBL.shape [0]

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            if((x==4 and y==3) or (x==4 and y==15) or (x==12 and y==15) or (x==12 and y==3)):
               GUM[x][y] = 2 # super pacgums
            else:
               GUM[x][y] = 1
   return GUM


GUM = PlacementsGUM()
score = 0
PacGumMange = 0
PacManDirection = ""
PacManPos = [4,11]

   # Toutes les cartes de distance ( pac-man, pacgums et ghosts)
DistPacGum=np.zeros(TBL.shape,dtype=np.int32)
DistGhosts=np.zeros(TBL.shape,dtype=np.int32)
DistPacMan=np.zeros(TBL.shape,dtype=np.int32)
DistPinkGhost  =np.zeros(TBL.shape,dtype=np.int32)
DistOrangeGhost=np.zeros(TBL.shape,dtype=np.int32)
DistCyanGhost  =np.zeros(TBL.shape,dtype=np.int32)
DistRedGhost   =np.zeros(TBL.shape,dtype=np.int32)
DistPinkGhostChase  =np.zeros(TBL.shape,dtype=np.int32)
DistCyanGhostChase  =np.zeros(TBL.shape,dtype=np.int32)
DistComeBack = np.zeros(TBL.shape,dtype=np.int32)

   # clocks pour gerer la durée des differents états de pac-man et des ghosts
clock = 0
clockAppeure = 0
clockGhosts = 0


Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR//2,  "pink"  , dir , "libre"  , "chasse","vivant"])
Ghosts.append(  [    7     ,     9     ,  "orange", dir , "enferme", "chasse","vivant"])
Ghosts.append(  [    9     ,     9     ,  "cyan"  , dir , "enferme", "chasse","vivant"])
Ghosts.append(  [    13    ,     7     ,  "red"   , dir , "libre"  , "chasse","vivant"])



##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################



ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' :
      PAUSE_FLAG = not PAUSE_FLAG

Window.bind("<KeyPress>", keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")
PoliceGameOver = tkfont.Font(family='Arial', size=50, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM

# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message,data1,data2):
   global anim_bouche

   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)

   canvas.delete("all")

   # murs

   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x)
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")

   # pacgum et super pacgum
   if(not Collision()):
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if ( GUM[x][y] == 1):
                  xx = To(x)
                  yy = To(y)
                  e = 5
                  canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            elif( GUM[x][y] == 2):
                  xx = To(x)
                  yy = To(y)
                  e = 7
                  canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="red")


   # dessine pacman
   xx = To(PacManPos[0])
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche]
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche


   #dessine les fantomes
   dec = -3
   for F in Ghosts:
      xx = To(F[0])
      yy = To(F[1])
      e = 16

      if(EtatGhosts() == "chasse" or EtatGhosts() == "fuite"):
         if(F == Ghosts[0]):
            F[2]= "pink"
         if(F == Ghosts[1]):
            F[2]= "orange"
         if(F == Ghosts[2]):
            F[2]= "cyan"
         if(F==Ghosts[3]):
            F[2]= "red"
      else:
         F[2] = "white"

      coul = F[2]

      # corps du fantome
      if(F[6]!="mort"):
         CreateCircle(dec+xx,dec+yy-e+6,e,coul)
         canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)

      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")

      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")

      dec += 3

   # texte

   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)




AfficherPage(0)

#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

   #Carte des distances
      # des pac gums
def InitCartePacGum():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (GUM[x][y] == 1  or GUM[x][y] == 2):
            DistPacGum[x][y] = 0
         elif(TBL[x][y]==1 or TBL[x][y]==2):
            DistPacGum[x][y] = 200
         else:
            DistPacGum[x][y]=100

      # de Pacman
def InitCartePacMan():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1):
            DistPacMan[x][y] = 200
         elif(TBL[x][y]==2):
            DistPacMan[x][y] = 150
         else:
            DistPacMan[x][y]=100

   DistPacMan[PacManPos[0]][PacManPos[1]] = 0

      # des ghosts
def InitCarteGhosts():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1 or TBL[x][y]==2):
            DistGhosts[x][y] = 200
         else:
            DistGhosts[x][y] = 100
   for F in Ghosts:
      if(TBL[F[0]][F[1]]!=2 and F[6]=="vivant"):
         DistGhosts[F[0]][F[1]]=0

      # du ghost rose par rapport au coin en haut à gauche
def InitCartePinkGhost():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1 ):
            DistPinkGhost[x][y] = 200
         elif(TBL[x][y]==2):
            DistPinkGhost[x][y] = 150
         else:
            DistPinkGhost[x][y]=100
   DistPinkGhost[1][1] = 0

      # du ghost orange par rapport au coin en haut à droite
def InitCarteOrangeGhost():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1 ):
            DistOrangeGhost[x][y] = 200
         elif(TBL[x][y]==2):
            DistOrangeGhost[x][y] = 150
         else:
            DistOrangeGhost[x][y]=100
   DistOrangeGhost[15][1] = 0

      # du ghost cyan par rapport au coin en bas à droite
def InitCarteCyanGhost():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1 ):
            DistCyanGhost[x][y] = 200
         elif(TBL[x][y]==2):
            DistCyanGhost[x][y] = 150
         else:
            DistCyanGhost[x][y]=100
   DistCyanGhost[1][17] = 0

      # du ghost rouge par rapport au coin en bas à gauche
def InitCarteRedGhost():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1):
            DistRedGhost[x][y] = 200
         elif(TBL[x][y]==2):
            DistRedGhost[x][y] = 150
         else:
            DistRedGhost[x][y]=100
   DistRedGhost[15][17] = 0

      # du ghost rose quand il est en mode chasse
def InitCartePinkGhostChase():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1):
            DistPinkGhostChase[x][y] = 200
         elif(TBL[x][y]==2):
            DistPinkGhostChase[x][y] = 150
         else:
            DistPinkGhostChase[x][y]=100

   x = PacManPos[0]
   y = PacManPos[1]
   if(PacManDirection=="haut"):
      if(x-4<0 and y-4<0):    # on gère pour chaque direction le cas ou la case ciblé par le ghost rose sort du terrain
         DistPinkGhostChase[x-1][y-1] = 0
      elif(x-4<0 and y-4>=0):
         DistPinkGhostChase[x-1][y-4] = 0
      elif(x-4>=0 and y-4<0):
         DistPinkGhostChase[x-4][y-1] = 0
      else:
         DistPinkGhostChase[x-4][y-4] = 0
   elif(PacManDirection=="bas"):
      if(y+4>18):
         DistPinkGhostChase[x][y+1] = 0
      else:
         DistPinkGhostChase[x][y+4] = 0
   elif(PacManDirection=="droite"):
      if(x+4>16):
         DistPinkGhostChase[x+1][y] = 0
      else:
         DistPinkGhostChase[x+4][y] = 0
   elif(PacManDirection=="gauche"):
      if(x-4<0):
         DistPinkGhostChase[x-1][y] = 0
      else:
         DistPinkGhostChase[x-4][y] = 0

      # du ghost bleu quand il est en mode chasse
def InitCarteCyanGhostChase():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1):
            DistCyanGhostChase[x][y] = 200
         elif(TBL[x][y]==2):
            DistCyanGhostChase[x][y] = 150
         else:
            DistCyanGhostChase[x][y]=100

   x= PacManPos[0]
   y= PacManPos[1]
   xx= Ghosts[3][0]-x
   yy= Ghosts[3][1]-y
   if(x-xx<0 or x-xx>16 or y-yy<0 or y-yy>18):
      DistCyanGhostChase[1][17] = 0
   else:
      DistCyanGhostChase[x-xx][y-yy] = 0

      # du chemin de retour des ghost lorsqu'ils sont mangé
def InitCarteComeBack():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y]==1):
            DistComeBack[x][y] = 200
         elif(TBL[x][y]==2):
            DistRedGhost[x][y] = 150
         else:
            DistComeBack[x][y]=100
   DistComeBack[int(LARGEUR/2)][int(HAUTEUR/2)] = 0

   #Mise à jour de la carte  des distances
      # des pac-gums
def MajCartePacGum():
   changements=True
   while(changements):
      changements = False
      for y in range(1,HAUTEUR):
         for x in range(1,LARGEUR):
            if(DistPacGum[x][y]!=200):
               a=min(DistPacGum[x+1][y],DistPacGum[x-1][y])
               b=min(DistPacGum[x][y+1],DistPacGum[x][y-1])
               c=min(a,b)+1
               if(DistPacGum[x][y]>c):
                  DistPacGum[x][y]= c
                  changements = True

      # de Pacman
def MajCartePacMan():
   changements=True
   while(changements):
      changements = False
      for y in range(1,HAUTEUR):
         for x in range(1,LARGEUR):
            if(DistPacMan[x][y]!=200 and DistPacMan[x][y]!=150):
               a=min(DistPacMan[x+1][y],DistPacMan[x-1][y])
               b=min(DistPacMan[x][y+1],DistPacMan[x][y-1])
               c=min(a,b)+1
               if(DistPacMan[x][y]>c):
                  DistPacMan[x][y]= c
                  changements = True

      # des ghosts
def MajCarteGhosts():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR):
         for x in range(1,LARGEUR):
            if(DistGhosts[x][y]!=200):
               a=min(DistGhosts[x+1][y],DistGhosts[x-1][y])
               b=min(DistGhosts[x][y+1],DistGhosts[x][y-1])
               c=min(a,b)+1
               if(DistGhosts[x][y]>c):
                  DistGhosts[x][y]= c
                  MajDistGhost = True

      # du coin en haut à gauche pour le ghost rose
def MajCartePinkGhost():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistPinkGhost[x][y]!=200 and DistPinkGhost[x][y]!=150):
               a=min(DistPinkGhost[x+1][y],DistPinkGhost[x-1][y])
               b=min(DistPinkGhost[x][y+1],DistPinkGhost[x][y-1])
               c=min(a,b)+1
               if(DistPinkGhost[x][y]>c):
                  DistPinkGhost[x][y]= c
                  MajDistGhost = True

      # du coin en haut à droite pour le ghost orange
def MajCarteOrangeGhost():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistOrangeGhost[x][y]!=200 and DistOrangeGhost[x][y]!=150):
               a=min(DistOrangeGhost[x+1][y],DistOrangeGhost[x-1][y])
               b=min(DistOrangeGhost[x][y+1],DistOrangeGhost[x][y-1])
               c=min(a,b)+1
               if(DistOrangeGhost[x][y]>c):
                  DistOrangeGhost[x][y]= c
                  MajDistGhost = True

      # du coin en bas à droite pour le ghost cyan
def MajCarteCyanGhost():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistCyanGhost[x][y]!=200 and DistCyanGhost[x][y]!=150):
               a=min(DistCyanGhost[x+1][y],DistCyanGhost[x-1][y])
               b=min(DistCyanGhost[x][y+1],DistCyanGhost[x][y-1])
               c=min(a,b)+1
               if(DistCyanGhost[x][y]>c):
                  DistCyanGhost[x][y]= c
                  MajDistGhost = True

      # du coin en bas à gauche pour le ghost rouge
def MajCarteRedGhost():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistRedGhost[x][y]!=200 and DistRedGhost[x][y]!=150):
               a=min(DistRedGhost[x+1][y],DistRedGhost[x-1][y])
               b=min(DistRedGhost[x][y+1],DistRedGhost[x][y-1])
               c=min(a,b)+1
               if(DistRedGhost[x][y]>c):
                  DistRedGhost[x][y]= c
                  MajDistGhost = True

      # de la case ou doit aller le ghost rose quand il chasse
def MajCartePinkGhostChase():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistPinkGhostChase[x][y]!=200 and DistPinkGhostChase[x][y]!=150):
               a=min(DistPinkGhostChase[x+1][y],DistPinkGhostChase[x-1][y])
               b=min(DistPinkGhostChase[x][y+1],DistPinkGhostChase[x][y-1])
               c=min(a,b)+1
               if(DistPinkGhostChase[x][y]>c):
                  DistPinkGhostChase[x][y]= c
                  MajDistGhost = True

      # de la case ou doit aller le ghost bleu quand il chasse
def MajCarteCyanGhostChase():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistCyanGhostChase[x][y]!=200 and DistCyanGhostChase[x][y]!=150):
               a=min(DistCyanGhostChase[x+1][y],DistCyanGhostChase[x-1][y])
               b=min(DistCyanGhostChase[x][y+1],DistCyanGhostChase[x][y-1])
               c=min(a,b)+1
               if(DistCyanGhostChase[x][y]>c):
                  DistCyanGhostChase[x][y]= c
                  MajDistGhost = True

   # du retour a la maison des ghost une fois mangé
def MajCarteComeBack():
   MajDistGhost = True
   while(MajDistGhost):
      MajDistGhost = False
      for y in range(1,HAUTEUR-1):
         for x in range(1,LARGEUR-1):
            if(DistComeBack[x][y]!=200 and DistComeBack[x][y]!=150):
               a=min(DistComeBack[x+1][y],DistComeBack[x-1][y])
               b=min(DistComeBack[x][y+1],DistComeBack[x][y-1])
               c=min(a,b)+1
               if(DistComeBack[x][y]>c):
                  DistComeBack[x][y]= c
                  MajDistGhost = True

   #Etats de Pac man
def EtatPacMan():
   etat = ""
   x,y = PacManPos
   if(clock>0 and clock <=15):
      etat = "chasse"
   elif(DistGhosts[x][y]<= 3 and etat != "chasse" and EtatGhosts()!="apeure"):
      etat = "fuite"
   else:
      etat = "mange"
   return etat

   #Etats des ghosts
def EtatGhosts():
   etat = ""
   for F in Ghosts:
      if(clockAppeure>0 and clockAppeure<=8):
         F[5]="apeure"
      else:
         if(clockGhosts>=0 and clockGhosts<=10):
            F[5]="chasse"
         elif(clockGhosts>10 and clockGhosts<=18):
            F[5]="fuite"
         elif(clockGhosts>18 and clockGhosts<=33):
            F[5]="chasse"
         elif(clockGhosts>33 and clockGhosts<=41):
            F[5]="fuite"
         elif(clockGhosts>41 and clockGhosts<=56):
            F[5]="chasse"
         elif(clockGhosts>56 and clockGhosts<=64):
            F[5]="fuite"
         else:
            F[5]="chasse"
      etat = F[5]
   return etat

   #Collisions
def Collision():
   global score, clockAppeure
   collision = False
   for F in Ghosts:
      if( PacManPos[0]==F[0] and PacManPos[1]==F[1] and F[6] != "mort"):
         if(EtatPacMan()=="chasse" or EtatGhosts()=="apeure" ):
            score += 2000
            F[6] = "mort"
            clockAppeure = 1
         else:
            collision=True
            return collision
   return collision


   #Directions où peut aller Pac-man, en fonction de son Etat
def PacManPossibleMove():
    L = []
    x,y = PacManPos
    if(EtatPacMan()=="mange"):

        caseHaut   = DistPacGum[x][y-1]
        caseBas    = DistPacGum[x][y+1]
        caseDroite = DistPacGum[x+1][y]
        caseGauche = DistPacGum[x-1][y]

        if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
            L.append((0,-1,"haut"))
        if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
            L.append((0, 1,"bas"))
        if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
            L.append(( 1,0,"droite"))
        if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
            L.append((-1,0,"gauche"))

    else:
        caseHaut = DistGhosts[x][y-1]
        caseBas = DistGhosts[x][y+1]
        caseDroite = DistGhosts[x+1][y]
        caseGauche = DistGhosts[x-1][y]

        if(EtatPacMan()=="chasse"):
            if(caseHaut<=caseBas and caseHaut<=caseGauche and caseHaut<=caseDroite):
                L.append((0,-1,"haut"))
            if(caseBas<=caseHaut and caseBas<=caseGauche and caseBas<=caseDroite):
                L.append((0, 1,"bas"))
            if(caseDroite<=caseBas and caseDroite<=caseGauche and caseDroite<=caseHaut):
                L.append(( 1,0,"droite"))
            if(caseGauche<=caseBas and caseGauche<=caseHaut and caseGauche<=caseDroite):
                L.append((-1,0,"gauche"))
        else:
            max = 0

            if(caseHaut>=max and caseHaut<200)  :max=caseHaut
            if(caseBas>=max and caseBas<200)      :max=caseBas
            if(caseDroite>=max and caseDroite<200):max=caseDroite
            if(caseGauche>=max and caseGauche<200):max=caseGauche

            if(max==caseHaut):
                L.append((0,-1,"haut"))
            elif(max==caseBas):
                L.append((0,1,"bas"))
            elif(max==caseDroite):
                L.append((1,0,"droite"))
            elif(max==caseGauche):
                L.append((-1,0,"gauche"))
    return L

   #Directions où peuvent aller chaques ghosts, en fonction de leurs Etats et personnalité
def GhostsPossibleMove(X,Y,F):
   x = int(X)
   y = int(Y)
   L = []
   if(F[6]=="mort"):
      caseHaut   = DistComeBack[x][y-1]
      caseBas    = DistComeBack[x][y+1]
      caseDroite = DistComeBack[x+1][y]
      caseGauche = DistComeBack[x-1][y]

      if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
            L.append((0,-1,"haut"))
      if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
            L.append((0, 1,"bas"))
      if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
            L.append(( 1,0,"droite"))
      if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
            L.append((-1,0,"gauche"))

      if(x == 8 and y == 9):
         F[6] = "vivant"

   elif(F[5]=="apeure"):
      caseActuelle= TBL[x][y]
      caseHaut    = TBL[x][y-1]
      caseBas     = TBL[x][y+1]
      caseDroite  = TBL[x+1][y]
      caseGauche  = TBL[x-1][y]

      if ( caseHaut   == 0 or (caseActuelle==2 and caseHaut   == 2)):
         L.append((0,-1,"haut"))
      if ( caseBas    == 0 or (caseActuelle==2 and caseBas    == 2)):
         L.append((0, 1,"bas"))
      if ( caseDroite == 0 or (caseActuelle==2 and caseDroite == 2)):
         L.append(( 1,0,"droite"))
      if ( caseGauche == 0 or (caseActuelle==2 and caseGauche == 2)):
         L.append((-1,0,"gauche"))

   elif(F[5]=="fuite"):
      if(F==Ghosts[0]):
         caseHaut   = DistPinkGhost[x][y-1]
         caseBas    = DistPinkGhost[x][y+1]
         caseDroite = DistPinkGhost[x+1][y]
         caseGauche = DistPinkGhost[x-1][y]
      elif(F==Ghosts[1]):
         caseHaut   = DistOrangeGhost[x][y-1]
         caseBas    = DistOrangeGhost[x][y+1]
         caseDroite = DistOrangeGhost[x+1][y]
         caseGauche = DistOrangeGhost[x-1][y]
      elif(F==Ghosts[2]):
         caseHaut   = DistCyanGhost[x][y-1]
         caseBas    = DistCyanGhost[x][y+1]
         caseDroite = DistCyanGhost[x+1][y]
         caseGauche = DistCyanGhost[x-1][y]
      elif(F==Ghosts[3]):
         caseHaut   = DistRedGhost[x][y-1]
         caseBas    = DistRedGhost[x][y+1]
         caseDroite = DistRedGhost[x+1][y]
         caseGauche = DistRedGhost[x-1][y]

      if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
            L.append((0,-1,"haut"))
      if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
            L.append((0, 1,"bas"))
      if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
            L.append(( 1,0,"droite"))
      if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
            L.append((-1,0,"gauche"))

   else: # Etat chase

      caseHaut   = DistPacMan[x][y-1]
      caseBas    = DistPacMan[x][y+1]
      caseDroite = DistPacMan[x+1][y]
      caseGauche = DistPacMan[x-1][y]

      if (F == Ghosts[0]) : # fantome pink
         caseHaut   = DistPinkGhostChase[x][y-1]
         caseBas    = DistPinkGhostChase[x][y+1]
         caseDroite = DistPinkGhostChase[x+1][y]
         caseGauche = DistPinkGhostChase[x-1][y]

         if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
               L.append((0,-1,"haut"))
         if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
               L.append((0, 1,"bas"))
         if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
               L.append(( 1,0,"droite"))
         if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
               L.append((-1,0,"gauche"))


      elif(F == Ghosts[1]) : # fantome orange
         if(caseHaut <= 6 or caseBas <= 6 or caseDroite <= 6 or caseGauche <= 6) :#il fuit
            caseHaut   = DistOrangeGhost[x][y-1]
            caseBas    = DistOrangeGhost[x][y+1]
            caseDroite = DistOrangeGhost[x+1][y]
            caseGauche = DistOrangeGhost[x-1][y]

            if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
                  L.append((0,-1,"haut"))
            if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
                  L.append((0, 1,"bas"))
            if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
                  L.append(( 1,0,"droite"))
            if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
                  L.append((-1,0,"gauche"))


         else :#il chasse pac-man comme le ghost rouge
            if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
                  L.append((0,-1,"haut"))
            if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
                  L.append((0, 1,"bas"))
            if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
                  L.append(( 1,0,"droite"))
            if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
                  L.append((-1,0,"gauche"))


      elif (F == Ghosts[2]) : # fantome cyan
         caseHaut   = DistCyanGhostChase[x][y-1]
         caseBas    = DistCyanGhostChase[x][y+1]
         caseDroite = DistCyanGhostChase[x+1][y]
         caseGauche = DistCyanGhostChase[x-1][y]

         if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
               L.append((0,-1,"haut"))
         if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
               L.append((0, 1,"bas"))
         if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
               L.append(( 1,0,"droite"))
         if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
               L.append((-1,0,"gauche"))


      elif (F == Ghosts[3]) : # fantome red
         if(caseHaut<=caseBas and caseHaut<=caseDroite and caseHaut<=caseGauche):
               L.append((0,-1,"haut"))
         if(caseBas<=caseHaut and caseBas<=caseDroite and caseBas<=caseGauche):
               L.append((0, 1,"bas"))
         if(caseDroite<=caseHaut and caseDroite<=caseBas and caseDroite<=caseGauche):
               L.append(( 1,0,"droite"))
         if(caseGauche<=caseHaut and caseGauche<=caseBas and caseGauche<=caseDroite):
               L.append((-1,0,"gauche"))

   return L


def GhostHaut(F):
   x = F[0]
   y = F[1]
   return TBL[x][y-1]==0
def GhostBas(F):
   x = F[0]
   y = F[1]
   return TBL[x][y+1]==0
def GhostDroite(F):
   x = F[0]
   y = F[1]
   return TBL[x+1][y]==0
def GhostGauche(F):
   x = F[0]
   y = F[1]
   return TBL[x-1][y]==0


def IA():
   global PacManPos, Ghosts, PacManDirection

   # initialisation et MAJ de toutes les cartes
   InitCartePacGum()
   InitCarteGhosts()
   InitCartePacMan()
   InitCartePinkGhost()
   InitCarteOrangeGhost()
   InitCarteCyanGhost()
   InitCarteRedGhost()
   InitCartePinkGhostChase()
   InitCarteCyanGhostChase()
   InitCarteComeBack()


   MajCartePacGum()
   MajCarteGhosts()
   MajCartePacMan()
   MajCartePinkGhost()
   MajCarteOrangeGhost()
   MajCarteCyanGhost()
   MajCarteRedGhost()
   MajCartePinkGhostChase()
   MajCarteCyanGhostChase()
   MajCarteComeBack()

   # conditions pour enfermer temporairement les ghosts orange et cyan
   if(PacGumMange>=20): Ghosts[1][4]="libre"
   else: Ghosts[1][4]="enferme"
   if(PacGumMange>=40): Ghosts[2][4]="libre"
   else: Ghosts[2][4]="enferme"

   if(PacGumMange >= 150):
      return


   if(not Collision()):

      #deplacement Pacman
      L = PacManPossibleMove()
      if(len(L)>1):
         choix = random.randrange(len(L))
         PacManPos[0] += L[choix][0]
         PacManPos[1] += L[choix][1]
         PacManDirection = L[choix][2]
      else:
         PacManPos[0] += L[0][0]
         PacManPos[1] += L[0][1]
         PacManDirection = L[0][2]

   if(not Collision()):

      #deplacement Fantome
      for F in Ghosts:

         T = GhostsPossibleMove(F[0],F[1],F)

         # intersections
         if(F[4]=="libre"):
            if(len(T)>2 or len(T)==1):
               choix = random.randrange(len(T))
               F[0] += T[choix][0]
               F[1] += T[choix][1]
               F[3] =  T[choix][2]
            # virages
            else:
               if (F[3]=="haut"):
                  if(GhostHaut(F)):
                     F[3] = "haut"
                     F[1] -= 1
                  elif(GhostDroite(F)):
                     F[3] = "droite"
                     F[0] += 1
                  elif(GhostGauche(F)):
                     F[3] = "gauche"
                     F[0] -= 1
               elif (F[3]=="bas"):
                  if(GhostBas(F)):
                     F[3] = "bas"
                     F[1] += 1
                  elif(GhostDroite(F)):
                     F[3] = "droite"
                     F[0] += 1
                  elif(GhostGauche(F)):
                     F[3] = "gauche"
                     F[0] -= 1
               elif (F[3]=="droite"):
                  if(GhostHaut(F)):
                     F[3] = "haut"
                     F[1] -= 1
                  elif(GhostBas(F)):
                     F[3] = "bas"
                     F[1] += 1
                  elif(GhostDroite(F)):
                     F[3] = "droite"
                     F[0] += 1
               elif (F[3]=="gauche"):
                  if(GhostHaut(F)):
                     F[3] = "haut"
                     F[1] -= 1
                  elif(GhostBas(F)):
                     F[3] = "bas"
                     F[1] += 1
                  elif(GhostGauche(F)):
                     F[3] = "gauche"
                     F[0] -= 1



#  Boucle principale de votre jeu appelée toutes les 500ms


def MainLoop():
   global score, DistPacGum, clock, DistGhosts, PacGumMange, clockGhosts, clockAppeure


   if(clockAppeure>0 and clockAppeure<=8):
      clockAppeure += 1
   else:
      clockAppeure = 0
      clockGhosts += 1

   if not PAUSE_FLAG : IA()
   if(EtatPacMan()=="chasse" and clock <=15):
      clock += 1
      coul = "red"
   else:
      clock = 0
      coul = "yellow"

   Affiche(PacmanColor = coul, message = "message", data1=DistPacGum, data2=DistGhosts)


   # supprimer les pac-gums que pacman à mangé
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(PacManPos == [x,y]):
            if(GUM[x][y] == 1):
               GUM[x][y] = 0
               score += 100
               PacGumMange += 1
            elif(GUM[x][y] == 2):
               GUM[x][y] = 0
               score += 500
               clock = 0
               clock += 1

   # affichage du score et des pac-gum mangé
   canvas.create_text( 80, screenHeight- 50 , text = "Pac-Gum:", fill ="red", font = PoliceTexte)
   canvas.create_text( 70, screenHeight- 20 , text = PacGumMange, fill ="red", font = PoliceTexte)
   canvas.create_text(screeenWidth - 70, screenHeight- 50 , text = "SCORE:", fill ="red", font = PoliceTexte)
   canvas.create_text(screeenWidth - 70, screenHeight- 20 , text = score, fill ="red", font = PoliceTexte)

   # affichage de l'écran de défaite ou de victoire
   if(Collision() == True):
      canvas.create_text( screeenWidth - 370, screenHeight - 280 , text = "GAME OVER !", fill ="yellow", font = PoliceTexte)
      return
   elif(PacGumMange == 150):
      canvas.create_text( screeenWidth - 370, screenHeight - 280 , text = "YOU WIN !", fill ="yellow", font = PoliceTexte)
      return


   #DistPacGum info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(DistCyanGhostChase[x][y]!=200 and DistCyanGhostChase[x][y]!=150 and DistCyanGhostChase[x][y]!=100):
            xx = To(x)
            yy = To(y) + 11
            canvas.create_text(xx,yy, text = DistCyanGhostChase[x][y], fill ="pink", font=("Purisa", 8))



###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()













