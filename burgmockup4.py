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
import commands

version = "Version 0.04" #set version number here

# Commands

# (shell) install process for debian-based systems, have apt work in the background
def debinstall():
    os.putenv("disk", drivelist_value.get()) #exports drivelist_value variable to BASH    
    subprocess.Popen("add-apt-repository ppa:bean123ch/burg && apt-get update && apt-get install burg burg-themes burg-emu && xterm -e burg-install $disk", shell=True)

# (shell) remove process for debian-based systems
def debremove():
    os.putenv("disk", drivelist_value.get()) #exports drivelist_value variable to BASH
    subprocess.Popen("xterm -e apt-get remove --purge burg burg-themes burg-emu", shell=True)

# (shell) burg-emu
def emulator():
    subprocess.Popen("xterm -e burg-emu", shell=True)

# (shell) restore grub
def restoregrub():
    os.putenv("disk", drivelist_value.get()) #exports drivelist_value variable to BASH
    subprocess.Popen("xterm -e grub-install $disk && update-grub", shell=True)

# (shell) text editor, fallback on nano, then vi if none are found
def textedit():
    subprocess.Popen("gedit /etc/default/burg || kate /etc/default/burg || leafpad /etc/default/burg || xterm -e nano /etc/default/burg || xterm -e vi /etc/default/burg", shell=True)

# (shell) open a terminal, fallback on xterm if none are found
def terminal():
    subprocess.Popen("gnome-terminal || konsole || xfce4-terminal || multi-gnome-terminal || eterm || aterm || wterm || rxvt || xterm", shell=True)

# (dialog) License - Unfinished and unchecked
def openlicens():
    tkMessageBox.showinfo("License", detail="Original program copyright (c) 2010 Ingalex & Canopus0003 project <http://www.sourceslist.eu>\nThis script is licensed under GNU GPL version 3.0 or above.\nRedistribution and use in source and binary forms, with or without modification are permitted provided that the following conditions are met:\n\n1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution:\n\nTHIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.")

# (dialog) About - Dialogs should use tkinter to remain consistent with main program
def opendialog():
    tkMessageBox.showinfo("About", "This is the python/tkinter port of burg-manager (BUC version).\nPlease note that this is a development version and is not intended for normal use.")
 

# Code starts here

# test if OS is windows or POSIX-compliant (UNIX or UNIX-like)
if os.name == "nt":
    root = Tk()
    Label(root, text="Sorry, Windows support has been dropped due to complexity").pack()
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
        password = passbox.get() #gets password string from passbox
        scriptname = sys.argv[0] #finds name/path of this script
        os.putenv("PASS", password) #exports password variable to BASH
        os.putenv("scriptname", scriptname) #exports scriptname variable to BASH
        subprocess.Popen('echo "$PASS" | sudo -S python $scriptname & unset PASS', shell=True)
        sys.exit(0)
    Button(root, text="Cancel", command=quit).pack(side=LEFT)    
    Button(root, text="Okay", command=UsePassword).pack(side=RIGHT)
    root.title("burgmockup.py")
    root.mainloop()


# define the main class (for Linux, BSD, UNIX, OS X, etc)
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
            subprocess.Popen("update-burg", shell=True) #updates burg in the background

        def applyresolution():
            os.putenv("resolution", reslist_value.get()) #exports reslist_value variable to BASH
            subprocess.Popen("sed -i '/GRUB_GFXMODE/d' /etc/default/burg ; echo 'GRUB_GFXMODE='$resolution | sudo tee -a /etc/default/burg", shell=True)

        # the main frame
        frame = Frame(master)

        # define the menubar and its contents
        menubar = Menu(master)
        menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Edit /etc/default/burg", command=textedit)
        menu.add_command(label="Open Terminal", command=terminal)
        menu.add_command(label="Exit", command=quit)
        menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Info", menu=menu)
        menu.add_command(label="About", command=opendialog)
        menu.add_command(label="License", command=openlicens)
        master.config(menu=menubar)

        # define the labels
        intro = Label(master, text="This is the burg-manager-tk mockup:")
        intro2 = Label(master, text="*Development version*")
        hd = Label(master, text="Specify HD for install (eg: sda)")
        reslabel = Label(master, text="Specify resolution to use:")
        timeout = Label(master, text="Edit timeout:")
        link = Label(master, text="www.sourceslist.eu")
        ver = Label(master, text=version)

        # define buttons
        install = Button(master, text="Install burg", fg="green", command=debinstall)
        uninstall = Button(master, text="Uninstall burg", fg="red", command=debremove)
        burgemu = Button(master, text="C h a n g e   T h e m e  |  B u r g - e m u", fg="orange", command=emulator)
        restore = Button(master, text="Restore grub", fg="blue", command=restoregrub)
        timeoutbutton = Button(master, text="Apply Timeout", command=applytimeout)
        resolutionbutton = Button(master, text="Apply Resolution", command=applyresolution)

        # define the timeout entry box
        timeoutbox = Entry(master, width=10)

        # define the hard drive list
        partitions = commands.getoutput("mount | grep ^/dev | cut -d' ' -f1")
        drives = re.sub(r'\d', "", partitions) #removes numbers (e.g. /dev/sda6 -> /dev/sda)
        drives = drives.replace('\n', " ") #replaces newline with space
        drives = drives.split(" ") #splits the string into a list based on spaces
        drives = list(set(drives)) #removes any duplicate entries
        drivelist_value = StringVar(master)
        drivelist_value.set(drives[0]) #sets default hard drive to first value
        drive_list = OptionMenu(master, drivelist_value, *drives) #creates drop-down list

        # define the resolution list
        os.popen("rm -rf /tmp/resolution; xrandr > /tmp/resolution; sed -i '/DFP/d' /tmp/resolution; sed -i '/Screen/d' /tmp/resolution; sed -i '/CRT/d' /tmp/resolution; awk '{print $1}' /tmp/resolution > /tmp/resolution_final_data")
        resoptions = open("/tmp/resolution_final_data", "r")
        resoptions = resoptions.read()
        resoptions = resoptions.replace('\n', " ")
        resoptions = resoptions.split(" ")
        reslist_value = StringVar(master)
        reslist_value.set(resoptions[0]) #sets default option to first value
        resolution_list = OptionMenu(master, reslist_value, *resoptions) #creates drop-down list
	
        # setup grid geometry
        intro.grid(row=0, column=0, columnspan=2, pady=2)
        intro2.grid(row=1, column=0, columnspan=2, pady=10)
        hd.grid(row=2, column=0, pady=1, padx=5)
        install.grid(row=3, column=0, pady=5)
        uninstall.grid(row=3, column=1, pady=5, padx=10)
        drive_list.grid(row=2, column=1, pady=5)
        burgemu.grid(row=4, columnspan=2, pady=5)
        restore.grid(row=5, column=0, columnspan=2, pady=5)
        reslabel.grid(row=6, column=0, pady=1)
        resolution_list.grid(row=6, column=1, pady=5)
        resolutionbutton.grid(row=7, column=0, columnspan=2, pady=2)
        timeout.grid(row=8, column=0, pady=2)
        timeoutbox.grid(row=8, column=1, pady=2)
        timeoutbutton.grid(row=9, column=0, columnspan=2, pady=2)
        link.grid(row=10, column=0, pady=1)
        ver.grid(row=10, column=1, pady=1)

# set root window
root = Tk()

# set root window title
root.title("burgmockup.py")

app = App(root)

root.mainloop()
