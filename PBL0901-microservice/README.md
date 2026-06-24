# c006-Microservice
Course 006 Microservice

## Persiapan Lingkungan (Setup Environment)
Sebelum menjalankan proyek ini, pastikan Anda telah menginstal Python. Proyek ini membutuhkan beberapa library, yang dapat dilihat pada file `r.txt` di masing-masing folder.

Anda dapat menginstal dependensi dengan masuk ke salah satu folder (misalnya `APPX`, `SiteA/MS1`, `SiteA/MS2`, atau `SiteB/MS3`) dan menjalankan perintah:
```bash
pip install -r r.txt
```
*(Atau Anda bisa menginstal library utamanya secara manual: `pip install Flask peewee requests flask_restful`)*

## Langkah-Langkah Menjalankan Project
Karena ini adalah arsitektur microservice, Anda perlu membuka **4 terminal terpisah** untuk menjalankan semua service secara bersamaan.

### 1. Menjalankan Microservice 1 (MS1)
Buka terminal baru dan jalankan perintah berikut:
```bash
cd SiteA/MS1
python ms1.py
```
*(Service ini akan berjalan di http://localhost:5051)*

### 2. Menjalankan Microservice 2 (MS2)
Buka terminal baru dan jalankan perintah berikut:
```bash
cd SiteA/MS2
python ms2.py
```
*(Service ini akan berjalan di http://localhost:5052)*

### 3. Menjalankan Microservice 3 (MS3)
Buka terminal baru dan jalankan perintah berikut:
```bash
cd SiteB/MS3
python ms3.py
```
*(Service ini akan berjalan di http://localhost:5053)*

### 4. Menjalankan Aplikasi Utama (Frontend APPX)
Buka terminal baru dan jalankan aplikasi frontend (yang akan menampilkan antarmuka dan memanggil MS1, MS2, MS3):
```bash
cd APPX
python appx.py
```
*(Aplikasi ini akan berjalan di http://localhost:5000)*

## Mengakses Aplikasi
Setelah semua keempat service di atas berstatus `Running`, buka web browser dan akses aplikasi melalui:
**[http://localhost:5000](http://localhost:5000)**

---
**Catatan Perintah Pip (Referensi):**
- `pip list` = it's for checking package list
- `pip install` = it's for installing package list
- `pip freeze > requirements.txt` = it's for saving requirements.txt file
