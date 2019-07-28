#!/usr/bin/env bash

python=$1
prefix=$2

[[ -z $python ]] && python=python
[[ -z $prefix ]] && prefix=/usr

$python -m pip install --upgrade pip setuptools wheel

# Install Python Modules
$python -m pip install -r requirements.txt

# Install vn.py
$python -m pip install .