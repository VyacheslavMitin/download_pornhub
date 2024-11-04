@echo OFF
cd "C:\Users\sonic\PycharmProjects\download_pornhub\"
./start\activate.ps1

python3.11 main.py --no-questions

PAUSE

REM wt -d "C:\Users\sonic\PycharmProjects\download_pornhub\" "cmd /k venv\Scripts\activate"