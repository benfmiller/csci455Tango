import tkinter as tk
import time

class Eyes():
    def __init__(self, win):
        self.win = win
        self.win.geometry("800x480")
        self.myCan = tk.Canvas(self.win, bg="#333333", width="500", height="500")

    def eyeballs(self):
        print("eyes")
        self.myCan.create_oval(75, 75, 200, 300, fil="white")
        self.myCan.create_oval(225, 75, 350, 300, fil="white")
        self.myCan.create_oval(105, 180, 165, 270, fil="black")
        self.myCan.create_oval(255, 180, 310, 270, fil="black")
        self.myCan.create_oval(110, 230, 130, 250, fil="white")
        self.myCan.create_oval(260, 230, 280, 250, fil="white")
        self.myCan.pack()

    def eyelids(self):
        print("blink")
        self.myCan.create_oval(75, 75, 200, 300, fil="yellow")
        self.myCan.create_oval(225, 75, 350, 300, fil="yellow")
        self.myCan.pack()

    def blink(self):
        self.eyeballs()
        self.win.update()
        self.win.after(2000, self.eyelids())
        self.win.update()
        self.win.after(250, self.eyeballs())

def main():
    win = tk.Tk()
    e = Eyes(win)
    for i in range(10):
        e.blink()
   
    win.mainloop()
    
main()
