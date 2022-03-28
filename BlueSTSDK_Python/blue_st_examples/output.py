import sys
import os

PATH = "output.txt"
oldContent = ""
newContent = ""

while(True):
    with open(PATH, "r") as messages:
        newContent = messages.read()
        if oldContent != newContent:
            if newContent == "$":
                sys.exit(0)
            print(newContent)
            oldContent = newContent