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

        maxTries = 5
        tries = maxTries
        while tries > 0:
            try:
                if tries < maxTries:
                    print('\n## Retrying... (' + str(tries) +
                          ' attempt(s) remaining)')
                urllib.request.urlretrieve(downloadURL, "download/" + file)
            except:
                tries -= 1
                if tries == 0:
                    os.system("cls")
                    print('Download failed!\n')
                    clearDownloadFolder()
                    downloadJPG()
            else:
                break

        end = time.time()

        os.system("cls")
        print('Downloaded ' + file + ' (' + str(i) +
              '/' + str(numberOfPhotos) + ' images)')
        progress = i/int(numberOfPhotos)*100
        diff = end - start
        estimate = int(diff * float(numberOfPhotos - i))
        print('Progress: '+"{:3.2f}".format(progress) +
              '% (Estimated ' + str(estimate) + 's remaining)')

    print("Done!\n")


def convertToPDF():
    images = glob.glob('download/*.jpg')
    pdf = FPDF()
    title = input("> Title of output file: ")

    print("Converting to pdf...")

    for image in images:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)

    pdf.output("output/" + title + ".pdf", "F")
    print("Done!")


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
