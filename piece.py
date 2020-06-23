class Piece:
    
    VIDE='.'
    nomPiece=(VIDE,'ROI','DAME','TOUR','CAVALIER','FOU','PION')
    valeurPiece=(0,0,9,5,3,3,1)
    tab120 = (
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
	-1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
	-1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
	-1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
	-1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
	-1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
	-1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
	-1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1
	)
    tab64 = (
	21, 22, 23, 24, 25, 26, 27, 28,
	31, 32, 33, 34, 35, 36, 37, 38,
	41, 42, 43, 44, 45, 46, 47, 48,
	51, 52, 53, 54, 55, 56, 57, 58,
	61, 62, 63, 64, 65, 66, 67, 68,
	71, 72, 73, 74, 75, 76, 77, 78,
	81, 82, 83, 84, 85, 86, 87, 88,
	91, 92, 93, 94, 95, 96, 97, 98
	)
    deplacements_tour=(-10,10,-1,1)
    deplacements_fou=(-11,-9,11,9)
    deplacements_cavalier=(-12,-21,-19,-8,12,21,19,8)
    
    def __init__(self,nom=VIDE,couleur=''):
        self.nom=nom
        self.couleur=couleur        
        self.valeur=self.valeurPiece[self.nomPiece.index(nom)]
        
    def isEmpty(self):
        return (self.nom==self.VIDE)
    
    def pos2_roi(self,pos1,cAd,echiquier,dontCallIsAttacked=False):
        liste=[]
        for i in (self.deplacements_tour+self.deplacements_fou):
            n=self.tab120[self.tab64[pos1]+i]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                    liste.append((pos1,n,''))
        if(dontCallIsAttacked):
            return liste
        c=echiquier.oppColor(cAd)
        if(c=='blanc'):
            if(echiquier.white_can_castle_63):
                if(echiquier.cases[63].nom=='TOUR' and \
                echiquier.cases[63].couleur=='blanc' and \
                echiquier.cases[61].isEmpty() and \
                echiquier.cases[62].isEmpty() and \
                echiquier.is_attacked(61,'noir')==False and \
                echiquier.is_attacked(62,'noir')==False and \
                echiquier.is_attacked(pos1,'noir')==False):
                    liste.append((pos1,62,''))
            if(echiquier.white_can_castle_56):
                if(echiquier.cases[56].nom=='TOUR' and \
                echiquier.cases[56].couleur=='blanc' and \
                echiquier.cases[57].isEmpty() and \
                echiquier.cases[58].isEmpty() and \
                echiquier.cases[59].isEmpty() and \
                echiquier.is_attacked(58,cAd)==False and \
                echiquier.is_attacked(59,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,58,''))
        elif(c=='noir'):
            if(echiquier.black_can_castle_7):
                if(echiquier.cases[7].nom=='TOUR' and \
                echiquier.cases[7].couleur=='noir' and \
                echiquier.cases[5].isEmpty() and \
                echiquier.cases[6].isEmpty() and \
                echiquier.is_attacked(5,cAd)==False and \
                echiquier.is_attacked(6,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,6,''))
            if(echiquier.black_can_castle_0):
                if(echiquier.cases[0].nom=='TOUR' and \
                echiquier.cases[0].couleur=='noir' and \
                echiquier.cases[1].isEmpty() and \
                echiquier.cases[2].isEmpty() and \
                echiquier.cases[3].isEmpty() and \
                echiquier.is_attacked(2,cAd)==False and \
                echiquier.is_attacked(3,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,2,''))
        return liste
    
    def pos2_tour(self,pos1,cAd,echiquier):
        liste=[]
        for k in self.deplacements_tour:        
            j=1
            while(True):
                n=self.tab120[self.tab64[pos1] + (k * j)]
                if(n!=-1):
                    if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                        liste.append((pos1,n,''))
                else:
                    break
                if(not echiquier.cases[n].isEmpty()):
                    break
                j=j+1
        return liste
    
    def pos2_cavalier(self,pos1,cAd,echiquier):
        liste=[]
        for i in self.deplacements_cavalier:
            n=self.tab120[self.tab64[pos1]+i]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                    liste.append((pos1,n,''))
        return liste
    
    def pos2_fou(self,pos1,cAd,echiquier):
        liste=[]
        for k in self.deplacements_fou:
            j=1
            while(True):
                n=self.tab120[self.tab64[pos1] + (k * j)]
                if(n!=-1):
                    if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                        liste.append((pos1,n,''))
                else:
                    break
                if(not echiquier.cases[n].isEmpty()):
                    break
                j=j+1
        return liste
    
    def pos2_pion(self,pos1,couleur,echiquier):
        liste=[]
        if(couleur=='blanc'):
            n=self.tab120[self.tab64[pos1]-10]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty()):
                    if(n<8):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
            if(echiquier.ROW(pos1)==6):
                if(echiquier.cases[pos1-8].isEmpty() and echiquier.cases[pos1-16].isEmpty()):
                    liste.append((pos1,pos1-16,''))
            n=self.tab120[self.tab64[pos1]-11]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='noir' or echiquier.ep==n):
                    if(n<8):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
            n=self.tab120[self.tab64[pos1]-9]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='noir' or echiquier.ep==n):
                    if(n<8):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
        else:
            n=self.tab120[self.tab64[pos1]+10]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty()):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
            if(echiquier.ROW(pos1)==1):
                if(echiquier.cases[pos1+8].isEmpty() and echiquier.cases[pos1+16].isEmpty()):
                    liste.append((pos1,pos1+16,''))
            n=self.tab120[self.tab64[pos1]+9]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='blanc' or echiquier.ep==n):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
            n=self.tab120[self.tab64[pos1]+11]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='blanc' or echiquier.ep==n):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
        return liste
