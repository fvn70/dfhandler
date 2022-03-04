import os
import sys
from os.path import splitext, getsize

args = sys.argv
rev = False

if len(args) < 2:
    print("Directory is not specified")
else:
    ext = input("Enter file format:\n")
    print("Size sorting options:\n1. Descending\n2. Ascending\n")

    while True:
        n = input("Enter a sorting option:\n")
        if n in ("1", "2"):
            rev = n == "1"
            break
        else:
            print("Wrong option")

    dic = {}
    for root, dirs, files in os.walk(args[1]):
        for name in files:
            ex = splitext(name)[1]
            if ext and ex != '.' + ext:
                continue
            fn = os.path.join(root, name)
            size = getsize(fn)
            dic.setdefault(size, []).append(fn)

    for size in sorted(dic, reverse=rev):
        print(f"\n{size} bytes")
        print(*dic[size], sep='\n')
