#attempt at catan dice roller
#@author Hu.man

import tkinter as tk
import random

class DiceRoller:
    print("DiceRoller")
    def __init__(self, parent):
        self.parent = parent
        self.rollNum = tk.StringVar()
        self.turn = tk.StringVar()
        self.rollNum.set("Roll")

        self.rollButton = tk.Button(parent, textvariable=self.rollNum, font=('Ariel', 100), bg='black',
            activebackground='gray20', activeforeground='white', fg='white', width=4,
            command=self.roll)
        self.rollButton.grid(row=1, column=0)
        self.turn = tk.Label(parent, textvariable=self.turn)
        self.turn.grid(row=0, column=0)
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
        self.graph.grid(row=0, column=1, rowspan=2)
        #each dictionary key holds an array containing the number, start position of the bar, roll times, and bar rectangle
        labelGap = 50
        self.labels = {2:['2', 30, 0], 3:['3', labelGap+30, 0], 4:['4', 2*labelGap+30, 0],
            5:['5', 3*labelGap+30, 0], 6:['6', 4*labelGap+30, 0], 7:['7', 5*labelGap+30, 0],
            8:['8', 6*labelGap+30, 0], 9:['9', 7*labelGap+30, 0], 10:['10', 8*labelGap+30, 0],
            11:['11', 9*labelGap+30, 0], 12:['12', 10*labelGap+30, 0]}
        self.drawLabels(self.graph)

    def drawGraph(self, entry): #update graph
        print("drawGraph")
        self.labels[entry][2] +=1
        self.graph.destroy()
        newGraph = tk.Canvas(self.parent, width= self.width, height = self.height, bg='light gray')
        self.drawLabels(newGraph)
        self.drawBars(newGraph)
        self.graph = newGraph
        #self.graph.update()
        self.graph.grid(row=0, column=1, rowspan=2)

    def drawLabels(self, canvas):
        for i in self.labels: #write labels
            canvas.create_text(self.labels[i][1], self.height-30, anchor='nw', text=self.labels[i][0], font=("Times", 20, "bold"))

    def drawBars(self, canvas): #draw bars on graph
        minHeight = self.height-30
        fullHeight = minHeight - 30
        if self.findMaxRolls()!=0:
            segmentHeight = fullHeight/self.findMaxRolls()
        for c in self.labels:
            canvas.create_rectangle(self.labels[c][1] -5, minHeight-(self.labels[c][2]*segmentHeight),
                self.labels[c][1] +20, minHeight, fill='blue')
            #labels indicating how many rolls
            if self.labels[c][2] != 0:
                canvas.create_text(self.labels[c][1] +3, minHeight-(self.labels[c][2]*segmentHeight), anchor='nw', fill='white', text=self.labels[c][2], font=("Times", 14))
            else:
                canvas.create_text(self.labels[c][1] +3, minHeight-(self.labels[c][2]*segmentHeight) -20, anchor='nw', fill='white', text=self.labels[c][2], font=("Times", 14))

    def findMaxRolls(self):
        max = 0
        for a in self.labels:
            if self.labels[a][2] > max :
                max = self.labels[a][2]
        return max

class SetupGame:
    def __init__(self, parent):
        self.parent = parent
        self.titleLabel = tk.Label(parent, text = "Best Catan Dice Roller", font=('Times', 50))
        self.titleLabel.grid(row=0, columnspan=6)

        self.info = tk.Label(parent, text ="select turn order", font=('Times', 20))
        self.info.grid(row=1, columnspan=6)

        self.resetOrder = tk.Button(parent, text='reset turns', font=('Times', 25), command=self.resetTurns)
        self.resetOrder.grid(row=3, column=0, columnspan=2)

        self.play = tk.Button(parent, text='Play', font=('Sans', 25))
        self.play.grid(row=3, column=2, columnspan=2)

        self.orderNum = {'red': tk.IntVar(), 'blue':tk.IntVar(), 'white':tk.IntVar(), 'orange':tk.IntVar(), 'green':tk.IntVar(), 'brown':tk.IntVar()}

        self.red = tk.Button(parent, bg='red', width=5, height=2, textvariable=self.orderNum['red'], font=('Times', 20, 'bold'), command=lambda: self.order('red'))
        self.red.grid(row=2, column=0)
        self.blue = tk.Button(parent, bg='royal blue', width=5, height=2, textvariable=self.orderNum['blue'], font=('Times', 20, 'bold'), command=lambda: self.order('blue'))
        self.blue.grid(row=2, column=1)
        self.white = tk.Button(parent, bg='white', width=5, height=2, textvariable=self.orderNum['white'], font=('Times', 20, 'bold'), command=lambda: self.order('white'))
        self.white.grid(row=2, column=2)
        self.orange = tk.Button(parent, bg='orange', width=5, height=2, textvariable=self.orderNum['orange'], font=('Times', 20, 'bold'), command=lambda: self.order('orange'))
        self.orange.grid(row=2, column=3)
        self.green = tk.Button(parent, bg='green', width=5, height=2, textvariable=self.orderNum['green'], font=('Times', 20, 'bold'), command=lambda: self.order('green'))
        self.green.grid(row=2, column=4)
        self.brown = tk.Button(parent, bg='brown', width=5, height=2, textvariable=self.orderNum['brown'], font=('Times', 20, 'bold'), command=lambda: self.order('brown'))
        self.brown.grid(row=2, column=5)

    def order(self, color): #sets the order
        self.orderNum[color].set(self.findNextTurn()+1)

    def resetTurns(self): #resets the turns
        for i in self.orderNum:
            self.orderNum[i].set(0)

    #def play(self): #changes to mainFrame

    def findNextTurn(self):
        max = 0
        for a in self.orderNum:
            if self.orderNum[a].get() > max :
                max = self.orderNum[a].get()
        return max


# class MainApplication(tk.Frame):
#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         self.parent = parent
#         self.diceRoller = DiceRoller(self.parent)
#         print("mainApp")
#         #self.barGraph.drawGraph(self.diceRoller.getRollNum())

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Catan Dice Roller")
    menuFrame = tk.Frame(root, bg='dark gray', width =500, height=500 )
    mainFrame = tk.Frame(root, bg='dark gray')

    SetupGame(menuFrame)
    DiceRoller(mainFrame)
    print("mainMethod")
    menuFrame.grid()
    mainFrame.grid()
    root.mainloop()
