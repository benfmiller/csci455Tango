import tkinter as tk


class MyTK():
    def __init__(self, win):
        self.win = win
        #self.win.geometry("800x480")
        self.win.attributes("-fullscreen", True)
        #width = self.win.winfo_screenwidth()
        #height = self.win.winfo_screenheight()
        #self.win.geometry("%dx%d"%(width, height))
    def createCanvas(self):
        self.myCan = tk.Canvas(self.win, bg="#333333", width="500", height="500")
        self.myCan.bind('<Motion>', self.motion)
        self.myCan.pack()

    def createLabel(self):
        lab = tk.Label(self.win, text="Hello Tkinter!")
        lab.pack()
        
    def createButton(self):
        #command = fun
        button = tk.Button(self.win, width="45", text="print", bg="blue", fg="yellow", command=lambda m="#print button pressed":self.fun3(m))
        button.pack(side = tk.RIGHT)
        button2 = tk.Button(self.win, width="15", text="Second", bg="blue", fg="yellow", command=lambda m="#second button pressed":self.fun3(m))
        button2.pack(side = tk.BOTTOM)
        button2 = tk.Button(self.win, width="15", text="exit", bg="blue", fg="yellow", command=lambda m="exit":self.fun3(m))
        button2.pack(side = tk.LEFT)

    def fun(self):
        print("Print is pushed")
        
    def fun2(self):
        print("Second is pressed")

    def fun3(self,  name):
        print(name)
        if(name == "exit"):
            print("leaving")
            self.win.destroy()
        
        
    def motion(self, event):
      print("Mouse position: (%s %s)" % (event.x, event.y))
      return   

    def mouseClick(self, event):
        print(event)
        
    def arrow(self, key):
        #print("Arrow up")
        print(self, key)
        if key.keycode==39:
            print("Right")
        
win = tk.Tk()
v = MyTK(win)
##Key bindings
win.bind('<Up>',  v.arrow)
win.bind('<Right>', v.arrow)
win.bind('<Button>', v.mouseClick)

#create a canvas and add it to window
v.createCanvas()
#Place a label on Window
v.createLabel()
x = input("click to continue")
v.createButton()
win.mainloop()
