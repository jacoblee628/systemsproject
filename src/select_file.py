from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import re
#import run

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

        #Automated tests folder select
        self.automatedTestspath=StringVar()
        self.automatedTestsnameLabel=Label(self, text="Automated Tests folder path:")
        self.automatedTestsnameLabel.grid(row=5,column=0)
        self.automatedTestsfileName=Entry(self, textvariable=self.automatedTestspath, width='60')
        self.automatedTestsfileName.grid(row=5,column=1)
        self.automatedTestsselectBtn=Button(self, text="select",command=self.selectautomatedTestsPath)
        self.automatedTestsselectBtn.grid(row=5,column=2)

        # version number input
        self.versionNumpath=StringVar()
        self.versionNumnameLabel=Label(self, text="Input Version Number(#.#.#) here :")
        self.versionNumnameLabel.grid(row=6,column=0)
        self.versionNumName=Entry(self, textvariable=self.versionNumpath, width='40')
        self.versionNumName.grid(row=6,column=1)

        #Select srs_prefix from drop down list
        self.srsPrefix=StringVar()
        self.srsPrefix.set("TC")
        self.srsPrefixLabel=Label(self, text="Select SRS Prefix")
        self.srsPrefixLabel.grid(row=7,column=0)
        self.srsPrefixName=OptionMenu(self, self.srsPrefix, "TC", "ESA-")
        self.srsPrefixName.grid(row=7,column=1)

        self.startBtn=Button(self, text="start", command=self.start)
        self.startBtn.grid(row=8,column=1)

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
    
    def selectautomatedTestsPath(self):
        automatedTestsfile_path = fd.askdirectory()
        self.automatedTestspath.set(automatedTestsfile_path)
        automatedTestsname=self.automatedTestsfileName.get()
        if 'er' in automatedTestsname.lower():
            messagebox.showinfo("Message",automatedTestsname)
        else:
            messagebox.showwarning("Message",'Wrong name!')
            self.automatedTestspath.set('')

 


    
    def start(self):
        if(re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$',self.versionNumName.get())==None):
            messagebox.showinfo('Message','Invalid Version Number')
        else:
            param_dict={"prd":self.PRDfileName.get(), "srs":self.SRSfileName.get(), "obselete_srs":self.ObsoleteSRSfileName.get(), "manual_as_runs":self.ManualfileName.get(), "prev_trace_matrix": self.TraceMatrixfileName.get(), "automated_tests_folder":self.automatedTestsfileName.get(), "version_num":self.versionNumName.get(),"srs_prefix":self.srsPrefixName.get() }
            #run.run(param_dict)
    

app = Application()
app.master.title('Produce trace matrix')
app.mainloop()
    