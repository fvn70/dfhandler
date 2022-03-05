import hashlib
import os
import re
import sys
from os.path import splitext, getsize

args = sys.argv
rev = False


def ask(q, yes='yes', no='no'):
    while True:
        cmd = input(f"\n{q}\n").lower()
        if cmd not in (yes, no):
            print("Wrong option")
        else:
            return cmd == yes


if len(args) < 2:
    print("Directory is not specified")
else:
    ext = input("Enter file format:\n")
    print("Size sorting options:\n1. Descending\n2. Ascending\n")

    rev = ask("Enter a sorting option:\n", '1', '2')

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

    if ask("Check for duplicates?"):
        h_dic = {}
        for size in dic:
            for fn in dic[size]:
                with open(fn, 'rb') as file:
                    data = file.read()
                    h = hashlib.md5(data)
                    h = h.hexdigest()
                    h_dic.setdefault(size, {}).setdefault(h, []).append(fn)

        h_dic = {size: {h: [fn for fn in h_dic[size][h]] for h in h_dic[size] if len(h_dic[size][h]) > 1}
                 for size in h_dic}

        n = 0
        for size in sorted(h_dic, reverse=rev):
            if len(h_dic[size]) > 0:
                print(f"\n{size} bytes")
                for h in h_dic[size]:
                    print(f"Hash: {h}")
                    for fn in h_dic[size][h]:
                        n += 1
                        print(f"{n}. {fn}")

        if ask("Delete files?"):
            while True:
                lst = input("Enter file numbers to delete:\n")
                if lst and re.match('[0-9]+\\s?', lst) and lst[-1] <= str(n):
                    break
                else:
                    print("Wrong format")
            n = 0
            space = 0
            for size in sorted(h_dic, reverse=rev):
                for h in h_dic[size]:
                    for fn in h_dic[size][h]:
                        n += 1
                        if str(n) in lst.split():
                            space += getsize(fn)
                            os.remove(fn)
            print(f"Total freed up space: {space} bytes")
