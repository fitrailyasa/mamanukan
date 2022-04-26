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
        pygame.display.set_caption('Mamanukan')

        # asset gambar dan audio
        #self.gambar, self.suara = asset('asset/')
        
        # pesan tampilan halaman awal
        self.pesan = [int((self.lebar - self.gambar['message'].get_width()) /2),
                      int(self.tinggi * 0.12)]

        # mengatur kecepatan gerak
        self.atur_kesulitan(mode)

        # instansiasi objek
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
            self.manuk.shm()
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
                    self.manuk.flap()

            # mengecek status ketika jatuh
            #isCrashed = checkCrash(self.manuk, self.pipa)
            #if isCrashed:
                #return

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
            p.move()
        
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
            p.draw(self.screen)
        if flag != 'over':
            self.jalan.update()
        self.jalan.draw(self.screen)

        # pesan & skor
        if flag == 'welc':
            self.screen.blit(self.gambar['message'], self.pesan)
        elif flag == 'over':
            self.screen.blit(self.gambar['gameover'], (50, 180))
        if flag in ('play', 'over'):
            self.tampil_skor()

        # manuk
        self.manuk.flapWing()
        if flag == 'over':
            self.manuk.draw(self.screen, 'dead')
        else:
            self.manuk.draw(self.screen)

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
  
# Kelas Manuk
class Manuk:
  # Konstruktor
  def __init__(self):
    pass

  # Method Gerak
  def gerak(self):
    pass

  # Method Update
  def update(self):
    pass

# Kelas Jalan
class Jalan:
  # Konstruktor
  def __init__(self):
    pass

  # Method Gerak 
  def gerak(self):
    pass

  # Method Keadaan
  def keadaan (self):
    pass

  # Method Soft_Reset 
  def reset(self):
    pass

  # Method Terbang
  def terbang(self):
    pass

  # Method Kepak_Sayap 
  def kepak_sayap(self):
    pass

  # Method Jatuh
  def jatuh(self):
    pass

  # Method Update
  def update(self):
    pass

# Kelas Pipa
class Pipa:
  # Konstruktor
  def __init__(self):
    pass

  # Method Gerak 
  def gerak(self):
    pass

  # Method Pindah
  def pindah(self):
    pass