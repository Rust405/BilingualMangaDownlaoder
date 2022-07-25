import urllib.request
import os
import glob
import time
from fpdf import FPDF


def makeDirectories():
    if not os.path.exists('download'):
        os.makedirs('download')
    if not os.path.exists('output'):
        os.makedirs('output')


def downloadJPG():
    lastImgURL = input("> Image URL of last image: ")
    lastPhotoNumber = lastImgURL[-9:-4]
    numberOfPhotos = int(lastPhotoNumber)
    imgURL = lastImgURL[:-10]

    for i in range(1, int(numberOfPhotos) + 1):

        file = 'P' + str(i).zfill(5) + '.jpg'
        downloadURL = imgURL + file

        start = time.time()
        urllib.request.urlretrieve(downloadURL, "download/" + file)
        end = time.time()

        os.system("cls")
        print('Downloading ' + file + '...')
        progress = i/int(numberOfPhotos)*100
        print('Download Progress: ' + "{:6.2f}".format(progress) + '%')

        diff = end - start
        estimate = int(diff * float(numberOfPhotos) - i)
        print('Estimated time remaining: ' + str(estimate) + ' seconds')

    print("Done!\n")


def convertToPDF():
    title = input("> Title of output file: ")

    print("\nConverting to pdf...")
    images = glob.glob('download/*.jpg')

    pdf = FPDF()
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
downloadJPG()
convertToPDF()
clearDownloadFolder()
