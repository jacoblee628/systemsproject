from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        #SRS file select
        self.SRSpath=StringVar()
        self.SRSnameLabel=Label(self, text="SRS file path:")
        self.SRSnameLabel.grid(row=0,column=0)
        self.SRSfileName=Entry(self, textvariable=self.SRSpath, width='60')
        self.SRSfileName.grid(row=0,column=1)
        self.SRSselectBtn=Button(self, text="select",command=self.selectSRSPath)
        self.SRSselectBtn.grid(row=0,column=2)

        #PRD file select
        self.PRDpath=StringVar()
        self.PRDnameLabel=Label(self, text="PRD file path:")
        self.PRDnameLabel.grid(row=1,column=0)
        self.PRDfileName=Entry(self, textvariable=self.PRDpath, width='60')
        self.PRDfileName.grid(row=1,column=1)
        self.PRDselectBtn=Button(self, text="select",command=self.selectPRDPath)
        self.PRDselectBtn.grid(row=1,column=2)

        #Use case file select
        self.UseCasepath=StringVar()
        self.UseCasenameLabel=Label(self, text="UseCase file path:")
        self.UseCasenameLabel.grid(row=2,column=0)
        self.UseCasefileName=Entry(self, textvariable=self.UseCasepath, width='60')
        self.UseCasefileName.grid(row=2,column=1)
        self.UseCaseselectBtn=Button(self, text="select",command=self.selectUseCasePath)
        self.UseCaseselectBtn.grid(row=2,column=2)

        #Manual as-runs file select
        self.Manualpath=StringVar()
        self.ManualnameLabel=Label(self, text="Manual file path:")
        self.ManualnameLabel.grid(row=3,column=0)
        self.ManualfileName=Entry(self, textvariable=self.Manualpath, width='60')
        self.ManualfileName.grid(row=3,column=1)
        self.ManualselectBtn=Button(self, text="select",command=self.selectManualPath)
        self.ManualselectBtn.grid(row=3,column=2)

        self.startBtn=Button(self, text="Start Process", command=self.start)
        self.startBtn.grid(row=5,column=1)

    def selectSRSPath(self):
        SRSfile_path = fd.askopenfilename()
        self.SRSpath.set(SRSfile_path)
        SRSname=self.SRSfileName.get()
        if 'SRS' in SRSname:
            messagebox.showinfo("Message",SRSname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.SRSpath.set('')
    
    def selectPRDPath(self):
        PRDfile_path = fd.askopenfilename()
        self.PRDpath.set(PRDfile_path)
        PRDname=self.PRDfileName.get()
        if 'PRD' in PRDname:
            messagebox.showinfo("Message",PRDname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.PRDpath.set('')  

    def selectUseCasePath(self):
        UseCasefile_path = fd.askopenfilename()
        self.UseCasepath.set(UseCasefile_path)
        UseCasename=self.UseCasefileName.get()
        if 'Use Case' in UseCasename:
            messagebox.showinfo("Message",UseCasename)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.UseCasepath.set('')    

    def selectManualPath(self):
        Manualfile_path = fd.askopenfilename()
        self.Manualpath.set(Manualfile_path)
        Manualname=self.ManualfileName.get()
        if 'Manual' in Manualname:
            messagebox.showinfo("Message",Manualname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.Manualpath.set('')
    
    def start(self):
        messagebox.showinfo('Message','waiting for further integration')
    
    

app = Application()
app.master.title('Produce trace matrix')
app.mainloop()
    