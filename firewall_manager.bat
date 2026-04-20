@echo off
title SNI Scanner - Firewall Manager
color 0E

:menu
cls
echo ========================================
echo     SNI Scanner - Firewall Manager
echo ========================================
echo.
echo Current Firewall Status:
echo ------------------------
netsh advfirewall show allprofiles | find "State"
echo.
echo ========================================
echo 1. Add Firewall Rules (Allow Ports)
echo 2. Remove Firewall Rules
echo 3. Show Current Rules
echo 4. Enable Firewall (Recommended)
echo 5. Disable Firewall (Not Recommended)
echo 6. Exit
echo ========================================
echo.
set /p choice="Select option (1-6): "

if "%choice%"=="1" goto add_rules
if "%choice%"=="2" goto remove_rules
if "%choice%"=="3" goto show_rules
if "%choice%"=="4" goto enable_firewall
if "%choice%"=="5" goto disable_firewall
if "%choice%"=="6" goto end
goto menu

:add_rules
cls
echo Adding firewall rules...
echo.

:: بررسی دسترسی ادمین
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    goto menu
)

for %%p in (443 2053 2083 2087 2096 8443) do (
    netsh advfirewall firewall add rule name="SNI_Scanner_TCP_%%p" dir=in action=allow protocol=TCP localport=%%p >nul 2>&1
    netsh advfirewall firewall add rule name="SNI_Scanner_TCP_%%p" dir=out action=allow protocol=TCP localport=%%p >nul 2>&1
    echo [OK] Port %%p configured
)

echo.
echo [SUCCESS] All ports added to firewall!
pause
goto menu

:remove_rules
cls
echo Removing firewall rules...
echo.

NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    goto menu
)

for %%p in (443 2053 2083 2087 2096 8443) do (
    netsh advfirewall firewall delete rule name="SNI_Scanner_TCP_%%p" >nul 2>&1
)

echo [SUCCESS] All rules removed!
pause
goto menu

:show_rules
cls
echo Current SNI Scanner rules:
echo ========================================
netsh advfirewall firewall show rule name="SNI_Scanner_TCP_*"
echo.
pause
goto menu

:enable_firewall
cls
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    goto menu
)

netsh advfirewall set allprofiles state on
echo [OK] Firewall enabled for all profiles!
pause
goto menu

:disable_firewall
cls
echo [WARNING] Disabling firewall is NOT recommended!
echo This will make your computer vulnerable!
echo.
set /p confirm="Are you sure? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Operation cancelled.
    pause
    goto menu
)

NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    goto menu
)

netsh advfirewall set allprofiles state off
echo [WARNING] Firewall disabled for all profiles!
pause
goto menu

:end
echo Goodbye!
exit /b 0