#Python script for project 2
import sys
import os
import hashlib

try:
    imageFile = sys.argv[1]
    with open(imageFile, 'rb') as disk:
        diskHex = disk.read().hex()
    disk.close()
except FileNotFoundError:
    sys.exit("File Not Found")

def recoverPDF():
    return 0
def recoverMPG():
    return 0
def recoverBMP():
    return 0
def recoverGIF():
    return 0