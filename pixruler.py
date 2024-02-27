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

   - Press "L"-Key to toggle mode for displaying distances on canvas
   
   - Press "Ctrl" + "Z" -Keys to remove the last drawned line

   - Press "esc" -Key to delete all lines on the canvas.
"""

import os
from sys import argv
from drawLines import DrawLine
import tkinter as tk
from tkinter.filedialog import askdirectory


DEBUG = 0 # If 1: window will not be transparent.






def capture_screenshot(root:tk.Tk, canvas:tk.Canvas,line:DrawLine):
   """
   Capture a screenshot of the current region of the window 
   and save it to a directory which is asked for by a fileDialoge.
   By now the lines won't be captured at all, 
   the window is just used as a region which could be moved to another region
   while its size stays constant...

   ### TODO: possibility to capture the content of the window 
   """
   

   try:
      import pyautogui
   except ModuleNotFoundError("To capture screenshot the module 'pyautogui' must be installed! Please install it and try again."):
      return
   


   w = canvas.winfo_width()
   h = canvas.winfo_height()
   
   
   x = canvas.winfo_rootx()
   y = canvas.winfo_rooty()

   if not line.screenshot_dir:
      line.screenshot_dir = askdirectory(initialdir="Desktop")



   # pyautogui.screenshot(save_path, region= (0,0,200,200))

   print("! NOTE : When you are using multiple monitors, the screenshot function will only work at the primary monitor! Otherwise you will get a black rectangle!")

   toggle_title_bar(root, True)
   root.wm_attributes('-alpha', 0.1)
   # However in this case even the widgets on the root will inherit the transparency.



   img = pyautogui.screenshot(region= (x,y, w, h))
   

   number = 0
   while True:
      file_path = os.path.join(line.screenshot_dir, "screenshot_pixelruler_{}.png".format(str(number).zfill(4)))
      if os.path.isfile(file_path):
         number += 1
      else:
         break
   

   img.save(file_path)

   toggle_title_bar(root, False)
   root.wm_attributes('-alpha', 0.3)







def modify_window_visibility(root:tk.Tk):
   """
   Make the window translucent 
   so that it can be put in the foreground on  top of other windows.
   """
   
   # Make the window translucent
   root.wait_visibility(root)
   root.configure(background='white')
   root.title("Resize window to relevant region. Toggle tittlebar: F11 / F12")
   # root.overrideredirect(True)
   if DEBUG:
      return
   
   root.wm_attributes('-alpha', 0.3)
   
   # root.wm_attributes('-alpha', 0.01)

   
def show_help():
   """
   Prints the docstring of this module to terminal.
   """
   print(__doc__)


def toggle_title_bar(root:tk.Tk, val:bool):
   
   root.overrideredirect(val)



def key_handler(event, line:DrawLine, canvas:tk.Canvas, root:tk.Tk):
   """
   Check if any specific key is pressed.
   Keys with special meanings:
      - F1 : to display help text in terminal
      - F5 : to set a new scale reference
      - L  : to toggle mode for displaying labels with distance
      - Ctrl + Z : to undo / remove the last drawned line from canvas
      - Escape : to clear entire canvas

   Args:
       event (event): Event
       line (DrawLine): Line-Object
       canvas (tk.Canvas) : canvas object
   """

   if event.keysym == 'F1':
      show_help()


   if event.keysym == 'F8':

      capture_screenshot(root, canvas, line)


   if event.keysym == 'F11':
      toggle_title_bar(root, True)
      root.wm_attributes('-alpha', 0.1)


   if event.keysym == 'F12':
      toggle_title_bar(root, False)
      root.wm_attributes('-alpha', 0.3)


   elif event.keysym == "F5":
      # Take a scale:
      # Set a flag for line object:
      line.watch_for_scale = True
      print("Draw the line for a distance which should be use as a known reference. For resetting / removing scale reference just click once to generate a line with zero distance...")


   elif event.keysym in ["L", "l"]:
      line.toggle_display_mode()


   elif event.keysym == "Escape":
      print("Clearing all lines...")
      canvas.delete("all")
      line.last_line = None

   

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
   root.bind("<Key>", lambda event: key_handler(event, line, canvas, root))

   root.bind("<Control-z>", line.undo)


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
    
    note_text = "This version is NOT FOR THE ACTUAL USAGE OF A RULER! It does only uses some of the implemented functions to generate a window to move and resize it as wished to capture screenshots with ALT + DRUCK (print) of this window. Herefore the  window has no title bar anymore , only a frame."
    
    print(note_text)
    
    main()