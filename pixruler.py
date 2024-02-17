#! /usr/bin/env python
"""
Usage:
   pixruler

   Takes no command line arguments. Requires Python 2.x to run.

   This script measures the distance between two consecutive clicks of the
   mouse in pixels and reports it.
"""

from sys       import argv
from drawLines import drawLine
from math      import hypot
import tkinter as tk
# import Tkinter as tk



DEBUG = 1

def modify_window_visibility():
   """
   Make the window translucent 
   so that it can be put in the foreground on  top of other windows.
   """
   
   # Make the window translucent
   root.wait_visibility(root)
   root.configure(background='white')
   
   if DEBUG:
      return
   
   root.wm_attributes('-alpha', 0.5)



# Print the docstring if help flag is passed
if len(argv) > 1 and (argv[1] == '-h' or argv[1] == '--help'):
   print(__doc__)




# Define the root window
root = tk.Tk()

modify_window_visibility()

canvas   = tk.Canvas(root, width=200, height=200)

# Initialize the line drawing object
line  = drawLine(canvas)

# Define the callback functions on the canvas object

# Start of line:
canvas.bind("<Button-1>", line.onclick_handler)

# While Drawing:
canvas.bind("<B1-Motion>", line.ondrag_handler) # usual mode

canvas.bind("<Shift-B1-Motion>", line.ondrag_handler_1d) # locked mode for 1D-lines


# End of line:
canvas.bind("<ButtonRelease-1>", line.onrelease_handler) # usual mode
canvas.bind("<Shift-ButtonRelease-1>", line.onrelease_handler_1d) # locked mode for 1D-lines


# TEST:
# canvas.bind("<Shift-B1-Motion>", line.onrelease_handler)

canvas.pack(fill=tk.BOTH, expand=tk.YES)

tk.mainloop()
