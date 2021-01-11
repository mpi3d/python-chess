from piece import *
import time
import pygame
from pygame.locals import *
pygame.init()
gagné = pygame.mixer.Sound("sons/bruits/gagné.wav")
erreur = pygame.mixer.Sound("sons/bruits/erreur.wav")
Coupincorect = pygame.mixer.Sound("sons/voix/mots/coup_incorect.wav")
Rechèreche = pygame.mixer.Sound("sons/voix/mots/rechèreche.wav")
Mats = pygame.mixer.Sound("sons/voix/mots/mats_pour.wav")
Noir = pygame.mixer.Sound("sons/voix/mots/noir.wav")
Blanc = pygame.mixer.Sound("sons/voix/mots/blanc.wav")
Pat = pygame.mixer.Sound("sons/voix/mots/pat.wav")
Niv = pygame.mixer.Sound("sons/voix/mots/niveau.wav")
n1 = pygame.mixer.Sound("sons/voix/nombres/1.wav")
n2 = pygame.mixer.Sound("sons/voix/nombres/2.wav")
n3 = pygame.mixer.Sound("sons/voix/nombres/3.wav")
n4 = pygame.mixer.Sound("sons/voix/nombres/4.wav")
n5 = pygame.mixer.Sound("sons/voix/nombres/5.wav")
n6 = pygame.mixer.Sound("sons/voix/nombres/6.wav")
n7 = pygame.mixer.Sound("sons/voix/nombres/7.wav")
n8 = pygame.mixer.Sound("sons/voix/nombres/8.wav")
n9 = pygame.mixer.Sound("sons/voix/nombres/9.wav")
n10 = pygame.mixer.Sound("sons/voix/nombres/10.wav")
n11 = pygame.mixer.Sound("sons/voix/nombres/11.wav")
n12 = pygame.mixer.Sound("sons/voix/nombres/12.wav")
n13 = pygame.mixer.Sound("sons/voix/nombres/13.wav")
n14 = pygame.mixer.Sound("sons/voix/nombres/14.wav")
n15 = pygame.mixer.Sound("sons/voix/nombres/15.wav")
n16 = pygame.mixer.Sound("sons/voix/nombres/16.wav")
n17 = pygame.mixer.Sound("sons/voix/nombres/17.wav")
n18 = pygame.mixer.Sound("sons/voix/nombres/18.wav")
n19 = pygame.mixer.Sound("sons/voix/nombres/19.wav")
n20 = pygame.mixer.Sound("sons/voix/nombres/20.wav")
n21 = pygame.mixer.Sound("sons/voix/nombres/21.wav")
n22 = pygame.mixer.Sound("sons/voix/nombres/22.wav")
n23 = pygame.mixer.Sound("sons/voix/nombres/23.wav")
n24 = pygame.mixer.Sound("sons/voix/nombres/24.wav")
n25 = pygame.mixer.Sound("sons/voix/nombres/25.wav")
n26 = pygame.mixer.Sound("sons/voix/nombres/26.wav")
n27 = pygame.mixer.Sound("sons/voix/nombres/27.wav")
n28 = pygame.mixer.Sound("sons/voix/nombres/28.wav")
n29 = pygame.mixer.Sound("sons/voix/nombres/29.wav")
n30 = pygame.mixer.Sound("sons/voix/nombres/30.wav")
n31 = pygame.mixer.Sound("sons/voix/nombres/31.wav")
rreur = pygame.mixer.Sound("sons/voix/mots/erreur.wav")

class Engine:
    
    def __init__(self):
        self.MAX_PLY=32
        self.pv_length=[0 for x in range(self.MAX_PLY)]
        self.INFINITY=32000        
        self.init()
        
    def usermove(self,b,c,p):
        global freefree
        global yest
        if(self.endgame):
            self.print_result(b,p)
            return        
        chk=self.chkCmd(c)
        if(chk!=''):
            print(chk)
            erreur.play()
            time.sleep(0.6)
            return
        pos1=b.caseStr2Int(c[0]+c[1])
        pos2=b.caseStr2Int(c[2]+c[3])
        promote=''
        if(len(c)>4):
            promote=c[4]
            if(promote=='q'):
                promote='q'
            elif(promote=='r'):
                promote='r'
            elif(promote=='n'):
                promote='n'
            elif(promote=='b'):
                promote='b'
        mList=b.gen_moves_list()
        if(((pos1,pos2,promote) not in mList) or \
        (b.domove(pos1,pos2,promote)==False)):
            print('\n'+c+' : Coup incorrect.')
            erreur.play()
            time.sleep(0.6)
            Coupincorect.play()
            time.sleep(1.5)
            b.render()
            return
        else:
            p.deconte_STOP()
            freefree = False
            yest = False
        b.render()
        self.print_result(b,p)
        
    def chkCmd(self,c):
        err=(
        '\nCoup incorrect\n',
        '\nErreur.\n'
        )        
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
        if(len(c)<4 or len(c)>5):
            return err[0]
        if(c[0] not in letters):
            return err[1]
        if(c[1] not in numbers):
            return err[1]
        if(c[2] not in letters):
            return err[1]
        if(c[3] not in numbers):
            return err[1]
        return ''
    
    def search(self,b,p):
        global freefree
        p.deconte_GO()
        print("\nRecherche veuillez patienter...")
        Rechèreche.play()
        time.sleep(2.8)
        if(self.endgame):
            self.print_result(b,p)
            return
        self.clear_pv()
        self.nodes=0
        b.ply=0
        for i in range(1,self.init_depth+1):
            score=self.alphabeta(i,-self.INFINITY,self.INFINITY,b)
            j=0
            while(self.pv[j][j]!=0):
                c=self.pv[j][j]
                pos1=b.caseInt2Str(c[0])
                pos2=b.caseInt2Str(c[1])
                j+=1
            if(score>self.INFINITY-100 or score<-self.INFINITY+100):
                break
        p.deconte_STOP()
        best=self.pv[0][0]
        b.domove(best[0],best[1],best[2])
        self.print_result(b,p)
        freefree = False
        
    def alphabeta(self,depth,alpha,beta,b):
        if(depth==0):
            return b.evaluer()
        self.nodes+=1
        self.pv_length[b.ply] = b.ply
        if(b.ply >= self.MAX_PLY-1):
            return b.evaluer()
        chk=b.in_check(b.side2move)
        if(chk):
            depth+=1
        mList=b.gen_moves_list()
        f=False
        for i,m in enumerate(mList):
            if(not b.domove(m[0],m[1],m[2])):
                continue
            f=True
            score=-self.alphabeta(depth-1,-beta,-alpha,b)
            b.undomove()
            if(score>alpha):
                if(score>=beta):
                    return beta
                alpha = score
                self.pv[b.ply][b.ply] = m
                j = b.ply + 1
                while(j<self.pv_length[b.ply+1]):
                    self.pv[b.ply][j] = self.pv[b.ply+1][j]
                    self.pv_length[b.ply] = self.pv_length[b.ply + 1]
                    j+=1
        if(not f):
            if(chk):
                return -self.INFINITY + b.ply
            else:
                return 0
        return alpha

    def newgame(self,b):
        self.init()
        b.init()
        
    def print_result(self,b,p):
        f=False
        for pos1,pos2,promote in b.gen_moves_list():
            if(b.domove(pos1,pos2,promote)):
                b.undomove()
                f=True
                break
        if(not f):
            if(b.in_check(b.side2move)):
                if(b.side2move=='blanc'):
                    p.blanc_perdu()
                    print("\nÉchec et mat pour les blancs.\n")
                    gagné.play()
                    time.sleep(3)
                    Mats.play()
                    time.sleep(1.5)
                    Blanc.play()
                    p.blanc_perdu()
                else:
                    p.noir_perdu()
                    print("\nÉchec et mat pour les noirs.\n")
                    gagné.play()
                    time.sleep(3)
                    Mats.play()
                    time.sleep(1.5)
                    Noir.play()
                    p.noir_perdu()
            else:
                print("\nPartie nulle (Pat).\n")
                erreur.play()
                time.sleep(0.6)
                Pat.play()
                time.sleep(2)
                self.init()
                b.init()
                p.__init__()
                p.cadence()
                p.GO()
            self.endgame=True
            
    def clear_pv(self):
        self.pv=[[0 for x in range(self.MAX_PLY)] for x in range(self.MAX_PLY)]
        
    def setboard(self,b,c):
        cmd=c.split()
        cmd.pop(0)
        if(b.setboard(' '.join(cmd))):
            self.endgame=False
        
    def setDepth(self,c):
        cmd=c.split()
        try:
            d=int(cmd[1])
        except ValueError:
            print("\nErreur.\n")
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return
        if(d<2 or d>self.MAX_PLY):
            print('\nErreur.\n')
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return
        self.init_depth=d
        print('\nNiveau :',d-1)
        Niv.play()
        time.sleep(1)
        if d-1 == 1:
            n1.play()
        elif d-1 == 2:
            n2.play()
        elif d-1 == 3:
            n3.play()
        elif d-1 == 4:
            n4.play()
        elif d-1 == 5:
            n5.play()
        elif d-1 == 6:
            n6.play()
        elif d-1 == 7:
            n7.play()
        elif d-1 == 8:
            n8.play()
        elif d-1 == 9:
            n9.play()
        elif d-1 == 10:
            n10.play()
        elif d-1 == 11:
            n11.play()
        elif d-1 == 12:
            n12.play()
        elif d-1 == 13:
            n13.play()
        elif d-1 == 14:
            n14.play()
        elif d-1 == 15:
            n15.play()
        elif d-1 == 16:
            n16.play()
        elif d-1 == 17:
            n17.play()
        elif d-1 == 18:
            n18.play()
        elif d-1 == 19:
            n19.play()
        elif d-1 == 20:
            n20.play()
        elif d-1 == 21:
            n21.play()
        elif d-1 == 22:
            n22.play()
        elif d-1 == 23:
            n23.play()
        elif d-1 == 24:
            n24.play()
        elif d-1 == 25:
            n25.play()
        elif d-1 == 26:
            n26.play()
        elif d-1 == 27:
            n27.play()
        elif d-1 == 28:
            n28.play()
        elif d-1 == 29:
            n29.play()
        elif d-1 == 30:
            n30.play()
        elif d-1 == 31:
            n31.play()
        time.sleep(1.5)
        
    def perft(self,c,b):
        cmd=c.split()
        try:
            d=int(cmd[1])
        except ValueError:
            print("\nErreur.\n")
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return
        if(d<1 or d>self.MAX_PLY):
            print('\nErreur.\n')
            erreur.play()
            time.sleep(0.6)
            rreur.play()
            time.sleep(0.7)
            return
        print("\nRecherche veuillez patienter...")
        Rechèreche.play()
        time.sleep(2.8)
        time1 = self.get_ms()
        for i in range(1,d+1):
            total=self.perftoption(0,i-1,b)
        time2 = self.get_ms()
        timeDiff = round((time2-time1)/1000,2)
        print('Temps :',timeDiff,' secondes')
        
    def perftoption(self,prof,limit,b):        
        cpt=0
        if(prof>limit):
            return 0
        l=b.gen_moves_list()
        for i,m in enumerate(l):
            if(not b.domove(m[0],m[1],m[2])):
                continue
            cpt+=self.perftoption(prof+1,limit,b)
            if(limit==prof):
                cpt+=1
            b.undomove()
        return cpt
    
    def legalmoves(self,b):
        mList=b.gen_moves_list()
        cpt=1
        for m in mList:
            if(not b.domove(m[0],m[1],m[2])):
                continue            
            print('Coup ',cpt,':',b.caseInt2Str(m[0])+b.caseInt2Str(m[1])+m[2])
            b.undomove()
            cpt+=1
            
    def getboard(self,b):
        print(b.getboard())
        
    def bench(self,b):
        oldDepth=self.init_depth
        self.init_depth=4
        timeDiff=[]
        for i in range(3):
            print('\nRecherche veuillez patienter...',self.init_depth,'...')
            Rechèreche.play()
            time.sleep(2.8)
            if(not b.setboard('1rb2rk1/p4ppp/1p1qp1n1/3n2N1/2pP4/2P3P1/PPQ2PBP/R1B1R1K1 w - - 0 1')):
                print('Impossible de définir le tableau ??? !!!')
                erreur.play()
                return
            start_time=self.get_ms()       
            self.search(b)
            stop_time=self.get_ms()
            timeDiff.append(stop_time-start_time)
            print('Temps :',timeDiff[i],'ms\n')
        if(timeDiff[1] < timeDiff[0]):
            timeDiff[0] = timeDiff[1]
        if(timeDiff[2] < timeDiff[0]):
            timeDiff[0] = timeDiff[2]
        print('Meilleur temps',timeDiff[0],'millisecondes')
        print('Nœuds :',self.nodes)
        print('Nœuds par seconde :',round(self.nodes/timeDiff[0],2),'kn/secondes')
        self.init_depth=oldDepth
        
    def undomove(self,b):
        b.undomove()
        self.endgame=False
        
    def get_ms(self):
        return int(round(time.time() * 1000))
    
    def init(self):
        self.endgame=False    
        self.init_depth=4
        self.nodes=0
        self.clear_pv()
