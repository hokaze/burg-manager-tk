#!/usr/bin/env python
# Burg Manager (Python/Tkinter Version)

# import everything here
import Tkinter
from Tkinter import *
import os
import sys
import subprocess
import tkMessageBox
import re
import commands
import time
from threading import Thread

version = "Version 0.05" #set version number here

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
    tkMessageBox.showinfo("About", "This is the python/tkinter port of the original burg-manager (BUC version).\nVersion 0.05 of burg-manager-tk marks the first public release.\n\nPlease report bugs to hokazenoflames@gmail.co.uk")

# (shell, dialog) Backup /etc/default/burg to /etc/burg/default/burg
def backup():
    if os.path.exists("/etc/default/burg.bak") == False:
        subprocess.Popen("cp /etc/default/burg /etc/default/burg.bak", shell=True)
        tkMessageBox.showinfo("Backup Settings", "Backup successful.")
    else:
        if tkMessageBox.askyesno("Backup Settings", "A backup already exists. Overwrite?") == True:
            subprocess.Popen("cp /etc/default/burg /etc/default/burg.bak", shell=True)
            tkMessageBox.showinfo("Backup Settings", "Backup successful.")
 
# (shell, dialog) Restore backup of /etc/default/burg
def backup_restore():
    if os.path.exists("/etc/default/burg.bak") == False:
        tkMessageBox.showerror("Restore Backup", "No backup found to restore.")
    else:
        subprocess.Popen("rm /etc/default/burg; cp /etc/default/burg.bak /etc/default/burg", shell=True)
        tkMessageBox.showinfo("Restore Backup", "Old settings have been restored.")

# (shell, dialog) Remove backup of /etc/default/burg
def backup_delete():
    if os.path.exists("/etc/default/burg.bak") == False:
        tkMessageBox.showerror("Delete Backup", "No backup found to delete.")
    else:
        subprocess.Popen("rm /etc/default/burg.bak", shell=True)
        tkMessageBox.showinfo("Delete Backup", "Backup deleted.")


# Code starts here

# test if OS is windows or POSIX-compliant (UNIX or UNIX-like)
if os.name == "nt":
    root = Tk()
    Label(root, text="Sorry, Windows support has been dropped due to complexity").pack()
    Button(root, text="Okay", command=root.quit).pack()
    root.title("burg-manager-tk")
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
    root.title("burg-manager-tk")
    root.mainloop()


# define the main class (for Linux, BSD, UNIX, OS X, etc)
class App:

    def __init__(self, master):

        # apply timeout settings
        def applytimeout():
            answer = int(timeoutbox.get()) #returns string from entrybox as an integer
            s = open("/etc/default/burg").read() #opens file
            s = re.sub("GRUB_TIMEOUT=\S\S?", "GRUB_TIMEOUT=%d" % answer, s) #YES! After over 3 hours in total, this finally, finally, finally works for both one digit and two digit answers!
            f = open("/etc/default/burg", 'w')
            f.write(s) #writes changes back to file
            f.close()
            subprocess.Popen("update-burg", shell=True) #updates burg in the background

        def applyresolution():
            os.putenv("resolution", reslist_value.get()) #exports reslist_value variable to BASH
            subprocess.Popen("sed -i '/GRUB_GFXMODE/d' /etc/default/burg ; echo 'GRUB_GFXMODE='$resolution | sudo tee -a /etc/default/burg", shell=True)
            subprocess.Popen("update-burg", shell=True) #updates burg in the background

        def apply_os():
            os.putenv("default_os", oslist_value.get()) #exports oslist_value variable to BASH
            subprocess.Popen("sed -i '/GRUB_DEFAULT/d' /etc/default/burg ; echo 'GRUB_DEFAULT='$default_os | tee -a /etc/default/burg", shell=True, executable = "/bin/bash")
            subprocess.Popen("update-burg", shell=True) #updates burg in the background


        # Advanced Settings window
        def advancedsettings():

            advanced = Toplevel()
            advanced.title("Advanced Settings")

            # obtain default linux cmdline parameters
            os.popen("sed -n -e '/^GRUB_CMDLINE_LINUX_DEFAULT/p' /etc/default/grub| awk -F[\\\'\\\"] '{print $2}' >> /tmp/cmdline_default")
            default_cmdline = open("/tmp/cmdline_default")
            default_cmdline = default_cmdline.readline()

            # setup labels
            adv_label = Label(advanced, text="Edit Advanced Settings:")
            recovery_label = Label(advanced, text="GRUB_DISABLE_LINUX_RECOVERY")
            cmdline_label = Label(advanced, text="GRUB_CMDLINE_LINUX_DEFAULT")
            savedefault_label = Label(advanced, text="GRUB_SAVEDEFAULT")
            linux16_label = Label(advanced, text="GRUB_LINUX16")
            uuid_label = Label(advanced, text="GRUB_DISABLE_LINUX_UUID")
            fold_label = Label(advanced, text="GRUB_FOLD")

            # setup button commands
            def recovery_off():
                os.popen("sed -i /GRUB_DISABLE_LINUX_RECOVERY/d /etc/default/burg && grubrecovery=\'GRUB_DISABLE_LINUX_RECOVERY=\"\'true\'\"\' && echo $grubrecovery >> /etc/default/burg")
            def recovery_on():
                os.popen("sed -i /GRUB_DISABLE_LINUX_RECOVERY/d /etc/default/burg")
            def cmdline_apply():
                os.putenv("cmdline_options", cmdline_entry.get())
                os.popen("sed -i /GRUB_CMDLINE_LINUX_DEFAULT/d /etc/default/burg && gdefault=\'GRUB_CMDLINE_LINUX_DEFAULT=\"\'$cmdline_options\'\"\' &&  echo $gdefault >> /etc/default/burg")
            def savedefault_on():
                os.popen("sed -i \'s/GRUB_SAVEDEFAULT=[a-z]*/GRUB_SAVEDEFAULT=true/g;s/^#GRUB_SAVE/GRUB_SAVE/g\' /etc/default/burg")
            def savedefault_off():
                os.popen("sed -i \'s/GRUB_SAVEDEFAULT=[a-z]*/GRUB_SAVEDEFAULT=false/g;s/^#GRUB_SAVE/GRUB_SAVE/g\' /etc/default/burg")
            def linux16_on():
                os.popen("echo \'GRUB_LINUX16=\"\'true\'\"\' >> /etc/default/burg")
            def linux16_off():
                os.popen("sed -i /GRUB_LINUX16/d /etc/default/burg")
            def uuid_off():
                os.popen("echo \'GRUB_DISABLE_LINUX_UUID=\"\'true\'\"\' >> /etc/default/burg")
            def uuid_on():
                os.popen("sed -i /GRUB_DISABLE_LINUX_UUID/d /etc/default/burg")
            def fold_on():
                os.popen("echo \'GRUB_FOLD=\"true\'\"\' >> /etc/default/burg")
            def fold_off():
                os.popen("sed -i /GRUB_FOLD/d /etc/default/burg")

            # setup buttons and entrybox
            recovery_b1 = Button(advanced, text="Enable", command=recovery_off)
            recovery_b2 = Button(advanced, text="Disable", command=recovery_on)
            cmdline_entry = Entry(advanced, text=default_cmdline)
            cmdline_apply = Button(advanced, text="Apply", command=cmdline_apply)
            savedefault_b1 = Button(advanced, text="Enable", command=savedefault_on)
            savedefault_b2 = Button(advanced, text="Disable", command=savedefault_off)
            linux16_b1 = Button(advanced, text="Enable", command=linux16_on)
            linux16_b2 = Button(advanced, text="Disable", command=linux16_off)
            uuid_b1 = Button(advanced, text="Enable", command=uuid_off)
            uuid_b2 = Button(advanced, text="Disable", command=uuid_on)
            fold_b1 = Button(advanced, text="Enable", command=fold_on)
            fold_b2 = Button(advanced, text="Disable", command=fold_off)

            # setup geometry
            adv_label.grid(row=0, column=0, columnspan=3, pady=2)
            recovery_label.grid(row=1, column=0, pady=2, padx=2)
            recovery_b1.grid(row=1, column=1, pady=2, padx=2)
            recovery_b1.grid(row=1, column=2, pady=2, padx=2)
            cmdline_label.grid(row=2, column=0, pady=2, padx=2)
            cmdline_entry.grid(row=2, column=1, pady=2, padx=2)
            cmdline_apply.grid(row=2, column=2, pady=2, padx=2)
            savedefault_label.grid(row=3, column=0, pady=2, padx=2)
            savedefault_b1.grid(row=3, column=1, pady=2, padx=2)
            savedefault_b2.grid(row=3, column=2, pady=2, padx=2)
            linux16_label.grid(row=4, column=0, pady=2, padx=2)
            linux16_b1.grid(row=4, column=1, pady=2, padx=2)
            linux16_b2.grid(row=4, column=2, pady=2, padx=2)
            uuid_label.grid(row=5, column=0, pady=2, padx=2)
            uuid_b1.grid(row=5, column=1, pady=2, padx=2)
            uuid_b2.grid(row=5, column=2, pady=2, padx=2)
            fold_label.grid(row=6, column=0, pady=2, padx=2)
            fold_b1.grid(row=6, column=1, pady=2, padx=2)
            fold_b2.grid(row=6, column=2, pady=2, padx=2)

            advanced.resizable(0,0)
            advanced.mainloop()


        # edit /boot/burg/burg.cfg directly
        def config_edit():
            if tkMessageBox.askyesno("Open burg.cfg?", "It is a advised to edit /etc/default/burg rather than modify burg.cfg directly. Mistakes may result in BURG not loading correctly. Continue anyway?") == True:
                subprocess.Popen("gedit /boot/burg/burg.cfg || kate /boot/burg/burg.cfg || leafpad /boot/burg/burg.cfg || xterm -e nano /boot/burg/burg.cfg || xterm -e vi /boot/burg/burg.cfg", shell=True)


        # start the thread
        def mynotes():
            notesthread().start()

        # a few words from me, relies on a thread to prevent program from crashing
        class notesthread(Thread): #establish class
            def run ( self ):
                notewin = Toplevel()
                notewin.title("From the programmer...")

                notebox = Text(notewin, width=50, height=20, wrap="word", bg="black", fg="green")
                notes = "I hope that my program has been helpful. I created burg-manager-tk for a few reasons...I did this to challenge myself, to see if I could do it and to allow users to have access to burg-manager without needing BUC. Python and Tkinter tend to be pre-installed on most Linux distros and being cross-platform, it allows BSD and OS X users to use this program too, in theory. It's been an interesting experience with me and I'd say I've learnt a lot from this.\nThere's still a lot that needs to be done and we're still miles behind the original burg-manager program but for now, what we have here should be enough for the first public release: Version 0.05.\nThe code is still ugly and I'm still learning but hopefully it does the job. If you find any bugs, either contact me via the BURG forum: http://www.burgloader.com/bbs/ (my username is HoKaze) or drop me an email at hokazenoflames@gmail.co.uk. To help me sift through my email, please put something like 'burg-manager-tk bug' as the subject header.\nThanks for using my program.\n\n[END OF FILE]"
                notelength = len(notes)+1
                char_start = 0
                char_end = 1
                delay = 0.03
                notebox.pack()

                while char_end <= notelength:
                    printchar = notes[char_start:char_end]
                    notebox.insert("end", printchar)
                    time.sleep(delay)
                    char_end += 1
                    char_start += 1
                    notebox.see(END)

                notebox.config(state="disabled")
                notewin.mainloop()


        # the main frame
        frame = Frame(master)

        # define the menubar and its contents
        menubar = Menu(master)
        menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Open /etc/default/burg", command=textedit)
        menu.add_command(label="Open Terminal", command=terminal)
        menu.add_command(label="Backup /etc/default/burg", command=backup)
        menu.add_command(label="Restore Backup", command=backup_restore)
        menu.add_command(label="Delete Backup", command=backup_delete)
        menu.add_command(label="Exit", command=quit)
        menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Advanced", menu=menu)
        menu.add_command(label="*Advanced Settings*", command=advancedsettings)
        menu.add_command(label="*Open /boot/burg/burg.cfg*", command=config_edit)
        menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Info", menu=menu)
        menu.add_command(label="About", command=opendialog)
        menu.add_command(label="License", command=openlicens)
        menu.add_command(label="A few words from the programmer", command=mynotes)
        master.config(menu=menubar)

        # define the labels
        intro = Label(master, text="Welcome to burg-manager-tk!")
        hd = Label(master, text="Specify HD for install (eg: sda)")
        reslabel = Label(master, text="Specify resolution to use:")
        oslabel = Label(master, text="Specify default OS to boot:")
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
        osbutton = Button(master, text="Apply default OS", command=apply_os)

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
        os.popen("rm -rf /tmp/resolution; rm -rf /tmp/resolution_final_data; xrandr > /tmp/resolution; sed -i '/DFP/d' /tmp/resolution; sed -i '/Screen/d' /tmp/resolution; sed -i '/CRT/d' /tmp/resolution; awk '{print $1}' /tmp/resolution > /tmp/resolution_final_data")
        resoptions = open("/tmp/resolution_final_data", "r")
        resoptions = resoptions.read()
        resoptions = resoptions.replace('\n', " ")
        resoptions = resoptions.split(" ")
        resoptions.remove('') #removes blank entries
        # the resoptions.remove() commands below remove some of the options xrandr generates that burg doesn't support. This area needs to be looked into further and possibly sorted out for burg-manager (BUC) too.
        #resoptions.remove('VGA1')
        #resoptions.remove('LVDS1')
        #resoptions.remove('DP1')
        reslist_value = StringVar(master)
        reslist_value.set(resoptions[0]) #sets default option to first value
        resolution_list = OptionMenu(master, reslist_value, *resoptions) #creates drop-down list

        # define the default os list
        #the line below took ages as it was constantly complaining of errors no matter how I structured it. This was solved by using subprocess.call instead of os.popen and setting it to use bash as before it would use sh. subprocess.call was used instead subprocess.Popen to prevent a race condition between opening the file and creating it that would cause the program to crash in some circumstances. It's an ugly hack but it works...
        subprocess.call("rm -rf /tmp/oslist; linenum=$(grep -i -e menuentry /boot/burg/burg.cfg | awk -F[\\\'\\\"] '{print $2}'| sed '/./!d'|wc -l); while (( linenum >=\"0\" )) ; do input[$linenum]=$(grep -i -e menuentry /boot/burg/burg.cfg | awk -F[\\\'\\\"] '{print $2}'| sed '/./!d'| head -$linenum | /usr/bin/tail -1); echo ${input[$linenum]}; i=$(($linenum-1)); linenum=$i; done >> /tmp/oslist", shell=True, executable = "/bin/bash")
        #time.sleep(0.5)
        os_options = open("/tmp/oslist", "r")
        os_options = os_options.read()
        os_options = os_options.split('\n')
        os_options.reverse() #reverses order so it's the same as in burg
        os_options.remove('') #removes blank entries
        os_options.remove('') #removes last blank entry...?
        oslist_value = StringVar(master)
        oslist_value.set(os_options[0]) #sets default OS choice to first option
        default_os_list = OptionMenu(master, oslist_value, *os_options) #creates the drop-down list
        default_os_list.configure(wraplength=150, justify='left') #wraps long lines

	
        # setup grid geometry
        intro.grid(row=0, column=0, columnspan=2, pady=5)
        hd.grid(row=2, column=0, pady=1, padx=5)
        install.grid(row=3, column=0, pady=5)
        uninstall.grid(row=3, column=1, pady=5, padx=10)
        drive_list.grid(row=2, column=1, pady=5)
        burgemu.grid(row=4, columnspan=2, pady=5)
        restore.grid(row=5, column=0, columnspan=2, pady=5)
        reslabel.grid(row=6, column=0, pady=5)
        resolution_list.grid(row=6, column=1, pady=5)
        resolutionbutton.grid(row=7, column=0, columnspan=2, pady=2)
        timeout.grid(row=8, column=0, pady=5)
        timeoutbox.grid(row=8, column=1, pady=5)
        timeoutbutton.grid(row=9, column=0, columnspan=2, pady=2)
        oslabel.grid(row=10, column=0, pady=5)
        default_os_list.grid(row=10, column=1, pady=5)
        osbutton.grid(row=11, column=0, columnspan=2, pady=2)
        link.grid(row=12, column=0, pady=5)
        ver.grid(row=12, column=1, pady=5)

# set root window
root = Tk()

# set root window title
root.title("burg-manager-tk")

app = App(root)

root.mainloop()
