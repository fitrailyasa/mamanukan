import random
import sys
import argparse
from itertools import cycle

# memilih tingkat kesulitan dalam game
parser = argparse.ArgumentParser(usage='%(prog)s [-h]/[-opt]',
                                 description='Play Mamanukan Game',
                                 allow_abbrev=False)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', '--easy', action='store_true', help='easy mode')
group.add_argument('-m', '--median', action='store_true', help='median mode')
group.add_argument('-d', '--difficult', action='store_true', help='hard mode')
args = parser.parse_args()

import pygame
# Kelas Game
class Game:
    # setting tampilan windows
    fps = 30
    lebar = 288
    tinggi = 512
    fpslock, screen = {}, {}
    
    # setting default game
    kecepatan = 4 
    jarak_pipa_X = 100 
    jarak_pipa_y = 100 
    
    # variabel gambar dan audio 
    gambar, suara = {}, {}

    # variabel objek
    manuk, pipa, jalan = {}, {}, {}

    # pesan tampilan halaman awal
    pesan = {}

    # skor game awal
    skor = 0

    # Konstruktor
    def __init__(self, mode):
        
        # init tampilan window
        pygame.init()
        self.fpslock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.lebar, self.tinggi))
        pygame.display.set_caption('Flappy Bird')

        # asset gambar dan audio
        self.gambar, self.suara = asset('asset/')
        
        # pesan tampilan halaman awal
        self.pesan = [int((self.lebar - self.gambar['message'].get_width()) /2),
                      int(self.tinggi * 0.12)]

        # mengatur kecepatan gerak
        self.atur_kesulitan(mode)

        # membangun objek
        jalan_xy = [0, int(self.tinggi * .79)]
        manuk_xy = [int(self.lebar * .2),
                  int((self.tinggi - self.gambar['bird'][0].get_height()) / 2)]
        self.jalan = Jalan(jalan_xy, self.kecepatan, self.gambar)
        self.manuk = Manuk(manuk_xy, jalan_xy[1], self.gambar)

        # perulangan program utama
        while True:
            self.tampilan_awal()
            self.mulai()
            self.game_berakhir()

    # Method tampilan awal
    def tampilan_awal(self):
        # reset
        self.manuk.reset()
        self.pipa.clear()
        self.skor = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    self.suara['wing'].play()
                    return

            # manuk terbang
            self.manuk.Keadaan()
            self.refresh('welc')
   
    # Method memulai
    def mulai(self):
        self.manuk.softreset()
        pipe1 = self.pipa_awal(self.lebar + 200)
        pipe2 = self.pipa_awal(self.lebar + 200 + pipe1.width + self.jarak_pipa_y)
        self.pipa = [pipe1, pipe2]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    self.suara['wing'].play()
                    self.manuk.terbang()

            # mengecek status ketika jatuh
            tabrakan = tabrak(self.manuk, self.pipa)
            if tabrakan:
                return

            # update skor
            birdMidPos = self.manuk.X + self.manuk.width / 2
            for pipe in self.pipa:
                pipeMidPos = pipe.x + pipe.width / 2
                if pipeMidPos <= birdMidPos < pipeMidPos + self.kecepatan:
                    self.suara['point'].play()
                    self.skor += 1

            # memperbarui manuk
            self.manuk.update()

            # memperbarui pipa
            self.update_pipa()
            self.refresh('play')
            
    # Method selesai (game over)
    def game_berakhir(self):
        # suara ketika menabrak dan mati
        self.suara['hit'].play()
        self.suara['die'].play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    return

            # manuk ketika jatuh
            self.manuk.update()
            self.refresh('over')

    # Method mengatur kesulitan game
    def atur_kesulitan(self, m):
        difficulty = {'-e': 4, '--easy': 4,
                      '-m': 5, '--median': 5,
                      '-d': 6, '--difficult': 6}
        self.kecepatan = difficulty.get(m, 4)

    # Method mengatur pipa
    def pipa_awal(self, pos_x):
        # mengatur jarak antara pipa atas dan bawah
        gapY = random.randrange(0, int(self.jalan.Y * 0.6 - self.jarak_pipa_X))
        gapY += int(self.jalan.Y * 0.2)
        pipeHeight = self.gambar['pipe'][0].get_height()
        pipeX = pos_x

        pipe_pair = {
            'x': pipeX,
            'upper': gapY - pipeHeight, # upper y
            'lower': gapY + self.jarak_pipa_X # lower y
        }
        return Pipa(pipe_pair, self.kecepatan, self.gambar)
    
    # Method mengupdate pipa
    def update_pipa(self):
        # menggeser pipa ke kiri
        for p in self.pipa:
            p.gerak()
        
        # menambah pipa baru
        if 0 < self.pipa[0].x < self.kecepatan+1: # x==4
            diff = self.pipa[1].x - self.pipa[0].x
            p = self.pipa_awal(self.pipa[1].x + diff)
            self.pipa.append(p)
        
        # menghapus pipa lama
        if self.pipa[0].x < -self.pipa[0].width:
            self.pipa.pop(0)

    # Method refresh
    def refresh(self, flag):
        # background, pipa & jalan
        self.screen.blit(self.gambar['background'], (0, 0))
        for p in self.pipa:
            p.update(self.screen)
        if flag != 'over':
            self.jalan.update()
        self.jalan.gerak(self.screen)

        # pesan & skor
        if flag == 'welc':
            self.screen.blit(self.gambar['message'], self.pesan)
        elif flag == 'over':
            self.screen.blit(self.gambar['gameover'], (50, 180))
        if flag in ('play', 'over'):
            self.tampil_skor()

        # manuk
        self.manuk.kepak_sayap()
        if flag == 'over':
            self.manuk.gerak(self.screen, 'dead')
        else:
            self.manuk.gerak(self.screen)

        pygame.display.update()
        self.fpslock.tick(self.fps)

    # Method menampilkan skor
    def tampil_skor(self):
        scoreDigits = [int(x) for x in list(str(self.skor))]
        totalWidth = 0 

        for digit in scoreDigits:
            totalWidth += self.gambar['numbers'][digit].get_width()

        Xoffset = (self.lebar - totalWidth) / 2

        for digit in scoreDigits:
            self.screen.blit( self.gambar['numbers'][digit],
                              (Xoffset, self.tinggi * 0.1) )
            Xoffset += self.gambar['numbers'][digit].get_width()

# Kelas Jalan
class Jalan:
    # Konstruktor
    def __init__(self, koordinat, kecepatan, gambar):
        self.x, self.Y = koordinat[0], koordinat[1]
        self.speed = kecepatan
        self.IMG = gambar['base']
        # basis jumlah dapat bergeser maksimum ke kiri 
        self.SHIFT = gambar['base'].get_width() - gambar['background'].get_width()

    # Method update posisi jalan
    def update(self):
        self.x = -((-self.x + self.speed) % self.SHIFT)

    # Method gerak jalan berdasarkan layar
    def gerak(self, obj):
        obj.blit(self.IMG, (self.x, self.Y))

# Kelas Manuk
class Manuk:

    # setting default manuk
    wingIndex = 0 
    wingMode = cycle([0, 1, 2, 1]) 
    loopIter = 0
    birdShm = {'val': 0, 'index': 1}
    X        =   0     
    y        =   0
    INITY    =   0      
    yTOP     = -24      
    yBOTTOM  = 100      
    velY     =   0
    velMAXY  =  10      
    velMINY  =  -8      
    ACCY     =   1      
    rotation =   0
    rate     =   3      
    flapVel  =  -9      
    flapped  =  False
    width, height = {}, {}

    # Konstruktor
    def __init__(self, koordinat, jalan_Y, gambar):
        self.X, self.y, self.INITY = koordinat[0], koordinat[1], koordinat[1]
        self.IMG = gambar['bird'] 
        self.width = gambar['bird'][0].get_width()
        self.height = gambar['bird'][0].get_height()
        self.yBOTTOM = jalan_Y - self.height
        self.MASK = (
            # hitmask untuk mode sayap
            get_gambar(gambar['bird'][0]),
            get_gambar(gambar['bird'][1]),
            get_gambar(gambar['bird'][2])
        )

    # Method osilasi nilai dari birdShm['val'] antara 8 dan -8
    def Keadaan(self):
        if abs(self.birdShm['val']) == 8:
            self.birdShm['index'] *= -1

        if self.birdShm['index'] == 1:
            self.birdShm['val'] += 1
        else:
            self.birdShm['val'] -= 1
        self.y += self.birdShm['val']

    # Method softreset status manuk
    def softreset(self):
        self.loopIter = 0
        self.wingIndex = 0
        self.velY = -9
        self.rotation = 30

    # Method reset status manuk
    def reset(self):
        self.softreset()
        self.rotation = 0
        self.y = self.INITY
        self.birdShm = {'val': 0, 'index': 1}

    # Method animasi sayap
    def kepak_sayap(self):
        self.loopIter += 1
        if self.loopIter == 10:
            self.wingIndex = next(self.wingMode)
            self.loopIter = 0

    # Method manuk terbang
    def terbang(self):
        self.flapped = True

    # Method update bird velocity dan rotasi
    def update(self):
        if self.flapped:
            self.velY = self.flapVel
            self.rotation = 30
            self.flapped = False
        elif self.velY < self.velMAXY:
            self.velY += self.ACCY

        self.y += self.velY
        if self.y < self.yTOP:
            self.y = self.yTOP
        elif self.y > self.yBOTTOM:
            self.y = self.yBOTTOM

        if not self.touchground():
            if self.rotation > -70:
                self.rotation -= self.rate

    # Method menggerakkan manuk
    def gerak(self, obj, isdead = ''):
        if isdead == 'dead':
            rotImg = pygame.transform.rotate(self.IMG[1],self.rotation)
        else:
            rotImg = pygame.transform.rotate(self.IMG[self.wingIndex],
                                             self.rotation)
        obj.blit(rotImg, (self.X, self.y))

    # Method cek jika menyentuh tanah
    def touchground(self):
        return self.y >= self.yBOTTOM

# Kelas Pipa
class Pipa:

    # Konstruktor
    def __init__(self, p, kecepatan, gambar):
        self.x = p['x']
        self.upperY, self.lowerY = p['upper'], p['lower']
        self.speed = kecepatan
        self.IMG = gambar['pipe'] 
        self.width = gambar['pipe'][0].get_width()
        self.height = gambar['pipe'][0].get_height()
        self.MASK = (
            # hitmask untuk pipa
            get_gambar(gambar['pipe'][0]), 
            get_gambar(gambar['pipe'][1]) 
        )

    # Method Gerak pipa
    def gerak(self):
        self.x -= self.speed

    # Method update pipa atas dan bawah
    def update(self, obj):
        obj.blit(self.IMG[0], (self.x, self.upperY))
        obj.blit(self.IMG[1], (self.x, self.lowerY))

# Method get gambar
def get_gambar(image):
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

# Method tabrak
def tabrak(bird, pipes):
  pass