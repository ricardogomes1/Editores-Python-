from Tkinter import *
from tkMessageBox import showerror
from string import replace
from sys import argv

template = """
class ActiveMap(insert_your_class_here):

    def __init__(self, master=None):

        self.image = PhotoImage(file="IMGFILE")
        if master = None:
            self.master = Tk()
        else:
            self.master = master
            
        self.canv = Canvas(self.master, width=self.image.width(), height=self.image.height())
        self.canv.create_image(0,0, image=self.image, anchor=NW)
        self.canv.pack()

        self.activemapbuttons = BUTTONS

        self.canv.bind('<Button-1>', self.MapCallback)

        self.master.mainloop()

    def MapCallback(self, event):

        x,y = event.x, event.y

        for funct in self.activemapbuttons.keys():
            for rect in self.activemapbuttons[funct]:
                if (x>rect[0] and x<rect[2]) and (y>rect[1] and y<rect[3]):
                    funct()

    def dummy(self):

        print "Dummy function. please assign a REAL function to this button!"
            
"""


class MapSelect:
    """
    create image hotspots out ouf image
    """

    def __init__(self, image):

        self.root = Tk()
        
        self.image = PhotoImage(file=image)
        self.canv = Canvas(self.root, width=self.image.width(), height=self.image.height())
        self.canv.create_image(0,0, image=self.image, anchor=NW)
        self.canv.pack()

        self.canv.bind('<Button-1>', self.OnClick)
        self.canv.bind('<B1-Motion>', self.OnMove)
        self.canv.bind('<ButtonRelease-1>', self.OnRelease)
        self.canv.bind('<Button-3>', self.ResetRectangle)

        self.selection = None # selected rectangle
        self.buttons = {} # holds buttons created
        self.greens = [] # holds green button markers
	
        self.status = Label(self.root, text="nothing selected", relief=GROOVE)
        self.status.pack(fill=X)

        Label(self.root, text="Please enter \nfunction name associated").pack(side=LEFT)

        self.function = Entry(self.root)
        self.function.pack(fill=X, side=LEFT, padx=10)

        self.validate = Button(self.root, text="OK", command=self.Ok)
        self.validate.pack(side=LEFT)
        self.cancel = Button(self.root, text="Reset", command=self.Reset)
        self.cancel.pack(side=LEFT)
        self.save = Button(self.root, text="Save map", command=self.OnSave)
        self.save.pack(side=LEFT)
        self.quit =  Button(self.root, text="Quit", command=self.root.quit)
        self.quit.pack(side=LEFT)
        
        self.root.mainloop()


    def Ok(self):

        if self.selection != None:
            
            func_text = self.function.get()
            if func_text == '':
                func_text = 'dummy'
            func_area = self.canv.coords(self.selection)
            if func_text not in self.buttons.keys():
                self.buttons[func_text] = [func_area]
            else:
                self.buttons[func_text].append(func_area)

            self.canv.delete(self.selection)
            self.greens.append(self.canv.create_rectangle(func_area[0], func_area[1], func_area[2], func_area[3],
                                                           outline='', stipple="gray25", fill='green'))
            self.function.delete(0,END)

        else:
            print "Select something first!"

    def Reset(self):

        for rect in self.greens:
            self.canv.delete(rect)
        self.canv.delete(self.selection)

        self.greens = []
        self.buttons = {}
        print "Reset clicked"

    def OnClick(self, event):

        if self.selection != None:
            self.canv.delete(self.selection)

        self.startx = event.x
        self.starty = event.y
        self.selection = self.canv.create_rectangle(event.x, event.y, event.x, event.y, outline='', fill='red', stipple='gray50')
        self.UpdateStatus(event)

    def OnRelease(self, event):

        pass

    def UpdateStatus(self, event):

        if self.selection != None:
            self.status['text']='selected: (%i, %i, %i, %i)'%(self.startx, self.starty, event.x, event.y)
        else:
            self.status['text']='nothing selected'
            
    def OnMove(self, event):

        self.canv.delete(self.selection)
        self.selection = self.canv.create_rectangle(self.startx, self.starty, event.x, event.y, outline='', fill='red', stipple='gray50')

        self.UpdateStatus(event)

    def ResetRectangle(self, event):

        self.canv.delete(self.selection)
        self.selection = None

        self.UpdateStatus(event)

    def OnSave(self):

        print self.buttons

        img = self.image.cget('file')
        

        buttonkeys = self.buttons.keys()
        buttonstring = '{self.%s : %s,'%(buttonkeys[0], self.buttons[buttonkeys[0]])
        for el in buttonkeys[1:-1]:
            buttonstring = buttonstring+'\n%sself.%s : %s,'%(" "*33, el, self.buttons[el])
        if len(buttonkeys) > 1:
            buttonstring = buttonstring + '\n%sself.%s : %s}'%(" "*33, buttonkeys[-1], self.buttons[buttonkeys[-1]])
        else:
            buttonstring = buttonstring[:-1]+'}'
            
        local_template = replace(template, "BUTTONS", buttonstring)
        local_template = replace(local_template, "IMGFILE", img)
        output = open('./mapselect_output', 'w')
        output.write(local_template)
        output.close()

if __name__ == '__main__':

    img = argv[1]
    MapSelect(img)
