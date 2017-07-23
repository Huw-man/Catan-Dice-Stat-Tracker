#attempt at catan dice roller
#@author Hu.man

import tkinter as tk
import random
from gtts import gTTS
import os
from threading import Thread

class DiceRoller(tk.Frame):
    print("DiceRoller")
    def __init__(self, parent, turnOrder, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.rollNum = tk.StringVar()
        self.rollNum.set("Roll")
        self.turnOrder = turnOrder
        self.turn = tk.StringVar()#number
        self.turnCount = 1
        print(turnOrder)

        self.rollButton = tk.Button(self, textvariable=self.rollNum, font=('Ariel', 100), bg='black',
            activebackground='gray20', activeforeground='white', fg='white', width=4,
            command=self.roll)
        self.rollButton.grid(row=1, column=0)

        #tn1 = self.trackTurn()
        self.turn.set(self.turnOrder[1][1]+ " turn")
        self.turnLabel = tk.Label(self, textvariable=self.turn, bg=self.turnOrder[1][1] ,font=('Sans', 30), width=13, height=4)
        self.turnLabel.grid(row=0, column=0)

        self.audioToggle = tk.IntVar() #1=on 0=off
        self.audio = tk.Checkbutton(self, variable = self.audioToggle, text="Audio", font=("Sans", 14, 'bold'))
        self.audio.grid()

        #create a barGraph
        self.barGraph = BarGraph(self)

    def roll(self):
        self.rollNum.set(random.randint(1,6)+random.randint(1,6))
        tn = self.trackTurn()
        self.barGraph.drawGraph(int(self.rollNum.get()), tn[1])
        if tn[1] == 'royal blue' :
            self.turn.set('blue turn')
        else:
            self.turn.set(tn[1]+" turn")
        self.turnLabel.configure(bg=tn[1])
        #audio text to speech
        tts= gTTS(text=self.rollNum.get(), lang='en')
        tts.save("number2.mp3")
        audioThread = Thread(target=self.enableAudio())
        audioThread.start()
        audioThread.join()

    def enableAudio(self):
        if self.audioToggle.get() == 1:
            os.system("number2.mp3")

    def trackTurn(self): #returns the current turn. called every roll to keep track
        for k in self.turnOrder:
            if self.turnOrder[k][0] == self.turnCount:
                self.turnCount +=1
                return [self.turnOrder[k][0], self.turnOrder[k][1]] #number, color
        self.turnCount = 2
        return [self.turnOrder[1][0], self.turnOrder[1][1]]

class BarGraph:
    print("barGraph")
    def __init__(self, parent):
        self.width = 800
        self.height = 600
        self.parent = parent
        #Canvas for barGraph
        self.graph = tk.Canvas(parent, width= self.width, height = self.height, bg='light gray')
        self.graph.grid(row=0, column=1, rowspan=2)

        labelGap = self.width/11 -7 #scales placement of labels and graphs according to canvas
        #each dictionary key holds an array containing the number, start position of the bar, rolltimes
        self.labels = {2:[labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            3:[2*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            4:[3*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            5:[4*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            6:[5*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            7:[6*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            8:[7*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            9:[8*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            10:[ 9*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            11:[ 10*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}],
            12:[ 11*labelGap, {'red': 0, 'royal blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}]}
        self.drawLabels(self.graph)
        self.drawBars(self.graph)

    def drawGraph(self, entry, player): #update graph
        #print(str(entry) + " "+player)
        self.labels[entry][1][player] +=1
        #print(self.labels)
        self.graph.destroy()
        newGraph = tk.Canvas(self.parent, width= self.width, height = self.height, bg='light gray')
        self.drawLabels(newGraph)
        self.drawBars(newGraph)
        self.totalRolls(newGraph)
        self.graph = newGraph
        #self.graph.update()
        self.graph.grid(row=0, column=1, rowspan=2)

    def drawLabels(self, canvas):
        for i in self.labels: #write labels
            canvas.create_text(self.labels[i][0], self.height-30, anchor='nw', text=i, font=("Times", 25, "bold"))

    def drawBars(self, canvas): #draw bars on graph
        minHeight = self.height-30
        fullHeight = minHeight - 30
        if self.findMaxRolls()==0:
            segmentHeight =0
        else:
            segmentHeight = fullHeight/self.findMaxRolls()
            for c in self.labels:
                tmin = minHeight
                for d in self.labels[c][1]:
                    #print(d + str(self.labels[c][1][d]))
                    if self.labels[c][1][d] != 0:
                        tmax = tmin - (self.labels[c][1][d]*segmentHeight)
                        canvas.create_rectangle(self.labels[c][0] -7, tmax, self.labels[c][0] +27, tmin, fill=d)
                        canvas.create_text(self.labels[c][0]+7, (tmin-tmax)/2+tmax, text=self.labels[c][1][d]) #rolls per color
                        tmin = tmax
                #labels indicating how many rolls
                rollsPer = self.rollsPerNumber(c)
                canvas.create_text(self.labels[c][0]+3, minHeight-(rollsPer*segmentHeight)-20, anchor='nw', text=rollsPer, font=("Times", 16, 'bold'))


    def totalRolls(self, canvas):
        total=0
        for x in self.labels:
            total+= self.rollsPerNumber(x)
        canvas.create_text(self.width*.87, self.height*.03, anchor='nw', text="Total: "+str(total), font=('Comic Sans', 14))

    def findMaxRolls(self): #finds maximum rolls of one number
        sumOfRolls = {} #holds list of rolls of each number
        for r in self.labels:
            sumOfRolls[r] = self.rollsPerNumber(r)
        maxRolls = 0
        for a in sumOfRolls:
            if sumOfRolls[a] > maxRolls :
                maxRolls = sumOfRolls[a]
        return maxRolls

    def rollsPerNumber(self, num):
        sumR = 0
        for p in self.labels[num][1]:
            sumR += self.labels[num][1][p]
        return sumR


class SetupGame(tk.Frame):
    print("setup")
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.titleLabel = tk.Label(self, text = "Best Catan Dice Roller", font=('Times', 50))
        self.titleLabel.grid(row=0, columnspan=6)

        self.info = tk.Label(self, text ="select turn order", font=('Times', 20))
        self.info.grid(row=1, columnspan=6)

        self.resetOrder = tk.Button(self, text='reset turns', font=('Times', 25), command=self.resetTurns)
        self.resetOrder.grid(row=3, column=0, columnspan=2)

        self.play = tk.Button(self, text='Play', font=('Sans', 25), command=self.play)
        self.play.grid(row=3, column=2, columnspan=2)

        self.orderNum = {'red': tk.IntVar(), 'royal blue':tk.IntVar(), 'white':tk.IntVar(), 'orange':tk.IntVar(), 'green':tk.IntVar(), 'brown':tk.IntVar()}

        self.red = tk.Button(self, bg='red', width=5, height=2, textvariable=self.orderNum['red'], font=('Times', 20, 'bold'), command=lambda: self.order('red'))
        self.red.grid(row=2, column=0)
        self.blue = tk.Button(self, bg='royal blue', width=5, height=2, textvariable=self.orderNum['royal blue'], font=('Times', 20, 'bold'), command=lambda: self.order('royal blue'))
        self.blue.grid(row=2, column=1)
        self.white = tk.Button(self, bg='white', width=5, height=2, textvariable=self.orderNum['white'], font=('Times', 20, 'bold'), command=lambda: self.order('white'))
        self.white.grid(row=2, column=2)
        self.orange = tk.Button(self, bg='orange', width=5, height=2, textvariable=self.orderNum['orange'], font=('Times', 20, 'bold'), command=lambda: self.order('orange'))
        self.orange.grid(row=2, column=3)
        self.green = tk.Button(self, bg='green', width=5, height=2, textvariable=self.orderNum['green'], font=('Times', 20, 'bold'), command=lambda: self.order('green'))
        self.green.grid(row=2, column=4)
        self.brown = tk.Button(self, bg='brown', width=5, height=2, textvariable=self.orderNum['brown'], font=('Times', 20, 'bold'), command=lambda: self.order('brown'))
        self.brown.grid(row=2, column=5)

    def order(self, color): #sets the order
        self.orderNum[color].set(self.findNextTurn(self.orderNum)+1)

    def resetTurns(self): #resets the turns
        for i in self.orderNum:
            self.orderNum[i].set(0)

    def play(self): #changes to mainFrame
        print("play")
        self.grid_forget()
        DiceRoller(self.parent, self.convertToArray(self.orderNum), bg='gray20').grid()

    def convertToArray(self, Tlist):
        t={}
        for (key, value) in Tlist.items():
            t[value.get()] = [value.get(), key] #number, color
        return t

    def findNextTurn(self, orderList):
        max = 0
        for a in orderList:
            if orderList[a].get() > max :
                max = orderList[a].get()
        return max


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        print("mainApp")
        setup = SetupGame(self, bg='gray20').grid()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Catan Dice Roller")
    print("mainMethod")
    MainApplication(root, bg='gray20').grid()
    root.mainloop()
