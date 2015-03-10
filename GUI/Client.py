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

class Chatting(Frame):
        def __init__(self,master):
                Frame.__init__(self,master)
                self.grid()
                self.create_widget()
                
        def create_widget(self):
                self.Text_Chat = Text(self, bd=2, bg="white", height="20", width="42", font="Arial")
                self.Text_Chat.config(state=DISABLED)
                self.Scroll_Bar = Scrollbar(self, command=self.Text_Chat.yview, cursor="heart")
                self.Text_Chat['yscrollcommand'] = self.Scroll_Bar.set
                self.Send_Button = Button(self, font=30, text="Send", width="8", height=3, bd=0, bg="#FFBF00", activebackground="#FACC2E",command="")
                self.Entry_Box = Text(self, bd=2, bg="white",width="35", height="3", font="Arial")

                self.Scroll_Bar.grid(row=1,column=5,sticky='ns')
                self.Text_Chat.grid(row=1,columnspan=5)
                self.Entry_Box.grid(row=2,columnspan=3)
                self.Send_Button.grid(row=2,column=4,columnspan=2)

class ListOnline(Frame):
        def __init__(self,master):
                Frame.__init__(self,master)
                self.grid()
                self.create_widget()
                
        def create_widget(self):
                self.Label_Password = Label(self,text = "Online Users")
                self.Label_Password.pack()
                MODES = [("Monochrome", "1"),("Grayscale", "L"),("True color", "RGB"),("Color separation", "CMYK"),]
                for text, mode in MODES:
                        self.Radio = Radiobutton(self, text=text,
                                        variable="Online", value = mode)
                        self.Radio.pack(anchor=W)
                self.Button_Submit = Button(self,text = "Chat")
                self.Button_Submit.pack(padx=50,pady=5)
                
        
client = socket.socket()
client.connect(('10.151.43.223', 22001))

root = Tk()
root.title("Chat Application")

app = ListOnline(root)

root.mainloop()
print client.recv(1024)
time.sleep(5)
