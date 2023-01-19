import os
import shutil
import re

from glob import glob
from threading import Thread
from urllib.request import urlretrieve as download

downloadsFolder = 'downloads'
downloadedParts = []

url = input("Enter URL: ")
targetTag = "#TSID#"
url = re.sub(r"seg-\d+-", f"seg-#TSID#-", url)


def main():
    if not os.path.exists(f'./{downloadsFolder}'):
        os.mkdir(downloadsFolder)

    latestId = findLatestId()
    downloadRest(latestId)
    mergeFiles()
    os.rmdir(downloadsFolder)
    print("Done!")


def urlFor(id: int):
    return url.replace("#TSID#", str(id))


def findLatestId():
    id = 1

    while True:
        try:
            download(urlFor(id), f'./{downloadsFolder}/{id}.ts')
        except:
            break
        downloadedParts.append(id)
        id += 50

    while True:
        id -= 1
        fileAddress = f'./{downloadsFolder}/{id}.ts'
        try:
            download(urlFor(id), fileAddress)
        except:
            pass
        if os.path.exists(fileAddress):
            break
    return id


def mergeFiles():
    parts = glob(f"./{downloadsFolder}/*.ts")
    parts.sort(key=lambda x: int(
        replace(x, ['.', '/', 'downloads', 'ts'], '')))

    with open('./merged.ts', 'wb') as mergedHandler:
        for part in parts:
            with open(part, 'rb') as partHandler:
                shutil.copyfileobj(partHandler, mergedHandler)


def replace(source: str, before: list, after: str):
    for a in before:
        source = source.replace(a, after)
    return source


def downloadRest(biggest: int):
    remaining = diff(list(range(1, biggest + 1)), downloadedParts)
    threads = []
    for i in remaining:
        print(i)
        threads.append(Thread(target=download, args=(
            urlFor(i), f"./downloads/{i}.ts",)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def diff(first: list, second: list):
    second = set(second)
    return [x for x in first if x not in second]


if __name__ == '__main__':
    main()
