@echo off
cd /d "%~dp0.."
python src\main.py --vfs "test-vfs.json" --script scripts\startup.txt