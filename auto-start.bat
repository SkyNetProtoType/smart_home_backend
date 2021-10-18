@echo off
cd %cd%
git pull
set currentdir=%cd%
%currentdir%\env\Scripts\python.exe %currentdir%\webserver.py
pause




