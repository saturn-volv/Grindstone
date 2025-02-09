import glob
import json
import os

def __main__():
    try:
        for _ in glob.glob('input\\*.json'):
            pass
    except IOError:
        os.mkdir('input')