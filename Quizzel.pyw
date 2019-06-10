#Quizzel by Nikesh Purohit 2017
from tkinter import *
import tkinter.ttk as ttk
import sqlite3, sys, time, hashlib, tkinter.messagebox, random, urllib.request, ftplib

database = sqlite3.connect('database.db')
cursor = database.cursor()
def h():
    global database, cursor
    #url = urllib.request.urlretrieve('http://quizzel.x10.mx/database.db')
    database = None
    #database = sqlite3.connect(url[0])
    database = sqlite3.connect('Quizzel files/database.db')
    cursor = None
    cursor = database.cursor()

def ConnectFTP():
    #global ftp_connection
    #server = 'ftp.quizzel.x10.mx'
    #username = 'database@quizzel.x10.mx'
    #password = '^ArvSiq1&;tx'
    #ftp_connection = None
    #ftp_connection = ftplib.FTP(server, username, password)
    return True

def u():
    if WaitForUnlock():
        #lockfile = open("Quizzel files/lock", "rb")
        #ftp_connection.storbinary('STOR ' + 'lock', lockfile)
        #d = open(url[0], "rb")
        #ftp_connection.storbinary('STOR ' + 'database.db', d)
        #ftp_connection.delete("lock")
        return True

def WaitForUnlock():
    #if "lock" in ftp_connection.nlst():
    #    return WaitForUnlock()
    #else:
    #    return True
    return True

class Splash(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        canvas = Canvas(self)
        background = PhotoImage(file="Quizzel files/splash2.png")
        self.overrideredirect(1)
        self.configure(bg="white")
        width = 764
        height = 460
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        canvas.create_image(0, 0, image=background, anchor="nw")
        canvas.image = background
        canvas.pack(expand=1, fill=BOTH, side=TOP)
        self.update()

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.withdraw()
        splash = Splash(self)
        #try:
        #    
        #    ConnectFTP()
        #    Splash.destroy(splash)
        #    self.deiconify()
        #except:
        #    Splash.destroy(splash)
        #    tkinter.messagebox.showerror("Quizzel cannot start", "Could not connect to database. Please ensure you have a working internet connection.")
        #    sys.exit(0)
        
        ConnectFTP()
        Splash.destroy(splash)
        self.deiconify()

        self.configure(bg="white")
        self.geometry("1100x650+100+50")
        #self.iconbitmap(r'Quizzel files/icon3.ico')
        container = Frame(self, bg='white')
        container.pack(side="top", fill=BOTH, expand=False)

        self.FirstTime = None
        self.ButtonColour = "#626262"
        self.labelcolour = "black"
        self.QuizIDSearch = []
        self.QuizItems = []
        self.Name = StringVar()
        self.YearGroup = StringVar()
        self.Username = StringVar()
        self.Teacher = StringVar()
        self.TargetGrade = StringVar()
        self.Subjects = StringVar()
        self.Results = []
        self.ChooserList = []
        self.UserDetailsList = []
        self.ChosenQuiz = None
        self.QuestionStack = []
        self.CurrentQuestion = 0
        self.Score = 0
        self.MaxScore = 0
        self.ChosenQuizTitle = None
        self.UserID = None
        self.WrongQuestion = []
        self.QuestionID = []
        self.WrongAnswer = []
        self.AllQID = []
        self.ShouldSave = False
        self.ModifyChooserList = []
        self.ModifyQuizID = 0
        self.ModifyUserList = []
        self.ModifyUserID = 0

        self.imgLogo = PhotoImage(file="Quizzel files/toplogosmallest.png")
        self.frameTopBanner = Frame(self, bg="#2b3033")
        self.lblTopLogo = Label(self.frameTopBanner, bg="#2b3033", fg="white", font=("Arial", 16, 'bold'), text="Quizzel", image=self.imgLogo)
        self.lblTopLogo.photo = self.imgLogo
        self.lblTopLogo.pack(anchor=CENTER, padx=9, pady=9)
        self.frameTopBanner.pack(side=TOP, fill=X)

        self.frames = {}
        self.PackFrame(frameLoginPage, container)

    def PackFrame(self, F, container):
        frame = F(container, self)
        self.frames[F] = frame
        frame.pack(expand=1, side=TOP)


class frameFirstTime(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Create Password")
        time_string = time.strftime('%d/%m/%Y, %H:%M')
        labeltext = "Welcome to your new Quizzel account! Before you can start using Quizzel, you must create a password. You can change your password later in settings. Once you have created your password, click continue to proceed to the tutorial on how to make the most of Quizzel."
        BoxVar1 = StringVar()
        BoxVar2 = StringVar()

        def Continue():
            cont = ChangePassword()
            if cont:
                if root.Teacher == 0:
                    self.pack_forget()
                    parent.pack_forget()
                    controller.PackFrame(frameStudentMenu, parent)
                    parent.pack(expand=1, fill=BOTH)
                if root.Teacher == 1:
                    self.pack_forget()
                    parent.pack_forget()
                    controller.PackFrame(frameTeacherMenu, parent)
                    parent.pack(expand=1, fill=BOTH)

        def CheckBoxes():
            global newpass
            emptyhash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            new1 = BoxVar1.get().encode('utf-8')
            h = hashlib.sha256()
            h.update(new1)
            new1 = h.hexdigest()
            new2 = BoxVar2.get().encode('utf-8')
            h = hashlib.sha256()
            h.update(new2)
            new2 = h.hexdigest()
            if new1 != emptyhash and new2 !=emptyhash:
                if new1 == new2:
                    newpass = new1
                    boxNewPassword1.configure(bg="#cee1ff")
                    boxNewPassword2.configure(bg="#cee1ff")
                    return True
                else:
                    lblOutput.configure(text="New passwords do not match.", fg="#bc0000")
                    boxNewPassword1.configure(bg="#bc0000")
                    boxNewPassword2.configure(bg="#bc0000")
                    return False
            else:
                lblOutput.configure(text="Password field can not be left empty.", fg="#bc0000")
                if new1 == emptyhash:
                    boxNewPassword2.configure(bg="#cee1ff")
                    boxNewPassword1.configure(bg="#bc0000")
                if new2 == emptyhash:
                    boxNewPassword1.configure(bg="#cee1ff")
                    boxNewPassword2.configure(bg="#bc0000")
                if new1 == emptyhash and new2 == emptyhash:
                    boxNewPassword1.configure(bg="#bc0000")
                    boxNewPassword2.configure(bg="#bc0000")
                    return False

        def ChangePassword():
            allowed = CheckBoxes()
            if allowed:
                
                cursor.execute('''UPDATE users SET password=? WHERE UserID=? ''',(newpass,root.UserID))
                cursor.execute('''UPDATE users SET FirstTime=0 WHERE UserID=?''', (root.UserID,))
                database.commit()
                
                lblOutput.configure(text="Password changed successfully!", fg="green")
                boxNewPassword1.delete(0, END)
                boxNewPassword2.delete(0, END)
                return True
            else:
                BoxVar1 = StringVar()
                BoxVar2 = StringVar()
                return False

        lblText = Label(self, text=labeltext, bg="white", fg="#04286f", font=("Arial", 14, ''), wraplength=800)
        lblOutput = Label(self, text="", bg="white", fg="red", font=("Arial", 12, ''))
        boxNewPassword1 = Entry(self, textvariable=BoxVar1, relief=FLAT, bg="#cee1ff", width=40, show="●")
        boxNewPassword2 = Entry(self, textvariable=BoxVar2, relief=FLAT, bg="#cee1ff", width=40, show="●")
        lblBox1 = Label(self, text="New password:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblBox2 = Label(self, text="Confirm new password:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        btnContinue = Button(self, command=Continue, text='Continue >', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        lblText.grid(columnspan=2, row=0)
        lblOutput.grid(pady=4, columnspan=2, row=1)
        boxNewPassword1.grid(pady=4, column=1, row=3, sticky=E)
        boxNewPassword2.grid(pady=7, column=1, row=4, sticky=E)
        lblBox1.grid(pady=4, column=0, row=3, sticky=E)
        lblBox2.grid(pady=7, column=0, row=4, sticky=E)
        btnContinue.grid(pady=10, columnspan=2)


class frameLoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Login")

        def LoginButton(event):
            
            u = username.get()
            p = password.get().encode('utf-8')
            h = hashlib.sha256()
            h.update(p)
            p = h.hexdigest()
            LoggedIn = False
            LoggedIn = Login(u,p)
            if LoggedIn == True:
                controller.unbind('<Return>')
                controller.unbind('<Button-1>')
                controller.unbind('<space>')
                if root.FirstTime == 0:
                    if root.Teacher == 0:
                        controller.PackFrame(frameStudentMenu, parent)
                        parent.pack_forget()
                        self.pack_forget()
                        parent.pack(expand=1, fill=BOTH)
                    if root.Teacher == 1:
                        controller.PackFrame(frameTeacherMenu, parent)
                        parent.pack_forget()
                        self.pack_forget()
                        parent.pack(expand=1, fill=BOTH)
                if root.FirstTime == 1:
                        controller.PackFrame(frameFirstTime, parent)
                        parent.pack_forget()
                        self.pack_forget()
                        parent.pack(expand=1, fill=BOTH)


        def Login(u,p):
            global loginlabel2colour, found
            
            cursor.execute('''SELECT * FROM Users WHERE Username=? AND Password=? ''',(u,p))
            found = cursor.fetchone()
            if found:
                cursor.execute('''SELECT UserID FROM Users WHERE Username=? AND Password=? ''',(u,p))
                UserID = cursor.fetchone()
                GetUserDetails(UserID)
                loginlabel2.set("Login successful!")
                loginlabel2colour = "#04286f"
                lblOutput = Label(self, textvariable=loginlabel2, bg="white", fg=loginlabel2colour, font=("Arial", 13, ''))
                lblOutput.grid(row = 1, pady=0)
                boxUsername.delete(0, END)
                boxPassword.delete(0, END)
                return True
            else:
                loginlabel2.set("The username or password is incorrect, please try again.")
                loginlabel2colour = "#bc0000"
                lblOutput = Label(self, textvariable=loginlabel2, bg="white", fg=loginlabel2colour, font=("Arial", 13, ''))
                lblOutput.grid(row = 1, pady=0)
                boxPassword.delete(0, END)
                controller.bell()
                return False


        def GetUserDetails(UserID):
            UserID = str(UserID)
            for s in ['(', ')', ',']:
                UserID = UserID.strip(s)
            
            cursor.execute("SELECT Name, YearGroup, Username, Teacher, TargetGrade, Subjects, FirstTime FROM users WHERE UserID=?",(UserID,))
            for column in cursor:
                root.UserDetailsList.append((column[0],column[1],column[2],column[3],column[4],column[5],column[6]))
            root.Name = root.UserDetailsList[0][0]
            root.YearGroup = root.UserDetailsList[0][1]
            root.Username = root.UserDetailsList[0][2]
            root.Teacher = root.UserDetailsList[0][3]
            root.TargetGrade = root.UserDetailsList[0][4]
            root.Subjects = root.UserDetailsList[0][5]
            root.FirstTime = root.UserDetailsList[0][6]
            if root.Subjects != None:
                root.Subjects = root.Subjects.split(", ")
            root.UserID = UserID

        controller.bind('<Return>',LoginButton)
        global loginlabel2
        imgArrow = PhotoImage(file="Quizzel files/loginbuttonsmall.png")
        loginlabel2 = StringVar()
        loginlabel2.set("Please enter your username and password to login: ")
        loginlabel2colour = "#282828"
        password = StringVar()
        username = StringVar()

        lblWelcome = Label(self, text="Welcome to Quizzel!", bg="white", fg="#282828", font=("Arial", 16, 'bold'))
        lblWelcome.grid(row = 0, pady=9)
        lblOutput = Label(self, textvariable=loginlabel2, bg="white", fg=loginlabel2colour, font=("Arial", 13, ''))
        lblOutput.grid(row = 1, pady=0)
        boxUsername = Entry(self, textvariable=username, relief=FLAT, bg="#87B2F3", width=40)
        boxUsername.grid(row = 2, pady=5)
        boxPassword = Entry(self, textvariable=password, relief=FLAT, bg="#87B2F3", show="●", width=40)
        boxPassword.grid(row = 3, pady=5)
        btnLogin = Button(self, text='Login', relief=FLAT, overrelief=FLAT, bg="white", fg="#04286f", image=imgArrow, activebackground="white", highlightthickness="0")
        btnLogin.photo = imgArrow
        btnLogin.grid(row = 4, pady=9)
        btnLogin.focus_force()
        btnLogin.bind('<Button-1>',LoginButton)
        btnLogin.bind('<space>',LoginButton)


class frameStudentMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white", highlightthickness=0)
        controller.title("Quizzel - Student (%s, Year %s)" % (root.Name, root.YearGroup))

        def ChooseQuizButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameQuizSelection, parent)
            parent.pack(expand=1)

        def ResultsButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameResultsStudent, parent)
            parent.pack(expand=1)

        def SettingsButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(framePasswordChange, parent)
            parent.pack(expand=1)

        def Logout():
            loginlabel2.set("Please enter your username and password to login: ")
            found = False
            LoggedIn = False
            root.ChooserList = []
            root.QuizIDSearch = []
            root.QuizItems = []
            root.Name = StringVar()
            root.YearGroup = StringVar()
            root.Username = StringVar()
            root.Teacher = StringVar()
            root.TargetGrade = StringVar()
            root.Subjects = StringVar()
            root.Results = []
            root.ChooserList = []
            root.UserDetailsList = []
            root.ChosenQuiz = None
            root.QuestionStack = []
            root.CurrentQuestion = 0
            root.Score = 0
            root.MaxScore = 0
            root.ChosenQuizTitle = None
            root.UserID = None
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameLoginPage, parent)

        QuizButton = Button(self, command=ChooseQuizButton, text='Take A Quiz', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        ResultsButton = Button(self, command=ResultsButton, text='See your results', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        SettingsButton = Button(self, command=SettingsButton, text='Settings', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        LogoutButton = Button(self, command=Logout, text='Logout', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        QuizButton.grid(pady=18)
        ResultsButton.grid(pady=18)
        SettingsButton.grid(pady=18)
        LogoutButton.grid(pady=18)

class frameTeacherMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        controller.title("Quizzel - Teacher (%s)" % root.Name)

        def mQuiz():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameModifyQuizSelector, parent)
            parent.pack(expand=1)

        def TeacherResultsButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameResultsTeacher, parent)
            parent.pack(expand=1)

        def ModifyUsersButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameModifyUser, parent)
            parent.pack(expand=1)

        def SubjectButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameNewSubject, parent)
            parent.pack(expand=1)

        def Logout():
            loginlabel2.set("Please enter your username and password to login: ")
            found = False
            LoggedIn = False
            root.ChooserList = []
            root.QuizIDSearch = []
            root.QuizItems = []
            root.Name = StringVar()
            root.YearGroup = StringVar()
            root.Username = StringVar()
            root.Teacher = StringVar()
            root.TargetGrade = StringVar()
            root.Subjects = StringVar()
            root.Results = []
            root.ChooserList = []
            root.UserDetailsList = []
            root.ChosenQuiz = None
            root.QuestionStack = []
            root.CurrentQuestion = 0
            root.Score = 0
            root.MaxScore = 0
            root.ChosenQuizTitle = None
            root.UserID = None
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameLoginPage, parent)

        btnModifyQuiz = Button(self, command=mQuiz, text='Create/Modify Quiz', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        btnResults = Button(self, command=TeacherResultsButton, text='See student results', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        btnManageUsers = Button(self, command=ModifyUsersButton, text='Add / Remove Users', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        btnAddSubject = Button(self, command=SubjectButton, text='Add New Subject', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        btnLogout = Button(self, command=Logout, text='Logout', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='43', pady='22')
        btnModifyQuiz.grid(pady=18)
        btnResults.grid(pady=18)
        btnManageUsers.grid(pady=18)
        btnAddSubject.grid(pady=18)
        btnLogout.grid(pady=18)

class frameResultsTeacher(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        reverse = False

        def TeacherMenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameTeacherMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def PopulateResults(sort):
            root.Results = []
            for i in tree.get_children():
                tree.delete(i)
            
            cursor.execute('SELECT UserID, QuizID, Result, Time FROM results')
            for column in cursor:
                root.Results.append([column[0],column[1],column[2],column[3]])
            for j in range (0, len(root.Results)):
                QuizID = root.Results[j][1]
                cursor.execute('SELECT QuizTitle from quizzes where QuizID=?',(QuizID,))
                k = cursor.fetchone()
                for s in ['(', ')', ',',"'"]:
                    k = str(k).strip(s)
                root.Results[j][1] = k
            for u in range (0, len(root.Results)):
                UserID = root.Results[u][0]
                cursor.execute('SELECT Name from users where UserID=?',(UserID,))
                h = cursor.fetchone()
                for s in ['(', ')', ',',"'"]:
                    h = str(h).strip(s)
                root.Results[u][0] = h
            if sort == "reverse":
                ReverseList(root.Results)
            if sort == "byname":
                root.Results = sorted(root.Results, key=lambda x: (x[0]))
            for item in root.Results:
                tree.insert('', 'end', values=item)

        def ReverseList(l, first=0, last=-1):
            if first >= len(l)/2:
                return
            l[first], l[last] = l[last], l[first]
            ReverseList(l, first+1, last-1)
        
        def SortA(l): #IMPLEMENT THIS CODE
            if len(l) == 1:
                return True
            elif l[0] <= l[1]:
                return SortA(l[1:])
            else:
                return False

        def SortAlphabetically(l): #IMPLEMENT THIS CODE
            if len(l) == 1:
                return
            elif l[0][0] <= l[1][0]:
                return SortAlphabetically(l[1:][0])
            else:
                return

        def CheckSort(event):
            if sortvar.get() == "Newest first":
                PopulateResults("reverse")
            if sortvar.get() == "Oldest first":
                PopulateResults("none")
            if sortvar.get() == "Name (A-Z)":
                PopulateResults("byname")

        sortvar=StringVar()
        lblSort = Label(self, text="Sort by:", bg="white", fg="#04286f", font=("Arial", 13, ''), wraplength="850")
        sortvar.set("Oldest first")
        comboSort = ttk.Combobox(self, textvariable=sortvar, state='readonly')
        comboSort['values'] = ('Oldest first','Newest first','Name')
        comboSort.bind('<<ComboboxSelected>>', CheckSort)

        frameTree = Frame(self)
        tree = ttk.Treeview(frameTree)
        tree["columns"] = ("one", "two", "three", "four")
        tree['show'] = 'headings'
        tree.column("one", width=100)
        tree.column("two", width=500)
        tree.column("three", width=100)
        tree.column("four", width=200)
        tree.heading("one", text="Student")
        tree.heading("two", text="Quiz Title")
        tree.heading("three", text="Result")
        tree.heading("four", text="Completed on")
        ysb = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
        tree['yscroll'] = ysb.set
        ysb.grid(in_=frameTree, row=0, column=1, sticky=NS)
        frameTree.grid(row=3, columnspan=100, pady=9)
        tree.grid(in_=frameTree, row=0, column=0, sticky=NSEW)

        btnMenu = Button(self, command=TeacherMenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnMenu.grid(row=4, columnspan=100)
        lblSort.grid(row=0, column=49, pady=10)
        comboSort.grid(row=0, column=50, pady=10)
        PopulateResults(reverse)

        #
        print("BEFORE ",root.Results)
        SortAlphabetically(root.Results)
        print(" ")
        print(sorted(root.Results,key=lambda x: (x[0])))
        #print("AFTER ",root.Results)
        #

class frameQuizSelection(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameStudentMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def MultiQuizButton():
            ChooserListIndex = listboxQuiz.index(ACTIVE)
            QuizID = root.ChooserList[ChooserListIndex][0]
            root.ChosenQuiz = QuizID
            
            cursor.execute("SELECT QuizTitle FROM quizzes WHERE QuizID=?",(root.ChosenQuiz,))
            root.ChosenQuizTitle = cursor.fetchone()
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(framePreQuiz, parent)
            parent.pack(expand=1, fill=BOTH)

        def FillQuizList():
            root.QuizItems = []
            root.ChooserList = []
            root.QuizIDSearch = []
            
            cursor.execute('SELECT QuizID FROM Quizzes')
            AllQuizzes = cursor.fetchall()
            for i in AllQuizzes:
                i = i[0]
                for SubID in root.Subjects:
                    cursor.execute('''SELECT QuizTitle FROM Quizzes WHERE QuizID=? AND SubjectID=? ''',(i,SubID))
                    QuizName = cursor.fetchone()
                    cursor.execute('''SELECT SubjectName FROM Subjects WHERE SubjectID=?''',SubID)
                    SubjectName = cursor.fetchall()
                    cursor.execute('''SELECT QuizID FROM Quizzes WHERE QuizID=? AND SubjectID=? ''',(i,SubID))
                    QuizID = cursor.fetchone()
                    try:
                        SubjectName = SubjectName[0][0]
                    except:
                        tkinter.messagebox.showerror("SubjectName[0][0] Failed","One or more of your subject(s) are not valid. You may have been entered for a subject that does not exist.")
                        self.pack_forget()
                        parent.pack_forget()
                        frameStudentMenu.pack(self)
                        parent.pack(expand=1, fill=BOTH)
                        return

                    if QuizName != None:
                        root.ChooserList.append(QuizID)
                        QuizName = str(QuizName[0])
                        ListItem = "%s - %s" %(SubjectName,QuizName)
                        listboxQuiz.insert(END, ListItem)
                        root.QuizItems.append(ListItem)
                        root.QuizIDSearch.append(QuizName)

        def SearchListBox():
            root.ChooserList = []
            root.QuizIDSearch = []
            QuizItems = []
            search_term = search_var.get()
            if search_term == "":
                FillQuizList()
            listboxQuiz.delete(0, END)
            for item in root.QuizItems:
                if search_term.lower() in item.lower():
                    listboxQuiz.insert(END, item)
            QuizItems = listboxQuiz.get(0, END)
            for z in QuizItems:
                z = z.split(' - ')
                z = z[1]
                root.QuizIDSearch.append(z)
            
            for i in root.QuizIDSearch:
                cursor.execute('SELECT QuizID FROM Quizzes WHERE QuizTitle=?',(i,))
                QuizID = cursor.fetchone()
                for s in ['(', ')', ',']:
                    QuizID = str(QuizID).strip(s)
                root.ChooserList.append(QuizID)

        search_var = StringVar()

        search_var.trace("w", lambda name, index, mode: SearchListBox())
        boxSearch = Entry(self, textvariable=search_var, relief=FLAT, bg="#cee1ff", width=40)
        lblQuizList = Label(self, text="Please select a Quiz from the list below or search: ", bg="white", fg="#04286f", font=("Arial", 13, 'bold'))
        listboxQuiz = Listbox(self, width=110, height=20)
        btnSelect = Button(self, command=MultiQuizButton, text='Proceed to Quiz >', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        FillQuizList()
        boxSearch.grid(row=2, columnspan=6, pady=19)
        lblQuizList.grid(row=1, pady=9, columnspan=6)
        listboxQuiz.grid(columnspan=6, pady=3)
        btnMenu.grid(pady=17, column=0, row=5)
        btnSelect.grid(pady=17, column=5, row=5)


class frameResultsStudent(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        reverse = False

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameStudentMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def PopulateResults(r):
            reverse = r
            root.Results = []
            for i in tree.get_children():
                tree.delete(i)
            
            cursor.execute('SELECT QuizID, Result, Time FROM results where UserID=?', (root.UserID,))
            for column in cursor:
                root.Results.append([column[0],column[1],column[2]])
            for j in range (0, len(root.Results)):
                QuizID = root.Results[j][0]
                cursor.execute('SELECT QuizTitle from quizzes where QuizID=?',(QuizID,))
                k = cursor.fetchone()
                for s in ['(', ')', ',',"'"]:
                    k = str(k).strip(s)
                root.Results[j][0] = k
            if reverse == True:
                ReverseList(root.Results)
            for item in root.Results:
                tree.insert('', 'end', values=item)

        NameLabelText = StringVar()
        YearLabelText = StringVar()
        TargetLabelText = StringVar()
        Name = root.Name
        YearGroup = root.YearGroup
        TargetGrade = root.TargetGrade
        NameLabelText.set(str("Name: "+Name+""))
        YearLabelText.set(str("Year: "+str(YearGroup)+""))
        TargetLabelText.set(str("Target Grade: " +TargetGrade))

        frameTree = Frame(self)
        tree = ttk.Treeview(frameTree)
        tree["columns"] = ("one", "two", "three")
        tree['show'] = 'headings'
        tree.column("one", width=500)
        tree.column("two", width=100)
        tree.column("three", width=200)
        tree.heading("one", text="Quiz Title")
        tree.heading("two", text="Result")
        tree.heading("three", text="Completed on")
        ysb = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
        tree['yscroll'] = ysb.set
        ysb.grid(in_=frameTree, row=0, column=1, sticky=NS)
        frameTree.grid(row=2, columnspan=100)
        tree.grid(in_=frameTree, row=0, column=0, sticky=NSEW)

        def ReverseList(l, first=0, last=-1):
            if first >= len(l)/2:
                return
            l[first], l[last] = l[last], l[first]
            ReverseList(l, first+1, last-1)

        def CheckSort(event):
            if sortvar.get() == "Newest first":
                reverse = True
                PopulateResults(reverse)
            else:
                reverse = False
                PopulateResults(reverse)

        sortvar=StringVar()
        lblSort = Label(self, text="Sort by:", bg="white", fg="#04286f", font=("Arial", 13, ''), wraplength="850")
        sortvar.set("Oldest first")
        comboSort = ttk.Combobox(self, textvariable=sortvar, state='readonly')
        comboSort['values'] = ('Oldest first','Newest first')
        comboSort.bind('<<ComboboxSelected>>', CheckSort)

        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnMenu.grid(row=3, columnspan=100)
        lblSort.grid(row=0, column=49, pady=10)
        comboSort.grid(row=0, column=50, pady=10)
        PopulateResults(reverse)


class framePreQuiz(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        root.title("Quizzel - %s" % (root.ChosenQuizTitle))

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameQuizSelection, parent)
            parent.pack(expand=1, fill=BOTH)

        def ProceedButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameQuiz, parent)
            parent.pack(expand=1, fill=BOTH)

        lblHeading = Label(self, text="On your marks...", bg="white", fg="blue", font=("Arial", 15, 'bold'))
        lblQuizTitle = Label(self, text="You are about to take: %s" % (root.ChosenQuizTitle[0]), bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblInfoText = Label(self, text="Think carefully when answering and take your time, there is no time limit. The results will be displayed once you have completed the quiz. Any questions you have answered wrong previously will be answered again.", bg="white", fg="#04286f", font=("Arial", 13, ''), wraplength="850")
        btnMenu = Button(self, command=MenuButton, text='< Back to Selection', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnProceed = Button(self, command=ProceedButton, text='''I'm ready! >''', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        lblHeading.grid(pady=19, columnspan=2, row=0)
        lblQuizTitle.grid(columnspan=2, row=1)
        lblInfoText.grid(pady=20, columnspan=2, row=2)
        btnProceed.grid(column=1, row=3)
        btnMenu.grid(column=0, row=3)

class frameQuiz(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        root.title("Quizzel - %s" % (root.ChosenQuizTitle))
        Choice = IntVar()
        root.CurrentQuestion = 0
        root.Score = 0
        A1Stack = []
        A2Stack = []
        A3Stack = []
        A4Stack = []
        strQuestionText = StringVar()
        strQuestionNo = StringVar()
        A1 = StringVar()
        A2 = StringVar()
        A3 = StringVar()
        A4 = StringVar()
        CorrectAStack = []

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameStudentMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def OpenQuiz():
            
            root.QuestionID = []
            root.QuestionStack = []
            root.WrongQuestion = []
            root.WrongAnswer = []
            root.CurrentQuestion = 1
            root.ShouldSave = False
            strQuestionNo.set("Question: 1")
            cursor.execute("SELECT QuestionID FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                root.QuestionID.append(row[0])
            root.AllQID = root.QuestionID

            cursor.execute("SELECT Question FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                root.QuestionStack.append(row[0])
            cursor.execute("SELECT Answer1 FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                A1Stack.append(row[0])
            cursor.execute("SELECT Answer2 FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                A2Stack.append(row[0])
            cursor.execute("SELECT Answer3 FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                A3Stack.append(row[0])
            cursor.execute("SELECT Answer4 FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                A4Stack.append(row[0])
            cursor.execute("SELECT CorrectAnswer FROM multichoicequestions WHERE QuizID=?",(root.ChosenQuiz,))
            for row in cursor:
                CorrectAStack.append(row[0])
            root.MaxScore = len(root.QuestionStack)
            if len(root.QuestionStack) == 1:
                btnNext.configure(command=DoneQuiz, text="Finish Quiz >", bg="green")
            ShuffleQuiz()
            SetLabels()

        def SetLabels():
            A1.set(A1Stack[len(A1Stack)-1])
            A2.set(A2Stack[len(A2Stack)-1])
            A3.set(A3Stack[len(A3Stack)-1])
            A4.set(A4Stack[len(A4Stack)-1])
            strQuestionText.set(root.QuestionStack[len(root.QuestionStack)-1])

        def ShuffleQuiz():
            combined = list(zip(root.QuestionStack, A1Stack, A2Stack, A3Stack, A4Stack, CorrectAStack, root.QuestionID))
            random.shuffle(combined)
            root.QuestionStack[:], A1Stack[:], A2Stack[:], A3Stack[:], A4Stack[:], CorrectAStack[:], root.QuestionID[:] = zip(*combined)


        def NextQuestion():
            C = Choice.get()
            rightorwrong = CheckAnswer()
            Q = str((root.MaxScore - len(root.QuestionStack)) + 2)
            strQuestionNo.set("Question: "+Q)
            root.CurrentQuestion = root.CurrentQuestion + 1
            if rightorwrong == True:
                root.Score = root.Score + 1
            for Stack in [A1Stack, A2Stack, A3Stack, A4Stack, root.QuestionStack, CorrectAStack]:
                    Stack.pop()
            if len(root.QuestionStack) == 1:
                btnNext.configure(command=DoneQuiz, text="Finish Quiz >", bg="green")
            if root.QuestionStack:
                strQuestionText.set(str(root.QuestionStack[len(root.QuestionStack)-1]))
                A1.set(str(A1Stack[len(A1Stack)-1]))
                A2.set(str(A2Stack[len(A2Stack)-1]))
                A3.set(str(A3Stack[len(A3Stack)-1]))
                A4.set(str(A4Stack[len(A4Stack)-1]))
            for A in [btnAnswer1, btnAnswer2, btnAnswer3, btnAnswer4]:
                A.deselect()
            Choice.set(0)

        def DoneQuiz():
            rightorwrong = CheckAnswer()
            if rightorwrong == True:
                root.Score = root.Score + 1
            root.ShouldSave = True
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(framePostQuiz, parent)
            parent.pack(expand=1, fill=BOTH)

        def CheckAnswer():
            C = Choice.get()
            if C == int(CorrectAStack[len(CorrectAStack)-1]):
                return True
            else:
                root.WrongAnswer.append(C)
                root.WrongQuestion.append(root.QuestionID[len(root.QuestionID)-1])
                root.QuestionID.pop()
                return False

        lblQuestionNumber = Label(self, textvariable=strQuestionNo, bg="white", fg="#04286f", font=("Arial", 15, 'bold'), wraplength="800")
        lblQuestionText = Label(self, textvariable=strQuestionText, bg="white", fg="#04286f", font=("Arial", 15, ''), wraplength="800")
        btnAnswer1 = Radiobutton(self, bg="#282828", offrelief=FLAT, wraplength="150", fg="white", activebackground="blue", selectcolor="blue", textvariable=A1, variable=Choice, value=1, indicatoron=0, width=20, height=4)
        btnAnswer2 = Radiobutton(self, bg="#282828", offrelief=FLAT, wraplength="150", fg="white", activebackground="blue", selectcolor="blue", textvariable=A2, variable=Choice, value=2, indicatoron=0, width=20, height=4)
        btnAnswer3 = Radiobutton(self, bg="#282828", offrelief=FLAT, wraplength="150", fg="white", activebackground="blue", selectcolor="blue", textvariable=A3, variable=Choice, value=3, indicatoron=0, width=20, height=4)
        btnAnswer4 = Radiobutton(self, bg="#282828", offrelief=FLAT, wraplength="150", fg="white", activebackground="blue", selectcolor="blue", textvariable=A4, variable=Choice, value=4, indicatoron=0, width=20, height=4)
        btnMenu = Button(self, command=MenuButton, text='< Leave Quiz', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnNext = Button(self, command=NextQuestion, text='Next Question >', relief=FLAT, bg=root.ButtonColour, fg="white", width='32')
        lblQuestionNumber.grid(row=0, columnspan=2)
        lblQuestionText.grid(columnspan=2)
        btnAnswer1.grid(row=2,column=0,padx=60,pady=30)
        btnAnswer2.grid(row=2,column=1,padx=60,pady=30)
        btnAnswer3.grid(row=3,column=0,padx=60,pady=30)
        btnAnswer4.grid(row=3,column=1,padx=60,pady=30)
        btnMenu.grid(column=0, row=4)
        btnNext.grid(column=1, row=4)
        try:
            OpenQuiz()
        except:
            tkinter.messagebox.showerror("Cannot Open Quiz","This quiz currently has no questions and therefore cannot be opened.")
            self.pack_forget()
            parent.pack_forget()
            frameStudentMenu.pack(self)
            parent.pack(expand=1, fill=BOTH)

class framePostQuiz(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Quiz Completed!")
        time_string = time.strftime('%d/%m/%Y, %H:%M')

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameStudentMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def ReviewButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameQuizReview, parent)
            parent.pack(expand=1, fill=BOTH)

        def SaveResults():
            Result = str(root.Score)+'/'+str(root.MaxScore)
            
            cursor.execute('INSERT INTO results(UserID, QuizID, Result, Time) VALUES(?,?,?,?)',(root.UserID,root.ChosenQuiz,Result,time_string))
            database.commit()
            

        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnReview = Button(self, command=ReviewButton, text='Review your answers >', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        lblQuizTitle = Label(self, text="Quiz Completed: %s" % (root.ChosenQuizTitle[0]), bg="white", fg="green", font=("Arial", 15, 'bold'))
        lblQuizTitle.grid(pady=19, columnspan=2)
        lblScore = Label(self, text="Relax... It's over! You have scored %s out of a total possible %s." % (root.Score, root.MaxScore), bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblScore.grid(columnspan=2)
        lblInfoText = Label(self, text="The results for this quiz will be saved. Select 'Review' too see where you went wrong feel free to repeat this quiz to improve your score.", bg="white", fg="#04286f", font=("Arial", 13, ''), wraplength="850")
        lblInfoText.grid(pady=20, columnspan=2)
        if not root.WrongQuestion:
            lblScore.configure(text="Amazing! You have scored a perfect %s out of %s!" % (root.Score, root.MaxScore))
            lblInfoText.configure(text="The results for this quiz will be saved.")
            btnMenu.grid(columnspan=2, row=5)
        else:
            btnMenu.grid(column=0, row=5)
            btnReview.grid(column=1, row=5)
        if root.ShouldSave:
            SaveResults()
            root.ShouldSave = False

class frameQuizReview(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Review Quiz")

        def PostQuizButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(framePostQuiz, parent)
            parent.pack(expand=1, fill=BOTH)

        def ListThings():
            r = 5
            btnPostQuiz = Button(self, command=PostQuizButton, text='< Back', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
            Label(self, text="Questions you have answered incorrectly:", bg="white", fg="#04286f", font=("Arial", 14, '')).grid(row=1, pady=19, columnspan=100)
            Label(self, text="Question:", bg="white", fg="#04286f", font=("Arial", 12, ''), anchor='w', justify=LEFT).grid(row=2, column=0, sticky='w', pady=20, padx=20)
            Label(self, text="Your Answer:", bg="white", fg="#04286f", font=("Arial", 12, ''), anchor='w', justify=LEFT).grid(row=2, column=1, sticky='w', pady=20, padx=20)
            
            for w in root.WrongQuestion:
                cursor.execute('''SELECT Question FROM multichoicequestions WHERE QuestionID=?''',(w,))
                QText = cursor.fetchone()
                r = r + 1
                Label(self, text=QText[0], bg="white", fg="#bc0000", font=("Arial", 12, ''), anchor='w', justify=LEFT).grid(row=r, column=0, sticky='w', padx=30)
            r = 5
            for a, b in zip(root.WrongAnswer, root.WrongQuestion):
                if a == 0:
                    AText = ["No answer"]
                else:
                    a = "Answer" + str(a)
                    cursor.execute('''SELECT %s FROM multichoicequestions WHERE QuestionID=?''' % (a), (b,))
                    AText = cursor.fetchone()
                r = r + 1
                Label(self, text=AText[0], bg="white", fg="#bc0000", font=("Arial", 12, ''), anchor='e', justify=RIGHT).grid(row=r, column=1, sticky='e', padx=20)
            r = r + 1
            btnPostQuiz.grid(row=r, columnspan=100, pady=19)

        ListThings()

class framePasswordChange(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Settings")
        CPOB = StringVar()
        BoxVar1 = StringVar()
        BoxVar2 = StringVar()

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameStudentMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def CheckBoxes():
            global newpass
            emptyhash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            old = CPOB.get().encode('utf-8')
            h = hashlib.sha256()
            h.update(old)
            old = h.hexdigest()
            new1 = BoxVar1.get().encode('utf-8')
            h = hashlib.sha256()
            h.update(new1)
            new1 = h.hexdigest()
            new2 = BoxVar2.get().encode('utf-8')
            h = hashlib.sha256()
            h.update(new2)
            new2 = h.hexdigest()
            
            cursor.execute('''SELECT * FROM Users WHERE Password=? AND UserID=? ''',(old,root.UserID))
            found = cursor.fetchone()
            if found:
                if new1 != emptyhash and new2 !=emptyhash:
                    if new1 == new2:
                        newpass = new1
                        boxNewPassword1.configure(bg="#cee1ff")
                        boxNewPassword2.configure(bg="#cee1ff")
                        boxCurrentPassword.configure(bg="#cee1ff")
                        return True
                    else:
                        lblOutput.configure(text="New passwords do not match.", fg="#bc0000")
                        boxCurrentPassword.configure(bg="#cee1ff")
                        boxNewPassword1.configure(bg="#bc0000")
                        boxNewPassword2.configure(bg="#bc0000")
                        return False
                else:
                    lblOutput.configure(text="Password field can not be left empty.", fg="#bc0000")
                    if new1 == emptyhash:
                        boxNewPassword2.configure(bg="#cee1ff")
                        boxCurrentPassword.configure(bg="#cee1ff")
                        boxNewPassword1.configure(bg="#bc0000")
                    if new2 == emptyhash:
                        boxNewPassword1.configure(bg="#cee1ff")
                        boxCurrentPassword.configure(bg="#cee1ff")
                        boxNewPassword2.configure(bg="#bc0000")
                    if new1 == emptyhash and new2 == emptyhash:
                        boxCurrentPassword.configure(bg="#cee1ff")
                        boxNewPassword1.configure(bg="#bc0000")
                        boxNewPassword2.configure(bg="#bc0000")
                    return False
            else:
                lblOutput.configure(text="Your password is incorrect, please try again", fg="#bc0000")
                boxNewPassword1.configure(bg="#cee1ff")
                boxNewPassword2.configure(bg="#cee1ff")
                boxCurrentPassword.configure(bg="#bc0000")
                return False

        def ChangePassword():
            allowed = CheckBoxes()
            if allowed:
                
                cursor.execute('''UPDATE users SET password=? WHERE UserID=? ''',(newpass,root.UserID))
                database.commit()
                
                lblOutput.configure(text="Password changed successfully!", fg="green")
                boxCurrentPassword.delete(0, END)
                boxNewPassword1.delete(0, END)
                boxNewPassword2.delete(0, END)
            else:
                CPOB = StringVar()
                BoxVar1 = StringVar()
                BoxVar2 = StringVar()

        lblTitle = Label(self, text="Update your password:", bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblOutput = Label(self, text="", bg="white", fg="red", font=("Arial", 12, ''))
        lblCurrentPassword = Label(self, text="Current password:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblNewPassword1 = Label(self, text="New password:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblNewPassword2 = Label(self, text="Confirm new password:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        boxCurrentPassword = Entry(self, textvariable=CPOB, relief=FLAT, bg="#cee1ff", width=40, show="●")
        boxNewPassword1 = Entry(self, textvariable=BoxVar1, relief=FLAT, bg="#cee1ff", width=40, show="●")
        boxNewPassword2 = Entry(self, textvariable=BoxVar2, relief=FLAT, bg="#cee1ff", width=40, show="●")
        btnUpdatePassword = Button(self, command=ChangePassword, text='Change Password', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='24')
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        lblTitle.grid(pady=4, columnspan=100)
        lblOutput.grid(pady=4, columnspan=100, row=1)
        lblCurrentPassword.grid(pady=4, column=0, row=2, sticky=E)
        boxCurrentPassword.grid(pady=7, column=1, row=2)
        lblNewPassword1.grid(pady=4, column=0, row=3, sticky=E)
        boxNewPassword1.grid(pady=7, column=1, row=3)
        lblNewPassword2.grid(pady=4, column=0, row=4, sticky=E)
        boxNewPassword2.grid(pady=7, column=1, row=4)
        btnUpdatePassword.grid(pady=3, columnspan=100)
        btnMenu.grid(pady=10, columnspan=100)

class frameNewUser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - New User")
        YearGroupList = ['Select One', '10', '11', '12', '13']
        ChosenYear = StringVar()
        TypeList = ['Select One','Student','Teacher']
        ChosenType = StringVar()
        FirstName = StringVar()
        LastName = StringVar()
        Username = StringVar()
        TargetList = ['Select One', 'A*','A','B','C','D','E','U']
        ChosenTarget = StringVar()
        ChosenSubjects = []
        AllSubjectList = []

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameTeacherMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def FillSubjectList():
            global AllSubjectList
            AllSubjectList = []
            
            cursor.execute('''SELECT SubjectID FROM subjects''')
            AllSubjects = cursor.fetchall()
            for ID in AllSubjects:
                ID = str(ID[0])
                cursor.execute('''SELECT SubjectName FROM subjects WHERE SubjectID=?''',ID)
                SName = cursor.fetchone()
                for S in SName:
                    listboxSubjects.insert(ID, S)
                    AllSubjectList.append(ID)

        def GetChosenSubjects():
            global AllSubjectList, ChosenSubjects
            ChosenSubjects = []
            SubjectListIndex = listboxSubjects.curselection()
            for pos in SubjectListIndex:
                ChosenSubjects.append(AllSubjectList[pos])
            return ChosenSubjects

        def CheckBoxes():
            cursor.execute('''SELECT Username FROM users''')
            if (ChosenType.get()).upper() == "SELECT ONE":
                    boxFirstName.configure(bg="#cee1ff")
                    boxLastName.configure(bg="#cee1ff")
                    boxUserName.configure(bg="#cee1ff")
                    lblOutput.configure(text="You must select a type of user.", fg="#bc0000")
                    return False
            if FirstName.get() == '':
                    boxFirstName.configure(bg="#bc0000")
                    boxLastName.configure(bg="#cee1ff")
                    boxUserName.configure(bg="#cee1ff")
                    lblOutput.configure(text="You must enter a First Name.", fg="#bc0000")
                    return False
            if LastName.get() == '':
                    boxFirstName.configure(bg="#cee1ff")
                    boxLastName.configure(bg="#bc0000")
                    boxUserName.configure(bg="#cee1ff")
                    lblOutput.configure(text="You must enter a Last Name.", fg="#bc0000")
                    return False
            if (ChosenYear.get()).upper() == "SELECT ONE" and (ChosenType.get()).upper() == "STUDENT":
                    boxFirstName.configure(bg="#cee1ff")
                    boxLastName.configure(bg="#cee1ff")
                    boxUserName.configure(bg="#cee1ff")
                    lblOutput.configure(text="You must select a year group.", fg="#bc0000")
                    return False
            for ExistingUsername in cursor:
                for s in ['(', ')', ',',"'"]:
                    ExistingUsername = str(ExistingUsername).strip(s)
                if ExistingUsername.upper() == (Username.get()).upper():
                    #Username already in the database
                    boxFirstName.configure(bg="#cee1ff")
                    boxLastName.configure(bg="#cee1ff")
                    boxUserName.configure(bg="#bc0000")
                    lblOutput.configure(text="A user with that username already exists. Please choose a different one.", fg="#bc0000")
                    return False
            if Username.get() == '':
                #Username is blank
                boxFirstName.configure(bg="#cee1ff")
                boxLastName.configure(bg="#cee1ff")
                boxUserName.configure(bg="#bc0000")
                lblOutput.configure(text="The username cannot be left blank.", fg="#bc0000")
                return False
            if ' ' in Username.get():
                #Username has a space
                boxFirstName.configure(bg="#cee1ff")
                boxLastName.configure(bg="#cee1ff")
                boxUserName.configure(bg="#bc0000")
                lblOutput.configure(text="A username cannot contain a space.", fg="#bc0000")
                return False
            if (ChosenTarget.get()).upper() == "SELECT ONE" and (ChosenType.get()).upper() == "STUDENT":
                boxFirstName.configure(bg="#cee1ff")
                boxLastName.configure(bg="#cee1ff")
                boxUserName.configure(bg="#cee1ff")
                lblOutput.configure(text="You must select a target grade.", fg="#bc0000")
                return False
            selection = listboxSubjects.curselection()
            if not selection and (ChosenType.get()).upper() == "STUDENT":
                boxFirstName.configure(bg="#cee1ff")
                boxLastName.configure(bg="#cee1ff")
                boxUserName.configure(bg="#cee1ff")
                lblOutput.configure(text="You must select at least one subject.", fg="#bc0000")
                return False
            boxFirstName.configure(bg="#cee1ff")
            boxLastName.configure(bg="#cee1ff")
            boxUserName.configure(bg="#cee1ff")
            lblOutput.configure(text="User added successfully!", fg="green")
            return True

        def AddUser():
            FirstTime = 1
            emptyhash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            if CheckBoxes():
                if ChosenType.get() == "Teacher":
                    Type = 1
                    ChosenSubjects = None
                    TargetGrade = None
                    YearGroup = None
                if ChosenType.get() == "Student":
                    Type = 0
                    TargetGrade = ChosenTarget.get()
                    ChosenSubjects = GetChosenSubjects()
                    ChosenSubjects = ', '.join(map(str, ChosenSubjects))
                    YearGroup = ChosenYear.get()
                FullName = FirstName.get() + ' ' + LastName.get()
                FullName = FullName.title()
                
                cursor.execute('''INSERT INTO users VALUES (?,?,?,?,?,?,?,?,1)''', (None, FullName, YearGroup, Username.get(), emptyhash, Type, TargetGrade, ChosenSubjects))
                database.commit()
                

        def Refresh():
            if ChosenType.get() == "Teacher":
                dropdownTarget.configure(state="disabled")
                listboxSubjects.configure(state="disabled")
                dropdownYear.configure(state="disabled")
            if ChosenType.get() == "Student":
                dropdownTarget.configure(state="normal")
                listboxSubjects.configure(state="normal")
                dropdownYear.configure(state="normal")

        def on_trace_choice(name, index, mode):
            Refresh()

        lblTitle = Label(self, text="Add a new user:", bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblOutput = Label(self, text="", bg="white", fg="red", font=("Arial", 12, ''))
        lblType = Label(self, text="Type:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblFirstName = Label(self, text="First Name:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblLastName = Label(self, text="Last Name:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblYearGroup = Label(self, text="Year Group: ", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblUsername = Label(self, text="Username: ", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblTargetGrade = Label(self, text="Target Grade: ", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblSubjects = Label(self, text="Subjects: (Select all that apply)", bg="white", fg="#04286f", font=("Arial", 12, ''))
        dropdownType = ttk.OptionMenu(self, ChosenType, *TypeList)
        dropdownType.configure(width=40)
        boxFirstName = Entry(self, relief=FLAT, textvariable=FirstName, bg="#cee1ff", width=45)
        boxLastName = Entry(self, relief=FLAT, textvariable=LastName, bg="#cee1ff", width=45)
        dropdownYear = ttk.OptionMenu(self, ChosenYear, *YearGroupList)
        dropdownYear.configure(width=40)
        dropdownTarget = ttk.OptionMenu(self, ChosenTarget, *TargetList)
        dropdownTarget.configure(width=40)
        boxUserName = Entry(self, relief=FLAT, bg="#cee1ff", textvariable=Username, width=45)
        listboxSubjects = Listbox(self, selectmode=MULTIPLE, height=10, width=75)
        btnAddUser = Button(self, command=AddUser, text='Add User', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='24')
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')

        lblTitle.grid(pady=4, columnspan=100, row=0)
        lblOutput.grid(pady=4, columnspan=100, row=1)
        lblType.grid(pady=4, column=0, row=2, sticky=E)
        lblFirstName.grid(pady=4, column=0, row=3, sticky=E)
        lblLastName.grid(pady=4, column=0, row=4, sticky=E)
        lblYearGroup.grid(pady=4, column=0, row=5, sticky=E)
        lblUsername.grid(pady=4, column=0, row=6, sticky=E)
        lblTargetGrade.grid(pady=4, column=0, row=7, sticky=E)
        lblSubjects.grid(pady=4, column=0, row=8, sticky=E)
        dropdownType.grid(pady=7, column=1, row=2)
        boxFirstName.grid(pady=7, column=1, row=3)
        boxLastName.grid(pady=7, column=1, row=4)
        dropdownYear.grid(pady=7, column=1, row=5)
        boxUserName.grid(pady=7, column=1, row=6)
        dropdownTarget.grid(pady=7, column=1, row=7)
        listboxSubjects.grid(pady=7, row=9, columnspan=2)
        btnAddUser.grid(pady=10, columnspan=100, row=11)
        btnMenu.grid(pady=10, columnspan=100, row=12)
        FillSubjectList()

        ChosenType.trace("w", on_trace_choice)

class frameModifyQuizSelector(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Modify Quiz")
        root.ModifyQuizID = None
        root.ModifyChooserList = []

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameTeacherMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def Proceed():
            ChooserListIndex = listboxQuiz.index(ACTIVE)
            QuizID = root.ModifyChooserList[ChooserListIndex]
            root.ModifyQuizID = QuizID
            if root.ModifyQuizID == "create":
                self.pack_forget()
                parent.pack_forget()
                controller.PackFrame(frameNewQuiz, parent)
                parent.pack(expand=1, fill=BOTH)
            else:
                self.pack_forget()
                parent.pack_forget()
                controller.PackFrame(frameAddQuestion, parent)
                parent.pack(expand=1, fill=BOTH)


        def FillQuizList():
            root.QuizItems = []
            root.ChooserList = []
            root.QuizIDSearch = []
            listboxQuiz.insert(END, "<Create new quiz>")
            root.ModifyChooserList.append("create")
            
            cursor.execute('SELECT QuizID FROM Quizzes')
            AllQuizzes = cursor.fetchall()
            for i in AllQuizzes:
                i = i[0]
                cursor.execute('''SELECT QuizTitle FROM Quizzes WHERE QuizID=?''',(i,))
                QuizName = cursor.fetchone()
                cursor.execute('''SELECT SubjectID FROM Quizzes WHERE QuizID=?''',(i,))
                SubjectID = cursor.fetchone()
                cursor.execute('''SELECT SubjectName FROM subjects WHERE SubjectID=?''',(SubjectID[0],))
                SubjectName = cursor.fetchone()
                if QuizName != None:
                    root.ModifyChooserList.append(i)
                    ListItem = "%s - %s" %(SubjectName[0],QuizName[0])
                    listboxQuiz.insert(END, ListItem)

        lblQuizList = Label(self, text="Please select a Quiz from the list below: ", bg="white", fg="#04286f", font=("Arial", 13, 'bold'))
        listboxQuiz = Listbox(self, width=110, height=20)
        btnSelectQuiz = Button(self, command=Proceed, text='Next >', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        FillQuizList()
        lblQuizList.grid(row=1, pady=9, columnspan=6)
        listboxQuiz.grid(columnspan=6, pady=3)
        btnMenu.grid(pady=17, column=0, row=5)
        btnSelectQuiz.grid(pady=17, column=5, row=5)

class frameNewQuiz(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title('Quizzel - New Quiz')
        NameOfQuiz = StringVar()
        AllSubjectList = []
        root.ModifyQuizID = None

        def CheckBoxes():
            boxQuizName.configure(bg="#cee1ff")
            lblOutput.configure(fg="red", text="")
            if NameOfQuiz.get() == "":
                lblOutput.configure(fg="red", text="You must pick a title for the quiz.")
                boxQuizName.configure(bg="#bc0000")
                return False
            selection = listboxSubjects.index(ACTIVE)
            if not selection:
                boxQuizName.configure(bg="#cee1ff")
                lblOutput.configure(fg="red", text="You must pick a subject.")
                return False
            return True

        def GetSubject():
            global AllSubjectList, ChosenSubjects
            ChosenSubject = []
            pos = listboxSubjects.index(ACTIVE)
            ChosenSubject.append(AllSubjectList[pos])
            return ChosenSubject

        def AddQuiz():
            SubjectID = GetSubject()
            QuizTitle = NameOfQuiz.get()
            if CheckBoxes():
                lblOutput.configure(fg="green", text="Quiz added successfully!")
                
                cursor.execute('''INSERT INTO quizzes VALUES(?,?,?,1)''',(None, SubjectID[0], QuizTitle))
                database.commit()
                

        def FillSubjectList():
            global AllSubjectList
            AllSubjectList = []
            
            cursor.execute('''SELECT SubjectID FROM subjects''')
            AllSubjects = cursor.fetchall()
            for ID in AllSubjects:
                ID = str(ID[0])
                cursor.execute('''SELECT SubjectName FROM subjects WHERE SubjectID=?''',ID)
                SName = cursor.fetchone()
                for S in SName:
                    listboxSubjects.insert(ID, S)
                    AllSubjectList.append(ID)

        def BackButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameModifyQuizSelector, parent)
            parent.pack(expand=1, fill=BOTH)

        lblTitle = Label(self, text="Create new quiz:", bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblOutput = Label(self, text="", bg="white", fg="red", font=("Arial", 12, ''))
        lblQuizName = Label(self, text="Quiz Name:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        boxQuizName = Entry(self, relief=FLAT, textvariable=NameOfQuiz, bg="#cee1ff", width=45)
        lblSubject = Label(self, text="Subject:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        listboxSubjects = Listbox(self, height=10, width=75)
        btnBack = Button(self, command=BackButton, text='< Back', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnAddQuiz = Button(self, command=AddQuiz, text='Add Quiz', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')

        lblTitle.grid()
        lblOutput.grid()
        lblQuizName.grid()
        boxQuizName.grid()
        lblSubject.grid()
        listboxSubjects.grid()
        btnAddQuiz.grid(pady=17, column=0, row=7)
        btnBack.grid(pady=17, column=0, row=9)
        FillSubjectList()


class frameAddQuestion(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title('Quizzel - Add Questoin')
        Question = StringVar()
        Answer1 = StringVar()
        Answer2 = StringVar()
        Answer3 = StringVar()
        Answer4 = StringVar()
        PossibleChoice =['Select One', '1','2','3','4']
        CorrectAnswer = StringVar()

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameTeacherMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def Refresh():
            if int(CorrectAnswer.get()) == 1:
                boxAnswer1.configure(bg="light green")
                boxAnswer2.configure(bg="#cee1ff")
                boxAnswer3.configure(bg="#cee1ff")
                boxAnswer4.configure(bg="#cee1ff")
            if int(CorrectAnswer.get()) == 2:
                boxAnswer2.configure(bg="light green")
                boxAnswer1.configure(bg="#cee1ff")
                boxAnswer3.configure(bg="#cee1ff")
                boxAnswer4.configure(bg="#cee1ff")
            if int(CorrectAnswer.get()) == 3:
                boxAnswer3.configure(bg="light green")
                boxAnswer1.configure(bg="#cee1ff")
                boxAnswer2.configure(bg="#cee1ff")
                boxAnswer4.configure(bg="#cee1ff")
            if int(CorrectAnswer.get()) == 4:
                boxAnswer4.configure(bg="light green")
                boxAnswer1.configure(bg="#cee1ff")
                boxAnswer2.configure(bg="#cee1ff")
                boxAnswer3.configure(bg="#cee1ff")

        def CheckBoxes():
            for b in [boxQuestion, boxAnswer1, boxAnswer2, boxAnswer3, boxAnswer4]:
                b.configure(bg="#cee1ff")
            if Question.get() == "":
                boxQuestion.configure(bg="#bc0000")
                lblOutput.configure(fg="red", text="You cannot leave the question box empty")
                return False
            if Answer1.get() == "" or Answer2.get() == "" or Answer3.get() == "" or Answer4.get() == "":
                lblOutput.configure(fg="red", text="You must fill in all answers")
                for b in [boxQuestion, boxAnswer1, boxAnswer2, boxAnswer3, boxAnswer4]:
                    b.configure(bg="#bc0000")
                return False
            return True

        def AddQuestion():
            A1 = Answer1.get()
            A2 = Answer2.get()
            A3 = Answer3.get()
            A4 = Answer4.get()
            Q = Question.get()
            Correct = CorrectAnswer.get()
            if CheckBoxes():
                for b in [boxQuestion, boxAnswer1, boxAnswer2, boxAnswer3, boxAnswer4]:
                    b.delete(0, END)
                
                cursor.execute('''INSERT INTO multichoicequestions VALUES(?,?,?,?,?,?,?,?)''',(None, root.ModifyQuizID, Q, A1, A2, A3, A4, Correct))
                database.commit()
                
                lblOutput.configure(fg="green", text="Question added successfully!")

        def on_trace_choice(name, index, mode):
            Refresh()

        lblTitle = Label(self, text="Add questions to an existing quiz:", bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblOutput = Label(self, text="", bg="white", fg="red", font=("Arial", 12, ''))
        lblQuestion = Label(self, text="Question:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblChoice1 = Label(self, text="Choice 1:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblChoice2 = Label(self, text="Choice 2:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblChoice3 = Label(self, text="Choice 3:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblChoice4 = Label(self, text="Choice 4:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblCorrectAnswer = Label(self, text="Correct Answer:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        boxQuestion = Entry(self, relief=FLAT, textvariable=Question, bg="#cee1ff", width=60)
        boxAnswer1 = Entry(self, relief=FLAT, textvariable=Answer1, bg="#cee1ff", width=25)
        boxAnswer2 = Entry(self, relief=FLAT, textvariable=Answer2, bg="#cee1ff", width=25)
        boxAnswer3 = Entry(self, relief=FLAT, textvariable=Answer3, bg="#cee1ff", width=25)
        boxAnswer4 = Entry(self, relief=FLAT, textvariable=Answer4, bg="#cee1ff", width=25)
        comboCorrectAnswer = ttk.OptionMenu(self, CorrectAnswer, *PossibleChoice)
        comboCorrectAnswer.configure(width=20)
        btnAddQuestion = Button(self, command=AddQuestion, text='Add Question', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        lblTitle.grid(row=0, pady=19, columnspan=20)
        lblOutput.grid(row=1, columnspan=20)
        lblQuestion.grid(row=2, columnspan=20)
        lblChoice1.grid(column=0, row=4)
        lblChoice2.grid(column=1, row=4)
        lblChoice3.grid(column=0, row=6)
        lblChoice4.grid(column=1, row=6)
        lblCorrectAnswer.grid(columnspan=20, row=8)
        boxQuestion.grid(columnspan=20, row=3, pady=7)
        boxAnswer1.grid(column=0, row=5, pady=7, padx=20)
        boxAnswer2.grid(column=1, row=5, pady=7, padx=20)
        boxAnswer3.grid(column=0, row=7, pady=7, padx=20)
        boxAnswer4.grid(column=1, row=7, pady=7, padx=20)
        comboCorrectAnswer.grid(columnspan=20, row=9, pady=7)
        btnAddQuestion.grid(row=13, columnspan=20, pady=17)
        btnMenu.grid(row=14, columnspan=20, pady=17)
        CorrectAnswer.trace("w", on_trace_choice)

class frameModifyUser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Add or Remove Users")
        AllUsersList = []

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameTeacherMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def Proceed():
            ChooserListIndex = listboxUsers.index(ACTIVE)
            UserID = root.ModifyUserList[ChooserListIndex]
            root.ModifyUserID = UserID
            if root.ModifyUserID == "create":
                self.pack_forget()
                parent.pack_forget()
                controller.PackFrame(frameNewUser, parent)
                parent.pack(expand=1, fill=BOTH)
            else:
                self.pack_forget()
                parent.pack_forget()
                controller.PackFrame(frameRemoveUser, parent)
                parent.pack(expand=1, fill=BOTH)

        def FillUserList():
            root.ModifyUserList = []
            listboxUsers.insert(END, "<Create new user>")
            root.ModifyUserList.append("create")
            
            cursor.execute('SELECT UserID FROM Users')
            AllUsers = cursor.fetchall()
            for i in AllUsers:
                i = i[0]
                cursor.execute('''SELECT Name FROM users WHERE UserID=?''',(i,))
                Name = cursor.fetchone()
                cursor.execute('''SELECT YearGroup FROM users WHERE UserID=?''',(i,))
                Year = cursor.fetchone()
                if Year[0] == None:
                    root.ModifyUserList.append(i)
                    ListItem = Name[0] + ' ' + '(Teacher)'
                    listboxUsers.insert(END, ListItem)
                elif Name != None:
                    root.ModifyUserList.append(i)
                    ListItem = Name[0] + ' ' + '(' + "Year " + str(Year[0]) +')'
                    listboxUsers.insert(END, ListItem)

        listboxUsers = Listbox(self, width=110, height=20)
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnProceed = Button(self, command=Proceed, text='Next >', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        listboxUsers.grid(pady=20, row=0, columnspan=3)
        btnMenu.grid(pady=10, column=0, row=1)
        btnProceed.grid(pady=10, column=2, row=1)
        FillUserList()

class frameRemoveUser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        cursor.execute('''SELECT Name FROM users WHERE UserID=?''', (root.ModifyUserID,))
        Name = cursor.fetchone()
        controller.title("Quizzel - Remove User")

        def BackButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameModifyUser, parent)
            parent.pack(expand=1, fill=BOTH)

        def DeleteUser():
            
            cursor.execute('''DELETE FROM users WHERE UserID=?''',(root.ModifyUserID,))
            database.commit()
            
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameModifyUser, parent)
            parent.pack(expand=1, fill=BOTH)

        lblTitle = Label(self, text="Remove User: %s" % (Name[0]), bg="white", fg="#bc0000", font=("Arial", 15, 'bold'))
        lblInfoText = Label(self, text="You are about to remove this user. Click proceed to continue or click cancel to go back.", bg="white", fg="#04286f", font=("Arial", 12))
        btnBack = Button(self, command=BackButton, text='< Back', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        btnDelete = Button(self, command=DeleteUser, text='Delete >', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')
        lblTitle.grid(columnspan=3, row=0, pady=20)
        lblInfoText.grid(columnspan=3, row=1, pady=10)
        btnBack.grid(pady=10, column=0, row=2)
        btnDelete.grid(pady=10, column=2, row=2)

class frameNewSubject(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, bg="white")
        controller.title("Quizzel - Add Subject")
        PrefixList = ['Select..','AS','A2','GCSE','BTEC','<None>']
        ChosenPrefix = StringVar()
        SubjectName = StringVar()

        def MenuButton():
            self.pack_forget()
            parent.pack_forget()
            controller.PackFrame(frameTeacherMenu, parent)
            parent.pack(expand=1, fill=BOTH)

        def CheckBoxes():
            lblOutput.configure(text="", fg="red")
            boxSubjectName.configure(bg="#cee1ff")
            if ChosenPrefix.get() == 'Select..':
                lblOutput.configure(text="Please select a prefix or select <None> for no prefix.", fg="red")
                return False
            if SubjectName.get() == '':
                lblOutput.configure(text="You must enter a subject name.", fg="red")
                return False
            
            cursor.execute('''SELECT SubjectName from subjects''')
            for existingsubjectname in cursor:
                for s in ['(', ')', ',',"'"]:
                    existingsubjectname = str(existingsubjectname).strip(s)
                if FinalName == existingsubjectname:
                    lblOutput.configure(text="This subject already exists", fg="red")
                    boxSubjectName.configure(bg="#bc0000")
                    return False
            return True

        def AddSubject():
            global FinalName
            if ChosenPrefix.get() == '<None>':
                FinalName = SubjectName.get()
            else:
                FinalName = ChosenPrefix.get() + ' ' + SubjectName.get()
            if CheckBoxes():
                
                cursor.execute('''INSERT INTO subjects VALUES (?,?)''', (None, FinalName))
                database.commit()
                
                lblOutput.configure(text="Subject added successfully!", fg="green")

        lblTitle = Label(self, text="Add a new subject:", bg="white", fg="#04286f", font=("Arial", 14, ''))
        lblOutput = Label(self, text="", bg="white", fg="red", font=("Arial", 12, ''))
        lblPrefix = Label(self, text="Prefix:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        lblSubjectTitle = Label(self, text="Subject Title:", bg="white", fg="#04286f", font=("Arial", 12, ''))
        comboPrefix = ttk.OptionMenu(self, ChosenPrefix, *PrefixList)
        comboPrefix.configure(width=7)
        boxSubjectName = Entry(self, relief=FLAT, textvariable=SubjectName, bg="#cee1ff", width=30)
        btnAddUser = Button(self, command=AddSubject, text='Add Subject', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='24')
        btnMenu = Button(self, command=MenuButton, text='< Back to Menu', relief=FLAT, overrelief=SUNKEN, bg=root.ButtonColour, fg="white", activebackground="#04286f", width='32')

        lblTitle.grid(pady=4, columnspan=3, row=0)
        lblOutput.grid(pady=4, columnspan=3, row=1)
        lblPrefix.grid(pady=4, column=1, row=2)
        lblSubjectTitle.grid(pady=4, column=2, row=2)
        comboPrefix.grid(pady=7, column=1, row=3, padx=5)
        boxSubjectName.grid(pady=7, column=2, row=3, padx=5)
        btnAddUser.grid(pady=10, columnspan=3, row=4)
        btnMenu.grid(pady=10, columnspan=3, row=5)


if __name__ == '__main__':
    root = App()
    root.mainloop()
