from engine import *
import pygame
from pygame.locals import *
from piece import *
import os
from sense_hat import SenseHat
import time
import sys
from tkinter import *
from threading import Thread

hat = SenseHat()
titre_fenetre = "Échiquier"
pygame.init()
erreur = pygame.mixer.Sound("sons/bruits/erreur.wav")
fenetre = pygame.display.set_mode((296, 396))
pygame.display.set_caption(titre_fenetre)
pygame.display.flip()
son = pygame.mixer.Sound("sons/bruits/gagné.wav")
n1 = pygame.mixer.Sound("sons/voix/nombres/1.wav")
n2 = pygame.mixer.Sound("sons/voix/nombres/2.wav")
n3 = pygame.mixer.Sound("sons/voix/nombres/3.wav")
n4 = pygame.mixer.Sound("sons/voix/nombres/4.wav")
n5 = pygame.mixer.Sound("sons/voix/nombres/5.wav")
n6 = pygame.mixer.Sound("sons/voix/nombres/6.wav")
n7 = pygame.mixer.Sound("sons/voix/nombres/7.wav")
n8 = pygame.mixer.Sound("sons/voix/nombres/8.wav")
na = pygame.mixer.Sound("sons/voix/lettres/a.wav")
nb = pygame.mixer.Sound("sons/voix/lettres/b.wav")
nc = pygame.mixer.Sound("sons/voix/lettres/c.wav")
nd = pygame.mixer.Sound("sons/voix/lettres/d.wav")
ne = pygame.mixer.Sound("sons/voix/lettres/e.wav")
nf = pygame.mixer.Sound("sons/voix/lettres/f.wav")
ng = pygame.mixer.Sound("sons/voix/lettres/g.wav")
nh = pygame.mixer.Sound("sons/voix/lettres/h.wav")
nperdt = pygame.mixer.Sound("sons/voix/mots/noirpert.wav")
bperdt = pygame.mixer.Sound("sons/voix/mots/blancpert.wav")
cade = pygame.mixer.Sound("sons/voix/mots/cadence.wav")
gopl = pygame.mixer.Sound("sons/voix/mots/go.wav")
joueur1 = pygame.mixer.Sound("sons/voix/mots/1_joueur.wav")
joueur2 = pygame.mixer.Sound("sons/voix/mots/2_joueur.wav")
au = pygame.mixer.Sound("sons/voix/mots/au.wav")
noir = pygame.mixer.Sound("sons/voix/mots/noir.wav")
blanc = pygame.mixer.Sound("sons/voix/mots/blanc.wav")
enplacej = pygame.mixer.Sound("sons/voix/mots/jeux_en_place.wav")
nompartie = pygame.mixer.Sound("sons/voix/mots/nom_partie.wav")
partieen_e = pygame.mixer.Sound("sons/voix/mots/enregistrement_de_la_p.wav")
partie_e = pygame.mixer.Sound("sons/voix/mots/partie_enregistré.wav")
v_en = pygame.mixer.Sound("sons/voix/mots/vouloir_enregistrer.wav")
rreur = pygame.mixer.Sound("sons/voix/mots/erreur.wav")
Dernier_coup = pygame.mixer.Sound("sons/voix/mots/dernier_coup_joué.wav")
Non_coup = pygame.mixer.Sound("sons/voix/mots/pas_de_coup_joué.wav")
an = pygame.mixer.Sound("sons/voix/mots/an.wav")

class Board:
    coord=[
        'a8','b8','c8','d8','e8','f8','g8','h8',
        'a7','b7','c7','d7','e7','f7','g7','h7',
        'a6','b6','c6','d6','e6','f6','g6','h6',
        'a5','b5','c5','d5','e5','f5','g5','h5',
        'a4','b4','c4','d4','e4','f4','g4','h4',
        'a3','b3','c3','d3','e3','f3','g3','h3',
        'a2','b2','c2','d2','e2','f2','g2','h2',
        'a1','b1','c1','d1','e1','f1','g1','h1',
        ]

    def __init__(self):
        self.init()

    def init(self):
        self.cases = [
            Piece('TOUR','noir'),Piece('CAVALIER','noir'),Piece('FOU','noir'),Piece('DAME','noir'),Piece('ROI','noir'),Piece('FOU','noir'),Piece('CAVALIER','noir'),Piece('TOUR','noir'),
            Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),
            Piece('TOUR','blanc'),Piece('CAVALIER','blanc'),Piece('FOU','blanc'),Piece('DAME','blanc'),Piece('ROI','blanc'),Piece('FOU','blanc'),Piece('CAVALIER','blanc'),Piece('TOUR','blanc')
            ]
        self.side2move='blanc'
        self.ep=-1
        self.history=[]
        self.ply=0
        self.white_can_castle_56=True
        self.white_can_castle_63=True
        self.black_can_castle_0=True
        self.black_can_castle_7=True

    def gen_moves_list(self,color='',dontCallIsAttacked=False):
        if(color==''):
            color=self.side2move
        mList=[]
        for pos1,piece in enumerate(self.cases):
            if piece.couleur!=color:
                continue
            if(piece.nom=='ROI'):
                mList+=piece.pos2_roi(pos1,self.oppColor(color),self,dontCallIsAttacked)
                continue
            elif(piece.nom=='DAME'):
                mList+=piece.pos2_tour(pos1,self.oppColor(color),self)
                mList+=piece.pos2_fou(pos1,self.oppColor(color),self)
                continue
            elif(piece.nom=='TOUR'):
                mList+=piece.pos2_tour(pos1,self.oppColor(color),self)
                continue
            elif(piece.nom=='CAVALIER'):
                mList+=piece.pos2_cavalier(pos1,self.oppColor(color),self)
                continue
            elif(piece.nom=='FOU'):
                mList+=piece.pos2_fou(pos1,self.oppColor(color),self)
                continue
            if(piece.nom=='PION'):
                mList+=piece.pos2_pion(pos1,piece.couleur,self)
                continue
        return mList

    def setboard(self,fen):
        f=fen.split()
        err=""
        if(len(f)!=6):
            err+="\nErreur.\n"
            print(err)
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return False
        self.init()
        self.white_can_castle_56=False
        self.white_can_castle_63=False
        self.black_can_castle_0=False
        self.black_can_castle_7=False
        fen =   f[0]
        trait = f[1]
        roque = f[2]
        ep =    f[3]
        rule50= f[4]
        num =   f[5]
        i=0
        for c in fen:
            if(c=='k'):
                self.cases[i]=Piece('ROI','noir')
                i=i+1
            elif(c=='q'):
                self.cases[i]=Piece('DAME','noir')
                i=i+1
            elif(c=='r'):
                self.cases[i]=Piece('TOUR','noir')
                i=i+1
            elif(c=='n'):
                self.cases[i]=Piece('CAVALIER','noir')
                i=i+1
            elif(c=='b'):
                self.cases[i]=Piece('FOU','noir')
                i=i+1
            elif(c=='p'):
                self.cases[i]=Piece('PION','noir')
                i=i+1
            elif(c=='K'):
               self.cases[i]=Piece('ROI','blanc')
               i=i+1
            elif(c=='Q'):
               self.cases[i]=Piece('DAME','blanc')
               i=i+1
            elif(c=='R'):
                self.cases[i]=Piece('TOUR','blanc')
                i=i+1
            elif(c=='N'):
                self.cases[i]=Piece('CAVALIER','blanc')
                i=i+1
            elif(c=='B'):
                self.cases[i]=Piece('FOU','blanc')
                i=i+1
            elif(c=='P'):
                self.cases[i]=Piece('PION','blanc')
                i=i+1
            elif(c=='/'):
                pass
            else:
                try:
                    nb=int(c)
                except ValueError:
                    print('\nErreur.\n')
                    erreur.play()
                    time.sleep(0.6)
                    rreur.play()
                    time.sleep(0.7)
                    return
                cpt=0
                while(cpt<nb):
                    self.cases[i]=Piece()
                    cpt=cpt+1
                    i=i+1
        if(i!=64):
            print('\nErreur.\n')
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            self.init()
            return False
        if(trait=='b'):
            self.side2move='noir'
        else:
            self.side2move='blanc'
        if(roque!='-'):
            if('K' in roque):
                self.white_can_castle_63=True
            if('Q' in roque):
                self.white_can_castle_56=True
            if('k' in roque):
                self.black_can_castle_7=True
            if('q' in roque):
                self.black_can_castle_0=True
        if(ep not in self.coord):
            self.ep=-1
        else:
            self.ep=self.coord.index(ep)
        return True

    def getboard(self):
        emptySq=0
        s=''
        for i,piece in enumerate(self.cases):
            p=piece.nom
            c=piece.couleur
            if(emptySq==8):
                s+='8'
                emptySq=0
            if(i and i%8==0):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                s+='/'
            if(piece.isEmpty()):
                emptySq+=1
            elif(p=='ROI'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='k'
                else:
                    s+='K'
            elif(p=='DAME'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='q'
                else:
                    s+='Q'
            elif(p=='TOUR'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='r'
                else:
                    s+='R'
            elif(p=='CAVALIER'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='n'
                else:
                    s+='N'
            elif(p=='FOU'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='b'
                else:
                    s+='B'
            elif(p=='PION'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='p'
                else:
                    s+='P'
        if(emptySq>0):
            s+=str(emptySq)
        if(self.side2move=='blanc'):
            s+=' w '
        else:
            s+=' b '
        no_castle_right=True
        if(self.white_can_castle_63):
            s+='K'
            no_castle_right=False
        if(self.white_can_castle_56):
            s+='Q'
            no_castle_right=False
        if(self.black_can_castle_7):
            s+='k'
            no_castle_right=False
        if(self.black_can_castle_0):
            s+='q'
            no_castle_right=False
        if(no_castle_right):
            s+='-'
        if(self.ep!=-1):
            s+=' '+self.coord[self.ep]
        else:
            s+=' -'
        s+=' -'
        s+=' '+str(int(len(self.history)/2))
        return s

    def domove(self,depart,arrivee,promote):
        global quoit
        global azertyuiopmlkjhgfdsqwxcvbngtrvt
        pieceDeplacee=self.cases[depart]
        piecePrise=self.cases[arrivee]
        isEp=False
        histEp=self.ep
        hist_roque_56=self.white_can_castle_56
        hist_roque_63=self.white_can_castle_63
        hist_roque_0=self.black_can_castle_0
        hist_roque_7=self.black_can_castle_7
        flagViderEp=True
        self.cases[arrivee]=self.cases[depart]
        self.cases[depart]=Piece()
        self.ply+=1
        if(pieceDeplacee.nom=='PION'):
            if(pieceDeplacee.couleur=='blanc'):
                if(self.ep==arrivee):
                    if azertyuiopmlkjhgfdsqwxcvbngtrvt == False:
                        quoit = ('prise en passent blanc')
                    piecePrise=self.cases[arrivee+8]
                    self.cases[arrivee+8]=Piece()
                    isEp=True
                if(self.ROW(depart)==6 and self.ROW(arrivee)==4):
                    self.ep=arrivee+8
                    flagViderEp=False
            else:
                if(self.ep==arrivee):
                    quoit = ('prise en passent noir')
                    piecePrise=self.cases[arrivee-8]
                    self.cases[arrivee-8]=Piece()
                    isEp=True
                elif(self.ROW(depart)==1 and self.ROW(arrivee)==3):
                    self.ep=arrivee-8
                    flagViderEp=False
        elif(pieceDeplacee.nom=='TOUR'):
            if(pieceDeplacee.couleur=='blanc'):
                if(depart==56):
                    self.white_can_castle_56=False
                elif(depart==63):
                    self.white_can_castle_63=False
            else:
                if(depart==0):
                    self.black_can_castle_0=False
                elif(depart==7):
                    self.black_can_castle_7=False
        elif(pieceDeplacee.nom=='ROI'):
            if(pieceDeplacee.couleur=='blanc'):
                if(depart==60):
                    self.white_can_castle_56=False
                    self.white_can_castle_63=False
                    if(arrivee==58):
                        self.cases[56]=Piece()
                        self.cases[59]=Piece('TOUR','blanc')
                        quoit = ('grand rook blanc')
                    elif(arrivee==62):
                        self.cases[63]=Piece()
                        self.cases[61]=Piece('TOUR','blanc')
                        quoit = ('petit rook blanc')
            else:
                if(depart==4):
                    self.black_can_castle_0=False
                    self.black_can_castle_7=False
                    if(arrivee==6):
                        self.cases[7]=Piece()
                        self.cases[5]=Piece('TOUR','noir')
                        quoit = ('petit rook noir')
                    elif(arrivee==2):
                        self.cases[0]=Piece()
                        self.cases[3]=Piece('TOUR','noir')
                        quoit = ('grand rook noir')
        if(flagViderEp==True):
            self.ep=-1
        if(promote!=''):
            if(promote=='q'):
                self.cases[arrivee]=Piece('DAME',self.side2move)
            elif(promote=='r'):
                self.cases[arrivee]=Piece('TOUR',self.side2move)
            elif(promote=='n'):
                self.cases[arrivee]=Piece('CAVALIER',self.side2move)
            elif(promote=='b'):
                self.cases[arrivee]=Piece('FOU',self.side2move)
        self.changeTrait()
        self.history.append((depart,\
        arrivee,\
        pieceDeplacee,\
        piecePrise,\
        isEp,\
        histEp,\
        promote,\
        hist_roque_56,\
        hist_roque_63,\
        hist_roque_0,\
        hist_roque_7))
        if(self.in_check(self.oppColor(self.side2move))):
            self.undomove()
            return False
        return True

    def undomove(self):
        if(len(self.history)==0):
            print('\nPas de coup joué.\n')
            erreur.play()
            time.sleep(0.6)
            Non_coup.play()
            time.sleep(1)
            return
        lastmove=self.history[-1]
        pos1=lastmove[0]
        pos2=lastmove[1]
        piece_deplacee=lastmove[2]
        piece_prise=lastmove[3]
        isEp=lastmove[4]
        ep=lastmove[5]
        promote=lastmove[6]
        self.white_can_castle_56=lastmove[7]
        self.white_can_castle_63=lastmove[8]
        self.black_can_castle_0=lastmove[9]
        self.black_can_castle_7 =lastmove[10]
        self.ply-=1
        self.changeTrait()
        self.cases[pos1]=self.cases[pos2]
        self.ep=ep
        if(promote!=''):
            self.cases[pos1]=Piece('PION',self.side2move)
        self.cases[pos2]=piece_prise
        if(self.cases[pos1].nom=='PION'):
            if(isEp):
                self.cases[pos2]=Piece()
                if(self.cases[pos1].couleur=='noir'):
                    self.cases[pos2-8]=Piece('PION','blanc')
                else:
                    self.cases[pos2+8]=Piece('PION','noir')
        elif(self.cases[pos1].nom=='ROI'):
            if(self.cases[pos1].couleur=='blanc'):
                if(pos1==60):
                    if(pos2==58):
                        self.cases[56]=Piece('TOUR','blanc')
                        self.cases[59]=Piece()
                    elif(pos2==62):
                        self.cases[63]=Piece('TOUR','blanc')
                        self.cases[61]=Piece()
            else:
                if(pos1==4):
                    if(pos2==2):
                        self.cases[0]=Piece('TOUR','noir')
                        self.cases[3]=Piece()
                    elif(pos2==6):
                        self.cases[7]=Piece('TOUR','noir')
                        self.cases[5]=Piece()
        self.history.pop()

    def changeTrait(self):
        if(self.side2move=='blanc'):
            self.side2move='noir'
        else:
            self.side2move='blanc'

    def hhdhhgg(self):
        self.endgame = True

    def oppColor(self,c):
        if(c=='blanc'):
            return 'noir'
        else:
            return 'blanc'

    def in_check(self,couleur):
        for i in range(0,64):
            if(self.cases[i].nom=='ROI' and self.cases[i].couleur==couleur):
                pos=i
                break
        return self.is_attacked(pos,self.oppColor(couleur))

    def is_attacked(self,pos,couleur):
        mList=self.gen_moves_list(couleur,True)
        for pos1,pos2,promote in mList:
            if(pos2==pos):
                return True
        return False

    def render(self):
        global blabla
        global poi
        global tempn
        global tempb
        global nbtyrueioap
        p = (255,100,0)
        t = (255,100,0)
        r = (255,100,0)
        d = (255,100,0)
        c = (255,100,0)
        f = (255,100,0)
        X = (0,0,0)
        P = (255,255,255)
        T = (255,255,255)
        R = (255,255,255)
        D = (255,255,255)
        C = (255,255,255)
        F = (255,255,255)
        azertyuiop = ()
        poiuytreza = []
        blabla = []
        p1 = ("pion_noir")
        t1 = ("tour_noir")
        r1 = ("roi_noir")
        d1 = ("dame_noir")
        c1 = ("cavalier_noir")
        f1 = ("fou_noir")
        X1 = ("rien")
        P1 = ("pion_blanc")
        T1 = ("tour_blanc")
        R1 = ("roi_blanc")
        D1 = ("dame_blanc")
        C1 = ("cavalier_blanc")
        F1 = ("fou_blanc")
        p1 = str(p1)
        t1 = str(t1)
        r1 = str(r1)
        d1 = str(d1)
        c1 = str(c1)
        f1 = str(f1)
        X1 = str(X1)
        P1 = str(P1)
        T1 = str(T1)
        R1 = str(R1)
        D1 = str(D1)
        C1 = str(C1)
        F1 = str(F1)
        i,y=1,7
        for piece in self.cases:
            if(piece.couleur=='noir'):
                azertyuiop = (piece.nom[0].lower())
                if azertyuiop == 't':
                    poiuytreza.append(t)
                    blabla.append(t1)
                elif azertyuiop == 'r':
                    poiuytreza.append(r)
                    blabla.append(r1)
                elif azertyuiop == 'c':
                    poiuytreza.append(c)
                    blabla.append(c1)
                elif azertyuiop == 'f':
                    poiuytreza.append(f)
                    blabla.append(f1)
                elif azertyuiop == 'd':
                    poiuytreza.append(d)
                    blabla.append(d1)
                elif azertyuiop == 'p':
                    poiuytreza.append(p)
                    blabla.append(p1)
                elif azertyuiop == 'P':
                    poiuytreza.append(P)
                    blabla.append(P1)
                elif azertyuiop == '.':
                    poiuytreza.append(X)
                    blabla.append(X1)
                elif azertyuiop == 'T':
                    poiuytreza.append(T)
                    blabla.append(T1)
                elif azertyuiop == 'D':
                    poiuytreza.append(D)
                    blabla.append(D1)
                elif azertyuiop == 'R':
                    poiuytreza.append(R)
                    blabla.append(R1)
                elif azertyuiop == 'C':
                    poiuytreza.append(C)
                    blabla.append(C1)
                elif azertyuiop == 'F':
                    poiuytreza.append(F)
                    blabla.append(F1)
                azertyuiop = ()
            else:
                azertyuiop = (piece.nom[0])
                if azertyuiop == 't':
                    poiuytreza.append(t)
                    blabla.append(t1)
                elif azertyuiop == 'r':
                    poiuytreza.append(r)
                    blabla.append(r1)
                elif azertyuiop == 'c':
                    poiuytreza.append(c)
                    blabla.append(c1)
                elif azertyuiop == 'f':
                    poiuytreza.append(f)
                    blabla.append(f1)
                elif azertyuiop == 'd':
                    poiuytreza.append(d)
                    blabla.append(d1)
                elif azertyuiop == 'p':
                    poiuytreza.append(p)
                    blabla.append(p1)
                elif azertyuiop == 'P':
                    poiuytreza.append(P)
                    blabla.append(P1)
                elif azertyuiop == '.':
                    poiuytreza.append(X)
                    blabla.append(X1)
                elif azertyuiop == 'T':
                    poiuytreza.append(T)
                    blabla.append(T1)
                elif azertyuiop == 'D':
                    poiuytreza.append(D)
                    blabla.append(D1)
                elif azertyuiop == 'R':
                    poiuytreza.append(R)
                    blabla.append(R1)
                elif azertyuiop == 'C':
                    poiuytreza.append(C)
                    blabla.append(C1)
                elif azertyuiop == 'F':
                    poiuytreza.append(F)
                    blabla.append(F1)
                azertyuiop = ()
            if(i%8==0):
                y=y-1
            i+=1
        hat.set_pixels(poiuytreza)
        case1 = pygame.image.load("images/échequier/" + blabla[0] + "_1.jpg").convert()
        fenetre.blit(case1, (0,0))
        case2 = pygame.image.load("images/échequier/" + blabla[1] + "_0.jpg").convert()
        fenetre.blit(case2, (37,0))
        case3 = pygame.image.load("images/échequier/" + blabla[2] + "_1.jpg").convert()
        fenetre.blit(case3, (74,0))
        case4 = pygame.image.load("images/échequier/" + blabla[3] + "_0.jpg").convert()
        fenetre.blit(case4, (111,0))
        case5 = pygame.image.load("images/échequier/" + blabla[4] + "_1.jpg").convert()
        fenetre.blit(case5, (148,0))
        case6 = pygame.image.load("images/échequier/" + blabla[5] + "_0.jpg").convert()
        fenetre.blit(case6, (185,0))
        case7 = pygame.image.load("images/échequier/" + blabla[6] + "_1.jpg").convert()
        fenetre.blit(case7, (222,0))
        case8 = pygame.image.load("images/échequier/" + blabla[7] + "_0.jpg").convert()
        fenetre.blit(case8, (259,0))
        case9 = pygame.image.load("images/échequier/" + blabla[8] + "_0.jpg").convert()
        fenetre.blit(case9, (0,37))
        case10 = pygame.image.load("images/échequier/" + blabla[9] + "_1.jpg").convert()
        fenetre.blit(case10, (37,37))
        case11 = pygame.image.load("images/échequier/" + blabla[10] + "_0.jpg").convert()
        fenetre.blit(case11, (74,37))
        case12 = pygame.image.load("images/échequier/" + blabla[11] + "_1.jpg").convert()
        fenetre.blit(case12, (111,37))
        case13 = pygame.image.load("images/échequier/" + blabla[12] + "_0.jpg").convert()
        fenetre.blit(case13, (148,37))
        case14 = pygame.image.load("images/échequier/" + blabla[13] + "_1.jpg").convert()
        fenetre.blit(case14, (185,37))
        case15 = pygame.image.load("images/échequier/" + blabla[14] + "_0.jpg").convert()
        fenetre.blit(case15, (222,37))
        case16 = pygame.image.load("images/échequier/" + blabla[15] + "_1.jpg").convert()
        fenetre.blit(case16, (259,37))
        case17 = pygame.image.load("images/échequier/" + blabla[16] + "_1.jpg").convert()
        fenetre.blit(case17, (0,74))
        case18 = pygame.image.load("images/échequier/" + blabla[17] + "_0.jpg").convert()
        fenetre.blit(case18, (37,74))
        case19 = pygame.image.load("images/échequier/" + blabla[18] + "_1.jpg").convert()
        fenetre.blit(case19, (74,74))
        case20 = pygame.image.load("images/échequier/" + blabla[19] + "_0.jpg").convert()
        fenetre.blit(case20, (111,74))
        case21 = pygame.image.load("images/échequier/" + blabla[20] + "_1.jpg").convert()
        fenetre.blit(case21, (148,74))
        case22 = pygame.image.load("images/échequier/" + blabla[21] + "_0.jpg").convert()
        fenetre.blit(case22, (185,74))
        case23 = pygame.image.load("images/échequier/" + blabla[22] + "_1.jpg").convert()
        fenetre.blit(case23, (222,74))
        case24 = pygame.image.load("images/échequier/" + blabla[23] + "_0.jpg").convert()
        fenetre.blit(case24, (259,74))
        case25 = pygame.image.load("images/échequier/" + blabla[24] + "_0.jpg").convert()
        fenetre.blit(case25, (0,111))
        case26 = pygame.image.load("images/échequier/" + blabla[25] + "_1.jpg").convert()
        fenetre.blit(case26, (37,111))
        case27 = pygame.image.load("images/échequier/" + blabla[26] + "_0.jpg").convert()
        fenetre.blit(case27, (74,111))
        case28 = pygame.image.load("images/échequier/" + blabla[27] + "_1.jpg").convert()
        fenetre.blit(case28, (111,111))
        case29 = pygame.image.load("images/échequier/" + blabla[28] + "_0.jpg").convert()
        fenetre.blit(case29, (148,111))
        case30 = pygame.image.load("images/échequier/" + blabla[29] + "_1.jpg").convert()
        fenetre.blit(case30, (185,111))
        case31 = pygame.image.load("images/échequier/" + blabla[30] + "_0.jpg").convert()
        fenetre.blit(case31, (222,111))
        case32 = pygame.image.load("images/échequier/" + blabla[31] + "_1.jpg").convert()
        fenetre.blit(case32, (259,111))
        case33 = pygame.image.load("images/échequier/" + blabla[32] + "_1.jpg").convert()
        fenetre.blit(case33, (0,148))
        case34 = pygame.image.load("images/échequier/" + blabla[33] + "_0.jpg").convert()
        fenetre.blit(case34, (37,148))
        case35 = pygame.image.load("images/échequier/" + blabla[34] + "_1.jpg").convert()
        fenetre.blit(case35, (74,148))
        case36 = pygame.image.load("images/échequier/" + blabla[35] + "_0.jpg").convert()
        fenetre.blit(case36, (111,148))
        case37 = pygame.image.load("images/échequier/" + blabla[36] + "_1.jpg").convert()
        fenetre.blit(case37, (148,148))
        case38 = pygame.image.load("images/échequier/" + blabla[37] + "_0.jpg").convert()
        fenetre.blit(case38, (185,148))
        case39 = pygame.image.load("images/échequier/" + blabla[38] + "_1.jpg").convert()
        fenetre.blit(case39, (222,148))
        case40 = pygame.image.load("images/échequier/" + blabla[39] + "_0.jpg").convert()
        fenetre.blit(case40, (259,148))
        case41 = pygame.image.load("images/échequier/" + blabla[40] + "_0.jpg").convert()
        fenetre.blit(case41, (0,185))
        case42 = pygame.image.load("images/échequier/" + blabla[41] + "_1.jpg").convert()
        fenetre.blit(case42, (37,185))
        case43 = pygame.image.load("images/échequier/" + blabla[42] + "_0.jpg").convert()
        fenetre.blit(case43, (74,185))
        case44 = pygame.image.load("images/échequier/" + blabla[43] + "_1.jpg").convert()
        fenetre.blit(case44, (111,185))
        case45 = pygame.image.load("images/échequier/" + blabla[44] + "_0.jpg").convert()
        fenetre.blit(case45, (148,185))
        case46 = pygame.image.load("images/échequier/" + blabla[45] + "_1.jpg").convert()
        fenetre.blit(case46, (185,185))
        case47 = pygame.image.load("images/échequier/" + blabla[46] + "_0.jpg").convert()
        fenetre.blit(case47, (222,185))
        case48 = pygame.image.load("images/échequier/" + blabla[47] + "_1.jpg").convert()
        fenetre.blit(case48, (259,185))
        case49 = pygame.image.load("images/échequier/" + blabla[48] + "_1.jpg").convert()
        fenetre.blit(case49, (0,222))
        case50 = pygame.image.load("images/échequier/" + blabla[49] + "_0.jpg").convert()
        fenetre.blit(case50, (37,222))
        case51 = pygame.image.load("images/échequier/" + blabla[50] + "_1.jpg").convert()
        fenetre.blit(case51, (74,222))
        case52 = pygame.image.load("images/échequier/" + blabla[51] + "_0.jpg").convert()
        fenetre.blit(case52, (111,222))
        case53 = pygame.image.load("images/échequier/" + blabla[52] + "_1.jpg").convert()
        fenetre.blit(case53, (148,222))
        case54 = pygame.image.load("images/échequier/" + blabla[53] + "_0.jpg").convert()
        fenetre.blit(case54, (185,222))
        case55 = pygame.image.load("images/échequier/" + blabla[54] + "_1.jpg").convert()
        fenetre.blit(case55, (222,222))
        case56 = pygame.image.load("images/échequier/" + blabla[55] + "_0.jpg").convert()
        fenetre.blit(case56, (259,222))
        case57 = pygame.image.load("images/échequier/" + blabla[56] + "_0.jpg").convert()
        fenetre.blit(case57, (0,259))
        case58 = pygame.image.load("images/échequier/" + blabla[57] + "_1.jpg").convert()
        fenetre.blit(case58, (37,259))
        case59 = pygame.image.load("images/échequier/" + blabla[58] + "_0.jpg").convert()
        fenetre.blit(case59, (74,259))
        case60 = pygame.image.load("images/échequier/" + blabla[59] + "_1.jpg").convert()
        fenetre.blit(case60, (111,259))
        case61 = pygame.image.load("images/échequier/" + blabla[60] + "_0.jpg").convert()
        fenetre.blit(case61, (148,259))
        case62 = pygame.image.load("images/échequier/" + blabla[61] + "_1.jpg").convert()
        fenetre.blit(case62, (185,259))
        case63 = pygame.image.load("images/échequier/" + blabla[62] + "_0.jpg").convert()
        fenetre.blit(case63, (222,259))
        case64 = pygame.image.load("images/échequier/" + blabla[63] + "_1.jpg").convert()
        fenetre.blit(case64, (259,259))
        pygame.display.flip()
        print('\nAu '+self.side2move)
        au.play()
        time.sleep(0.6)
        if self.side2move == 'noir':
            poi = True
            noir.play()
            time.sleep(0.6)
        if self.side2move == 'blanc':
            poi = False
            blanc.play()
            time.sleep(0.6)
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        if poi == False:
            B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
            fenetre.blit(B, (132,377))
        elif poi == True:
            N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
            fenetre.blit(N, (158,377))
        PP = pygame.image.load("images/pendule/play.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        if nbtyrueioap > 0:
            Information = pygame.image.load("images/pendule/go.png").convert_alpha()
            fenetre.blit(Information, (133,313))
        pygame.display.flip()
        yyyui = 'eer'
        if(self.ep!=-1):
            yyyui = 'eettg'
        no_castle_right=True
        if(self.white_can_castle_63):
            no_castle_right=False
        if(self.white_can_castle_56):
            no_castle_right=False
        if(self.black_can_castle_7):
            no_castle_right=False
        if(self.black_can_castle_0):
            no_castle_right=False
        if(no_castle_right):
            dgdcebbfye = 2345678
        self.showHistory()

    def caseStr2Int(self,c):
        err=(
        '\nErreur.\n',
        '\nErreur.\n'
        )
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
        if(len(c)!=2):
            print(err[0])
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return -1
        if(c[0] not in letters):
            print(err[1])
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return -1
        if(c[1] not in numbers):
            print(err[1])
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return -1
        return self.coord.index(c)

    def rtyui(self):
        b.azsqzsqaz(self)

    def caseInt2Str(self,i):
        err=(
        '\nErreur.\n',
        )
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
        if(i<0 or i>63):
            print(err[0])
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return
        return self.coord[i]

    @staticmethod
    def ROW(x):
        return (x >> 3)

    @staticmethod
    def COL(x):
        return (x & 7)

    def showHistory(self):
        global zzzzzzzzzzzzzz
        global k
        global quoit
        juyjuyjuyjuy = []
        if(len(self.history)==0):
            return
        rtyui = ()
        cpt,aff=1.0,True
        for (depart,\
        arrivee,\
        pieceDeplacee,\
        piecePrise,\
        isEp,\
        histEp,\
        promote,\
        roque56,\
        roque63,\
        roque0,\
        roque7) in self.history:
            a=self.caseInt2Str(depart)
            b=self.caseInt2Str(arrivee)
            if(aff==True):
                tgitjigtjigjti = ("{}{}".format(a,b))
                juyjuyjuyjuy.append(tgitjigtjigjti)
                aff=False
            else:
                fyerverbgutnugns = ("{}{}".format(a,b))
                juyjuyjuyjuy.append(fyerverbgutnugns)
                aff=True
            cpt+=0.5
        trerrrrrrr = (juyjuyjuyjuy[len(juyjuyjuyjuy)-1])
        troutrou = (len(trerrrrrrr))
        print("Dernier coup joué :")
        Dernier_coup.play()
        time.sleep(1.5)
        zzzzzzzzzzzzzz = (trerrrrrrr)
        print(zzzzzzzzzzzzzz)
        ygyrefyafgrufr = []
        ygyrefyafgrufr.extend(zzzzzzzzzzzzzz)
        if ygyrefyafgrufr[0] == "a":
            na.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "b":
            nb.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "c":
            nc.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "d":
            nd.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "e":
            ne.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "f":
            nf.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "g":
            ng.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[0] == "h":
            nh.play()
            time.sleep(0.5)
        if ygyrefyafgrufr[1] == "1":
            n1.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "2":
            n2.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "3":
            n3.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "4":
            n4.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "5":
            n5.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "6":
            n6.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "7":
            n7.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[1] == "8":
            n8.play()
            time.sleep(0.5)
        an.play()
        time.sleep(0.8)
        if ygyrefyafgrufr[2] == "a":
            na.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "b":
            nb.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "c":
            nc.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "d":
            nd.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "e":
            ne.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "f":
            nf.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "g":
            ng.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[2] == "h":
            nh.play()
            time.sleep(0.5)
        if ygyrefyafgrufr[3] == "1":
            n1.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "2":
            n2.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "3":
            n3.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "4":
            n4.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "5":
            n5.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "6":
            n6.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "7":
            n7.play()
            time.sleep(0.5)
        elif ygyrefyafgrufr[3] == "8":
            n8.play()
            time.sleep(0.5)

    def azsqzsqaz(self):
        self.showHistory()

    def evaluer(self):
        WhiteScore=0
        BlackScore=0
        for pos1,piece in enumerate(self.cases):
            if(piece.couleur=='blanc'):
                WhiteScore+=piece.valeur
            else:
                BlackScore+=piece.valeur
        if(self.side2move=='blanc'):
            return WhiteScore-BlackScore
        else:
            return BlackScore-WhiteScore
class pendule:
    def __init__():
        global tempn
        global tempb
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        pygame.display.flip()
    def go():
        global tempn
        global tempb
        global poi
        global nbtyrueioap
        nbtyrueioap = 6
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        if poi == False:
            B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
            fenetre.blit(B, (132,377))
        elif poi == True:
            N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
            fenetre.blit(N, (158,377))
        PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        Information = pygame.image.load("images/pendule/3m.png").convert_alpha()
        fenetre.blit(Information, (133,313))
        pygame.display.flip()
        n3.play()
        time.sleep(1)
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        if poi == False:
            B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
            fenetre.blit(B, (132,377))
        elif poi == True:
            N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
            fenetre.blit(N, (158,377))
        PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        Information = pygame.image.load("images/pendule/2m.png").convert_alpha()
        fenetre.blit(Information, (133,313))
        pygame.display.flip()
        n2.play()
        time.sleep(1)
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        if poi == False:
            B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
            fenetre.blit(B, (132,377))
        elif poi == True:
            N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
            fenetre.blit(N, (158,377))
        PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        Information = pygame.image.load("images/pendule/1m.png").convert_alpha()
        fenetre.blit(Information, (133,313))
        pygame.display.flip()
        n1.play()
        time.sleep(1)
        gopl.play()
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        if poi == False:
            B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
            fenetre.blit(B, (132,377))
        elif poi == True:
            N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
            fenetre.blit(N, (158,377))
        PP = pygame.image.load("images/pendule/play.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        Information = pygame.image.load("images/pendule/go.png").convert_alpha()
        fenetre.blit(Information, (133,313))
        pygame.display.flip()
    def cadence():
        cade.play()
        global pen
        global tempn
        global tempb
        fenetre = Tk()
        h = ()
        m = ()
        s = ()
        h = StringVar()
        h.set(00)
        m = StringVar()
        m.set(00)
        s = StringVar()
        s.set(00)
        def raf():
            global tempn
            global tempb
            tempb = []
            tempn = []
            if h.get() == '0':
                h.set('0'+str(h.get()))
            elif h.get() == '1':
                h.set('0'+str(h.get()))
            elif h.get() == '2':
                h.set('0'+str(h.get()))
            elif h.get() == '3':
                h.set('0'+str(h.get()))
            elif h.get() == '4':
                h.set('0'+str(h.get()))
            elif h.get() == '5':
                h.set('0'+str(h.get()))
            elif h.get() == '6':
                h.set('0'+str(h.get()))
            elif h.get() == '7':
                h.set('0'+str(h.get()))
            elif h.get() == '8':
                h.set('0'+str(h.get()))
            elif h.get() == '9':
                h.set('0'+str(h.get()))
            elif h.get() == '':
                h.set('00')
            elif int(h.get()) > 12:
                h.set('12')
            elif int(h.get()) < 0:
                h.set('00')
            if m.get() == '0':
                m.set('0'+str(m.get()))
            elif m.get() == '1':
                m.set('0'+str(m.get()))
            elif m.get() == '2':
                m.set('0'+str(m.get()))
            elif m.get() == '3':
                m.set('0'+str(m.get()))
            elif m.get() == '4':
                m.set('0'+str(m.get()))
            elif m.get() == '5':
                m.set('0'+str(m.get()))
            elif m.get() == '6':
                m.set('0'+str(m.get()))
            elif m.get() == '7':
                m.set('0'+str(m.get()))
            elif m.get() == '8':
                m.set('0'+str(m.get()))
            elif m.get() == '9':
                m.set('0'+str(m.get()))
            elif m.get() == '':
                m.set('00')
            elif int(m.get()) > 59:
                m.set('59')
            elif int(m.get()) < 0:
                m.set('00')
            if s.get() == '0':
                s.set('0'+str(s.get()))
            elif s.get() == '1':
                s.set('0'+str(s.get()))
            elif s.get() == '2':
                s.set('0'+str(s.get()))
            elif s.get() == '3':
                s.set('0'+str(s.get()))
            elif s.get() == '4':
                s.set('0'+str(s.get()))
            elif s.get() == '5':
                s.set('0'+str(s.get()))
            elif s.get() == '6':
                s.set('0'+str(s.get()))
            elif s.get() == '7':
                s.set('0'+str(s.get()))
            elif s.get() == '8':
                s.set('0'+str(s.get()))
            elif s.get() == '9':
                s.set('0'+str(s.get()))
            elif s.get() == '':
                s.set('00')
            elif int(s.get()) > 59:
                s.set('59')
            elif int(s.get()) < 0:
                s.set('00')
            tempn.extend(h.get())
            tempn.extend(m.get())
            tempn.extend(s.get())
            tempb.extend(h.get())
            tempb.extend(m.get())
            tempb.extend(s.get())
            p.__init__()
        def val():
            global pen
            global tempn
            global tempb
            raf()
            if tempb[0] == '0' and tempb[1] == '0' and tempb[2] == '0' and tempb[3] == '0' and tempb[4] == '0' and tempb[5] == '0':
                pen = False
            fenetre.destroy()
        fenetre.title('Cadence')
        fenetre.geometry('100x150')
        label = Label(fenetre, text="Heure(s):",fg = "black")
        label.pack()
        heures = Spinbox(fenetre, textvariable=h, width=5,from_=0, to=12, command = raf)
        heures.pack()
        label = Label(fenetre, text="Minute(s):",fg = "black")
        label.pack()
        minutes = Spinbox(fenetre, textvariable=m, width=5,from_=0, to=59, command = raf)
        minutes.pack()
        label = Label(fenetre, text="Seconde(s):",fg = "black")
        label.pack()
        secondes = Spinbox(fenetre, textvariable=s, width=5,from_=0, to=59, command = raf)
        secondes.pack()
        bouton=Button(fenetre, text="Valider", command = val)
        bouton.pack(pady = 5)
        raf()
        fenetre.mainloop()
    def blanc_perdu():
        global yest
        b.hhdhhgg()
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        Information = pygame.image.load("images/pendule/blanc_perdu.png").convert_alpha()
        fenetre.blit(Information, (133,313))
        pygame.display.flip()
        bperdt.play()
        time.sleep(5)
        exit()
        yest = False
    def noir_perdu():
        global yest
        global calr
        b.hhdhhgg()
        calr = False
        Fond = pygame.image.load("images/pendule/pendule.png").convert()
        fenetre.blit(Fond, (0,296))
        PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
        fenetre.blit(PP, (142,374))
        posixb = 15
        bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixb,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixb+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixb+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixb+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixb+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixb+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixb+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixb+80,348))
        posixn = 190
        bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
        fenetre.blit(bn1, (posixn,348))
        bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
        fenetre.blit(bn2, (posixn+12,348))
        bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn3, (posixn+23,348))
        bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
        fenetre.blit(bn4, (posixn+34,348))
        bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
        fenetre.blit(bn5, (posixn+46,348))
        bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
        fenetre.blit(bn6, (posixn+57,348))
        bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
        fenetre.blit(bn7, (posixn+68,348))
        bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
        fenetre.blit(bn8, (posixn+80,348))
        Information = pygame.image.load("images/pendule/noir_perdu.png").convert_alpha()
        fenetre.blit(Information, (133,313))
        pygame.display.flip()
        nperdt.play()
        time.sleep(5)
        exit()
        yest = False
    def deconte_gol():
        global poi
        global nbtyrueioap
        global pen
        global cont
        global freefree
        global tempn
        global tempb
        global yest
        lmem = []
        cont = 0
        if pen == True:
            while cont == 0:
                Fond = pygame.image.load("images/pendule/pendule.png").convert()
                fenetre.blit(Fond, (0,296))
                if poi == False:
                    B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                    fenetre.blit(B, (132,377))
                elif poi == True:
                    N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                    fenetre.blit(N, (158,377))
                PP = pygame.image.load("images/pendule/play.png").convert_alpha()
                fenetre.blit(PP, (142,374))
                posixb = 15
                bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixb,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixb+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixb+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixb+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixb+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixb+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixb+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixb+80,348))
                posixn = 190
                bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixn,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixn+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixn+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixn+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixn+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixn+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixn+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixn+80,348))
                if nbtyrueioap > 0:
                    Information = pygame.image.load("images/pendule/go.png").convert_alpha()
                    fenetre.blit(Information, (133,313))
                    nbtyrueioap = nbtyrueioap-1
                pygame.display.flip()
                time.sleep(0.98)
                lmem = []
                if poi == True:
                    lmem.extend(tempn)
                    if lmem[0] == 0 and lmem[1] == 0 and lmem[2] == 0 and lmem[3] == 0 and lmem[4] == 0 and lmem[5] == 0:
                        print('Les noirs ont perdus au temps.')
                        p.noir_perdu()
                        cont = 1
                    else:
                        if int(lmem[5])-1 < 0:
                            if int(lmem[4])-1 < 0:
                                if int(lmem[3])-1 < 0:
                                    if int(lmem[2])-1 < 0:
                                        if int(lmem[1])-1 < 0:
                                            tempn = []
                                            tempn.append(int(lmem[0])-1)
                                            tempn.append(9)
                                            tempn.append(5)
                                            tempn.append(9)
                                            tempn.append(5)
                                            tempn.append(9)
                                        else:
                                            tempn = []
                                            tempn.append(int(lmem[0]))
                                            tempn.append(int(lmem[1])-1)
                                            tempn.append(5)
                                            tempn.append(9)
                                            tempn.append(5)
                                            tempn.append(9)
                                    else:
                                        tempn = []
                                        tempn.append(int(lmem[0]))
                                        tempn.append(int(lmem[1]))
                                        tempn.append(int(lmem[2])-1)
                                        tempn.append(9)
                                        tempn.append(5)
                                        tempn.append(9)
                                else:
                                    tempn = []
                                    tempn.append(int(lmem[0]))
                                    tempn.append(int(lmem[1]))
                                    tempn.append(int(lmem[2]))
                                    tempn.append(int(lmem[3])-1)
                                    tempn.append(5)
                                    tempn.append(9)
                            else:
                                tempn = []
                                tempn.append(int(lmem[0]))
                                tempn.append(int(lmem[1]))
                                tempn.append(int(lmem[2]))
                                tempn.append(int(lmem[3]))
                                tempn.append(int(lmem[4])-1)
                                tempn.append(9)
                        else:
                            tempn = []
                            tempn.append(int(lmem[0]))
                            tempn.append(int(lmem[1]))
                            tempn.append(int(lmem[2]))
                            tempn.append(int(lmem[3]))
                            tempn.append(int(lmem[4]))
                            tempn.append(int(lmem[5])-1)
                elif poi == False:
                    lmem.extend(tempb)
                    if lmem[0] == 0 and lmem[1] == 0 and lmem[2] == 0 and lmem[3] == 0 and lmem[4] == 0 and lmem[5] == 0:
                        print('Les blancs ont perdus au temps.')
                        p.blanc_perdu()
                        cont = 1
                    else:
                        if int(lmem[5])-1 < 0:
                            if int(lmem[4])-1 < 0:
                                if int(lmem[3])-1 < 0:
                                    if int(lmem[2])-1 < 0:
                                        if int(lmem[1])-1 < 0:
                                            tempb = []
                                            tempb.append(int(lmem[0])-1)
                                            tempb.append(9)
                                            tempb.append(5)
                                            tempb.append(9)
                                            tempb.append(5)
                                            tempb.append(9)
                                        else:
                                            tempb = []
                                            tempb.append(int(lmem[0]))
                                            tempb.append(int(lmem[1])-1)
                                            tempb.append(5)
                                            tempb.append(9)
                                            tempb.append(5)
                                            tempb.append(9)
                                    else:
                                        tempb = []
                                        tempb.append(int(lmem[0]))
                                        tempb.append(int(lmem[1]))
                                        tempb.append(int(lmem[2])-1)
                                        tempb.append(9)
                                        tempb.append(5)
                                        tempb.append(9)
                                else:
                                    tempb = []
                                    tempb.append(int(lmem[0]))
                                    tempb.append(int(lmem[1]))
                                    tempb.append(int(lmem[2]))
                                    tempb.append(int(lmem[3])-1)
                                    tempb.append(5)
                                    tempb.append(9)
                            else:
                                tempb = []
                                tempb.append(int(lmem[0]))
                                tempb.append(int(lmem[1]))
                                tempb.append(int(lmem[2]))
                                tempb.append(int(lmem[3]))
                                tempb.append(int(lmem[4])-1)
                                tempb.append(9)
                        else:
                            tempb = []
                            tempb.append(int(lmem[0]))
                            tempb.append(int(lmem[1]))
                            tempb.append(int(lmem[2]))
                            tempb.append(int(lmem[3]))
                            tempb.append(int(lmem[4]))
                            tempb.append(int(lmem[5])-1)
                if freefree == True:
                    Fond = pygame.image.load("images/pendule/pendule.png").convert()
                    fenetre.blit(Fond, (0,296))
                    if poi == False:
                        B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                        fenetre.blit(B, (132,377))
                    elif poi == True:
                        N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                        fenetre.blit(N, (158,377))
                    PP = pygame.image.load("images/pendule/play.png").convert_alpha()
                    fenetre.blit(PP, (142,374))
                    posixb = 15
                    bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                    fenetre.blit(bn1, (posixb,348))
                    bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                    fenetre.blit(bn2, (posixb+12,348))
                    bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn3, (posixb+23,348))
                    bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                    fenetre.blit(bn4, (posixb+34,348))
                    bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                    fenetre.blit(bn5, (posixb+46,348))
                    bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn6, (posixb+57,348))
                    bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                    fenetre.blit(bn7, (posixb+68,348))
                    bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                    fenetre.blit(bn8, (posixb+80,348))
                    posixn = 190
                    bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                    fenetre.blit(bn1, (posixn,348))
                    bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                    fenetre.blit(bn2, (posixn+12,348))
                    bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn3, (posixn+23,348))
                    bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                    fenetre.blit(bn4, (posixn+34,348))
                    bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                    fenetre.blit(bn5, (posixn+46,348))
                    bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn6, (posixn+57,348))
                    bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                    fenetre.blit(bn7, (posixn+68,348))
                    bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                    fenetre.blit(bn8, (posixn+80,348))
                    if nbtyrueioap > 0:
                        Information = pygame.image.load("images/pendule/go.png").convert_alpha()
                        fenetre.blit(Information, (133,313))
                    pygame.display.flip()
    def deconte_STOP():
        global cont
        cont = 1
        t2.join()
    def deconte_go():
        def rerey():
            lavariablequineserearien=5
        t1=Thread(target=rerey,args=())
        t2.start()
        t1.start()
        t1.join()

p=pendule
b=Board()
e=Engine()
t2=Thread(target=p.deconte_gol,args=())
freefree = True
poi = True
nbtyrueioap = 0
cont = 0
pen = True
tempb = [0, 0, 0, 0, 0, 0]
tempn = [0, 0, 0, 0, 0, 0]
def verticale_terminal(event):
    global c
    global coco
    global terua
    global zuziol
    global freefree
    if event.pos[1] < 37:
        c = c + '8'
        terua = terua + '8'
        coco = False
        time.sleep(0.5)
        n8.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 37 and event.pos[1] < 74:
        c = c + '7'
        terua = terua + '7'
        coco = False
        time.sleep(0.5)
        n7.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 74 and event.pos[1] < 111:
        c = c + '6'
        terua = terua + '6'
        coco = False
        time.sleep(0.5)
        n6.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 111 and event.pos[1] < 148:
        c = c + '5'
        terua = terua + '5'
        coco = False
        time.sleep(0.5)
        n5.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 148 and event.pos[1] < 185:
        c = c + '4'
        terua = terua + '4'
        coco = False
        time.sleep(0.5)
        n4.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 185 and event.pos[1] < 222:
        c = c + '3'
        terua = terua + '3'
        coco = False
        time.sleep(0.5)
        n3.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 222 and event.pos[1] < 259:
        c = c + '2'
        terua = terua + '2'
        coco = False
        time.sleep(0.5)
        n2.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)
    elif event.pos[1] > 259:
        c = c + '1'
        terua = terua + '1'
        coco = False
        time.sleep(0.5)
        n1.play()
        time.sleep(0.5)
        zuziol = False
        e.usermove(b,c,p)

def orisotale_terminal(event):
    global c
    global terua
    global zuziol
    global freefree
    if event.pos[0] < 37:
        p.deconte_STOP
        c = c + 'a'
        terua = terua + 'a'
        na.play()
        verticale_terminal(event)
    elif event.pos[0] > 37 and event.pos[0] < 74:
        p.deconte_STOP
        c = c + 'b'
        terua = terua + 'b'
        nb.play()
        verticale_terminal(event)
    elif event.pos[0] > 74 and event.pos[0] < 111:
        p.deconte_STOP
        c = c + 'c'
        terua = terua + 'c'
        nc.play()
        verticale_terminal(event)
    elif event.pos[0] > 111 and event.pos[0] < 148:
        p.deconte_STOP
        c = c + 'd'
        terua = terua + 'd'
        nd.play()
        verticale_terminal(event)
    elif event.pos[0] > 148 and event.pos[0] < 185:
        p.deconte_STOP
        c = c + 'e'
        terua = terua + 'e'
        ne.play()
        verticale_terminal(event)
    elif event.pos[0] > 185 and event.pos[0] < 222:
        p.deconte_STOP
        c = c + 'f'
        terua = terua + 'f'
        nf.play()
        verticale_terminal(event)
    elif event.pos[0] > 222 and event.pos[0] < 259:
        p.deconte_STOP
        c = c + 'g'
        terua = terua + 'g'
        ng.play()
        verticale_terminal(event)
    elif event.pos[0] > 259:
        p.deconte_STOP
        c = c + 'h'
        terua = terua + 'h'
        nh.play()
        verticale_terminal(event)

def verticale(event):
    global c
    global teru
    global zuziol
    global freefree
    if event.pos[1] < 37:
        c = c + '8'
        teru = teru + '8'
        time.sleep(0.5)
        n8.play()
    elif event.pos[1] > 37 and event.pos[1] < 74:
        c = c + '7'
        teru = teru + '7'
        time.sleep(0.5)
        n7.play()
    elif event.pos[1] > 74 and event.pos[1] < 111:
        c = c + '6'
        teru = teru + '6'
        time.sleep(0.5)
        n6.play()
    elif event.pos[1] > 111 and event.pos[1] < 148:
        c = c + '5'
        teru = teru + '5'
        time.sleep(0.5)
        n5.play()
    elif event.pos[1] > 148 and event.pos[1] < 185:
        c = c + '4'
        teru = teru + '4'
        time.sleep(0.5)
        n4.play()
    elif event.pos[1] > 185 and event.pos[1] < 222:
        c = c + '3'
        teru = teru + '3'
        time.sleep(0.5)
        n3.play()
    elif event.pos[1] > 222 and event.pos[1] < 259:
        c = c + '2'
        teru = teru + '2'
        time.sleep(0.5)
        n2.play()
    elif event.pos[1] > 259:
        c = c + '1'
        teru = teru + '1'
        time.sleep(0.5)
        n1.play()

def tete(event):
    global rara
    global continuerzz
    lll = pygame.image.load("images/échequier/echec_level.png").convert()
    fenetre.blit(lll, (0,0))
    pygame.display.flip()
    while rara:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if event.pos[0] < 37 and event.pos[1] < 37:
                    c = 'sd 2'
                    rara = False
                elif event.pos[0] > 37 and event.pos[0] < 74 and event.pos[1] < 37:
                    c = 'sd 3'
                    rara = False
                elif event.pos[0] > 74 and event.pos[0] < 111 and event.pos[1] < 37:
                    c = 'sd 4'
                    rara = False
                elif event.pos[0] > 111 and event.pos[0] < 148 and event.pos[1] < 37:
                    c = 'sd 5'
                    rara = False
                elif event.pos[0] > 148 and event.pos[0] < 185 and event.pos[1] < 37:
                    c = 'sd 6'
                    rara = False
                elif event.pos[0] > 185 and event.pos[0] < 222 and event.pos[1] < 37:
                    c = 'sd 7'
                    rara = False
                elif event.pos[0] > 222 and event.pos[0] < 259 and event.pos[1] < 37:
                    c = 'sd 8'
                    rara = False
                elif event.pos[0] > 259 and event.pos[1] < 37:
                    c = 'sd 9'
                    rara = False
                elif event.pos[0] < 37 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 10'
                    rara = False
                elif event.pos[0] > 37 and event.pos[0] < 74 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 11'
                    rara = False
                elif event.pos[0] > 75 and event.pos[0] < 111 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 12'
                    rara = False
                elif event.pos[0] > 111 and event.pos[0] < 148 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 13'
                    rara = False
                elif event.pos[0] > 148 and event.pos[0] < 185 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 14'
                    rara = False
                elif event.pos[0] > 185 and event.pos[0] < 222 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 15'
                    rara = False
                elif event.pos[0] > 222 and event.pos[0] < 259 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 16'
                    rara = False
                elif event.pos[0] > 259 and event.pos[1] < 74 and event.pos[1] > 37:
                    c = 'sd 17'
                    rara = False
                elif event.pos[0] < 37 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 18'
                    rara = False
                elif event.pos[0] > 37 and event.pos[0] < 74 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 19'
                    rara = False
                elif event.pos[0] > 74 and event.pos[0] < 111 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 20'
                    rara = False
                elif event.pos[0] > 111 and event.pos[0] < 148 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 21'
                    rara = False
                elif event.pos[0] > 148 and event.pos[0] < 185 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 22'
                    rara = False
                elif event.pos[0] > 185 and event.pos[0] < 222 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 23'
                    rara = False
                elif event.pos[0] > 222 and event.pos[0] < 259 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 24'
                    rara = False
                elif event.pos[0] > 259 and event.pos[1] < 111 and event.pos[1] > 74:
                    c = 'sd 25'
                    rara = False
                elif event.pos[0] < 37 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 26'
                    rara = False
                elif event.pos[0] > 37 and event.pos[0] < 74 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 27'
                    rara = False
                elif event.pos[0] > 74 and event.pos[0] < 111 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 28'
                    rara = False
                elif event.pos[0] > 111 and event.pos[0] < 148 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 29'
                    rara = False
                elif event.pos[0] > 150 and event.pos[0] < 185 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 30'
                    rara = False
                elif event.pos[0] > 185 and event.pos[0] < 222 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 31'
                    rara = False
                elif event.pos[0] > 222 and event.pos[0] < 259 and event.pos[1] < 148 and event.pos[1] > 111:
                    c = 'sd 32'
                    rara = False
                elif event.pos[0] > 259 and event.pos[1] < 148 and event.pos[1] > 111:
                    son.play()
                    print('############################################################')
                    print('##                                                        ##')
                    print('##     #####   ##    ##   ########    ######     ######   ##')
                    print('##   ###       ##    ##   ##         ##         ##        ##')
                    print('##  ##         ##    ##   ##         ##         ##        ##')
                    print('##  ##         ########   ########    ######     ######   ##')
                    print('##  ##         ##    ##   ##               ##         ##  ##')
                    print('##   ###       ##    ##   ##               ##         ##  ##')
                    print('##     #####   ##    ##   ########    ######     ######   ##')
                    print('##                                                        ##')
                    print('############################################################')
                    print('                  Copyright © 2018 MPi3D                    ')
                    print('                      Version : 3.5                         ')
    e.setDepth(c)

def rer() :
    global tempb
    global tempn
    nompartie.play()
    print('Nom de la partie :')
    dgftjjs = ""
    djue = 0
    while djue == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    djue = 1
                elif event.key == K_a:
                    sys.stdout.write("a")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "a"
                elif event.key == K_b:
                    sys.stdout.write("b")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "b"
                elif event.key == K_c:
                    sys.stdout.write("c")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "c"
                elif event.key == K_d:
                    sys.stdout.write("d")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "d"
                elif event.key == K_e:
                    sys.stdout.write("e")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "e"
                elif event.key == K_f:
                    sys.stdout.write("f")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "f"
                elif event.key == K_g:
                    sys.stdout.write("g")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "g"
                elif event.key == K_h:
                    sys.stdout.write("h")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "h"
                elif event.key == K_i:
                    sys.stdout.write("i")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "i"
                elif event.key == K_j:
                    sys.stdout.write("j")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "j"
                elif event.key == K_k:
                    sys.stdout.write("k")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "k"
                elif event.key == K_l:
                    sys.stdout.write("l")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "l"
                elif event.key == K_m:
                    sys.stdout.write("m")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "m"
                elif event.key == K_n:
                    sys.stdout.write("n")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "n"
                elif event.key == K_o:
                    sys.stdout.write("o")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "o"
                elif event.key == K_p:
                    sys.stdout.write("p")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "p"
                elif event.key == K_q:
                    sys.stdout.write("q")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "q"
                elif event.key == K_r:
                    sys.stdout.write("r")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "r"
                elif event.key == K_s:
                    sys.stdout.write("s")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "s"
                elif event.key == K_t:
                    sys.stdout.write("t")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "t"
                elif event.key == K_u:
                    sys.stdout.write("u")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "u"
                elif event.key == K_v:
                    sys.stdout.write("v")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "v"
                elif event.key == K_w:
                    sys.stdout.write("w")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "w"
                elif event.key == K_x:
                    sys.stdout.write("x")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "x"
                elif event.key == K_y:
                    sys.stdout.write("y")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "y"
                elif event.key == K_z:
                    sys.stdout.write("z")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "z"
                elif event.key == K_1:
                    sys.stdout.write("1")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "1"
                elif event.key == K_2:
                    sys.stdout.write("2")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "2"
                elif event.key == K_3:
                    sys.stdout.write("3")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "3"
                elif event.key == K_4:
                    sys.stdout.write("4")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "4"
                elif event.key == K_5:
                    sys.stdout.write("5")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "5"
                elif event.key == K_6:
                    sys.stdout.write("6")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "6"
                elif event.key == K_7:
                    sys.stdout.write("7")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "7"
                elif event.key == K_8:
                    sys.stdout.write("8")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "8"
                elif event.key == K_9:
                    sys.stdout.write("9")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "9"
                elif event.key == K_0:
                    sys.stdout.write("0")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "0"
                elif event.key == K_SPACE:
                    sys.stdout.write(" ")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + " "
    mon_fichier1 = open("Parties/" + dgftjjs + ".txt", "w")
    mon_fichier1.write(b.getboard())
    mon_fichier1.write('\n')
    mon_fichier1.write(" ".join(k))
    mon_fichier1.write('\n')
    mon_fichier1.write(str(tempb[0]) + " " + str(tempb[1]) + " " + str(tempb[2]) + " " + str(tempb[3]) + " " + str(tempb[4]) + " " + str(tempb[5]))
    mon_fichier1.write('\n')
    mon_fichier1.write(str(tempn[0]) + " " + str(tempn[1]) + " " + str(tempn[2]) + " " + str(tempn[3]) + " " + str(tempn[4]) + " " + str(tempn[5]))
    mon_fichier1.close()
    pygame.display.set_caption(dgftjjs)
    print('\nEnregistrement de la partie au nom de ' + dgftjjs)
    partieen_e.play()
    time.sleep(2)
    partie_e.play()
    print ('Partie enregistrée')
    time.sleep(1.7)

def ttex():
    global c
    global k
    global tempb
    global tempn
    nompartie.play()
    dgftjjs = ""
    djue = 0
    print('Nom de la partie :')
    while djue == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    djue = 1
                elif event.key == K_a:
                    sys.stdout.write("a")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "a"
                elif event.key == K_b:
                    sys.stdout.write("b")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "b"
                elif event.key == K_c:
                    sys.stdout.write("c")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "c"
                elif event.key == K_d:
                    sys.stdout.write("d")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "d"
                elif event.key == K_e:
                    sys.stdout.write("e")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "e"
                elif event.key == K_f:
                    sys.stdout.write("f")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "f"
                elif event.key == K_g:
                    sys.stdout.write("g")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "g"
                elif event.key == K_h:
                    sys.stdout.write("h")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "h"
                elif event.key == K_i:
                    sys.stdout.write("i")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "i"
                elif event.key == K_j:
                    sys.stdout.write("j")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "j"
                elif event.key == K_k:
                    sys.stdout.write("k")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "k"
                elif event.key == K_l:
                    sys.stdout.write("l")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "l"
                elif event.key == K_m:
                    sys.stdout.write("m")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "m"
                elif event.key == K_n:
                    sys.stdout.write("n")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "n"
                elif event.key == K_o:
                    sys.stdout.write("o")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "o"
                elif event.key == K_p:
                    sys.stdout.write("p")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "p"
                elif event.key == K_q:
                    sys.stdout.write("q")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "q"
                elif event.key == K_r:
                    sys.stdout.write("r")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "r"
                elif event.key == K_s:
                    sys.stdout.write("s")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "s"
                elif event.key == K_t:
                    sys.stdout.write("t")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "t"
                elif event.key == K_u:
                    sys.stdout.write("u")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "u"
                elif event.key == K_v:
                    sys.stdout.write("v")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "v"
                elif event.key == K_w:
                    sys.stdout.write("w")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "w"
                elif event.key == K_x:
                    sys.stdout.write("x")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "x"
                elif event.key == K_y:
                    sys.stdout.write("y")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "y"
                elif event.key == K_z:
                    sys.stdout.write("z")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "z"
                elif event.key == K_1:
                    sys.stdout.write("1")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "1"
                elif event.key == K_2:
                    sys.stdout.write("2")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "2"
                elif event.key == K_3:
                    sys.stdout.write("3")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "3"
                elif event.key == K_4:
                    sys.stdout.write("4")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "4"
                elif event.key == K_5:
                    sys.stdout.write("5")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "5"
                elif event.key == K_6:
                    sys.stdout.write("6")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "6"
                elif event.key == K_7:
                    sys.stdout.write("7")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "7"
                elif event.key == K_8:
                    sys.stdout.write("8")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "8"
                elif event.key == K_9:
                    sys.stdout.write("9")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "9"
                elif event.key == K_0:
                    sys.stdout.write("0")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + "0"
                elif event.key == K_SPACE:
                    sys.stdout.write(" ")
                    sys.stdout.flush()
                    dgftjjs = dgftjjs + " "
    pygame.display.set_caption(dgftjjs)
    mon_fichier = open("Parties/" + dgftjjs + ".txt", "r")
    contenu = ()
    print('')
    contenu = mon_fichier.read().split('\n')
    c = ('setboard ' + contenu[0])
    k = []
    k.extend(contenu[1].split(' '))
    tempb = []
    tempb.extend(contenu[2].split(' '))
    tempn = []
    tempn.extend(contenu[3].split(' '))
    mon_fichier.close()
    e.setboard(b,c)

def recherche():
    e.search(b,p)

zzzzzzzzzzzzzz = ()
quoit = ()
k = ['a1','b1','c1','d1','e1','f1','g1','h1','a2','b2','c2','d2','e2','f2','g2','h2','a7','b7','c7','d7','e7','f7','g7','h7','a8','b8','c8','d8','e8','f8','g8','h8']
print('')
print('Commandes :')
print('n pour une nouvelle partie.')
print('l pour savoir les coups autorisés.')
print('e pour enregistrer la partie.')
print('o pour ouvrir une partie enregistrée.')
print('c pour choisir le niveau.')
print("a pour changer le nombre de jouers.")
print("<─┘ pour faire jouer l'ordinateur.")
print('')
print("/!\ La promotion est refusée.")
print('')
blabla = []
p.__init__()
b.render()
p.cadence()
p.go()
c = ()
azertyuiopmlkjhgfdsqwxcvbngtrvt = True
coco = True
teru = ()
rara = ()
terua = ()
eezz = True
yest = False
zuziol = True
continuerzz = True
calr = True
while continuerzz == True:
    freefree = True
    teru = ()
    terua = ()
    if eezz == True :
        if poi == True:
            t2=Thread(target=p.deconte_gol,args=())
            e.search(b,p)
            b.render()
            yest = False
    zuziol = True
    freefree = True
    calr = True
    if yest == False:
        t2=Thread(target=p.deconte_gol,args=())
        p.deconte_go()
        yest = True
    for event in pygame.event.get():
        c = str(c)
        teru = str(teru)
        terua = str(terua)
        terua = ''
        teru = ''
        c = ''
        coco = True
        rara = True
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                recherche()
                b.render()
            elif event.key == K_a:
                if eezz == True:
                    p.deconte_STOP()
                    freefree = False
                    Fond = pygame.image.load("images/pendule/pendule.png").convert()
                    fenetre.blit(Fond, (0,296))
                    PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
                    fenetre.blit(PP, (142,374))
                    if poi == False:
                        B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                        fenetre.blit(B, (132,377))
                    elif poi == True:
                        N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                        fenetre.blit(N, (158,377))
                    posixb = 15
                    bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                    fenetre.blit(bn1, (posixb,348))
                    bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                    fenetre.blit(bn2, (posixb+12,348))
                    bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn3, (posixb+23,348))
                    bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                    fenetre.blit(bn4, (posixb+34,348))
                    bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                    fenetre.blit(bn5, (posixb+46,348))
                    bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn6, (posixb+57,348))
                    bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                    fenetre.blit(bn7, (posixb+68,348))
                    bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                    fenetre.blit(bn8, (posixb+80,348))
                    posixn = 190
                    bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                    fenetre.blit(bn1, (posixn,348))
                    bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                    fenetre.blit(bn2, (posixn+12,348))
                    bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn3, (posixn+23,348))
                    bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                    fenetre.blit(bn4, (posixn+34,348))
                    bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                    fenetre.blit(bn5, (posixn+46,348))
                    bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn6, (posixn+57,348))
                    bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                    fenetre.blit(bn7, (posixn+68,348))
                    bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                    fenetre.blit(bn8, (posixn+80,348))
                    pygame.display.flip()
                    yest = False
                    eezz = False
                    print('Mode 2 joueurs.')
                    joueur2.play()
                    time.sleep(2)
                    azertyuiopmlkjhgfdsqwxcvbngtrvt = False
                else:
                    p.deconte_STOP()
                    freefree = False
                    Fond = pygame.image.load("images/pendule/pendule.png").convert()
                    fenetre.blit(Fond, (0,296))
                    PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
                    fenetre.blit(PP, (142,374))
                    if poi == False:
                        B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                        fenetre.blit(B, (132,377))
                    elif poi == True:
                        N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                        fenetre.blit(N, (158,377))
                    posixb = 15
                    bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                    fenetre.blit(bn1, (posixb,348))
                    bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                    fenetre.blit(bn2, (posixb+12,348))
                    bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn3, (posixb+23,348))
                    bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                    fenetre.blit(bn4, (posixb+34,348))
                    bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                    fenetre.blit(bn5, (posixb+46,348))
                    bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn6, (posixb+57,348))
                    bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                    fenetre.blit(bn7, (posixb+68,348))
                    bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                    fenetre.blit(bn8, (posixb+80,348))
                    posixn = 190
                    bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                    fenetre.blit(bn1, (posixn,348))
                    bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                    fenetre.blit(bn2, (posixn+12,348))
                    bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn3, (posixn+23,348))
                    bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                    fenetre.blit(bn4, (posixn+34,348))
                    bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                    fenetre.blit(bn5, (posixn+46,348))
                    bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                    fenetre.blit(bn6, (posixn+57,348))
                    bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                    fenetre.blit(bn7, (posixn+68,348))
                    bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                    fenetre.blit(bn8, (posixn+80,348))
                    pygame.display.flip()
                    eezz = True
                    yest = False
                    print("Mode 1 joueur (contre l'ordinateur).")
                    joueur1.play()
                    time.sleep(1.5)
                    azertyuiopmlkjhgfdsqwxcvbngtrvt = True
                b.render()
            elif event.key == K_n:
                p.deconte_STOP()
                freefree = False
                tempb = [0,0,0,0,0,0]
                tempn = [0,0,0,0,0,0]
                Fond = pygame.image.load("images/pendule/pendule.png").convert()
                fenetre.blit(Fond, (0,296))
                PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
                fenetre.blit(PP, (142,374))
                if poi == False:
                    B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                    fenetre.blit(B, (132,377))
                elif poi == True:
                    N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                    fenetre.blit(N, (158,377))
                posixb = 15
                bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixb,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixb+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixb+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixb+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixb+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixb+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixb+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixb+80,348))
                posixn = 190
                bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixn,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixn+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixn+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixn+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixn+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixn+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixn+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixn+80,348))
                pygame.display.flip()
                yest = False
                k = ['a1','b1','c1','d1','e1','f1','g1','h1','a2','b2','c2','d2','e2','f2','g2','h2','a7','b7','c7','d7','e7','f7','g7','h7','a8','b8','c8','d8','e8','f8','g8','h8']
                e.newgame(b)
                b.render()
                pygame.display.set_caption(titre_fenetre)
                p.__init__()
                p.cadence()
                p.go()
            elif event.key == K_l:
                e.legalmoves(b)
                b.render()
            elif event.key == K_c:
                p.deconte_STOP()
                freefree = False
                Fond = pygame.image.load("images/pendule/pendule.png").convert()
                fenetre.blit(Fond, (0,296))
                PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
                fenetre.blit(PP, (142,374))
                if poi == False:
                    B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                    fenetre.blit(B, (132,377))
                elif poi == True:
                    N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                    fenetre.blit(N, (158,377))
                posixb = 15
                bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixb,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixb+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixb+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixb+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixb+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixb+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixb+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixb+80,348))
                posixn = 190
                bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixn,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixn+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixn+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixn+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixn+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixn+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixn+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixn+80,348))
                pygame.display.flip()
                yest = False
                rara = True
                tete(event)
                b.render()
            elif event.key == K_e:
                p.deconte_STOP()
                freefree = False
                Fond = pygame.image.load("images/pendule/pendule.png").convert()
                fenetre.blit(Fond, (0,296))
                PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
                fenetre.blit(PP, (142,374))
                if poi == False:
                    B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                    fenetre.blit(B, (132,377))
                elif poi == True:
                    N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                    fenetre.blit(N, (158,377))
                posixb = 15
                bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixb,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixb+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixb+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixb+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixb+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixb+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixb+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixb+80,348))
                posixn = 190
                bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixn,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixn+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixn+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixn+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixn+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixn+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixn+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixn+80,348))
                pygame.display.flip()
                yest = False
                rer()
            elif event.key == K_o:
                p.deconte_STOP()
                freefree = False
                Fond = pygame.image.load("images/pendule/pendule.png").convert()
                fenetre.blit(Fond, (0,296))
                PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
                fenetre.blit(PP, (142,374))
                if poi == False:
                    B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                    fenetre.blit(B, (132,377))
                elif poi == True:
                    N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                    fenetre.blit(N, (158,377))
                posixb = 15
                bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixb,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixb+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixb+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixb+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixb+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixb+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixb+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixb+80,348))
                posixn = 190
                bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
                fenetre.blit(bn1, (posixn,348))
                bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
                fenetre.blit(bn2, (posixn+12,348))
                bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn3, (posixn+23,348))
                bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
                fenetre.blit(bn4, (posixn+34,348))
                bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
                fenetre.blit(bn5, (posixn+46,348))
                bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
                fenetre.blit(bn6, (posixn+57,348))
                bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
                fenetre.blit(bn7, (posixn+68,348))
                bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
                fenetre.blit(bn8, (posixn+80,348))
                pygame.display.flip()
                yest = False
                ttex()
                b.render()
        if event.type == QUIT:
            p.deconte_STOP()
            freefree = False
            Fond = pygame.image.load("images/pendule/pendule.png").convert()
            fenetre.blit(Fond, (0,296))
            PP = pygame.image.load("images/pendule/pause.png").convert_alpha()
            fenetre.blit(PP, (142,374))
            if poi == False:
                B = pygame.image.load("images/pendule/blancs.png").convert_alpha()
                fenetre.blit(B, (132,377))
            elif poi == True:
                N = pygame.image.load("images/pendule/noirs.png").convert_alpha()
                fenetre.blit(N, (158,377))
            posixb = 15
            bn1 = pygame.image.load("images/pendule/"+str(tempb[0])+".png").convert_alpha()
            fenetre.blit(bn1, (posixb,348))
            bn2 = pygame.image.load("images/pendule/"+str(tempb[1])+".png").convert_alpha()
            fenetre.blit(bn2, (posixb+12,348))
            bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
            fenetre.blit(bn3, (posixb+23,348))
            bn4 = pygame.image.load("images/pendule/"+str(tempb[2])+".png").convert_alpha()
            fenetre.blit(bn4, (posixb+34,348))
            bn5 = pygame.image.load("images/pendule/"+str(tempb[3])+".png").convert_alpha()
            fenetre.blit(bn5, (posixb+46,348))
            bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
            fenetre.blit(bn6, (posixb+57,348))
            bn7 = pygame.image.load("images/pendule/"+str(tempb[4])+".png").convert_alpha()
            fenetre.blit(bn7, (posixb+68,348))
            bn8 = pygame.image.load("images/pendule/"+str(tempb[5])+".png").convert_alpha()
            fenetre.blit(bn8, (posixb+80,348))
            posixn = 190
            bn1 = pygame.image.load("images/pendule/"+str(tempn[0])+".png").convert_alpha()
            fenetre.blit(bn1, (posixn,348))
            bn2 = pygame.image.load("images/pendule/"+str(tempn[1])+".png").convert_alpha()
            fenetre.blit(bn2, (posixn+12,348))
            bn3 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
            fenetre.blit(bn3, (posixn+23,348))
            bn4 = pygame.image.load("images/pendule/"+str(tempn[2])+".png").convert_alpha()
            fenetre.blit(bn4, (posixn+34,348))
            bn5 = pygame.image.load("images/pendule/"+str(tempn[3])+".png").convert_alpha()
            fenetre.blit(bn5, (posixn+46,348))
            bn6 = pygame.image.load("images/pendule/deux_o.png").convert_alpha()
            fenetre.blit(bn6, (posixn+57,348))
            bn7 = pygame.image.load("images/pendule/"+str(tempn[4])+".png").convert_alpha()
            fenetre.blit(bn7, (posixn+68,348))
            bn8 = pygame.image.load("images/pendule/"+str(tempn[5])+".png").convert_alpha()
            fenetre.blit(bn8, (posixn+80,348))
            pygame.display.flip()
            yest = False
            erreur.play()
            time.sleep(0.6)
            v_en.play()
            Mafenetre = Tk()
            Mafenetre.title('Enregistrement ?')
            Mafenetre.geometry('300x100+400+400')
            Texte = StringVar()
            Texte.set('Voulez vous enregistrer ?')
            LabelResultat = Label(Mafenetre, textvariable = Texte, fg ='black')
            LabelResultat.pack(side = LEFT, padx = 5, pady = 5)
            BoutonLancer = Button(Mafenetre, text ='Oui', command = rer)
            BoutonLancer.pack(side = LEFT, padx = 5, pady = 5)
            BoutonQuitter = Button(Mafenetre, text ='Non', command = Mafenetre.destroy)
            BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)
            Mafenetre.mainloop()
            continuerzz = False
            yest = True
            zuziol = False
            exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] < 37:
                c = c + 'a'
                teru = teru + 'a'
                na.play()
                verticale(event)
            elif event.pos[0] > 37 and event.pos[0] < 74:
                c = c + 'b'
                teru = teru + 'b'
                nb.play()
                verticale(event)
            elif event.pos[0] > 74 and event.pos[0] < 111:
                c = c + 'c'
                teru = teru + 'c'
                nc.play()
                verticale(event)
            elif event.pos[0] > 111 and event.pos[0] < 148:
                c = c + 'd'
                teru = teru + 'd'
                nd.play()
                verticale(event)
            elif event.pos[0] > 148 and event.pos[0] < 185:
                c = c + 'e'
                teru = teru + 'e'
                ne.play()
                verticale(event)
            elif event.pos[0] > 185 and event.pos[0] < 222:
                c = c + 'f'
                teru = teru + 'f'
                nf.play()
                verticale(event)
            elif event.pos[0] > 222 and event.pos[0] < 259:
                c = c + 'g'
                teru = teru + 'g'
                ng.play()
                verticale(event)
            elif event.pos[0] > 259:
                c = c + 'h'
                teru = teru + 'h'
                nh.play()
                verticale(event)
            mList=b.gen_moves_list()
            cpt=1
            coupsdebut = []
            coupsfin = []
            coupstous = []
            for m in mList:
                if(not b.domove(m[0],m[1],m[2])):
                    continue
                coupstous.append(b.caseInt2Str(m[0])+b.caseInt2Str(m[1])+m[2])
                coupsdebut.append(b.caseInt2Str(m[0]))
                coupsfin.append(b.caseInt2Str(m[1])+m[2])
                b.undomove()
                cpt+=1
            nombredel = 0
            while nombredel < len(coupsdebut) :
                if c == coupsdebut[nombredel]:
                    nhbgavfc = []
                    nhbgavfc.extend(coupsfin[nombredel])
                    fer = []
                    if nhbgavfc[0] == 'a':
                        fer.append(0)
                    elif nhbgavfc[0] == 'b':
                        fer.append(37)
                    elif nhbgavfc[0] == 'c':
                        fer.append(74)
                    elif nhbgavfc[0] == 'd':
                        fer.append(111)
                    elif nhbgavfc[0] == 'e':
                        fer.append(148)
                    elif nhbgavfc[0] == 'f':
                        fer.append(185)
                    elif nhbgavfc[0] == 'g':
                        fer.append(222)
                    elif nhbgavfc[0] == 'h':
                        fer.append(259)
                    if nhbgavfc[1] == '1':
                        fer.append(259)
                    elif nhbgavfc[1] == '2':
                        fer.append(222)
                    elif nhbgavfc[1] == '3':
                        fer.append(185)
                    elif nhbgavfc[1] == '4':
                        fer.append(148)
                    elif nhbgavfc[1] == '5':
                        fer.append(111)
                    elif nhbgavfc[1] == '6':
                        fer.append(74)
                    elif nhbgavfc[1] == '7':
                        fer.append(37)
                    elif nhbgavfc[1] == '8':
                        fer.append(0)
                    qaqa = pygame.image.load("images/échequier/case_proposé.png").convert_alpha()
                    fenetre.blit(qaqa, (fer))
                    pygame.display.flip()
                    time.sleep(0.01)
                nombredel = nombredel + 1
            while coco:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        orisotale_terminal(event)
                    if event.type == MOUSEBUTTONDOWN and event.button == 3:
                        case1 = pygame.image.load("images/échequier/" + blabla[0] + "_1.jpg").convert()
                        fenetre.blit(case1, (0,0))
                        case2 = pygame.image.load("images/échequier/" + blabla[1] + "_0.jpg").convert()
                        fenetre.blit(case2, (37,0))
                        case3 = pygame.image.load("images/échequier/" + blabla[2] + "_1.jpg").convert()
                        fenetre.blit(case3, (74,0))
                        case4 = pygame.image.load("images/échequier/" + blabla[3] + "_0.jpg").convert()
                        fenetre.blit(case4, (111,0))
                        case5 = pygame.image.load("images/échequier/" + blabla[4] + "_1.jpg").convert()
                        fenetre.blit(case5, (148,0))
                        case6 = pygame.image.load("images/échequier/" + blabla[5] + "_0.jpg").convert()
                        fenetre.blit(case6, (185,0))
                        case7 = pygame.image.load("images/échequier/" + blabla[6] + "_1.jpg").convert()
                        fenetre.blit(case7, (222,0))
                        case8 = pygame.image.load("images/échequier/" + blabla[7] + "_0.jpg").convert()
                        fenetre.blit(case8, (259,0))
                        case9 = pygame.image.load("images/échequier/" + blabla[8] + "_0.jpg").convert()
                        fenetre.blit(case9, (0,37))
                        case10 = pygame.image.load("images/échequier/" + blabla[9] + "_1.jpg").convert()
                        fenetre.blit(case10, (37,37))
                        case11 = pygame.image.load("images/échequier/" + blabla[10] + "_0.jpg").convert()
                        fenetre.blit(case11, (74,37))
                        case12 = pygame.image.load("images/échequier/" + blabla[11] + "_1.jpg").convert()
                        fenetre.blit(case12, (111,37))
                        case13 = pygame.image.load("images/échequier/" + blabla[12] + "_0.jpg").convert()
                        fenetre.blit(case13, (148,37))
                        case14 = pygame.image.load("images/échequier/" + blabla[13] + "_1.jpg").convert()
                        fenetre.blit(case14, (185,37))
                        case15 = pygame.image.load("images/échequier/" + blabla[14] + "_0.jpg").convert()
                        fenetre.blit(case15, (222,37))
                        case16 = pygame.image.load("images/échequier/" + blabla[15] + "_1.jpg").convert()
                        fenetre.blit(case16, (259,37))
                        case17 = pygame.image.load("images/échequier/" + blabla[16] + "_1.jpg").convert()
                        fenetre.blit(case17, (0,74))
                        case18 = pygame.image.load("images/échequier/" + blabla[17] + "_0.jpg").convert()
                        fenetre.blit(case18, (37,74))
                        case19 = pygame.image.load("images/échequier/" + blabla[18] + "_1.jpg").convert()
                        fenetre.blit(case19, (74,74))
                        case20 = pygame.image.load("images/échequier/" + blabla[19] + "_0.jpg").convert()
                        fenetre.blit(case20, (111,74))
                        case21 = pygame.image.load("images/échequier/" + blabla[20] + "_1.jpg").convert()
                        fenetre.blit(case21, (148,74))
                        case22 = pygame.image.load("images/échequier/" + blabla[21] + "_0.jpg").convert()
                        fenetre.blit(case22, (185,74))
                        case23 = pygame.image.load("images/échequier/" + blabla[22] + "_1.jpg").convert()
                        fenetre.blit(case23, (222,74))
                        case24 = pygame.image.load("images/échequier/" + blabla[23] + "_0.jpg").convert()
                        fenetre.blit(case24, (259,74))
                        case25 = pygame.image.load("images/échequier/" + blabla[24] + "_0.jpg").convert()
                        fenetre.blit(case25, (0,111))
                        case26 = pygame.image.load("images/échequier/" + blabla[25] + "_1.jpg").convert()
                        fenetre.blit(case26, (37,111))
                        case27 = pygame.image.load("images/échequier/" + blabla[26] + "_0.jpg").convert()
                        fenetre.blit(case27, (74,111))
                        case28 = pygame.image.load("images/échequier/" + blabla[27] + "_1.jpg").convert()
                        fenetre.blit(case28, (111,111))
                        case29 = pygame.image.load("images/échequier/" + blabla[28] + "_0.jpg").convert()
                        fenetre.blit(case29, (148,111))
                        case30 = pygame.image.load("images/échequier/" + blabla[29] + "_1.jpg").convert()
                        fenetre.blit(case30, (185,111))
                        case31 = pygame.image.load("images/échequier/" + blabla[30] + "_0.jpg").convert()
                        fenetre.blit(case31, (222,111))
                        case32 = pygame.image.load("images/échequier/" + blabla[31] + "_1.jpg").convert()
                        fenetre.blit(case32, (259,111))
                        case33 = pygame.image.load("images/échequier/" + blabla[32] + "_1.jpg").convert()
                        fenetre.blit(case33, (0,148))
                        case34 = pygame.image.load("images/échequier/" + blabla[33] + "_0.jpg").convert()
                        fenetre.blit(case34, (37,148))
                        case35 = pygame.image.load("images/échequier/" + blabla[34] + "_1.jpg").convert()
                        fenetre.blit(case35, (74,148))
                        case36 = pygame.image.load("images/échequier/" + blabla[35] + "_0.jpg").convert()
                        fenetre.blit(case36, (111,148))
                        case37 = pygame.image.load("images/échequier/" + blabla[36] + "_1.jpg").convert()
                        fenetre.blit(case37, (148,148))
                        case38 = pygame.image.load("images/échequier/" + blabla[37] + "_0.jpg").convert()
                        fenetre.blit(case38, (185,148))
                        case39 = pygame.image.load("images/échequier/" + blabla[38] + "_1.jpg").convert()
                        fenetre.blit(case39, (222,148))
                        case40 = pygame.image.load("images/échequier/" + blabla[39] + "_0.jpg").convert()
                        fenetre.blit(case40, (259,148))
                        case41 = pygame.image.load("images/échequier/" + blabla[40] + "_0.jpg").convert()
                        fenetre.blit(case41, (0,185))
                        case42 = pygame.image.load("images/échequier/" + blabla[41] + "_1.jpg").convert()
                        fenetre.blit(case42, (37,185))
                        case43 = pygame.image.load("images/échequier/" + blabla[42] + "_0.jpg").convert()
                        fenetre.blit(case43, (74,185))
                        case44 = pygame.image.load("images/échequier/" + blabla[43] + "_1.jpg").convert()
                        fenetre.blit(case44, (111,185))
                        case45 = pygame.image.load("images/échequier/" + blabla[44] + "_0.jpg").convert()
                        fenetre.blit(case45, (148,185))
                        case46 = pygame.image.load("images/échequier/" + blabla[45] + "_1.jpg").convert()
                        fenetre.blit(case46, (185,185))
                        case47 = pygame.image.load("images/échequier/" + blabla[46] + "_0.jpg").convert()
                        fenetre.blit(case47, (222,185))
                        case48 = pygame.image.load("images/échequier/" + blabla[47] + "_1.jpg").convert()
                        fenetre.blit(case48, (259,185))
                        case49 = pygame.image.load("images/échequier/" + blabla[48] + "_1.jpg").convert()
                        fenetre.blit(case49, (0,222))
                        case50 = pygame.image.load("images/échequier/" + blabla[49] + "_0.jpg").convert()
                        fenetre.blit(case50, (37,222))
                        case51 = pygame.image.load("images/échequier/" + blabla[50] + "_1.jpg").convert()
                        fenetre.blit(case51, (74,222))
                        case52 = pygame.image.load("images/échequier/" + blabla[51] + "_0.jpg").convert()
                        fenetre.blit(case52, (111,222))
                        case53 = pygame.image.load("images/échequier/" + blabla[52] + "_1.jpg").convert()
                        fenetre.blit(case53, (148,222))
                        case54 = pygame.image.load("images/échequier/" + blabla[53] + "_0.jpg").convert()
                        fenetre.blit(case54, (185,222))
                        case55 = pygame.image.load("images/échequier/" + blabla[54] + "_1.jpg").convert()
                        fenetre.blit(case55, (222,222))
                        case56 = pygame.image.load("images/échequier/" + blabla[55] + "_0.jpg").convert()
                        fenetre.blit(case56, (259,222))
                        case57 = pygame.image.load("images/échequier/" + blabla[56] + "_0.jpg").convert()
                        fenetre.blit(case57, (0,259))
                        case58 = pygame.image.load("images/échequier/" + blabla[57] + "_1.jpg").convert()
                        fenetre.blit(case58, (37,259))
                        case59 = pygame.image.load("images/échequier/" + blabla[58] + "_0.jpg").convert()
                        fenetre.blit(case59, (74,259))
                        case60 = pygame.image.load("images/échequier/" + blabla[59] + "_1.jpg").convert()
                        fenetre.blit(case60, (111,259))
                        case61 = pygame.image.load("images/échequier/" + blabla[60] + "_0.jpg").convert()
                        fenetre.blit(case61, (148,259))
                        case62 = pygame.image.load("images/échequier/" + blabla[61] + "_1.jpg").convert()
                        fenetre.blit(case62, (185,259))
                        case63 = pygame.image.load("images/échequier/" + blabla[62] + "_0.jpg").convert()
                        fenetre.blit(case63, (222,259))
                        case64 = pygame.image.load("images/échequier/" + blabla[63] + "_1.jpg").convert()
                        fenetre.blit(case64, (259,259))
                        pygame.display.flip()
                        coco = False
