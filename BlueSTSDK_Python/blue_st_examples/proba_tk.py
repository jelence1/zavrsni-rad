import tkinter as tk
import sys
import os
import zmq


received = ""

CONTEXT = zmq.Context()
SOCKET = CONTEXT.socket(zmq.REP)
SOCKET.bind("tcp://*:5555")

class Program(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Mikrofon&ja")
        super().__init__(self.root)
        self.grid(rows=10, columns=10, padx=10, pady=10)
        self.createInterface()
        return

    def createInterface(self):
        self.tA=tk.StringVar()
        self.A=tk.Entry(self,textvariable=self.tA)
        self.A.grid(row=1,column=1)
        self.tB=tk.StringVar()
        self.B=tk.Entry(self,textvariable=self.tB)
        self.B.grid(row=2,column=1)
        self.Z=tk.Button(self,text='Zbroji',command=self.zbroji)
        self.Z.grid(row=3,column=1)
        self.tL=tk.StringVar()
        self.tL.set(0)
        self.L=tk.Label(self,textvariable=self.tL)
        self.L.grid(row=4,column=1)
        return

    def zbroji(self):
        try:
            a=int(self.A.get())
            b=int(self.B.get())
            c=a+b
            self.tL.set(c)
        except ValueError:
            self.tL.set('UPISO SI KRIVI ZNAK')
        return


p = Program(tk.Tk())