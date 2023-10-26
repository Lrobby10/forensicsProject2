#Python script for project 2


#Courtney is doing JPG, DOCX, AVI, and PNG
import sys
import os
import hashlib
#import time

#sources
#https://www.w3schools.com/python/ref_func_open.asp
#https://docs.python.org/3/library/hashlib.html



#variables
fileName = sys.argv[1]
imageSize = os.path.getsize(fileName)

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
                if (index % 0x100 != 0):
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
                index = s.index(b'\x50\x4B\x03\x04\x14\x14\x00\x06\x00', index)
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
        print(str(count) + ' DOCX files found')
    return count
