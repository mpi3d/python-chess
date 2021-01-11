import pygame
from pygame.locals import *
import time
import random
pygame.init()
son = pygame.mixer.Sound("sons/bruits/gagné.wav")
son1 = pygame.mixer.Sound("sons/bruits/etindre.wav")
son2 = pygame.mixer.Sound("sons/voix/mots/démarage_en_cour.wav")
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
print('                           MPi3D                            ')
print('                      Version : 3.5                         ')
time.sleep(4)
print('\n\nDémarrage...\n\n')
son2.play()
time.sleep(2)
time.sleep(random.randint(1, 6))
from threading import Thread

def échec():
    import échec
def musique():
    while True :
        nb = random.randint(1, 5)
        if nb == 1:
            pygame.mixer.music.load("sons/musiques/1.wav")
            pygame.mixer.music.play()
            time.sleep(183)
        elif nb == 2:
            pygame.mixer.music.load("sons/musiques/2.wav")
            pygame.mixer.music.play()
            time.sleep(241)
        elif nb == 3:
            pygame.mixer.music.load("sons/musiques/3.wav")
            pygame.mixer.music.play()
            time.sleep(282)
        elif nb == 4:
            pygame.mixer.music.load("sons/musiques/4.wav")
            pygame.mixer.music.play()
            time.sleep(191)
        elif nb == 5:
            pygame.mixer.music.load("sons/musiques/5.wav")
            pygame.mixer.music.play()
            time.sleep(171)

        
t1=Thread(target=musique,args=())      
t2=Thread(target=échec,args=())

t1.start()
t2.start()

t2.join()
pygame.mixer.music.fadeout(1000)
son1.play()
quit(0)
