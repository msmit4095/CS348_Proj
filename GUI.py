from atexit import register
import tkinter as tk
import tkinter.font as TkFont
import mysql.connector
from tkinter import BOTH, DISABLED, END, LEFT, Tk
from tkinter import *

tempId = -1
tempEpId= -1
tempString= ""
curUserID = ""
curUsername = ""


class SampleApp(tk.Tk):


    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = TkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        width=1280
        height=720
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
        for F in (StartPage, MainPage, MoviePage, TVPage, MovieDetailPage,SettingsPage,TVDetailPage, ReviewPage):
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
    def show_frameSPECIAL(self, page_name, id):
        '''Show a frame for the given page name , but set global var to id'''
        global tempId
        global tempString
        tempId = str(id)
        frame = self.frames[page_name]
        frame.tkraise()
    def show_frameSPECIALTV(self, page_name, id,ep_id):
        '''Show a frame for the given page name , but set global var to id'''
        global tempId
        global tempString
        global tempEpId
        tempId = str(id)
        tempEpId = ep_id
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



        
        register_button = tk.Button(self, text="Register",command=lambda:self.registerUser(self,self.username_var,self.password_var,controller)
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
    def validateLogin(self,username,password1,controller):
        print("username entered :", username.get())
        print("password entered :", password1.get())
        
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        global curUserID
        global curUsername
        
        my_cursor.execute("SELECT * FROM users WHERE username = \'" +username.get()+ "\'")
        #print("SELECT * FROM users WHERE username = \'" +username.get()+ "\'")

        rows = my_cursor.fetchall()
        #print(rows)
        if rows:
            #print(rows)
            print("success")
        else:
            print("error")
            #rint(my_cursor.rowcount)
            return
        
        dbPass = ""
        
        for epic in rows:
            dbPass = epic[2]
            curUsername = epic[1]
            curUserID = epic[0]
        
        if dbPass == password1.get():
            self.controller = controller
            controller.show_frame("MainPage")
            username.set("")
            password1.set("")
            

        return
    
    @staticmethod
    def registerUser(self,username,password1,controller):
        
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        global curUserID
        global curUsername
        
        args =[username.get(),password1.get()]
        
        my_cursor.callproc("AddUser", args)

        self.controller = controller
        controller.show_frame("MainPage")
        curUsername = username.get()
        username.set("")
        password1.set("") 
        my_connect.commit() 
        
        
        return
        
        
        
  
  
class TVPage(tk.Frame):

  def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      title=tk.Label(self)
      button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("MainPage"),height= 1, width=8)
        #button.pack()
      button.grid(row=0,column=7)

        
      id_label = tk.Label(self,text="Show id")
      id_label.grid(row=0,column=0,sticky=W,pady=2)
      id_label = tk.Label(self,text="Episode")
      id_label.grid(row=0,column=1,sticky=W,pady=2)
      id_label = tk.Label(self,text="Show")
      id_label.grid(row=0,column=2,sticky=W,pady=2) 
      id_label = tk.Label(self,text="Episode Title")
      id_label.grid(row=0,column=3,sticky=W,pady=2)      
      id_label = tk.Label(self,text="Duration")
      id_label.grid(row=0,column=4,sticky=W,pady=2)
      id_label = tk.Label(self,text="ReleaseDate")
      id_label.grid(row=0,column=5,sticky=W,pady=2)  
      id_label = tk.Label(self,text="Director")
      id_label.grid(row=0,column=6,sticky=W,pady=2)

    
      my_connect = mysql.connector.connect(
        host="35.188.140.250",
        user="root",
        passwd="12345",
        database="proj_db"
      )
      my_cursor = my_connect.cursor()
    
      my_cursor.execute("SELECT * FROM episodes limit 0, 100")
      i =1
      showid = 0
      temp = 0
      j=0
      for shows in my_cursor:
        for j in range(len(shows)):
            e = tk.Entry(self,width=15,fg='blue')
            e.grid(row=i,column=j)
            e.insert(END,shows[j])
            e.config(state=DISABLED)
            #print(shows)
            if j == 1:
              buttonTemp = tk.Button(self, text="View",
                           command=lambda shows = shows: controller.show_frameSPECIALTV("TVDetailPage",shows[0],shows[1]),height= 1, width=8)
            
              buttonTemp.grid(row=i,column=7)
        i=i+1
        #label = tk.Label(self, text="This is page 2", font=controller.title_font)
        #label.grid(row=9,column=0)
        







class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        #label.grid(row=0, column=0, pady=10)
        
        self.wha = int()

        logoutButton=tk.Button(self)
        logoutButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        logoutButton["font"] = ft
        logoutButton["fg"] = "#000000"
        logoutButton["justify"] = "center"
        logoutButton["text"] = "Logout"
        logoutButton["command"] =command=lambda: controller.show_frame("StartPage")
        logoutButton.grid(row=0, column=1)

        SettingsButton=tk.Button(self)
        SettingsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        SettingsButton["font"] = ft
        SettingsButton["fg"] = "#000000"
        SettingsButton["justify"] = "center"
        SettingsButton["text"] = "Settings"
        SettingsButton["command"] =command=lambda: controller.show_frame("SettingsPage")
        SettingsButton.grid(row=0,column=2)


        ReviewsButton=tk.Button(self)
        ReviewsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        ReviewsButton["font"] = ft
        ReviewsButton["fg"] = "#000000"
        ReviewsButton["justify"] = "center"
        ReviewsButton["text"] = "Reviews"
        ReviewsButton["command"] =command=lambda: controller.show_frame("ReviewPage")
        ReviewsButton.grid(row=0, column=3)


        MoviesButton=tk.Button(self)
        MoviesButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        MoviesButton["font"] = ft
        MoviesButton["fg"] = "#000000"
        MoviesButton["justify"] = "center"
        MoviesButton["text"] = "TV Shows"
        MoviesButton["command"] =command=lambda: controller.show_frame("TVPage")
        MoviesButton.grid(row=0, column=4)


        TVButton=tk.Button(self)
        TVButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        TVButton["font"] = ft
        TVButton["fg"] = "#000000"
        TVButton["justify"] = "center"
        TVButton["text"] = "Movies"
        TVButton["command"] = command=lambda: controller.show_frame("MoviePage");
        TVButton.grid(row=0, column=5)


        TitleLabel=tk.Label(self)
        ft = TkFont.Font(family='Times',size=10)
        TitleLabel["font"] = ft
        TitleLabel["fg"] = "#333333"
        TitleLabel["justify"] = "center"
        TitleLabel["text"] = "FlixList"
        TitleLabel.grid(row=0, column=6)
        

        global tempId
        tempId = 0

        
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
            for j in range(len(movies)):
               e = tk.Entry(self,width=14,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,movies[j])
               e.config(state=DISABLED)
               e.grid_info
               #print(movies)

               
               

            i=i+1



    @staticmethod
    def updateValue(id,self):
        global tempId
        tempId = id

        return
            
            




class MoviePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("MainPage"),height= 1, width=8)
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
            for j in range(len(movies)):
               e = tk.Entry(self,width=15,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,movies[j])
               e.config(state=DISABLED)
               
               buttonTemp = tk.Button(self, text="View",
                           command=lambda i=i: controller.show_frameSPECIAL("MovieDetailPage",str(i)),height= 1, width=8)
               buttonTemp.grid(row=i,column=6)

               #print(movies[j])
            i=i+1
        #label = tk.Label(self, text="This is page 2", font=controller.title_font)
        #label.grid(row=9,column=0)
        
class MovieDetailPage(tk.Frame):
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        global tempId
        global tempString
        #print("dont print on run")
        #print("wja")
        #print(tempString)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(column=6, row=5, rowspan=2,  sticky=N+S+W)
        
        
        
        
        
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
        
        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("MoviePage"),
                           height= 1, width=10)
        #button.pack()
        button.grid(row=0,column=5)
        button2 = tk.Button(self, text="Update", command=lambda: self.showTable(self,controller),height= 1, width=10)
        #button.pack()
        button2.grid(row=0,column=6)
        #
        
        self.new_rating_var = tk.StringVar()
        self.new_comment_var = tk.StringVar()
        self.movie_rating_entry=tk.Entry(self)
        self.movie_comment_entry=tk.Entry(self)
        
        
        self.movie_rating_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_rating_entry["font"] = ft
        self.movie_rating_entry["fg"] = "#333333"
        self.movie_rating_entry["justify"] = "center"
        self.movie_rating_entry["textvariable"] = self.movie_rating_entry
        
        self.movie_comment_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_comment_entry["font"] = ft
        self.movie_comment_entry["fg"] = "#333333"
        self.movie_comment_entry["justify"] = "center"
        self.movie_comment_entry["textvariable"] = self.new_comment_var
        
        button = tk.Button(self, text="Post Comment",command=lambda: self.postMovieRating(self, self.new_comment_var.get() ,controller),
                           height= 1, width=10)
        button2 = tk.Button(self, text="Post Rating",command=lambda:self.postMovieRating(self, self.new_rating_var.get() ,controller),
                           height= 1, width=10)
        #button.pack()

        
        self.movie_comment_entry.grid(row=5,column=0)
        button.grid(row=5,column=1)
        self.movie_rating_entry.grid(row=6,column=0)
        button2.grid(row=6,column=1)
        
        
        
  
      
        #print("SELECT * FROM movies WHERE show_id=" +str(tempId)+ ", 10")
        #print(tempId)
        #print(tempString)
        #button.grid(row=10,column=0)
        #print("What?")
    
    @staticmethod
    def showTable(self,controller):

        for widget in self.winfo_children():
            widget.destroy()
        
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(column=6, row=5, rowspan=2,  sticky=N+S+W)
        
        
        
        
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
        
        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("MainPage"),
                           height= 1, width=10)
        #button.pack()
        button.grid(row=0,column=5)
        button2 = tk.Button(self, text="Update", command=lambda: self.showTable(self,controller),height= 1, width=10)
        #button.pack()
        button2.grid(row=0,column=6)
        
        self.new_rating_var = tk.StringVar()
        self.new_comment_var = tk.StringVar()
        self.movie_rating_entry=tk.Entry(self)
        self.movie_comment_entry=tk.Entry(self)
        
        
        self.movie_rating_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_rating_entry["font"] = ft
        self.movie_rating_entry["fg"] = "#333333"
        self.movie_rating_entry["justify"] = "center"
        self.movie_rating_entry["textvariable"] = self.movie_rating_entry
        
        self.movie_comment_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_comment_entry["font"] = ft
        self.movie_comment_entry["fg"] = "#333333"
        self.movie_comment_entry["justify"] = "center"
        self.movie_comment_entry["textvariable"] = self.new_comment_var
        
        button = tk.Button(self, text="Post Comment",command=lambda: self.postMovieRating(self, self.new_comment_var.get() ,controller),
                           height= 1, width=10)
        button2 = tk.Button(self, text="Post Rating",command=lambda:self.postMovieRating(self, self.new_rating_var.get() ,controller),
                           height= 1, width=10)

        
        self.movie_comment_entry.grid(row=5,column=0)
        button.grid(row=5,column=1)
        self.movie_rating_entry.grid(row=6,column=0)
        button2.grid(row=6,column=1)
        
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        global tempId
        #print(tempId)
        
        
        my_cursor.execute("SELECT * FROM movies WHERE show_id ="+str(tempId)+" limit 1")
        i =1
        j=0
        for movies in my_cursor:
            for j in range(len(movies)):
               #print(movies)
               e = tk.Entry(self,width=16,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,movies[j])
               e.config(state=DISABLED)

               #print(movies[j])
            i=i+1
        
        
        id_label = tk.Label(self,text="User id")
        id_label.grid(row=i,column=0,sticky=W,pady=2)
        id_label = tk.Label(self,text="Movie id")
        id_label.grid(row=i,column=1,sticky=W,pady=2)
        id_label = tk.Label(self,text="Rating")
        id_label.grid(row=i,column=2,sticky=W,pady=2)  
        i=i+1
        my_cursor.execute("SELECT * FROM movieComments WHERE show_id ="+str(tempId)+" limit 100")

        j = 0
        for guh in my_cursor:
            for j in range(len(guh)):
               #print(movies)
               e = tk.Entry(self,width=16,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,guh[j])
               e.config(state=DISABLED)

               #print(movies[j])
            i=i+1
            
    


        #print("henlo")

        return
    
    @staticmethod
    def postMovieRating(self,rating,controller):

        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        global curUserID
        global curUsername
        
        args =[]
        

        my_connect.commit() 
        

        return
    @staticmethod
    def postMovieComment(self,comment,controller):

        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        global curUserID
        global curUsername
        
        args =[]
        

        my_connect.commit() 
        
        
        return
    
class SettingsPage(tk.Frame):
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        logoutButton=tk.Button(self)
        logoutButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        logoutButton["font"] = ft
        logoutButton["fg"] = "#000000"
        logoutButton["justify"] = "center"
        logoutButton["text"] = "Logout"
        logoutButton["command"] =command=lambda: controller.show_frame("StartPage")
        logoutButton.grid(row=0, column=1)


        SettingsButton=tk.Button(self)
        SettingsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        SettingsButton["font"] = ft
        SettingsButton["fg"] = "#000000"
        SettingsButton["justify"] = "center"
        SettingsButton["text"] = "Settings"
        SettingsButton.grid(row=0,column=2)


        ReviewsButton=tk.Button(self)
        ReviewsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        ReviewsButton["font"] = ft
        ReviewsButton["fg"] = "#000000"
        ReviewsButton["justify"] = "center"
        ReviewsButton["text"] = "Reviews"
        ReviewsButton.grid(row=0, column=3)


        MoviesButton=tk.Button(self)
        MoviesButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        MoviesButton["font"] = ft
        MoviesButton["fg"] = "#000000"
        MoviesButton["justify"] = "center"
        MoviesButton["text"] = "TV Shows"
        MoviesButton.grid(row=0, column=4)


        TVButton=tk.Button(self)
        TVButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        TVButton["font"] = ft
        TVButton["fg"] = "#000000"
        TVButton["justify"] = "center"
        TVButton["text"] = "Movies"
        TVButton["command"] = command=lambda: controller.show_frame("MoviePage");
        TVButton.grid(row=0, column=5)
        
        deleteUser=tk.Button(self)
        deleteUser["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        deleteUser["font"] = ft
        deleteUser["fg"] = "#000000"
        deleteUser["justify"] = "center"
        deleteUser["text"] = "Delete Account"
        deleteUser["command"] = command=lambda: self.deleteAccount(self,self.controller);
        
                
        self.new_username_var = tk.StringVar()
        self.new_username_var_entry=tk.Entry(self)
        
        
        deleteUser.grid(row=0, column=6)
        
        
        changeName=tk.Button(self)
        changeName["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        changeName["font"] = ft
        changeName["fg"] = "#000000"
        changeName["justify"] = "center"
        changeName["text"] = "Change Password"
        changeName["command"] = command=lambda: self.updateUsername(self,self.new_username_var, controller);
        changeName.grid(row=0, column=7)
        

        
        self.new_username_var_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.new_username_var_entry["font"] = ft
        self.new_username_var_entry["fg"] = "#333333"
        self.new_username_var_entry["justify"] = "center"
        self.new_username_var_entry["textvariable"] = self.new_username_var
        #username_var = self.username_entry["textvariable"]
        self.new_username_var_entry.grid(row=0,column=8) 
 
    @staticmethod
    def updateUsername(self,new_password,controller):
        
         
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        global curUserID
        global curUsername
        
        args =[curUserID, new_password.get()]
        
        my_cursor.callproc("UpdatePass", args)
        my_connect.commit()
        
        return
    
    
    @staticmethod
    def deleteAccount(self,controller):
        
         
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        
        global curUserID
        global curUsername
        
        args =[curUserID]
        
        my_cursor.callproc("DeleteUser", args)
        my_connect.commit()
        controller.show_frame("StartPage")
        
        return
        
class TVDetailPage(tk.Frame):
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        global tempId
        global tempString
        #print("dont print on run")
        #print("wja")
        #print(tempString)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(column=6, row=5, rowspan=2,  sticky=N+S+W)
        
        
        
        
        
        id_label = tk.Label(self,text="Show id")
        id_label.grid(row=0,column=0,sticky=W,pady=2)
        id_label = tk.Label(self,text="Title")
        id_label.grid(row=0,column=1,sticky=W,pady=2)
        id_label = tk.Label(self,text="Duration")
        id_label.grid(row=0,column=2,sticky=W,pady=2)      
        id_label = tk.Label(self,text="Year")
        id_label.grid(row=0,column=3,sticky=W,pady=2)
        id_label = tk.Label(self,text="Director")
        id_label.grid(row=0,column=4,sticky=W,pady=2)  
        
        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("TVPage"),
                           height= 1, width=10)
        #button.pack()
        button.grid(row=0,column=5)
        button2 = tk.Button(self, text="Update", command=lambda: self.showTable(self,controller),height= 1, width=10)
        #button.pack()
        button2.grid(row=0,column=6)
        #
        
        self.new_rating_var = tk.StringVar()
        self.new_comment_var = tk.StringVar()
        self.movie_rating_entry=tk.Entry(self)
        self.movie_comment_entry=tk.Entry(self)
        
        
        self.movie_rating_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_rating_entry["font"] = ft
        self.movie_rating_entry["fg"] = "#333333"
        self.movie_rating_entry["justify"] = "center"
        self.movie_rating_entry["textvariable"] = self.movie_rating_entry
        
        self.movie_comment_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_comment_entry["font"] = ft
        self.movie_comment_entry["fg"] = "#333333"
        self.movie_comment_entry["justify"] = "center"
        self.movie_comment_entry["textvariable"] = self.new_comment_var
        
        button = tk.Button(self, text="Post Comment",command=lambda: self.postMovieRating(self, self.new_comment_var.get() ,controller),
                           height= 1, width=10)
        button2 = tk.Button(self, text="Post Rating",command=lambda:self.postMovieRating(self, self.new_rating_var.get() ,controller),
                           height= 1, width=10)
        #button.pack()

        
        self.movie_comment_entry.grid(row=5,column=0)
        button.grid(row=5,column=1)
        self.movie_rating_entry.grid(row=6,column=0)
        button2.grid(row=6,column=1)
        
        
        
  
      
        #print("SELECT * FROM movies WHERE show_id=" +str(tempId)+ ", 10")
        #print(tempId)
        #print(tempString)
        #button.grid(row=10,column=0)
        #print("What?")
    
    @staticmethod
    def showTable(self,controller):

        for widget in self.winfo_children():
            widget.destroy()
        
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(column=6, row=5, rowspan=2,  sticky=N+S+W)
        
        
        
        
        id_label = tk.Label(self,text="show id")
        id_label.grid(row=0,column=0,sticky=W,pady=2)
        id_label = tk.Label(self,text="Title")
        id_label.grid(row=0,column=1,sticky=W,pady=2)
        id_label = tk.Label(self,text="Duration")
        id_label.grid(row=0,column=2,sticky=W,pady=2)      
        id_label = tk.Label(self,text="Year")
        id_label.grid(row=0,column=3,sticky=W,pady=2)
        id_label = tk.Label(self,text="Director")
        id_label.grid(row=0,column=4,sticky=W,pady=2)  
        
        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("TVPage"),
                           height= 1, width=10)
        #button.pack()
        button.grid(row=0,column=5)
        button2 = tk.Button(self, text="Update", command=lambda: self.showTable(self,controller),height= 1, width=10)
        #button.pack()
        button2.grid(row=0,column=6)
        
        self.new_rating_var = tk.StringVar()
        self.new_comment_var = tk.StringVar()
        self.movie_rating_entry=tk.Entry(self)
        self.movie_comment_entry=tk.Entry(self)
        
        
        self.movie_rating_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_rating_entry["font"] = ft
        self.movie_rating_entry["fg"] = "#333333"
        self.movie_rating_entry["justify"] = "center"
        self.movie_rating_entry["textvariable"] = self.movie_rating_entry
        
        self.movie_comment_entry["borderwidth"] = "1px"
        ft = TkFont.Font(family='Times',size=10)
        self.movie_comment_entry["font"] = ft
        self.movie_comment_entry["fg"] = "#333333"
        self.movie_comment_entry["justify"] = "center"
        self.movie_comment_entry["textvariable"] = self.new_comment_var
        
        button = tk.Button(self, text="Post Comment",
                           height= 1, width=10)
        button2 = tk.Button(self, text="Post Rating",
                           height= 1, width=10)

        
        self.movie_comment_entry.grid(row=5,column=0)
        button.grid(row=5,column=1)
        self.movie_rating_entry.grid(row=6,column=0)
        button2.grid(row=6,column=1)
        
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        global tempId
        global tempEpId
        #print(tempId)
        print("SELECT * FROM episodes WHERE show_id ="+str(tempId)+" AND episode_id ="+str(tempEpId)  +" limit 1")
        
        my_cursor.execute("SELECT * FROM episodes WHERE show_id ="+str(tempId)+" AND episode_id ="+str(tempEpId)  +" limit 1")

        i =1
        j=0
        for movies in my_cursor:
            for j in range(len(movies)):
               #print(movies)
               e = tk.Entry(self,width=16,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,movies[j])
               e.config(state=DISABLED)

               #print(movies[j])
            i=i+1
        
        
        id_label = tk.Label(self,text="User id")
        id_label.grid(row=i,column=0,sticky=W,pady=2)
        id_label = tk.Label(self,text="show id")
        id_label.grid(row=i,column=1,sticky=W,pady=2)
        id_label = tk.Label(self,text="episode id")
        id_label.grid(row=i,column=2,sticky=W,pady=2)
        id_label = tk.Label(self,text="Comment")
        id_label.grid(row=i,column=2,sticky=W,pady=2)  
        i=i+1
        my_cursor.execute("SELECT * FROM TVComments WHERE show_id ="+str(tempId)+" limit 100")
        j = 0
        for guh in my_cursor:
            for j in range(len(guh)):
               #print(movies)
               e = tk.Entry(self,width=16,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,guh[j])
               e.config(state=DISABLED)

               #print(movies[j])
            i=i+1
            
    


        #print("henlo")

        return

class ReviewPage(tk.Frame):
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        global tempId
        global tempString
        logoutButton=tk.Button(self)
        logoutButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        logoutButton["font"] = ft
        logoutButton["fg"] = "#000000"
        logoutButton["justify"] = "center"
        logoutButton["text"] = "Logout"
        logoutButton["command"] =command=lambda: controller.show_frame("StartPage")
        logoutButton.grid(row=0, column=0)


        SettingsButton=tk.Button(self)
        SettingsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        SettingsButton["font"] = ft
        SettingsButton["fg"] = "#000000"
        SettingsButton["justify"] = "center"
        SettingsButton["text"] = "Settings"
        SettingsButton.grid(row=0,column=1)


        ReviewsButton=tk.Button(self)
        ReviewsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        ReviewsButton["font"] = ft
        ReviewsButton["fg"] = "#000000"
        ReviewsButton["justify"] = "center"
        ReviewsButton["text"] = "Reviews"
        ReviewsButton.grid(row=0, column=2)


        MoviesButton=tk.Button(self)
        MoviesButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        MoviesButton["font"] = ft
        MoviesButton["fg"] = "#000000"
        MoviesButton["justify"] = "center"
        MoviesButton["text"] = "TV Shows"
        MoviesButton["command"] = command=lambda: controller.show_frame("TVPage");
        MoviesButton.grid(row=0, column=3)


        TVButton=tk.Button(self)
        TVButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        TVButton["font"] = ft
        TVButton["fg"] = "#000000"
        TVButton["justify"] = "center"
        TVButton["text"] = "Movies"
        TVButton["command"] = command=lambda: controller.show_frame("MoviePage");
        TVButton.grid(row=0, column=4)
        
        button2 = tk.Button(self, text="Update", command=lambda: self.showTable(self,controller),height= 1, width=10)
        #button.pack()
        button2.grid(row=0,column=5)
        
    @staticmethod
    def showTable(self,controller):

        for widget in self.winfo_children():
            widget.destroy()
        
        logoutButton=tk.Button(self)
        logoutButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        logoutButton["font"] = ft
        logoutButton["fg"] = "#000000"
        logoutButton["justify"] = "center"
        logoutButton["text"] = "Logout"
        logoutButton["command"] =command=lambda: controller.show_frame("StartPage")
        logoutButton.grid(row=0, column=0)


        SettingsButton=tk.Button(self)
        SettingsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        SettingsButton["font"] = ft
        SettingsButton["fg"] = "#000000"
        SettingsButton["justify"] = "center"
        SettingsButton["text"] = "Settings"
        SettingsButton.grid(row=0,column=1)


        ReviewsButton=tk.Button(self)
        ReviewsButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        ReviewsButton["font"] = ft
        ReviewsButton["fg"] = "#000000"
        ReviewsButton["justify"] = "center"
        ReviewsButton["text"] = "Reviews"
        ReviewsButton.grid(row=0, column=2)


        MoviesButton=tk.Button(self)
        MoviesButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        MoviesButton["font"] = ft
        MoviesButton["fg"] = "#000000"
        MoviesButton["justify"] = "center"
        MoviesButton["text"] = "TV Shows"
        MoviesButton["command"] = command=lambda: controller.show_frame("TVPage");
        MoviesButton.grid(row=0, column=3)


        TVButton=tk.Button(self)
        TVButton["bg"] = "#f0f0f0"
        ft = TkFont.Font(family='Times',size=10)
        TVButton["font"] = ft
        TVButton["fg"] = "#000000"
        TVButton["justify"] = "center"
        TVButton["text"] = "Movies"
        TVButton["command"] = command=lambda: controller.show_frame("MoviePage");
        TVButton.grid(row=0, column=4)
        
        button2 = tk.Button(self, text="Update", command=lambda: self.showTable(self,controller),height= 1, width=10)
        #button.pack()
        button2.grid(row=0,column=5)
        
        my_connect = mysql.connector.connect(
            host="35.188.140.250",
            user="root",
            passwd="12345",
            database="proj_db"
        )
        my_cursor = my_connect.cursor()
        global curUserID
        #print(tempId)
        
        
        
        
        my_cursor.execute("SELECT * FROM movieComments WHERE user_id ="+str(curUserID))
        i =1
        id_label = tk.Label(self,text="User id")
        id_label.grid(row=i,column=0,sticky=W,pady=2)
        id_label = tk.Label(self,text="movie id")
        id_label.grid(row=i,column=1,sticky=W,pady=2)
        id_label = tk.Label(self,text="Comment")
        id_label.grid(row=i,column=2,sticky=W,pady=2)  
        i = i +1
        j=0
        for movies in my_cursor:
            for j in range(len(movies)):
               #print(movies)
               e = tk.Entry(self,width=16,fg='blue')
               e.grid(row=i,column=j)
               e.insert(END,movies[j])
               e.config(state=DISABLED)

               #print(movies[j])
            i=i+1
        
   
    


        #print("henlo")

        return
        

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()