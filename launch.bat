@echo off
title Revenue Dashboard
echo Starting dashboard, please wait...
cd /d "%~dp0"

if not exist "venv\" (
    echo Setting up for first time...
    python -m venv venv
)

call venv\Scripts\activate.bat

pip install flask pandas numpy --quiet

if not exist "data\erp_sales.csv" (
    python generate_data.py
)

start "" http://127.0.0.1:5000
python app.py
pause