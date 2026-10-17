# Warning AI generated
# Exit on error
$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot

Write-Host "[1/5] Processing dictionary dumps..." -ForegroundColor Yellow
Set-Location $ScriptDir
python tools/process_cedict.py full/cedict_ts.u8 full/cedict_ts.processed.u8
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: CEDict processing failed" -ForegroundColor Red
    exit 1
}
python tools/process_cccanto.py full/cccanto-webdist.txt full/cccanto-webdist.processed.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: CC-Canto processing failed" -ForegroundColor Red
    exit 1
}
Write-Host "Processed dictionaries generated (gitignored)." -ForegroundColor Green
Write-Host ""

Write-Host "[2/5] Building dictionary data..." -ForegroundColor Yellow
Set-Location "$ScriptDir\console"
cargo run -- build no_query
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Dictionary build failed" -ForegroundColor Red
    exit 1
}
Write-Host "Dictionary data built successfully!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Building web client..." -ForegroundColor Yellow
Set-Location "$ScriptDir\web_client"
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Web client build failed" -ForegroundColor Red
    exit 1
}
Write-Host "Web client built successfully!" -ForegroundColor Green
Write-Host ""

Write-Host "[4/5] Preparing docs directory..." -ForegroundColor Yellow
Set-Location $ScriptDir

if (Test-Path "docs") {
    Remove-Item -Path "docs" -Recurse -Force
    Write-Host "Removed old docs directory" -ForegroundColor Gray
}

New-Item -ItemType Directory -Path "docs" | Out-Null
Write-Host "Created docs directory" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Copying build output to docs..." -ForegroundColor Yellow
Copy-Item -Path "web_client\dist\*" -Destination "docs\" -Recurse -Force
Write-Host "Build output copied to docs directory!" -ForegroundColor Green
Write-Host ""

Write-Host "Docs directory contents:" -ForegroundColor Cyan
Get-ChildItem -Path "docs" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
