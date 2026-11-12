@echo off
cd /d "%~dp0.."
python src\main.py --script scripts\test_all.txt --vfs vfs\nested.json