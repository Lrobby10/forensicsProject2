#!/usr/bin/env python3

#sources:
#https://stackoverflow.com/questions/2269827/how-to-convert-an-int-to-a-hex-string
#https://stackoverflow.com/questions/48613002/sha-256-hashing-in-python
# https://stackoverflow.com/questions/24953303/how-to-reverse-an-int-in-python
# https://stackoverflow.com/questions/931092/how-do-i-reverse-a-string-in-python


import sys
import os
import math
import hashlib

try:
    imageFile = sys.argv[1]
    with open(imageFile, 'rb') as disk:
        diskHex = disk.read().hex()
    disk.close()
except FileNotFoundError:
    sys.exit("File Not Found")

def recoverPDF():
    pdfCount = 0
    signatureIndex = 0
    pdfSig = "25504446"
    pdfTrail = "0a2525454f460a", "0a2525454f46", "0d0a2525454f460d0a", "0d25254f4f460d"

    location = 0
    indexList = []
    while location < len(diskHex):
        pdfLocation = diskHex.find(pdfSig, location)
        if pdfLocation % 512 == 0:
            indexList.append(pdfLocation)
        location = pdfLocation + 7
        if location == 6: break
        # print(indexList)

    for i in range (len(indexList)):
        startIndex = indexList[i]
        if indexList[i] == indexList[-1]:
            searchLocation = diskHex[indexList[-1]:]
            print(indexList[-1])
        else: 
            searchLocation = diskHex[indexList[i]:indexList[i+1]]
            print(indexList[i], indexList[i + 1])

        start_offset = int(startIndex / 2)
        # print(searchLocation)
        # lasEof = findLastEof(searchLocation, pdfTrail)
        # print(lasEof)
        end_offset = int(findLastEof(searchLocation, pdfTrail) / 2) + start_offset

        hex_start = hex(start_offset)
        hex_end = hex(end_offset)
        pdfCount += 1
        fileName = fileName = 'PDFfile' + str(pdfCount) + '.pdf'
        print("pdf file found: " + fileName + "\n" + f"start offset: {hex_start}" + "\t" + f"end offset: {hex_end}")
                
        fileRecovery = 'dd if=' + str(sys.argv[1]) + ' of=' + fileName + ' bs=512 skip=' + str(int(start_offset / 512)) + ' count=' + str(math.ceil((end_offset-start_offset) / 512)) + ' 2>error_log.txt &'
        print(fileRecovery)
        os.system(fileRecovery)

        hashCmd = "sha256sum " + fileName
        print("sha256 hash: ")
        # os.system(hashCmd)
        print('\n')

    # while True:
    #     # print("start sig index: " + str(signatureIndex))
    #             pdfCount += 1

    #             start_offset = int(signatureIndex / 2)
    #             end_offset = 0
    #             for trailer in pdfTrail:
    #                 trailerIndex = diskHex.find(trailer, signatureIndex)
    #                 if trailerIndex != -1: 
    #                     end_offset = int((trailerIndex + len(trailer) - 1) / 2)
    #                     break

    #             hex_start = hex(start_offset)
    #             hex_end = hex(end_offset)
    #             fileName = 'PDFfile' + str(pdfCount) + '.pdf'
    #             print("pdf file found: " + fileName + "\n" + f"start offset: {hex_start}" + "\t" + f"end offset: {hex_end}")
                
    #             fileRecovery = 'dd if=' + str(sys.argv[1]) + ' of=' + fileName + ' bs=512 skip=' + str(int(start_offset / 512)) + ' count=' + str(math.ceil((end_offset-start_offset) / 512)) + ' 2>error_log.txt &'
    #             print(fileRecovery)
    #             # os.system(fileRecovery)

    #             hashCmd = "sha256sum " + fileName
    #             print("sha256 hash: ")
    #             # os.system(hashCmd)
    #             print('\n')
    #             signatureIndex = end_offset * 2
    # return 0
    return 0
def recoverMPG():
    mpgCount = 0
    signatureIndex = 0
    mpgSig = "000001b3"
    mpgTrail = "000001b7", "000001b9"
    while True:
        signatureIndex = diskHex.find(mpgSig, signatureIndex)
        # print("start sig index: " + str(signatureIndex))
        if signatureIndex != -1:
            if signatureIndex % 512 == 0:

                mpgCount += 1

                start_offset = int(signatureIndex / 2)
                trailerIndex = diskHex.find(mpgTrail[0], signatureIndex)
                if trailerIndex == -1: trailerIndex = diskHex.find(mpgTrail[1], signatureIndex)
                end_offset = int(((trailerIndex + 7)/ 2))
                hex_start = hex(start_offset)
                hex_end = hex(end_offset)
                fileName = 'MPGfile' + str(mpgCount) + '.mpg'
                print("mpg file found: " + fileName + "\n" + f"start offset: {hex_start}" + "\t" + f"end offset: {hex_end}")
                
                fileRecovery = 'dd if=' + str(sys.argv[1]) + ' of=' + fileName + ' bs=512 skip=' + str(int(start_offset / 512)) + ' count=' + str(math.ceil((end_offset-start_offset) / 512)) + ' 2>error_log.txt &'
                # print(fileRecovery)
                os.system(fileRecovery)

                hashCmd = "sha256sum " + fileName
                print("sha256 hash: ")
                os.system(hashCmd)
                print('\n')
                signatureIndex = end_offset * 2
            else: signatureIndex = signatureIndex + 8
        else: break
    return 0
def recoverBMP():
    bmpCount = 0
    signatureIndex = 0
    bmpSig = "424d"
    while True:
        signatureIndex = diskHex.find(bmpSig, signatureIndex)
        if signatureIndex != -1:
            checkThese = diskHex[(signatureIndex + 12):(signatureIndex + 20)]
            if signatureIndex % 512 == 0 and checkThese == '00000000':

                bmpCount += 1

                # start_offset = int(signatureIndex / 2)
                # leFileSize = diskHex[signatureIndex + 4: signatureIndex + 12]
                beFileSize = getBEfromString(diskHex[signatureIndex:])
                # print('beFileSize: ' + beFileSize)
                # print(type(beFileSize))
                fileSize = int(beFileSize, 16)
                # print('fileSize: ' + f'{fileSize}')

                # print (fileSize)
                start_offset = int(signatureIndex / 2)
                end_offset = int(start_offset + fileSize)
                hex_start = hex(start_offset)
                hex_end = hex(end_offset)
                fileName = 'BMPfile' + str(bmpCount) + '.bmp'
                print("bmp file found: " + fileName + "\n" + f"start offset: {hex_start}" + "\t" + f"end offset: {hex_end}")
                
                fileRecovery = 'dd if=' + str(sys.argv[1]) + ' of=' + fileName + ' bs=512 skip=' + str(int(start_offset / 512)) + ' count=' + str(math.ceil(fileSize / 512)) + ' 2>error_log.txt &'
                # print(fileRecovery)
                os.system(fileRecovery)

                hashCmd = "sha256sum " + fileName
                print("sha256 hash: ")
                os.system(hashCmd)
                print('\n')
                signatureIndex = end_offset * 2
                # print("end sig index: " + str(signatureIndex))
            else: signatureIndex = signatureIndex + 8
        else: break
    return 0
def recoverGIF():
    gifCount = 0
    signatureIndex = 0
    gifSig = "474946383961", "474946383961" 
    gifTrail = "003b0000"
    while True:
        signatureIndex = diskHex.find(gifSig[0], signatureIndex)
        # print(signatureIndex)
        # print("start sig index: " + str(signatureIndex))
        if signatureIndex != -1:
            if signatureIndex % 512 == 0:

                gifCount += 1

                start_offset = int(signatureIndex / 2)
                trailerIndex = diskHex.find(gifTrail, signatureIndex)
                end_offset = int(((trailerIndex + 7)/ 2))
                hex_start = hex(start_offset)
                hex_end = hex(end_offset)
                fileName = 'GIFfile' + str(gifCount) + '.gif'
                print("gif file found: " + fileName + "\n" + f"start offset: {hex_start}" + "\t" + f"end offset: {hex_end}")
                
                fileRecovery = 'dd if=' + str(sys.argv[1]) + ' of=' + fileName + ' bs=512 skip=' + str(int(start_offset / 512)) + ' count=' + str(math.ceil((end_offset-start_offset) / 512)) + ' 2>error_log.txt &'
                # print(fileRecovery)
                os.system(fileRecovery)

                hashCmd = "sha256sum " + fileName
                print("sha256 hash: ")
                os.system(hashCmd)
                print('\n')
                signatureIndex = end_offset * 2
            else: signatureIndex = signatureIndex + 8
        else: break
    while True:
        signatureIndex = diskHex.find(gifSig[1], signatureIndex)
        # print("start sig index: " + str(signatureIndex))
        if signatureIndex != -1:
            if signatureIndex % 512 == 0:

                gifCount += 1

                start_offset = int(signatureIndex / 2)
                trailerIndex = diskHex.find(gifTrail, signatureIndex)
                end_offset = int(((trailerIndex + 7)/ 2))
                hex_start = hex(start_offset)
                hex_end = hex(end_offset)
                fileName = 'GIFfile' + str(gifCount) + '.gif'
                print("gif file found: " + fileName + "\n" + f"start offset: {hex_start}" + "\t" + f"end offset: {hex_end}")
                
                fileRecovery = 'dd if=' + str(sys.argv[1]) + ' of=' + fileName + ' bs=512 skip=' + str(int(start_offset / 512)) + ' count=' + str(math.ceil((end_offset-start_offset) / 512)) + ' 2>error_log.txt &'
                # print(fileRecovery)
                os.system(fileRecovery)

                hashCmd = "sha256sum " + fileName
                print("sha256 hash: ")
                os.system(hashCmd)
                print('\n')
                signatureIndex = end_offset * 2
            else: signatureIndex = signatureIndex + 8
        else: break
    return 0

def getBEfromString(input_string):
    beString = input_string[10:12] + input_string[8:10] + input_string[6:8]+ input_string[4:6]
    return beString

def findLastEof(input_string: str, eofList: list) -> int:
    currentLast = 0
    print('length of string: ' + str(len(input_string)))
    for x in eofList:
        # print(x)
        eofLoc = input_string.find(x)
        print('last eof locatioin: ' + str(eofLoc))
        if eofLoc + len(x) > currentLast: currentLast = eofLoc
    return currentLast + len(x) - 1

if __name__ == "__main__":
    # recoverMPG()
    # recoverBMP()
    # recoverGIF()
    recoverPDF()