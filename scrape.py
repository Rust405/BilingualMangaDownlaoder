import requests
import urllib.request
import os
import glob
import time
from fpdf import FPDF
from bs4 import BeautifulSoup


def makeDirectories():
    if not os.path.exists('download'):
        os.makedirs('download')
    if not os.path.exists('output'):
        os.makedirs('output')


def clearDownloadFolder():
    trash = glob.glob('download/*')
    for t in trash:
        os.remove(t)


def downloadImg():
    url = input("Link to manga volume: ")

    sauce = requests.get(url)
    soup = BeautifulSoup(sauce.content, 'html.parser')

    elements = soup.findAll('img', attrs={
                            'class': 'wp-manga-chapter-img img-responsive lazyload effect-fade'})

    urlList = []
    for element in elements:
        urlList.append(element['data-src'])

    for i in range(1, len(urlList)+1):

        start = time.time()

        maxTries = 5
        tries = maxTries
        while tries > 0:
            try:
                srcURL = urlList[i-1].strip()

                if tries < maxTries:
                    print('\n## Retrying... (' + str(tries - 1) +
                          ' attempt(s) remaining)')
                urllib.request.urlretrieve(
                    srcURL, "download/" + str(i) + '.jpg')
            except:
                tries -= 1
                time.sleep(1)
            else:
                break
        if tries == 0:
            os.system("cls")
            print('Download failed! Server down/Check your connection.\n')
            clearDownloadFolder()
            downloadImg()

        end = time.time()

        diff = end - start
        progress = i/len(urlList)*100
        estimate = int(diff * float(len(urlList) - i))

        os.system("cls")
        print('Downloaded (' + str(i) + '/' + str(len(urlList)) + ')')
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


os.system("cls")
makeDirectories()
clearDownloadFolder()
downloadImg()
convertToPDF()
clearDownloadFolder()
