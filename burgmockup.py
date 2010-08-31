#!/usr/bin/env python
# Mockup for burg-manager-tk

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

# if OS is POSIX-compliant, check if we are root
if os.geteuid() != 0:
    root = Tk()
    Label(root, text="Sorry, you need to run this as root").pack()
    Button(root, text="Okay", command=root.quit).pack()
    root.title("burgmockup.py")
    root.mainloop()
    sys.exit(1)

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

# apply timeout settings
def applytimeout():
    answer = timeoutbox.get()
    o = open("output","w")
    data = open("/etc/default/burg").read()
    o.write( re.sub("GRUB_TIMEOUT","GRUB_TIMEOUT=%d" % answer,data)  )
    o.close() #UNFINISHED!

# (shell) text editor, fallback on nano, then vi if none are found
def textedit():
    subprocess.call("gedit /etc/default/burg || kate /etc/default/burg || leafpad /etc/default/burg || xterm -e nano /etc/default/burg || xterm -e vi /etc/default/burg", shell=True)

# (dialog) About
def aboutdialog():
    tkMessageBox.showinfo("About", "This is the python/tkinter port of burg-manager.\nPlease note that this is a development version and is not intended for use.")

# define the main class
class App:

    def __init__(self, master):

        # the main frame
        frame = Frame(master)

        # define the labels
        intro = Label(master, text="This is the burg-manager-tk mockup.")
        timeout = Label(master, text="Edit timeout:") 

        # define buttons
        install = Button(master, text="Install burg", command=debinstall)
        uninstall = Button(master, text="Uninstall burg", fg="red", command=debremove)
        burgemu = Button(master, text="Test burg", command=emulator)
        restore = Button(master, text="Restore grub", fg="blue", command=restoregrub)
        editfile = Button(master, text="Open /etc/default/burg", command=textedit)
        about = Button(master, text="About", command=aboutdialog)
        settings = Button(master, text="Apply settings", command=applytimeout)

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
        about.grid(row=6, column=0, columnspan=2, pady=5)

# set root window
root = Tk()

# set root window title
root.title("burgmockup.py")

app = App(root)

root.mainloop()
