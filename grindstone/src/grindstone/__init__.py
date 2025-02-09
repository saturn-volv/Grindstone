import glob
import os

try:
    for _ in glob.glob('input\\*.json'):
        pass
except IOError:
    os.mkdir('input')