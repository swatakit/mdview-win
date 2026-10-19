@echo off
rem Builds MDViewer.exe (a tiny launcher with the icon inside) using the C# compiler
rem that ships with Windows. Nothing is downloaded. Keep this file next to
rem mdview.bat, mdview.py, mdview.ico and mdview-launcher.cs.
rem Only writes to this folder and to your own user profile (HKEY_CURRENT_USER).
set "HERE=%~dp0"
set "CSC=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%CSC%" set "CSC=%WINDIR%\Microsoft.NET\Framework\v4.0.30319\csc.exe"
if not exist "%CSC%" (echo Could not find the Windows C# compiler ^(csc.exe^). & pause & exit /b)
if not exist "%HERE%mdview.ico" (echo mdview.ico is not in this folder. & pause & exit /b)
if not exist "%HERE%mdview-launcher.cs" (echo mdview-launcher.cs is not in this folder. & pause & exit /b)

"%CSC%" /nologo /target:winexe /win32icon:"%HERE%mdview.ico" /out:"%HERE%MDViewer.exe" "%HERE%mdview-launcher.cs"
if errorlevel 1 (echo Build failed. Send Claude a screenshot of this window. & pause & exit /b)
if not exist "%HERE%MDViewer.exe" (echo MDViewer.exe was not created or was removed. Send Claude a screenshot. & pause & exit /b)

set "APP=HKCU\Software\Classes\Applications\MDViewer.exe"
reg add "%APP%" /v FriendlyAppName /d "MD Viewer" /f >nul
reg add "%APP%\DefaultIcon" /ve /d "%HERE%mdview.ico" /f >nul
reg add "%APP%\SupportedTypes" /v ".md" /d "" /f >nul
reg add "%APP%\shell\open\command" /ve /d "\"%HERE%MDViewer.exe\" \"%%1\"" /f >nul
ie4uinit.exe -show
echo.
echo Built MDViewer.exe. Now set it as the app for .md files (see Claude's steps).
pause
