
import tkinter as tk

class MouseMovement():
    def __init__(self, c):
        self.flag = False
        self.myCan = c
        self.x = 5
        self.y = 5

    def mousePressed(self, event):   
        if event.x > self.x and event.x < self.x + 45 and event.y > self.y and event.y < self.y +45:
            self.flag = True  

    def mouseDragged(self, event):
        if self.flag == True:
            #self.myCan.delete('all')
            self.myCan.create_oval(event.x, event.y, event.x+45, event.y+45, fill="#FFFF00")    
            
    def mouseRelease(self, event):
        if self.flag == True:
            self.flag = False
            self.x = event.x
            self.y = event.y
            self.myCan.delete('all')
            self.myCan.create_oval(event.x, event.y, event.x+45, event.y+45, fill="#FFFF00")
            print("Released at", self.x)
        

win = tk.Tk()
myCan = tk.Canvas(win, bg="#333333", width="1000", height="750")
m = MouseMovement(myCan)
myCan.bind('<B1-Motion>', m.mouseDragged)
myCan.bind('<ButtonPress-1>', m.mousePressed)
myCan.bind('<ButtonRelease-1>', m.mouseRelease)
myCan.create_oval(5, 5, 45, 45, fill="#FFFF00")
myCan.pack()
