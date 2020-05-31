"""

WHAT IS THIS: tooltips for tkinter that follow the cursor.


HOW TO USE THIS: 

- save this file as tooltips.py either in the same root as your file or in a folder
- use "from tooltips import tips" or "from foldername.tooltips import tips"

- tt=tips(*args,**kwargs) 
- it can be applied to any widget, including root windows.
- you should include root.mainloop() to improve the performance of the tooltips


NECESSARY ARGUMENTS: the parent widget, i.e. the widget you want the tooltip to appear for when hovered over


OPTIONAL KEYWORD ARGUMENTS:

- text="..." : the text that the tooltip will show. supports standard text like other tkinter widgets. if not supplied, defaults to "".

- bg="..." : the background colour of the tip. supports hex values and tkinter defined colours. if not supplied, defaults to "yellow".

- fg="..." : the text colour of the tip. supports hex values and tkinter defined colours. if not supplied, defaults to "black".

- delay=0 : sets the delay in seconds between hovering and the tip appearing. supports integers. if not supplied, defaults to 0.

- state="..." : sets whether the tip should follow the cursor or not. supports "static" and "mobile". if not supplied, defaults to "mobile".


METHODS: (assuming "tt" is the name of the tooltip you defined)

- tt.configure : change an attribute of the tooltip (accepts text,bg,fg,delay,state)

- tt.destroy : destroy a tooltip so that it no longer appears

SCREENSHOTS:

- http://prntscr.com/hfzwyv

- http://prntscr.com/hfzxc3 (after the button is clicked)

"""

from tkinter import Toplevel, Message


__author__="GEO"


class tips:

    "ARGS: <WIDGET> | KWARGS: text, bg, fg, delay, state"

    def __init__(self,*args,**kwargs):

        try:
            self.parent=args[0]
        except IndexError:
            raise Exception("No root supplied")


        try:
            self.txt=kwargs["text"]
        except KeyError:
            self.txt=""


        try:
            self.bg=kwargs["bg"]
        except KeyError:
            self.bg="yellow"


        try:
            self.fg=kwargs["fg"]
        except KeyError:
            self.fg="black"


        try:
            self.delay=kwargs["delay"]*1000
        except KeyError:
            self.delay=0


        try:
            self.state=kwargs["state"]
            
            if self.state!="static" and self.state!="mobile":
                self.state="mobile"

        except KeyError:
            self.state="mobile"


        self.tip=Toplevel()
        self.tip.withdraw()
        self.tip.overrideredirect(True)
        self.tip.geometry("+500+500")
        self.msg=Message(self.tip,text=self.txt,bg=self.bg,fg=self.fg,aspect=1000,relief="solid")
        self.msg.grid()


        self.parent.bind("<Enter>",lambda e:self.parent.after(self.delay,self.showtip(e)))

        self.parent.bind("<Leave>",self.hidetip)

        if self.state=="mobile":

            self.parent.bind("<Motion>",self.movetip)


    def showtip(self,event):
        
        self.tip.deiconify()

        if self.state=="static":

            x,y=self.parent.winfo_rootx()+15,self.parent.winfo_rooty()+10

        elif self.state=="mobile":

            x,y=event.x_root+10,event.y_root+10

        self.tip.geometry("+"+str(x)+"+"+str(y))


    def hidetip(self,event):
        self.tip.withdraw()

    def movetip(self,event):
        x,y=event.x_root+10,event.y_root+10
        self.tip.geometry("+"+str(x)+"+"+str(y))


    def configure(self,**kwargs):

        try:
            self.txt=kwargs["text"]
            self.msg.configure(text=self.txt)
        except KeyError:
            pass
        try:
            self.bg=kwargs["bg"]
            self.msg.configure(bg=self.bg)
        except KeyError:
            pass
        try:
            self.fg=kwargs["fg"]
            self.msg.configure(fg=self.fg)
        except KeyError:
            pass

        try:
            self.delay=kwargs["delay"]*1000
            self.parent.bind("<Enter>",lambda e:self.parent.after(self.delay,self.showtip(e)))
        except KeyError:
            pass
        
        try:
            self.state=kwargs["state"]
            if self.state=="mobile":
                self.parent.bind("<Motion>",self.movetip)
        except KeyError:
            pass


    def destroy(self):
        self.parent.unbind("<Enter>")
        self.parent.unbind("<Leave>")
        self.parent.unbind("<Motion>")
        self.tip.destroy()
        del self


