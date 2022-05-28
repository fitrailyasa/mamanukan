# Game Mamanukan
<img src="asset/home.png" width="100%">

## Deskripsi
Aplikasi game yang akan dibuat adalah, sebuah game burung terbang yang ditujukan agar si pemain dapat menjaga burung tersebut untuk tetap terbang dengan cara menekan tombol. Bukan hanya itu, pemain juga harus menjaga agar burung tidak terkena pipa untuk mendapatkan skor yang tinggi.

## Tugas Besar | Hands-On 4
Mata Kuliah Pemrograman Berorientasi Objek Kelas RD & Sistem Operasi RD

## Kelompok 4 : Ope Warnet
| NIM | NAMA | SEBAGAI |
| --- | ---- | ------- |
| 120140180 | [Merysah] | Project Leader & Tester |
| 120140048 | [Fitra Ilyasa] | Programmer |
| 120140168 | [M Haikal Fauzananda] | Programmer |
| 120140169 | [Emirssyah Putra] | Programmer |
| 120140170 | [Pandu Wiratama] | Tester |
| 120140184 | [Rahma Wati] | Designer |

## Fitur Game
- Mode Siang dan Mode Malam
- Tingkat Kesulitan Game
- Random Karakter Manuk (Burung)

## Penggunaan Sifat Dasar PBO
- Inheritance (Pewarisan)
- Encapsulation (Enkapsulasi)
- Abstract (Absraksi)

## 

## Teknologi
Teknologi yang digunakan untuk membuat game mamanukan:
- [Python] - Bahasa pemrograman yang digunakan.
- [Pygame] - Library python untuk membuat game.
- [Photoshop] - Aplikasi yang digunakan untuk membuat desain aset gambar.

## 1. Instalasi Manual
#### a. Untuk mengkloning source code game
```sh
git clone git@github.com:fitrailyasa/mamanukan.git
```

#### b. Requirement:
- Pygame

Instalasi [pygame] menggunakan PIP
```sh
pip install pygame
```

#### c. Tingkatan
Tingkat Kesulitan = Mudah
```sh
py main.py -e
```
Tingkat Kesulitan = Sedang
```sh
py main.py -m
```
Tingkat Kesulitan = Sulit
```sh
py main.py -d
```

## 2. Instalasi Menggunakan Docker Kontainer
#### a. Untuk mengkloning source code game
```sh 
git clone git@github.com:fitrailyasa/mamanukan.git
```

### b. Build game  :
Docker membuild game mamanukan (.) untuk menunjukkan direktori
```sh 
docker build -t mamanukan .
```

Docker Menjalankan game mamanukan
```sh
docker run mamanukan
```

#### c. Tingkatan
Tingkat Kesulitan = Mudah
```sh
py main.py -e
```
Tingkat Kesulitan = Sedang
```sh
py main.py -m
```
Tingkat Kesulitan = Sulit
```sh
py main.py -d
```

## Plugin

Petunjuk tentang cara menggunakan game ini dijelaskan dengan plugin berikut:
| Plugin | README |
| ------ | ------ |
| GitHub | [https://github.com/fitrailyasa/mamanukan/blob/fitra/README.md] |

## Link Demo Game "MAMANUKAN"
[![MAMANUKAN](https://img.youtube.com/vi/6v41BSRLSng/0.jpg)](https://www.youtube.com/watch?v=6v41BSRLSng)

   [Python]: <https://www.python.org/>
   [Pygame]: <https://www.pygame.org/>
   [Photoshop]: <https://www.adobe.com/sea/products/photoshop.html>
   [Merysah]: <https://github.com/chchaaa12>
   [Fitra Ilyasa]: <https://github.com/fitrailyasa>
   [M Haikal Fauzananda]: <https://github.com/muhammadhaikalfauzananda>
   [Emirssyah Putra]: <https://github.com/emirssyahputra>
   [Pandu Wiratama]: <https://github.com/PanduWiratama>
   [Rahma Wati]: <https://github.com/rahma0891>
