import os
import re
import shutil

from sys import argv
from glob import glob
from threading import Thread
from urllib.request import urlretrieve as download

onlyMerge = len(argv) > 1 and "merge" in argv[1]
downloadsFolder = 'downloads'

if not onlyMerge:
    url = input("Enter URL: ")
    targetTag = "#TSID#"
    url = re.sub(r"seg-\d+-", f"seg-#TSID#-", url)


def main():
    if onlyMerge:
        mergeFiles()
        return True

    restartEnv()
    latestId = findLatestId()
    while len(glob(f"./{downloadsFolder}/*.ts")) < latestId:
        print("Redownloading")
        downloadRest(latestId)
    mergeFiles()
    shutil.rmtree(downloadsFolder)
    print("Done!")


def urlFor(id: int):
    return url.replace("#TSID#", str(id))


def restartEnv():
    os.path.exists(f'./{downloadsFolder}') and shutil.rmtree(downloadsFolder)
    os.path.exists('./merged.ts') and os.remove('./merged.ts')
    os.mkdir(downloadsFolder)


def findLatestId():
    id = 1

    while True:
        try:
            download(urlFor(id), f'./{downloadsFolder}/{id}.ts')
        except:
            break
        id += 50

    while True:
        id -= 1
        fileAddress = f'./{downloadsFolder}/{id}.ts'
        downloadOrPass(urlFor(id), fileAddress)
        if os.path.exists(fileAddress):
            break
    return id


def mergeFiles():
    parts = glob(f"./{downloadsFolder}/*.ts")
    parts.sort(key=lambda x: extractNumber(x))

    with open('./merged.ts', 'wb') as mergedHandler:
        for part in parts:
            with open(part, 'rb') as partHandler:
                shutil.copyfileobj(partHandler, mergedHandler)


def replace(source: str, before: list, after: str):
    for a in before:
        source = source.replace(a, after)
    return source


def extractNumber(target: str):
    return int(re.findall(r"\d+", target)[0])


def downloadedFiles():
    return list(map(extractNumber, glob(f'./{downloadsFolder}/*.ts')))


def downloadRest(biggest: int):
    remaining = diff(list(range(1, biggest + 1)), downloadedFiles())
    threads = []
    for i in remaining:
        print(i)
        fileAddress = f"./downloads/{i}.ts"
        if os.path.exists(fileAddress):
            continue
        threads.append(Thread(target=downloadOrPass,
                       args=(urlFor(i), fileAddress,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=10)


def downloadOrPass(remoteAddress: str, localAddress: str):
    try:
        download(remoteAddress, localAddress)
    except:
        pass


def diff(first: list, second: list):
    second = set(second)
    return [x for x in first if x not in second]


if __name__ == '__main__':
    main()
