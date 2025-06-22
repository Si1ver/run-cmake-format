@echo off
rem This script updates the Pipfile and Pipfile.lock.
rem The pipenv is used to pin the versions of the packages and dependencies to achieve reproducibility.

rem To change the required version of cmakelang, modify the version number in the command below and run the script.
pipenv install cmakelang[yaml]==0.6.13
