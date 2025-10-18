#!/bin/csh

cd '/Users/sonic/PycharmProjects/download_pornhub/'
source .venv/bin/activate.csh

clear

python3.11 delete_old_dubles.py
