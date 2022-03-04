import os
import sys

args = sys.argv
if len(args) < 2:
    print("Directory is not specified")
else:
    dic = {}
    for root, dirs, files in os.walk(args[1]):
        for name in files:
            print(os.path.join(root, name))
