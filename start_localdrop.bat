@echo off
title LocalDrop - Wireless File Transfer
echo.
echo  Starting LocalDrop...
echo  Make sure your PC and iPhone are on the same Wi-Fi!
echo.
python server.py
if errorlevel 1 (
  echo.
  echo  ERROR: Python not found. Please install Python from https://python.org
  echo.
  pause
)
