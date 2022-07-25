import urllib.request
import os
import glob
import time
from fpdf import FPDF

numberOfPhotos = 0


def makeDirectories():
    if not os.path.exists('download'):
        os.makedirs('download')
    if not os.path.exists('output'):
        os.makedirs('output')


def downloadJPG():
    lastImgURL = input("> Image URL of last image: ")
    lastPhotoNumber = lastImgURL[-9:-4]
    global numberOfPhotos
    numberOfPhotos = int(lastPhotoNumber)
    imgURL = lastImgURL[:-10]

    for i in range(1, int(numberOfPhotos) + 1):
        file = 'P' + str(i).zfill(5) + '.jpg'
        downloadURL = imgURL + file

        start = time.time()
        urllib.request.urlretrieve(downloadURL, "download/" + file)
        end = time.time()

        os.system("cls")
        print('Downloaded ' + file)
        progress = i/int(numberOfPhotos)*100
        diff = end - start
        estimate = int(diff * float(numberOfPhotos - i))
        print('Progress: '+"{:3.2f}".format(progress) +
              '% (Estimated ' + str(estimate) + 's remaining)')

    print("Done!\n")


def convertToPDF():
    images = glob.glob('download/*.jpg')
    i = 1
    pdf = FPDF()
    global numberOfPhotos

    title = input("> Title of output file: ")

    for image in images:
        start = time.time()
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)
        end = time.time()

        os.system("cls")
        print("Converting to pdf...")

        progress = i/int(numberOfPhotos)*100
        diff = end - start
        estimate = int(diff * float(numberOfPhotos - i))
        print('Progress: '+"{:3.2f}".format(progress) +
              '% (Estimated ' + str(estimate) + 's remaining)')
        i += 1

    pdf.output("output/" + title + ".pdf", "F")
    print("Done!\n")


def clearDownloadFolder():
    trash = glob.glob('download/*')
    for t in trash:
        os.remove(t)


os.system("cls")
makeDirectories()
clearDownloadFolder()
downloadJPG()
convertToPDF()
clearDownloadFolder()
