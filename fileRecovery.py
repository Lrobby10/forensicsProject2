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


#Courtney is doing JPG, DOCX, AVI, and PNG
#import time

#sources
#https://www.w3schools.com/python/ref_func_open.asp
#https://docs.python.org/3/library/hashlib.html



#variables
fileName = sys.argv[1]

#recovers files with JPG extension
def JPGrecover():
    print('\nJPG files:\n')
    with open(fileName, 'rb') as f:
        s = f.read()
        index = 0;
        count = 0;
        try:
            while True:
                #for JPG files the starting signature is 0xFF D8
                index = s.index(b'\xFF\xD8', index)

                #check if we're at the start of a sector 
                #if we aren't increment, if we are continue
                if (index % 0x1000 != 0):
                    index += 2
                    continue

                #JPG files have footer of 0xFF D9, trailing with 00's to ensure end
                endIndex = s.index(b'\xFF\xD9\x00\x00\x00\x00', index) + 1

                #write contents to file
                writtenFile = open(str(count) + ".jpg", "wb")
                writtenFile.write(s[index:endIndex + 1])
                writtenFile.close()
                print('File contents written to ' + str(count) + '.jpg')

                #print offset info
                print('Start Offset: ' + hex(index))
                print('End Offset: ' + hex(endIndex))

                #get hash info
                hash = hashlib.sha256(s[index:endIndex + 1]).hexdigest()
                print('SHA-256: ' + hash)

                #increment index to continue checking for JPG files
                index = endIndex
                count += 1
                print()
        except ValueError:
            print("End of file")
        print(str(count) + ' JPG files found')
    return count

#recover files with DOCX extension
def DOCXrecover():
    print('\nDOCX Files:\n')
    with open(fileName, 'rb') as f:
        s = f.read()
        index = 0
        count = 0

        try:
            while True:
                #for DOCX files the header is 0x50 4B 03 04 14 00 06 00
                index = s.index(b'\x50\x4B\x03\x04\x14\x00\x06\x00', index)
                if(index % 0x1000 != 0):
                    index += 8
                    continue

                #DOCX has footer of 0x50 4B 05 06 followed by 18 bytes 
                endIndex = s.index(b'\x50\x4B\x05\x06', index) + 21

                writtenFile = open(str(count) + ".docx", "wb")
                writtenFile.write(s[index:endIndex + 1])
                writtenFile.close()
                print('File contents written to ' + str(count) + '.docx')

                #print offset info
                print('Start Offset: ' + hex(index))
                print('End Offset: ' + hex(endIndex))

                #get hash info
                hash = hashlib.sha256(s[index:endIndex + 1]).hexdigest()
                print('SHA-256: ' + hash)

                #increment to keep checking for other DOCX files
                index = endIndex
                count += 1
                print()
        except ValueError:
            print("End of file")
        print(str(count) + ' DOCX file found')
    return count

#recover files with AVI extension
def AVIrecover():
    print('\nAVI Files:\n')
    with open(fileName, 'rb') as f:
        s = f.read()
        index = 0
        count = 0

        try:
            while True:
                #for AVI files the RIFF header is 0x52 49 46 46
                #then the actual AVI header is 0x41 56 49 20 4C 49 53 54
                index = s.index(b'\x52\x49\x46\x46', index)

                if(index + 8 != s.index(b'\x41\x56\x49\x20\x4C\x49\x53\x54', index)):
                    index += 4
                    continue

                if(index % 0x1000 != 0):
                    index += 4
                    continue


                #find the file size
                #which is in spot 4-8 (in little endian)
                sizeAVI = int.from_bytes(s[index + 4:index + 8], 'little')
                endIndex = index + sizeAVI

                writtenFile = open(str(count) + ".avi", "wb")
                writtenFile.write(s[index:endIndex + 1])
                writtenFile.close()
                print('File contents written to ' + str(count) + '.avi')

                #print offset info
                print('Start Offset: ' + hex(index))
                print('End Offset: ' + hex(endIndex))

                #get hash info
                hash = hashlib.sha256(s[index:endIndex + 1]).hexdigest()
                print('SHA-256: ' + hash)

                #increment to keep checking for other AVI files
                index = endIndex
                count += 1
                print()
        except ValueError:
            print("End of file")
        print(str(count) + ' AVI files found')
    return count

#recover files with PNG extension
def PNGrecover():
    print('\nPNG Files:\n')
    with open(fileName, 'rb') as f:
        s = f.read()
        index = 0
        count = 0

        try:
            while True:
                #for PNG files the header is 0x89 50 4E 47 0D 0A 1A 0A
                index = s.index(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', index)
                if(index % 0x1000 != 0):
                    index += 8
                    continue

                #PNG has footer of 0x49 45 4E 44 AE 42 60 82
                endIndex = s.index(b'\x49\x45\x4E\x44\xAE\x42\x60\x82', index) + 7

                writtenFile = open(str(count) + ".png", "wb")
                writtenFile.write(s[index:endIndex + 1])
                writtenFile.close()
                print('File contents written to ' + str(count) + '.png')

                #print offset info
                print('Start Offset: ' + hex(index))
                print('End Offset: ' + hex(endIndex))

                #get hash info
                hash = hashlib.sha256(s[index:endIndex + 1]).hexdigest()
                print('SHA-256: ' + hash)

                #increment to keep checking for other PNG files
                index = endIndex
                count += 1
                print()
        except ValueError:
            print("End of file")
        print(str(count) + ' PNG file found')
    return count

#to find total number of recovered files:

numRecovered = 0
numRecovered += recoverMPG()
numRecovered += recoverPDF()
numRecovered += recoverBMP()
numRecovered += recoverGIF()
numRecovered += JPGrecover()
numRecovered += DOCXrecover()
numRecovered += AVIrecover()
numRecovered += PNGrecover()
print('\nNumber of recovered files: ' + str(numRecovered))