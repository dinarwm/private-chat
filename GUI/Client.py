import socket
import time
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
                self.Label_Password = Label(self,text = "Password")
                self.Label_Password.grid()
                self.Entry_Password = Entry(self, bd=2)
                self.Entry_Password.grid()
                self.Label_Sembunyi = Label(self, text="Username tidak tersedia")
                self.Button_Submit = Button(self,text = "Log In", command=self.show_label)
                self.Button_Submit.grid(padx=50,pady=5)
        
client = socket.socket()
client.connect(('localhost', 7891))

root = Tk()
root.title("Chat Application")

app = Chatting(root)

root.mainloop()
print client.recv(1024)
time.sleep(5)
