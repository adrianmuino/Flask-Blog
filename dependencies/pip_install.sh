#!/bin/bash

# This script has to be run inside a python virtual environment
pip install "$1"
pip list > ./dependencies/pkg_list.txt
pip freeze > ./dependencies/requirements.txt
