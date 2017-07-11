# Since the catan dice were frickin rigged
# I made another dice roller to help us balance the game
#@author Newman

import tkinter as tk
import random

root = tk.Tk()
root.title("Catan Dice")
mainFrame = tk.Frame(root, bg ='white', bd='3c')
word = tk.StringVar()

num = tk.Label(mainFrame, textvariable = word, font=('Ariel', 100))
num.grid()

rollDice = tk.Button(mainFrame, text="Roll", font=('Ariel', 100), command=lambda: roll())
rollDice.grid()

def roll():
    #to simulate dice rolls you need to use two dice simulations
    word.set(random.randint(1,6)+random.randint(1,6))

mainFrame.grid()
root.mainloop()
