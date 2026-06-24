# PBL0903 FastAPI Microservice

PBL0903 menghubungkan Site A dan Site B dengan dua pola:

- READ: APPX menjadi API Gateway Aggregator.
- WRITE: Create disimpan di DB milik tab aktif. Update/Delete memakai pola proxy:
  jika `owner` milik DB lokal maka database lokal diubah, jika milik tetangga
  maka request diteruskan lewat REST `httpx`.

```text
PBL0903
  APPX
    appx.py
    templates/index.html
    static/styles.css
    static/app.js

  SiteA
    DB-A.db
    MS1/ms1.py
    MS2/ms2.py

  SiteB
    MS3/DB-B.db
    MS3/ms3.py

  microservice_common.py
```

## Alur

```text
Tab MS1:
Browser -> APPX /gateway/ms1/cars -> MS1/DB-A

Tab MS2:
Browser -> APPX /gateway/ms2/cars -> asyncio.gather(MS2/DB-A, MS3/DB-B)

Tab MS3:
Browser -> APPX /gateway/ms3/cars -> asyncio.gather(MS3/DB-B, MS2/DB-A)

Update/Hapus mobil MS3 dari tab MS2:
Browser -> MS2 PUT/DELETE /cars/{id}?owner=MS3
        -> MS2 proxy via httpx ke MS3
        -> MS3 mengubah DB-B

Update/Hapus mobil MS2 dari tab MS1:
Browser -> MS1 PUT/DELETE /cars/{id}?owner=MS2
        -> MS1 proxy via httpx ke MS2
        -> MS2 mengubah DB-A
```

## Port

```text
APPX = http://127.0.0.1:8011
MS1  = http://127.0.0.1:5051
MS2  = http://127.0.0.1:5052
MS3  = http://127.0.0.1:5053
```

## Setup

```powershell
cd "C:\Users\MyBook Z Series\OneDrive\Documents\antigravity PABW\PBL0901\PBL0903"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r APPX\r.txt
```

## Menjalankan

Buka 4 terminal. Di setiap terminal:

```powershell
cd "C:\Users\MyBook Z Series\OneDrive\Documents\antigravity PABW\PBL0901\PBL0903"
.\.venv\Scripts\Activate.ps1
```

Terminal 1:

```powershell
uvicorn SiteA.MS1.ms1:app --reload --port 5051
```

Terminal 2:

```powershell
uvicorn SiteA.MS2.ms2:app --reload --port 5052
```

Terminal 3:

```powershell
uvicorn SiteB.MS3.ms3:app --reload --port 5053
```

Terminal 4:

```powershell
uvicorn APPX.appx:app --reload --port 8011
```

Buka:

```text
http://127.0.0.1:8011
```
