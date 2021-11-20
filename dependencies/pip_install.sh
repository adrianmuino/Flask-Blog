#!/bin/bash

# This script has to be run inside a python virtual environment
pip install "$1"
pip list > pkg_list.txt
pip freeze > requirements.txt
