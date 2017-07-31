@ECHO off
SETLOCAL ENABLEDELAYEDEXPANSION

:: No argument provided - show file Usage
IF [%1]==[] GOTO :USAGE

SET WORK_DIR=%1

::  Check if directory already exists
IF EXIST %~dp0\%1 GOTO DIREXISTS

:: Create directory if it does not already exist
@ECHO Creating directory %WORK_DIR%
MKDIR %WORK_DIR%
@ECHO DIR='%WORK_DIR%' > var.py

:: Clone Devnet Express Git Repo
@ECHO Cloning DevNet Express Sample repository
git clone https://github.com/CiscoDevNet/devnet-express-code-samples.git "%WORK_DIR%/devnet-express-code-samples"

:: Create Python Virtual Environment
@ECHO Creating virtual environment in %WORK_DIR%
virtualenv "%WORK_DIR%/env"

:: Verification Instructions
@ECHO
@ECHO ****
@ECHO To activate virtual environment, install libraries and verify your environment.
@ECHO Please run the following commands
@ECHO ****
@ECHO "%WORK_DIR%/env/Scripts/activate"
@ECHO "pip install -r requirements.txt"
@ECHO "verify.py <SPARK-TOKEN>"

GOTO :EOF

:: Script usage displayed if no argument is supplied
:USAGE
@ECHO Usage: %0 ^<Your-Directory^>
@ECHO e.g. %0 adam-dne
EXIT /B 1

:: Directory already exists
:DIREXISTS
@ECHO File %WORK_DIR% exists, cannot create directory %WORK_DIR%, please remove file or choose a different name

:: End of File
:EOF
EXIT /B 1