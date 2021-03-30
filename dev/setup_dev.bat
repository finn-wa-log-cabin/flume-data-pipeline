@REM Run from root of repo
python -m venv .venv
CALL .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt -r test\test_requirements.txt -r dev\dev_requirements.txt -e .
