#!/usr/bin/env python
# Mockup for burg-manager-tk

# import everything here
import Tkinter
from Tkinter import *
import os
import sys
import subprocess
import tkMessageBox
import re

# test if OS is windows or POSIX-compliant (UNIX or UNIX-like)
if os.name == "nt":
    root = Tk()
    Label(root, text="Sorry, Windows is not supported yet.").pack()
    Button(root, text="Okay", command=root.quit).pack()
    root.title("burgmockup.py")
    root.mainloop()
    sys.exit(1)
        
# if OS is POSIX-compliant, ensure that we are root user
if os.geteuid() != 0:
    root = Tk()
    Label(root, text="Please enter root password to continue").pack()
    passbox = Entry(root, bg="white", show="*") #create password box
    passbox.pack()
    
    # exports password as a variable then pipes it into sudo and reloads this program, then removes variable for security reasons
    def UsePassword():
        password = passbox.get()
        os.putenv("PASS", password)
        subprocess.Popen('echo "$PASS" | sudo -S python burgmockup2.py & unset PASS', shell=True)
        sys.exit(0)
    Button(root, text="Cancel", command=quit).pack(side=LEFT)    
    Button(root, text="Okay", command=UsePassword).pack(side=RIGHT)
    root.title("burgmockup.py")
    root.mainloop()

# (shell) install process for debian-based systems, have apt work in the background
def debinstall():
    subprocess.call("add-apt-repository ppa:bean123ch/burg && apt-get update && apt-get install burg burg-themes burg-emu && xterm -e burg-install /dev/sda", shell=True)

# (shell) remove process for debian-based systems
def debremove():
    subprocess.call("xterm -e apt-get remove --purge burg burg-themes burg-emu", shell=True)

# (shell) burg-emu
def emulator():
    subprocess.call("xterm -e burg-emu", shell=True)

# (shell) restore grub
def restoregrub():
    subprocess.call("xterm -e grub-install /dev/sda && update-grub", shell=True)

# (shell) text editor, fallback on nano, then vi if none are found
def textedit():
    subprocess.call("gedit /etc/default/burg || kate /etc/default/burg || leafpad /etc/default/burg || xterm -e nano /etc/default/burg || xterm -e vi /etc/default/burg", shell=True)

# (dialog) License - Unfinished and unchecked
def openlicens():
    tkMessageBox.showinfo("License", detail="Original program copyright (c) 2010 Ingalex & Canopus0003 project <http://www.sourceslist.eu>\nThis script is licensed under GNU GPL version 3.0 or above.\nRedistribution and use in source and binary forms, with or without modification are permitted provided that the following conditions are met:\n\n1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution:\n\nTHIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.")

# (dialog) About - Dialogs should use tkinter to remain consistent with main program
def opendialog():
    tkMessageBox.showinfo("About", "This is the python/tkinter port of burg-manager (BUC version).\nPlease note that this is a development version and is not intended for use.")

# define the main class
class App:

    def __init__(self, master):

        # apply timeout settings
        def applytimeout():
            answer = int(timeoutbox.get()) #returns string from entrybox as an integer
            s = open("/etc/default/burg").read() #opens file
            s = re.sub("GRUB_TIMEOUT=\S\S?", "GRUB_TIMEOUT=%d" % answer, s) #YES! After over 3 hours in total, this finally, finally, finally works for both one digit and one digit answers!
            f = open("/etc/default/burg", 'w')
            f.write(s) #writes changes back to file
            f.close()
            suprocess.call("update-burg", shell=True) #updates burg in the background



        # the main frame
        frame = Frame(master)

        # define the labels
        intro = Label(master, text="This is the burg-manager-tk mockup.")
        timeout = Label(master, text="Edit timeout:")
        link = Label(master, text="www.sourceslist.eu")

        # define buttons
        install = Button(master, text="Install burg", command=debinstall)
        uninstall = Button(master, text="Uninstall burg", fg="red", command=debremove)
        burgemu = Button(master, text="Test burg", command=emulator)
        restore = Button(master, text="Restore grub", fg="blue", command=restoregrub)
        editfile = Button(master, text="Open /etc/default/burg", command=textedit)
        settings = Button(master, text="Apply settings", command=applytimeout)
        licens = Button(master, text="License",fg="green", command=openlicens)
        info = Button(master, text='Info', command=opendialog)

        # define the timeout entry box
        timeoutbox = Entry(master, width=10)

        # setup grid geometry
        intro.grid(row=0, column=0, columnspan=2, pady=5)
        install.grid(row=1, column=0, pady=10)
        uninstall.grid(row=1, column=1, pady=10)
        burgemu.grid(row=2, column=0, pady=5)
        restore.grid(row=2, column=1, pady=5)
        timeout.grid(row=3, column=0, pady=5)
        timeoutbox.grid(row=3, column=1, pady=5)
        settings.grid(row=4, column=0, columnspan=2, pady=5)
        editfile.grid(row=5, column=0, columnspan=2, pady=5)
        licens.grid(row=7, column=0, pady=10)
        info.grid(row=7, column=1, pady=10)
        link.grid(row=8, column=0, columnspan=2, pady=5)

# set root window
root = Tk()

# set root window title
root.title("burgmockup.py")

app = App(root)

root.mainloop()
