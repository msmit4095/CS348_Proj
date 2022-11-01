from atexit import register
import tkinter as tk
import tkinter.font as TkFont
import mysql.connector 
from tkinter import BOTH, DISABLED, END, LEFT, Tk
from tkinter import *


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = TkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        width=600
        height=500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title=tk.Label(self)
        ft = TkFont.Font(family='Times',size=38)
        title["font"] = ft
        title["fg"] = "#333333"
        title["justify"] = "center"
        title["text"] = "FlixList"
        title.place(x=180,y=110,width=234,height=72)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()



        
        register_button = tk.Button(self, text="Register",
                            )
                            
        register_button["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        register_button["font"] = ft
        register_button["fg"] = "#000000"
        register_button["justify"] = "center"
        register_button["text"] = "Register"
        register_button.place(x=310,y=300,width=128,height=36)


        self.username_entry=tk.Entry(self)
        self.username_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.username_entry["font"] = ft
        self.username_entry["fg"] = "#333333"
        self.username_entry["justify"] = "center"
        self.username_entry["textvariable"] = self.username_var
        #username_var = self.username_entry["textvariable"]
 
        self.username_entry.place(x=170,y=240,width=128,height=35)
        #self.username_entry.insert(0,"Username")


        self.password_entry=tk.Entry(self)
        self.password_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.password_entry["font"] = ft
        self.password_entry["fg"] = "#333333"
        self.password_entry["justify"] = "center"
        self.password_entry["textvariable"] = self.password_var
        #password_var = self.password_entry["textvariable"]

        self.password_entry.place(x=310,y=240,width=128,height=36)
        #self.password_entry.insert(0,"Password")

        login = tk.Button(self, text="Login", command=lambda:self.validateLogin(self,self.username_var,self.password_var,controller))
        login["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        login["font"] = ft
        login["fg"] = "#000000"
        login["justify"] = "center"
        login["text"] = "Login"
        login.place(x=170,y=300,width=128,height=36)
        #self.updateUsernamePassword()



    @staticmethod
    def validateLogin(self,username,password,controller):
        print("username entered :", username.get())
        print("password entered :", password.get())
        if username.get() == "test" and password.get():
            self.controller = controller
            controller.show_frame("PageOne")
            username.set("")
            password.set("")


        return






class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        logoutButton=tk.Button(self)
        logoutButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        logoutButton["font"] = ft
        logoutButton["fg"] = "#000000"
        logoutButton["justify"] = "center"
        logoutButton["text"] = "Logout"
        logoutButton["command"] =command=lambda: controller.show_frame("StartPage")
        logoutButton.place(x=500,y=0,width=96,height=43)


        SettingsButton=tk.Button(self)
        SettingsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        SettingsButton["font"] = ft
        SettingsButton["fg"] = "#000000"
        SettingsButton["justify"] = "center"
        SettingsButton["text"] = "Settings"
        SettingsButton.place(x=410,y=0,width=96,height=43)


        ReviewsButton=tk.Button(self)
        ReviewsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        ReviewsButton["font"] = ft
        ReviewsButton["fg"] = "#000000"
        ReviewsButton["justify"] = "center"
        ReviewsButton["text"] = "Reviews"
        ReviewsButton.place(x=320,y=0,width=96,height=43)


        MoviesButton=tk.Button(self)
        MoviesButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        MoviesButton["font"] = ft
        MoviesButton["fg"] = "#000000"
        MoviesButton["justify"] = "center"
        MoviesButton["text"] = "Movies"
        MoviesButton.place(x=230,y=0,width=96,height=43)


        TVButton=tk.Button(self)
        TVButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        TVButton["font"] = ft
        TVButton["fg"] = "#000000"
        TVButton["justify"] = "center"
        TVButton["text"] = "TV shows"
        TVButton["command"] = command=lambda: controller.show_frame("PageTwo");
        TVButton.place(x=140,y=0,width=96,height=43)


        TitleLabel=tk.Label(self)
        ft = TkFont.Font(family='Times',size=10)
        TitleLabel["font"] = ft
        TitleLabel["fg"] = "#333333"
        TitleLabel["justify"] = "center"
        TitleLabel["text"] = "FlixList"
        TitleLabel.place(x=0,y=0,width=70,height=25)





        #button = tk.Button(self, text="Go to the start page",
        #                   command=lambda: controller.show_frame("StartPage"))
        #button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("PageOne"),height= 1, width=8)
        #button.pack()
        button.grid(row=10,column=0)
        
        id_label = tk.Label(self,text="Movie id")
        id_label.grid(row=0,column=0,sticky=W,pady=2)
        id_label = tk.Label(self,text="Title")
        id_label.grid(row=0,column=1,sticky=W,pady=2)
        id_label = tk.Label(self,text="Duration")
        id_label.grid(row=0,column=2,sticky=W,pady=2)      
        id_label = tk.Label(self,text="Year")
        id_label.grid(row=0,column=3,sticky=W,pady=2)
        id_label = tk.Label(self,text="Director")
        id_label.grid(row=0,column=4,sticky=W,pady=2)  
        
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        my_cursor.execute("SELECT * FROM movies limit 0, 10")
        i =1
        j=0
        for movies in my_cursor:
            for j in range(len(movies)-1):
               e = tk.Entry(self,width=15,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,movies[j])
               e.config(state=DISABLED)
               #print(movies[j])
            i=i+1;
        #label = tk.Label(self, text="This is page 2", font=controller.title_font)
        #label.grid(row=9,column=0)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()