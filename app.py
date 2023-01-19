import os
import shutil
from random import random
from glob import glob
from threading import Thread
from urllib.request import urlretrieve as download

downloadsFolder = 'downloads'
downloadedParts = []
foundedNumbers = []

url = f"https://cfvod.kaltura.com/scf/hls/p/2203921/sp/220392100/serveFlavor/entryId/1_mz8otpis/v/1/ev/3/flavorId/1_eq39gahj/name/a.mp4/seg-#TSID#-v1-a1.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMjIwMzkyMS9zcC8yMjAzOTIxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8xX216OG90cGlzL3YvMS9ldi8zL2ZsYXZvcklkLzFfZXEzOWdhaGovbmFtZS9hLm1wNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjc0MjMyNzAxfX19XX0_&Signature=DnvzkO5rfglBHFJbotUn2fpaprruRhWyv4xqUZRnZDPD~9d2GEx9gKE78sFIcZprxr-HVa4hR3N0ehLs2GUwnYdzA~goQutTN5zy-zf5WG7ugjkmQaZNKNaotO5lAK-YHtCCXsx1Str9zQCWBUXaik4MqT2MFwH3sUlgPoYFfaN53AL0yYDyMkO7gQXEEBDiAdnTlYMALUmMvxrMxq7iiWrc70BGVhXgnTIPKb50SqubVvufCTZ8UMAbtVQN0x5s2WB4mV-eD0plGL7-fnL3ulHY6JcIGlNRhP3hgTeYTJn28vl04HI3pT6Zv5QgZEw5Lzcy4Z6oNGHS78eREJzUWw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"


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
