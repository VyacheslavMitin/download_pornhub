#!/opt/bin/fish

set PATH_SCRIPT_DIR '/opt/root/download_pornhub/'
set PYTHON_BIN_VER python3.11

cd $PATH_SCRIPT_DIR
source ven/bin/activate.fish

clear

# python3 main.py --no-questions
python3 main.py --edit-models
