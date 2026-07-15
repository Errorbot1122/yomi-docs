#!/bin/bash

rm -f class_ref/*.rst
rm -rf _build/*.rst
pyenv exec python3 _tools/autobuild.py classes
