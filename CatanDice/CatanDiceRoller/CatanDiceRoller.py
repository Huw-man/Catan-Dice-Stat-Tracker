#attempt at catan dice roller
#@author Hu.man
import tkinter as tk
from tkinter import messagebox
import random
from gtts import gTTS
import playsound
import sys
import os

class DiceRoller(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.configure(bg = MainApp.BG_COLOR)
        self.rollNum = tk.StringVar()
        self.turnOrder = {} #initialized empty, to be filled when turns are set
        self.turn = tk.StringVar()#number
        self.turnCount = 1
        self.parent = parent
        self.barGraph = BarGraph(self) #creat BarGraph object

        self.rollButton = tk.Button(self, text='Roll', font=('Ariel', 100), bg='black',
            activebackground='dark gray', activeforeground='white', fg='white', width=4,
            command=self.roll)
        self.rollButton.bind('<space>', self.roll_a)
        self.rollButton.grid(row=4, column=0, padx=10, pady=10)

        self.turn.set("Start")
        self.turnLabel = tk.Label(self, textvariable=self.turn, bg='snow' ,font=('Sans', 35, 'bold'), width=10, height=3)
        self.turnLabel.grid(row=2, column=0, padx=10, pady=10)

        self.nextTurn = tk.Label(self, text='', bg='snow' ,font=('Sans', 20), width=13, height=1)
        self.nextTurn.grid(row=3, column=0, sticky='n')

        self.prevTurn = tk.Label(self, text='', bg='snow' ,font=('Sans', 20), width=13, height=1)
        self.prevTurn.grid(row=1, column=0, sticky='s')

        back = tk.Button(self, text='<<<', bg='black', fg='white', font=("Sans", 14, 'bold'), command= lambda: controller.show_frame(Setup))
        back.grid(row=0, column=0, sticky='w')

        self.audioToggle = tk.IntVar() #1=on 0=off
        audio = tk.Checkbutton(self, variable = self.audioToggle, bg='black', fg='white', activebackground=MainApp.BG_COLOR, activeforeground='white',
            selectcolor='red', text="Audio", font=("Sans", 14, 'bold'))
        audio.grid(row=0, column=2, sticky='e')

        statReset = tk.Button(self, text="reset stats", bg='black', fg='white', font=("Sans", 14, 'bold'), command=self.reset_stats)
        statReset.grid(row=0, column=1, sticky='e')

    def reset_stats(self):
        if messagebox.askyesno("reset Statistics?", "Are you sure you want to reset the roll statistics?"):
            self.barGraph.clearStatInfo()

    def roll_a(self, event): #handles keypress
        self.roll()
        return "break"

    def roll(self):
        dice1 = random.SystemRandom().randint(1,6)
        dice2 = random.SystemRandom().randint(1,6)
        self.rollNum.set(dice1 + dice2) #uses SystemRandom to produce better results
        self.rollButton.configure(text= str(dice1)+ "+" +str(dice2))
        tn = self.trackTurn()
        self.barGraph.drawGraph(int(self.rollNum.get()), tn[1])
        self.turn.set(str(tn[1])+" turn")
        self.turnLabel.configure(bg=tn[2])
        try:
            self.nextTurn.configure(text="next "+self.turnOrder[tn[0]+1]['player'], bg=self.turnOrder[tn[0]+1]['color'])
        except:
            self.nextTurn.configure(text="next "+self.turnOrder[1]['player'], bg=self.turnOrder[1]['color'])
        if tn[0]-1 == 0:
            self.prevTurn.configure(text="previous "+self.turnOrder[len(self.turnOrder)-1]['player'], bg=self.turnOrder[len(self.turnOrder)-1]['color'])
        else:
            self.prevTurn.configure(text="previous "+self.turnOrder[tn[0]-1]['player'], bg=self.turnOrder[tn[0]-1]['color'])
        #audio
        if self.audioToggle.get() == 1:
            self.sound(tn[1])

    def sound(self, player):
        sound_file = find_data_file("sounds\\"+player+self.rollNum.get()+".mp3")
        playsound.playsound(sound_file, False)
        #False runs asynchronously

    def trackTurn(self): #returns the current turn. called every roll to keep track
        for num, value in self.turnOrder.items():
            if num == self.turnCount:
                self.turnCount +=1
                return [num, value['player'], value['color']] #number, player, color
        self.turnCount = 2 #set to turn 2 but displays turn 1 because next iteration will display turn 2
        return [1, self.turnOrder[1]['player'], self.turnOrder[1]['color']]

    def postupdate(self):
        self.rollButton.focus()
        self.turnOrder = Setup.turns

class BarGraph:
    def __init__(self, parent):
        self.width = 1000
        self.height = 800
        self.parent = parent
        #Canvas for barGraph
        self.graph = tk.Canvas(parent, width= self.width, height = self.height, bg='light gray')
        self.graph.grid(row=1, column=1, rowspan=4, columnspan=2, padx=10, pady=10)

        labelGap = self.width/11 -7 #scales placement of labels and graphs according to canvas
        #each dictionary key holds an array containing the number, start position of the bar, and rolltimes
        self.labels={}
        for i in range(2,13):
            self.labels[i] = [(i-1)*labelGap, {'red': 0, 'blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}]

        self.drawLabels(self.graph)
        self.drawBars(self.graph)

    def clearStatInfo(self):
        for index, entry in self.labels.items():
            entry[1] = {'red': 0, 'blue':0, 'white':0, 'orange':0, 'green':0, 'brown':0}

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
        self.graph.grid(row=1, column=1, rowspan=4, columnspan=2, padx=10, pady=10)

    def drawLabels(self, canvas):
        for i in self.labels: #write labels
            canvas.create_text(self.labels[i][0], self.height-30, anchor='nw', text=i, font=("Sans", 25, "bold"))

    def drawBars(self, canvas): #draw bars on graph
        minHeight = self.height-30
        fullHeight = minHeight - 30
        if self.findMaxRolls() != 0:
            segmentHeight = fullHeight/self.findMaxRolls()
            for c in self.labels:
                tmin = minHeight
                for d in self.labels[c][1]:
                    #print(d + str(self.labels[c][1][d]))
                    if self.labels[c][1][d] != 0:
                        tmax = tmin - (self.labels[c][1][d]*segmentHeight)
                        canvas.create_rectangle(self.labels[c][0] -7, tmax, self.labels[c][0] +30, tmin, fill=MainApp.displayed_color[d])
                        canvas.create_text(self.labels[c][0]+7, (tmin-tmax)/2+tmax, text=self.labels[c][1][d]) #rolls per color
                        tmin = tmax
                #labels indicating how many rolls
                rollsPer = self.rollsPerNumber(c)
                canvas.create_text(self.labels[c][0]+5, minHeight-(rollsPer*segmentHeight)-20, anchor='nw', text=rollsPer, font=("Sans", 14, 'bold'))

    def totalRolls(self, canvas):
        total=0
        for x in self.labels:
            total+= self.rollsPerNumber(x)
        canvas.create_text(self.width*.87, self.height*.03, anchor='nw', text="Total: "+str(total), font=('Comic Sans', 14))

    def findMaxRolls(self): #finds maximum rolls in all numbers
        sumOfRolls = {} #holds list of rolls of each number
        for r in self.labels:
            sumOfRolls[r] = self.rollsPerNumber(r)
        maxRolls = 0
        for a in sumOfRolls:
            if sumOfRolls[a] > maxRolls :
                maxRolls = sumOfRolls[a]
        return maxRolls

    def rollsPerNumber(self, num): #sum rolls of one number
        sumR = 0
        for p in self.labels[num][1]:
            sumR += self.labels[num][1][p]
        return sumR

class Setup(tk.Frame):
    turns = {} #holds turns. {turn : [turn: color]}
    startTime= 0.0
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.configure(bg = MainApp.BG_COLOR)
        subContainer = tk.Frame(self, bg = MainApp.BG_COLOR)
        self.titleLabel = tk.Label(subContainer, text = "Catan Dice Stat Tracker", bg='grey20', fg='white', font=('Times', 70, 'italic'))
        self.titleLabel.grid(row=0, columnspan=6, padx=20, pady=10)

        self.info = tk.Label(subContainer, text ="select turn order", bg='grey20', fg='white', font=('Sans', 20))
        self.info.grid(row=1, columnspan=6, pady=5)

        self.reset = tk.Button(subContainer, text='reset turns', bg='black', fg='white', activebackground='gray25', activeforeground='white',
            font=('Sans', 18), command=self.resetTurns)
        self.reset.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.play = tk.Button(subContainer, text='Play', width=8, bg='black', fg='white', activebackground='gray25', activeforeground='white',
            font=('Sans', 25), command=self.play)
        self.play.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        toQuickRoll = tk.Button(subContainer, text='Simple Dice', bg='black', fg='white', activebackground='gray25', activeforeground='white',
            font=('Sans', 18), command= lambda: controller.show_frame(QuickRoll))
        toQuickRoll.grid(row=3, column=4, columnspan=2, padx=10, pady=10)

        self.orderNum = {'red': tk.IntVar(), 'blue':tk.IntVar(), 'white':tk.IntVar(), 'orange':tk.IntVar(), 'green':tk.IntVar(), 'brown':tk.IntVar()}

        self.red = tk.Button(subContainer, bg=MainApp.displayed_color['red'], width=6, height=2, disabledforeground='gray25', textvariable=self.orderNum['red'], font=('Sans', 30, 'bold'), command=lambda: self.order('red', self.red))
        self.red.grid(row=2, column=0)
        self.blue = tk.Button(subContainer, bg=MainApp.displayed_color['blue'], width=6, height=2, disabledforeground='gray25', textvariable=self.orderNum['blue'], font=('Sans', 30, 'bold'), command=lambda: self.order('blue', self.blue))
        self.blue.grid(row=2, column=1)
        self.white = tk.Button(subContainer, bg=MainApp.displayed_color['white'], width=6, height=2, disabledforeground='gray25', textvariable=self.orderNum['white'], font=('Sans', 30, 'bold'), command=lambda: self.order('white', self.white))
        self.white.grid(row=2, column=2)
        self.orange = tk.Button(subContainer, bg=MainApp.displayed_color['orange'], width=6, height=2, disabledforeground='gray25', textvariable=self.orderNum['orange'], font=('Sans', 30, 'bold'), command=lambda: self.order('orange', self.orange))
        self.orange.grid(row=2, column=3)
        self.green = tk.Button(subContainer, bg=MainApp.displayed_color['green'], width=6, height=2, disabledforeground='gray25', textvariable=self.orderNum['green'], font=('Sans', 30, 'bold'), command=lambda: self.order('green', self.green))
        self.green.grid(row=2, column=4)
        self.brown = tk.Button(subContainer, bg=MainApp.displayed_color['brown'], width=6, height=2, disabledforeground='gray25', textvariable=self.orderNum['brown'], font=('Sans', 30, 'bold'), command=lambda: self.order('brown', self.brown))
        self.brown.grid(row=2, column=5)
        subContainer.pack(expand=1)

    def order(self, color, button): #sets the order
        self.orderNum[color].set(self.findNextTurn(self.orderNum)+1)
        button.configure(state='disabled')

    def resetTurns(self): #resets the turns
        for i in self.orderNum:
            self.orderNum[i].set(0)
        self.red.configure(state='normal')
        self.blue.configure(state='normal')
        self.white.configure(state='normal')
        self.orange.configure(state='normal')
        self.green.configure(state='normal')
        self.brown.configure(state='normal')

    def play(self): #changes to DiceRoller
        if self.findNextTurn(self.orderNum) > 1:
            Setup.turns = self.convertToArray(self.orderNum)
            #self.reset.configure(state='disabled')
            #disable turn buttons
            self.red.configure(state='disabled')
            self.blue.configure(state='disabled')
            self.white.configure(state='disabled')
            self.orange.configure(state='disabled')
            self.green.configure(state='disabled')
            self.brown.configure(state='disabled')
            self.controller.show_frame(DiceRoller)
        else:
            self.info.configure(text="select at least 2 players")

    def convertToArray(self, Tlist):
        t={}
        for key, value in Tlist.items():
            t[value.get()] = {'turn':value.get(), 'player':key, 'color':MainApp.displayed_color[key]}
        return t

    def findNextTurn(self, orderList):
        max = 0
        for a in orderList:
            if orderList[a].get() > max :
                max = orderList[a].get()
        return max

class QuickRoll(tk.Frame):
    #mainly just to roll for turns
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.configure(bg = MainApp.BG_COLOR)
        subContainer = tk.Frame(self, bg = MainApp.BG_COLOR)

        back = tk.Button(subContainer, text='<<<', bg='black', fg='white', font=("Sans", 14, 'bold'), command= lambda: controller.show_frame(Setup))
        back.grid(row=0, column=0)

        self.info = tk.Label(subContainer, text ="Simple Dice \n Mainly to roll for turns", bg='grey20', fg='white', font=('Sans', 20))
        self.info.grid(row=1, column=1)

        self.quickDice = tk.Button(subContainer, text='Roll', font=('Ariel', 200), bg='black', activebackground='dark gray', activeforeground='white', fg='white', width=4,
            command=self.simpleRoll)
        self.quickDice.grid(row=2, column=1)
        self.quickDice.bind('<space>', self.simpleRoll_a)
        #self.quickDice.focus_force()

        subContainer.pack(expand=True)

    def simpleRoll_a(self, event): #handles keypress
        self.simpleRoll()
        return "break"

    def simpleRoll(self):
        dice1 = random.SystemRandom().randint(1,6)
        dice2 = random.SystemRandom().randint(1,6)
        self.quickDice.configure(text= str(dice1) +"+"+ str(dice2))

    def postupdate(self): #after this frame is brought up
        self.quickDice.focus()

class MainApp(tk.Tk):
    #color to be used for each player (tkinter colors)
    displayed_color = {'blue' : 'royal blue',
                        'red'   : 'red2',
                        'white' : 'snow',
                        'orange': 'dark orange',
                        'green' : 'dark green',
                        'brown' : 'saddle brown'
                        }
    BG_COLOR = 'gray20' #background color

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.configure(bg = MainApp.BG_COLOR)
        container = tk.Frame(self)
        container.pack(expand=True)

        self.frames = {}
        for F in (Setup, DiceRoller, QuickRoll):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Setup)

    def show_frame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()
        try:
            frame.postupdate()
        except AttributeError:
            pass

def find_data_file(filename): #desktop shortcut needs this because of different working directory
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

app = MainApp()
app.title("Catan Dice Stat Tracker")
app.iconbitmap(find_data_file('icon.ico'))
app.mainloop()
