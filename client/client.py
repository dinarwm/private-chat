import socket
import sys
import thread
from Tkinter import *

class Login(Frame):
        def __init__(self,master):
                Frame.__init__(self,master)
                self.grid()
                self.create_widget()

        def show_label(self, event=None):
                self.Label_Sembunyi.grid();
                self.Button_Submit.grid(padx=50,pady=5)

        def hide_label(self, event=None):
                self.Label_Sembunyi.lower(self.frame)

        def create_widget(self):
                self.Label_Username = Label(self,text = "Username")
                self.Label_Username.grid()
                self.Entry_Username = Entry(self, bd=2)
                self.Entry_Username.grid()
                self.Button_Submit = Button(self,text = "Log In", command=self.kirim)
                self.Button_Submit.grid(padx=50,pady=5)

        def kirim(self):
                s.send('login:' + self.Entry_Username.get())
                self.master.destroy()

class ListOnline(Frame):
        def __init__(self,master):
                Frame.__init__(self,master)
                self.grid()
                self.create_widget()
                
        def create_widget(self):
                self.Label_Password = Label(self,text = "Online Users")
                self.Label_Password.pack()
                self.var = IntVar()
                msg = s.recv(size)
                print msg
                words = msg.split(':')
                a = -1
                for word in words:
                        if a == -1:
                                a=a+1
                                pass
                        else:
                                listuser=[]
                                iduser = word.split('#')[0]
                                username = word.split('#')[1]
                                self.Radio = Radiobutton(self, text=username,variable=self.var, value = iduser)
                                self.Radio.pack(anchor = W)
                self.Button_Submit = Button(self,text = "Chat", command=self.sel)
                self.Button_Submit.pack(padx=50,pady=5)

        def sel(self):
                print(str(self.var.get()))
                Chat(str(self.var.get()))
                self.master.destroy()
                
class Chatting(Frame):
        global urutan
        urutan = 1
        global kata
        kata = ""
        def __init__(self,master,string):
                Frame.__init__(self,master)
                self.grid()
                self.create_widget()
                kata = string
                print(string)
                
        def create_widget(self):
                self.Text_Chat = Listbox(self, bd=2, bg="white", height="20", width="42", font="Arial")
                self.Scroll_Bar = Scrollbar(self, command=self.Text_Chat.yview, cursor="heart")
                self.Text_Chat['yscrollcommand'] = self.Scroll_Bar.set
                self.Send_Button = Button(self, font=30, text="Send", width="8", height=3, bd=0, bg="#FFBF00", activebackground="#FACC2E",command=self.cetak)
                self.Entry_Box = Text(self, bd=2, bg="white",width="35", height="3", font="Arial")

                self.Scroll_Bar.grid(row=1,column=5,sticky='ns')
                self.Text_Chat.grid(row=1,columnspan=5)
                self.Entry_Box.grid(row=2,columnspan=3)
                self.Send_Button.grid(row=2,column=4,columnspan=2)

        def cetak(self):
                abc = self.Entry_Box.get("1.0",END)
                self.Text_Chat.insert(END,abc)

def Log():
        root = Tk()
        root.title("Login Chat Application")
        app = Login(root)
        root.mainloop()

def List():
        root = Tk()
        root.title("List Online Users")
        app = ListOnline(root)
        root.mainloop()

def Chat(string):
        root = Tk()
        root.title("Chatting Users")
        app = Chatting(root,string)
        root.mainloop()

host = '10.151.43.223'
port = 22001
size = 1024
login = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

sys.stdout.write('You are connected to server, please login to continue...\n')

try:
    while login==0:
        Log()
        msg = s.recv(size)
        auth = msg.split(':')[1]
        if auth=='1':
            login = 1
            List()

except KeyboardInterrupt:
    s.close()
    sys.exit(0)
