# Script untuk menjalankan PBL0903 secara otomatis

Write-Host "=== Memulai Setup PBL0903 ===" -ForegroundColor Green

# 1. Tentukan folder PBL0903
$PBL_DIR = "c:\Users\MyBook Z Series\OneDrive\Documents\antigravity PABW\PBL0901\PBL0903"
Set-Location $PBL_DIR

# 2. Setup Virtual Environment jika belum ada
if (-not (Test-Path ".venv")) {
    Write-Host "Membuat virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
}

# 3. Install Dependensi
Write-Host "Menginstal dependensi..." -ForegroundColor Yellow
& ".\.venv\Scripts\pip" install -r APPX\r.txt

# 4. Menjalankan Microservices di Terminal Terpisah
Write-Host "Menjalankan MS1, MS2, MS3, dan APPX..." -ForegroundColor Green

# Terminal 1: MS1 (Port 5051)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PBL_DIR'; .\.venv\Scripts\Activate.ps1; uvicorn SiteA.MS1.ms1:app --reload --port 5051"

# Terminal 2: MS2 (Port 5052)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PBL_DIR'; .\.venv\Scripts\Activate.ps1; uvicorn SiteA.MS2.ms2:app --reload --port 5052"

# Terminal 3: MS3 (Port 5053)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PBL_DIR'; .\.venv\Scripts\Activate.ps1; uvicorn SiteB.MS3.ms3:app --reload --port 5053"

# Terminal 4: APPX (Gateway - Port 8011)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PBL_DIR'; .\.venv\Scripts\Activate.ps1; uvicorn APPX.appx:app --reload --port 8011"

# 5. Membuka Browser
Write-Host "Membuka browser ke http://127.0.0.1:8011..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:8011"

Write-Host "=== Semua service telah dijalankan! ===" -ForegroundColor Green
