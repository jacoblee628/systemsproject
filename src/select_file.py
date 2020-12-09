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

        #Obsolete srs file select
        self.ObsoleteSRSpath=StringVar()
        self.ObsoleteSRSnameLabel=Label(self, text="Obsolete SRS file path:")
        self.ObsoleteSRSnameLabel.grid(row=2,column=0)
        self.ObsoleteSRSfileName=Entry(self, textvariable=self.ObsoleteSRSpath, width='60')
        self.ObsoleteSRSfileName.grid(row=2,column=1)
        self.ObsoleteSRSselectBtn=Button(self, text="select",command=self.selectObsoleteSRSPath)
        self.ObsoleteSRSselectBtn.grid(row=2,column=2)

        #Manual as-runs file select
        self.Manualpath=StringVar()
        self.ManualnameLabel=Label(self, text="Manual file path:")
        self.ManualnameLabel.grid(row=3,column=0)
        self.ManualfileName=Entry(self, textvariable=self.Manualpath, width='60')
        self.ManualfileName.grid(row=3,column=1)
        self.ManualselectBtn=Button(self, text="select",command=self.selectManualPath)
        self.ManualselectBtn.grid(row=3,column=2)

        #TraceMatrix file select
        self.TraceMatrixpath=StringVar()
        self.TraceMatrixnameLabel=Label(self, text="Trace Matrix file path:")
        self.TraceMatrixnameLabel.grid(row=4,column=0)
        self.TraceMatrixfileName=Entry(self, textvariable=self.TraceMatrixpath, width='60')
        self.TraceMatrixfileName.grid(row=4,column=1)
        self.TraceMatrixselectBtn=Button(self, text="select",command=self.selectTraceMatrixPath)
        self.TraceMatrixselectBtn.grid(row=4,column=2)

        #Rest api folder select
        self.RestAPIpath=StringVar()
        self.RestAPInameLabel=Label(self, text="RestAPI folder path:")
        self.RestAPInameLabel.grid(row=5,column=0)
        self.RestAPIfileName=Entry(self, textvariable=self.RestAPIpath, width='60')
        self.RestAPIfileName.grid(row=5,column=1)
        self.RestAPIselectBtn=Button(self, text="select",command=self.selectRestAPIPath)
        self.RestAPIselectBtn.grid(row=5,column=2)

        #Performance test results file select
        self.performancepath=StringVar()
        self.performancenameLabel=Label(self, text="Performance Test file path:")
        self.performancenameLabel.grid(row=6,column=0)
        self.performancefileName=Entry(self, textvariable=self.performancepath, width='60')
        self.performancefileName.grid(row=6,column=1)
        self.performanceselectBtn=Button(self, text="select",command=self.selectperformancePath)
        self.performanceselectBtn.grid(row=6,column=2)

        self.startBtn=Button(self, text="Start Process", command=self.start)
        self.startBtn.grid(row=7,column=1)

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

    def selectObsoleteSRSPath(self):
        ObsoleteSRSfile_path = fd.askopenfilename()
        self.ObsoleteSRSpath.set(ObsoleteSRSfile_path)
        ObsoleteSRSname=self.ObsoleteSRSfileName.get()
        if 'obsolete' in ObsoleteSRSname.lower():
            messagebox.showinfo("Message",ObsoleteSRSname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.ObsoleteSRSpath.set('')    

    def selectManualPath(self):
        Manualfile_path = fd.askopenfilename()
        self.Manualpath.set(Manualfile_path)
        Manualname=self.ManualfileName.get()
        if 'manual' in Manualname.lower():
            messagebox.showinfo("Message",Manualname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.Manualpath.set('')

    def selectTraceMatrixPath(self):
        TraceMatrixfile_path = fd.askopenfilename()
        self.TraceMatrixpath.set(TraceMatrixfile_path)
        TraceMatrixname=self.TraceMatrixfileName.get()
        if 'trace matrix' in TraceMatrixname.lower():
            messagebox.showinfo("Message",TraceMatrixname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.TraceMatrixpath.set('')
    
    def selectRestAPIPath(self):
        RestAPIfile_path = fd.askdirectory()
        self.RestAPIpath.set(RestAPIfile_path)
        RestAPIname=self.RestAPIfileName.get()
        if 'rest' in RestAPIname.lower():
            messagebox.showinfo("Message",RestAPIname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.RestAPIpath.set('')

    def selectperformancePath(self):
        performancefile_path = fd.askopenfilename()
        self.performancepath.set(performancefile_path)
        performancename=self.performancefileName.get()
        if 'performance' in performancename.lower():
            messagebox.showinfo("Message",performancename)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.performancepath.set('')
 


    
    def start(self):
        messagebox.showinfo('Message','waiting for further integration')
    
    

app = Application()
app.master.title('Produce trace matrix')
app.mainloop()
    