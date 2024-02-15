# pixruler
A simple pixel ruler written in Python, using Tk.

I have tried to base this on "pure" Python as far as I can, so I will not
be porting it to Qt or GTK anytime soon. Window compositing will have to
be enabled, and transparency supported for this pixel ruler to work.

Resize the pixel ruler screen to cover the region of interest, and drag
your mouse pointer across whatever you want to measure. The length of
the line will be printed on the terminal. 

I'm using this project to learn some basic Tcl/Tk so once I figure out
better ways of doing things, I'll incorporate them in here.


Installation
------------
Add the folder containing the files to your PYTHONPATH variable, and/or
navigate to the folder and run pixruler.py like

    python pixruler.py

NOTE: You will have to have Python 2 installed with Tk support. In some 
newer distros (Arch), the Python 2 interpreter is called `python2`. 
