#!/bin/bash

rm -f class_ref/*.rst
rm -rf _build/*
pyenv exec python3 _tools/autobuild.py classes
