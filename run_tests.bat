@echo off
REM Run Tests Script for CE-API-II

setlocal enabledelayedexpansion

if "%1"=="" (
    echo Usage: run_tests.bat [command]
    echo.
    echo Available commands:
    echo   run_all         Run all tests
    echo   run_verbose     Run all tests with verbose output
    echo   run_cov         Run tests with coverage report
    echo   install_deps    Install test dependencies
    echo   run_schemas     Run schema tests only
    echo   run_models      Run model tests only
    echo   run_services    Run service tests only
    echo   run_repos       Run repository tests only
    echo   run_controllers Run controller tests only
    echo   run_utils       Run utility tests only
    echo   clean           Clean cache and temporary files
    echo.
    exit /b 1
)

if "%1"=="install_deps" (
    echo Installing test dependencies...
    pip install -r requirements\test.txt
    exit /b !errorlevel!
)

if "%1"=="run_all" (
    echo Running all tests...
    pytest tests\ -q
    exit /b !errorlevel!
)

if "%1"=="run_verbose" (
    echo Running all tests with verbose output...
    pytest tests\ -v
    exit /b !errorlevel!
)

if "%1"=="run_cov" (
    echo Running tests with coverage report...
    pytest tests\ --cov=app --cov-report=html --cov-report=term-missing
    echo.
    echo Coverage report generated in htmlcov\index.html
    exit /b !errorlevel!
)

if "%1"=="run_schemas" (
    echo Running schema tests...
    pytest tests\test_schemas.py -v
    exit /b !errorlevel!
)

if "%1"=="run_models" (
    echo Running model tests...
    pytest tests\test_models.py -v
    exit /b !errorlevel!
)

if "%1"=="run_services" (
    echo Running service tests...
    pytest tests\test_services.py -v
    exit /b !errorlevel!
)

if "%1"=="run_repos" (
    echo Running repository tests...
    pytest tests\test_repositories.py -v
    exit /b !errorlevel!
)

if "%1"=="run_controllers" (
    echo Running controller tests...
    pytest tests\test_controllers.py -v
    exit /b !errorlevel!
)

if "%1"=="run_utils" (
    echo Running utility tests...
    pytest tests\test_utils.py -v
    exit /b !errorlevel!
)

if "%1"=="clean" (
    echo Cleaning cache files...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
    for /d /r . %%d in (.coverage) do @if exist "%%d" rd /s /q "%%d"
    for /d /r . %%d in (htmlcov) do @if exist "%%d" rd /s /q "%%d"
    del /s /q *.pyc > nul 2>&1
    echo Cache cleaned successfully!
    exit /b 0
)

echo Unknown command: %1
exit /b 1
