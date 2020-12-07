from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.path=StringVar()
        self.nameLabel=Label(self, text="file path:")
        self.nameLabel.pack()
        self.fileName=Entry(self, textvariable=self.path, width='20')
        self.fileName.pack()
        self.selectBtn=Button(self, text="select",command=self.selectPath)
        self.selectBtn.pack()
        self.showBtn=Button(self, text="show file name", command=self.showName)
        self.showBtn.pack()

    def selectPath(self):
        file_path = fd.askopenfilename()
        self.path.set(file_path)
        
    
    def showName(self):
        name=self.fileName.get()
        messagebox.showinfo("Message",name)
    

app = Application()
app.master.title('Hello World')
app.mainloop()
    