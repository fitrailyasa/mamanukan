# Tugas Besar 
Pemrograman Berorientasi Objek Kelas RD
## Game Mamanukan
Aplikasi game yang akan dibuat adalah, sebuah game burung terbang yang ditujukan agar si pemain dapat menjaga burung tersebut untuk tetap terbang dengan cara menekan tombol. Bukan hanya itu, pemain juga harus menjaga agar burung tidak terkena pipa untuk mendapatkan skor yang tinggi.

## Kelompok 4 : Ope Warnet
- 120140180 Merysah (Project Leader)
- 120140048 Fitra Ilyasa (Programmer)
- 120140168 M Haikal Fauzananda (Programmer)
- 120140169 Emirssyah Putra (Programmer)
- 120140170 Pandu Wiratama (Tester)
- 120140184 Rahma Wati (Designer)


## Fitur Game

- Mode Siang dan Mode Malam
- Tingkat Kesulitan Game
- Random Karakter Manuk (Burung)

## Teknologi

Teknologi yang digunakan untuk membuat game mamanukan:

- [Python] - Bahasa pemrograman yang digunakan.
- [Pygame] - Library python untuk membuat game.
- [Photoshop] - Aplikasi yang digunakan untuk membuat desain aset gambar.

## Instalasi
Untuk mengkloning source code game.

```sh
https://github.com/fitrailyasa/mamanukan.git
```

Requirement:
- Pygame

Instalasi menggunakan PIP
```sh
pip install pygame
```

## Cara Penggunaan Game:
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
## instalasi container
Buat file dengan nama Dockerfile (tanpa extensi) yang isinya :
```sh 
FROM python:3

WORKDIR (directory file)

COPY /asset .
COPY main.py . 
COPY requirements.txt .
COPY README.md .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py", "-e"]
```

## Plugin

Petunjuk tentang cara menggunakan game ini dijelaskan dengan plugin berikut:
| Plugin | README |
| ------ | ------ |
| GitHub | [https://github.com/fitrailyasa/mamanukan/blob/fitra/README.md][PlDb] |

   [Python]: <https://www.python.org/>
   [Pygame]: <https://www.pygame.org/>
   [Photoshop]: <https://www.adobe.com/sea/products/photoshop.html>
