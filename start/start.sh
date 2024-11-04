#!/opt/homebrew/bin/fish

set PATH_SCRIPT_DIR '/Users/sonic/PycharmProjects/download_pornhub/'
set PYTHON_BIN_VER python3.11

cd $PATH_SCRIPT_DIR
. venv/bin/activate.fish

clear

$PYTHON_BIN_VER main.py
# $PYTHON_BIN_VER main.py --edit-models
# $PYTHON_BIN_VER main.py --no-questions
