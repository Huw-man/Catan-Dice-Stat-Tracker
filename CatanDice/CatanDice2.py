#attempt at catan dice roller
#@author Hu.man

import tkinter as tk
import random

class DiceRoller:
    print("DiceRoller")
    def __init__(self, parent):
        self.parent = parent
        self.rollNum = tk.StringVar()
        self.rollNum.set("Roll")

        self.rollButton = tk.Button(parent, textvariable=self.rollNum, font=('Ariel', 100), bg='black',
            activebackground='dark gray', activeforeground='white', fg='white', width=4,
            command=self.roll)
        self.rollButton.grid(row=0, column=0)
        #create a barGraph
        self.barGraph = BarGraph(self.parent)

    def roll(self):
        self.rollNum.set(random.randint(1,6)+random.randint(1,6))
        self.barGraph.drawGraph(int(self.rollNum.get()))

class BarGraph:
    print("barGraph")
    def __init__(self, parent):
        self.width = 600
        self.height = 500
        self.parent = parent
        #Canvas for barGraph
        self.graph = tk.Canvas(parent, width= self.width, height = self.height, bg='light gray')
        self.graph.grid(row=0, column=1)
        #each dictionary key holds an array containing the number, start position of the bar, roll times, and bar rectangle
        labelGap = 50
        self.labels = {2:['2', 30, 0, 1], 3:['3', labelGap+30, 0, 1], 4:['4', 2*labelGap+30, 0, 1],
            5:['5', 3*labelGap+30, 0, 1], 6:['6', 4*labelGap+30, 0, 1], 7:['7', 5*labelGap+30, 0, 1],
            8:['8', 6*labelGap+30, 0, 1], 9:['9', 7*labelGap+30, 0, 1], 10:['10', 8*labelGap+30, 0, 1],
            11:['11', 9*labelGap+30, 0, 1], 12:['12', 10*labelGap+30, 0, 1]}
        self.drawLabels()

    def drawLabels(self):
        for i in self.labels:     #write labels
            self.graph.create_text(self.labels[i][1], self.height-30, anchor='nw', text=self.labels[i][0], font=("Times", 20, "bold"))

    def drawGraph(self, entry): #update and draw graph
        print("drawGraph")
        minHeight = self.height-30
        fullHeight = minHeight - 30
        self.labels[entry][2] += 1
        if self.findMaxRolls()!=0:
            segmentHeight = fullHeight/self.findMaxRolls()
        else:
            segmentHeight=0
        print ("segment"+str(self.labels[entry][2]*segmentHeight))
        self.graph.create_rectangle(self.labels[entry][1] -5, minHeight-(self.labels[entry][2]*segmentHeight),
            self.labels[entry][1] +20, minHeight, fill='blue')
        self.graph.update()

    def findMaxRolls(self):
        max = 0
        for a in self.labels:
            if self.labels[a][2] > max :
                max = self.labels[a][2]
        return max

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.diceRoller = DiceRoller(self.parent)
        print("mainApp")
        #self.barGraph.drawGraph(self.diceRoller.getRollNum())

root = tk.Tk()
root.title("Catan Dice Roller")
MainApplication(root).grid()
print("mainMethod")
root.mainloop()
