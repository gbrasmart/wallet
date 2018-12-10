#!/usr/bin/env bash

cp -r api/ src/main/python/api/
cp -r widgets/ src/main/python/widgets/
cp main.py src/main/python/main.py
cp requirements.txt src/main/python/requirements.txt
cp settings.ini src/main/resources/base/settings.ini

python -m fbs freeze

python -m fbs installer
