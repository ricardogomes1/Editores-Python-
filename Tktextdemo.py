
#Created on 20/01/2001
#Martin Stevens, budgester@budgester.com

from Tkinter import *

class App:

##  Create GUI 

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.get_text = Button(frame, text="Get", fg="red", command=self.retrieve_text)
        self.get_text.pack(side=LEFT)

        self.put_text = Button(frame, text="Put", command=self.enter_text)
        self.put_text.pack(side=LEFT)

        self.text_box = Text(frame)
        self.text_box.pack(side=LEFT)

##  Insert 'Hi there everyone!' into the text box 

    def enter_text(self):
        self.text_box.insert(END, "Hi there everyone!")
        
##  Retrieve text from the text box and print to the console

    def retrieve_text(self):
        contents = self.text_box.get(1.0, END)
        print contents

root = Tk()

app = App(root)

root.mainloop()

