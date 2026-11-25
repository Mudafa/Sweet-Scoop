@echo off
REM Sweet Scoop - build the containers, start the app, and run the 7 Selenium tests.
REM Double-click this file (Docker Desktop must be running).
cd /d "%~dp0"

echo.
echo ===== 1. Checking Docker =====
docker version --format "Docker {{.Server.Version}} is running"
if errorlevel 1 (
  echo.
  echo Docker is not running. Start Docker Desktop, wait for "Engine running", then run this again.
  pause
  exit /b 1
)

echo.
echo ===== 2. Building images and starting backend + frontend =====
docker compose up -d --build
if errorlevel 1 goto failed

docker compose ps

echo.
echo ===== 3. Running Selenium tests (first run downloads Chrome, ~1 GB) =====
docker compose --profile test run --rm tests
if errorlevel 1 goto failed

echo.
echo ===== ALL TESTS PASSED =====
echo The app is still running at http://localhost
echo To stop it:  docker compose --profile test down
pause
exit /b 0

:failed
echo.
echo ===== SOMETHING FAILED - copy the error above and send it to Claude =====
pause
exit /b 1
