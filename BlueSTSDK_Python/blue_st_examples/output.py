import sys
import os

PATH = "output.txt"
oldContent = ""
newContent = ""

while(True):
    with open(PATH, "r") as messages:
        newContent = messages.read()
        if oldContent != newContent:
            print(newContent)
            oldContent = newContent