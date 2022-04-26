import random
import sys
import argparse
from itertools import cycle
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
    
    # variabel gambar dan audio (suara)
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
        self.gambar, self.suara = asset('asset/')
        
        # pesan tampilan halaman awal
        self.pesan = [int((self.lebar - self.gambar['home'].get_width()) /2),
                      int(self.tinggi * 0.12)]

        # mengatur kecepatan gerak
        self.atur_kesulitan(mode)

        # membangun objek
        jalan_xy = [0, int(self.tinggi * .79)]
        manuk_xy = [int(self.lebar * .2),
                  int((self.tinggi - self.gambar['manuk'][0].get_height()) / 2)]
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
        pipa1 = self.pipa_awal(self.lebar + 200)
        pipa2 = self.pipa_awal(self.lebar + 200 + pipa1.width + self.jarak_pipa_y)
        self.pipa = [pipa1, pipa2]

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
            keadaan_manuk = self.manuk.X + self.manuk.width / 2
            for pipa in self.pipa:
                keadaan_pipa = pipa.x + pipa.width / 2
                if keadaan_pipa <= keadaan_manuk < keadaan_pipa + self.kecepatan:
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
        pipaHeight = self.gambar['pipa'][0].get_height()
        pipaX = pos_x

        pipa_pair = {
            'x': pipaX,
            'upper': gapY - pipaHeight, # upper y
            'lower': gapY + self.jarak_pipa_X # lower y
        }
        return Pipa(pipa_pair, self.kecepatan, self.gambar)
    
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
            self.screen.blit(self.gambar['home'], self.pesan)
        elif flag == 'over':
            self.screen.blit(self.gambar['selesai'], (50, 180))
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
            totalWidth += self.gambar['nomor'][digit].get_width()

        Xoffset = (self.lebar - totalWidth) / 2

        for digit in scoreDigits:
            self.screen.blit( self.gambar['nomor'][digit],
                              (Xoffset, self.tinggi * 0.1) )
            Xoffset += self.gambar['nomor'][digit].get_width()

# Kelas Jalan
class Jalan:
    # Konstruktor
    def __init__(self, koordinat, kecepatan, gambar):
        self.x, self.Y = koordinat[0], koordinat[1]
        self.speed = kecepatan
        self.IMG = gambar['jalan']
        # basis jumlah dapat bergeser maksimum ke kiri 
        self.SHIFT = gambar['jalan'].get_width() - gambar['background'].get_width()

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
    manuk_Shm = {'val': 0, 'index': 1}
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
        self.IMG = gambar['manuk'] 
        self.width = gambar['manuk'][0].get_width()
        self.height = gambar['manuk'][0].get_height()
        self.yBOTTOM = jalan_Y - self.height
        self.MASK = (
            # hitmask untuk mode sayap
            get_gambar(gambar['manuk'][0]),
            get_gambar(gambar['manuk'][1]),
            get_gambar(gambar['manuk'][2])
        )

    # Method osilasi nilai dari manuk_Shm['val'] antara 8 dan -8
    def Keadaan(self):
        if abs(self.manuk_Shm['val']) == 8:
            self.manuk_Shm['index'] *= -1

        if self.manuk_Shm['index'] == 1:
            self.manuk_Shm['val'] += 1
        else:
            self.manuk_Shm['val'] -= 1
        self.y += self.manuk_Shm['val']

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
        self.manuk_Shm = {'val': 0, 'index': 1}

    # Method animasi sayap
    def kepak_sayap(self):
        self.loopIter += 1
        if self.loopIter == 10:
            self.wingIndex = next(self.wingMode)
            self.loopIter = 0

    # Method manuk terbang
    def terbang(self):
        self.flapped = True

    # Method update manuk_ velocity dan rotasi
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
        self.IMG = gambar['pipa'] 
        self.width = gambar['pipa'][0].get_width()
        self.height = gambar['pipa'][0].get_height()
        self.MASK = (
            # hitmask untuk pipa
            get_gambar(gambar['pipa'][0]), 
            get_gambar(gambar['pipa'][1]) 
        )

    # Method Gerak pipa
    def gerak(self):
        self.x -= self.speed

    # Method update pipa atas dan bawah
    def update(self, obj):
        obj.blit(self.IMG[0], (self.x, self.upperY))
        obj.blit(self.IMG[1], (self.x, self.lowerY))


def get_gambar(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

# Method tabbrak
def tabrak(manuk_, pipa):
    if manuk_.touchground():
        return True
    
    manuk_Rect = pygame.Rect(manuk_.X, manuk_.y, manuk_.width, manuk_.height)
    manuk_Mask = manuk_.MASK[manuk_.wingIndex]
    for p in pipa:
        uRect = pygame.Rect(p.x, p.upperY, p.width, p.height)
        lRect = pygame.Rect(p.x, p.lowerY, p.width, p.height)
        uMask = p.MASK[0]
        lMask = p.MASK[1]
        uCollide = pixel_gambar(manuk_Rect, uRect, manuk_Mask, uMask)
        lCollide = pixel_gambar(manuk_Rect, lRect, manuk_Mask, lMask)

        if uCollide or lCollide:
            return True

    return False

# Method pixel gambar
def pixel_gambar(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

# Method Asset Gambar & Audio
def asset(folder):
    gambar, audio = {}, {}
    jenis_manuk = (
        # manuk emir
        (
            folder + 'gambar/manuk_emir.png',
            folder + 'gambar/manuk_emir.png',
            folder + 'gambar/manuk_emir.png',
        ),
        # manuk fitra
        (
            folder + 'gambar/manuk_fitra.png',
            folder + 'gambar/manuk_fitra.png',
            folder + 'gambar/manuk_fitra.png',
        ),
        # manuk haikal
        (
            folder + 'gambar/manuk_haikal.png',
            folder + 'gambar/manuk_haikal.png',
            folder + 'gambar/manuk_haikal.png',
        ),
        # manuk mery
        (
            folder + 'gambar/manuk_mery.png',
            folder + 'gambar/manuk_mery.png',
            folder + 'gambar/manuk_mery.png',
        ),
        # manuk pandu
        (
            folder + 'gambar/manuk_pandu.png',
            folder + 'gambar/manuk_pandu.png',
            folder + 'gambar/manuk_pandu.png',
        ),
        # manuk rahma
        (
            folder + 'gambar/manuk_rahma.png',
            folder + 'gambar/manuk_rahma.png',
            folder + 'gambar/manuk_rahma.png',
        ),
    )

    # warna background
    warna_bg = (
        folder + 'gambar/mode_siang.png',
        folder + 'gambar/mode_malam.png',
    )

    # warna pipa
    warna_pipa = (
        folder + 'gambar/pipa_merah.png',
        folder + 'gambar/pipa_biru.png',
    )

    # skor
    gambar['nomor'] = (
        pygame.image.load(folder + 'gambar/0.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/1.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/2.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/3.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/4.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/5.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/6.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/7.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/8.png').convert_alpha(),
        pygame.image.load(folder + 'gambar/9.png').convert_alpha()
    )

    # gambar selesai
    gambar['selesai'] = pygame.image.load(
        folder + 'gambar/selesai.png').convert_alpha()
    
    # gambar home
    gambar['home'] = pygame.image.load(
        folder + 'gambar/home.png').convert_alpha()
    
    # gambar jalan
    gambar['jalan'] = pygame.image.load(
        folder + 'gambar/jalan.png').convert_alpha()
    
    # gambar background
    indeks_bg = random.randint(0, len(warna_bg) - 1)
    gambar['background'] = pygame.image.load(warna_bg[indeks_bg]).convert()

    # gambar manuk
    indeks_manuk = random.randint(0, len(jenis_manuk) - 1)
    gambar['manuk'] = (
        pygame.image.load(jenis_manuk[indeks_manuk][0]).convert_alpha(),
        pygame.image.load(jenis_manuk[indeks_manuk][1]).convert_alpha(),
        pygame.image.load(jenis_manuk[indeks_manuk][2]).convert_alpha(),
    )

    # gambar pipa
    indeks_pipa = random.randint(0, len(warna_pipa) - 1)
    gambar['pipa'] = (
        pygame.transform.flip(
            pygame.image.load(warna_pipa[indeks_pipa]).convert_alpha(), False, True),
        pygame.image.load(warna_pipa[indeks_pipa]).convert_alpha(),
    )

    # audio
    if 'menang' in sys.platform:
        ekstensi_audio = '.wav'
    else:
        ekstensi_audio = '.ogg'
    audio['die']    = pygame.mixer.Sound(folder + 'audio/die' + ekstensi_audio)
    audio['hit']    = pygame.mixer.Sound(folder + 'audio/hit' + ekstensi_audio)
    audio['point']  = pygame.mixer.Sound(folder + 'audio/point' + ekstensi_audio)
    audio['swoosh'] = pygame.mixer.Sound(folder + 'audio/swoosh' + ekstensi_audio)
    audio['wing']   = pygame.mixer.Sound(folder + 'audio/wing' + ekstensi_audio)

    return gambar, audio

# Instansiasi objek
# memilih tingkat kesulitan dalam game
parser = argparse.ArgumentParser(usage='%(prog)s [-h]/[-opt]',
                                 description='Play Game Mamanukan',
                                 allow_abbrev=False)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', '--easy', action='store_true', help='easy mode')
group.add_argument('-m', '--median', action='store_true', help='median mode')
group.add_argument('-d', '--difficult', action='store_true', help='hard mode')
args = parser.parse_args()

# Method utama / main untuk memilih mode
def main(mode):
    Game(mode)


if __name__ == '__main__':
    main(sys.argv[1])
