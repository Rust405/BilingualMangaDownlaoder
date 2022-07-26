import urllib.request
import os
import glob
import time
from fpdf import FPDF


class Modifier:
    def __init__(self, startOfPhoto, startWZero, URLWOFile, startingFileNumber, leadingP, leadingZeroes, fileType, fileTypeLen):
        self.startOfPhoto = startOfPhoto
        self.startWZero = startWZero
        self.URLWOFile = URLWOFile
        self.startingFileNumber = startingFileNumber
        self.leadingP = leadingP
        self.leadingZeroes = leadingZeroes
        self.fileType = fileType
        self.fileTypeLen = fileTypeLen


def makeDirectories():
    if not os.path.exists('download'):
        os.makedirs('download')
    if not os.path.exists('output'):
        os.makedirs('output')


def downloadImg():
    lastImgURL = input("> Image URL of last image: ")

    if lastImgURL[-11] == '/':
        # P00001.jpg
        mod = Modifier(-9, 0, -10, 1, 'P', 5, '.jpg', -4)
    elif lastImgURL[-8] == '/':
        # 000.jpg
        mod = Modifier(-7, 1, -7, 0, '', 3, '.jpg', -4)
    elif lastImgURL[-9] == '/':
        # 000.jpeg
        mod = Modifier(-8, 1, -8, 0, '', 3, '.jpeg', -5)

    lastPhotoNumber = lastImgURL[mod.startOfPhoto:mod.fileTypeLen]
    numberOfPhotos = int(lastPhotoNumber) + mod.startWZero
    imgFolderURL = lastImgURL[:mod.URLWOFile]

    for i in range(mod.startingFileNumber, int(numberOfPhotos) + mod.startingFileNumber):
        fileName = mod.leadingP + \
            str(i).zfill(mod.leadingZeroes) + mod.fileType
        downloadURL = imgFolderURL + fileName

        start = time.time()

        maxTries = 5
        tries = maxTries
        while tries > 0:
            try:
                if tries < maxTries:
                    print('\n## Retrying... (' + str(tries - 1) +
                          ' attempt(s) remaining)')
                urllib.request.urlretrieve(downloadURL, "download/" + fileName)
            except:
                tries -= 1
                if tries == 0:
                    os.system("cls")
                    print('Download failed! Server down/Check your connection.\n')
                    clearDownloadFolder()
                    downloadImg()
                time.sleep(1)
            else:
                break

        end = time.time()

        os.system("cls")
        print('Downloaded ' + fileName + ' (' + str(i + mod.startWZero) +
              '/' + str(numberOfPhotos) + ' images)')
        progress = (i + mod.startWZero)/int(numberOfPhotos)*100
        diff = end - start
        estimate = int(diff * float(numberOfPhotos - i + mod.startWZero))
        print('Progress: '+"{:3.2f}".format(progress) +
              '% (Estimated ' + str(estimate) + 's remaining)')

    print("Done!\n")


def convertToPDF():
    images = glob.glob('download/*')
    pdf = FPDF()
    title = input("> Title of output file: ")

    print("Converting to pdf...")

    for image in images:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)

    pdf.output("output/" + title + ".pdf", "F")
    print("Done!\n")


def clearDownloadFolder():
    trash = glob.glob('download/*')
    for t in trash:
        os.remove(t)


os.system("cls")
makeDirectories()
clearDownloadFolder()
downloadImg()
convertToPDF()
clearDownloadFolder()
