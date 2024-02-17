#! /usr/bin/env python
"""
Usage:
   PixelRuler

   Takes no command line arguments. Requires Python 3.x to run.

   This script measures the distance between two consecutive clicks of the
   mouse in pixels and reports it.

   Additional functions:

   - Hold the 'Shift'-Key while drawing by moving the mouse to lock one dimension. So you can get horicontal or vertical lines easyly.

   - Press 'F5'-Key for draw a line as a reference scale. After drawing prompt the meant distance into the terminal (e.g. "50 mm"). All distances of the following lines will be converted into this scale as well. To reset scale: Press 'F5'-Key again and just click on the window.
"""

from sys import argv
from drawLines import DrawLine
import tkinter as tk



DEBUG = 0 # If 1: window will not be transparent.




def modify_window_visibility(root:tk.Tk):
   """
   Make the window translucent 
   so that it can be put in the foreground on  top of other windows.
   """
   
   # Make the window translucent
   root.wait_visibility(root)
   root.configure(background='white')
   root.title("PixelRuler (Press 'F1' for printing help in terminal)")
   if DEBUG:
      return
   
   root.wm_attributes('-alpha', 0.5)

   
def show_help():
   """
   Prints the docstring of this module to terminal.
   """
   print(__doc__)




def key_handler(event, line:DrawLine):
   """
   Check if any specific key is pressed.
   Keys with special meanings:
      - F1
      - F5
      - Escape

   Args:
       event (event): Event
       line (DrawLine): Line-Object
   """

   if event.keysym == 'F1':
      show_help()


   elif event.keysym == "F5":
      # Take a scale:
      # Set a flag for line object:
      line.watch_for_scale = True
      print("Draw the line for a distance which should be use as a known reference. For resetting / removing scale reference just click once to generate a line with zero distance...")


   elif event.keysym == "Escape":
      # TODO: Clear and remove all lines or generate a new window (see #3)
      print("Function to clear all lines is not available yet. See Issue #3.")
   

def define_keybindings(root:tk.Tk, canvas:tk.Canvas, line:DrawLine):
   """
   Define all the callback functions on the canvas object.
   This allows to use keybindings.

   General format:
      
      canvas.bind("<KEYNAME>", event_handler_callback_function)

   The current event is passed automatically to the callback_function.
   If one or more additional parameters are needed in this function,
   they can be passed via lambda function:

      canvas.bind("<KEYNAME>", lambda event: event_handler_callback_function(event, additional_param))
   """
   
   # Bind the virtual F1 key to print the help-text to terminal:
   # pass line as well for updating flag-objectvariables if F5 has been pressed:
   root.bind("<Key>", lambda event: key_handler(event, line))


   # Start of line: (mouse-left-click)
   canvas.bind("<Button-1>", line.onclick_handler)


   # While Drawing: (mouse moving)
   canvas.bind("<B1-Motion>", lambda event: line.ondrag_handler(event, lock_dimension=False)) # usual mode
   canvas.bind("<Shift-B1-Motion>", lambda event: line.ondrag_handler(event, lock_dimension=True)) # locked mode for 1D-lines


   # End of line:
   canvas.bind("<ButtonRelease-1>", lambda event: line.onrelease_handler(event, lock_dimension=False)) # usual mode
   canvas.bind("<Shift-ButtonRelease-1>", lambda event: line.onrelease_handler(event, lock_dimension=True)) # locked mode for 1D-lines






# =============================================================================
#### MAIN: 
# =============================================================================
def main():

   # Print the docstring if help flag is passed
   if len(argv) > 1 and (argv[1] == '-h' or argv[1] == '--help'):
      show_help()

   # Define the root window
   root = tk.Tk()
   modify_window_visibility(root)
   canvas = tk.Canvas(root, width=200, height=200)

   # Initialize the line drawing object
   line = DrawLine(canvas)

   define_keybindings(root, canvas, line)
   canvas.pack(fill=tk.BOTH, expand=tk.YES)

   tk.mainloop()







if __name__ == '__main__':
    main()