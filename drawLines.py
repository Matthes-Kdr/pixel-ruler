"""
Defines the class that does the line drawing with the callback functions
"""

from math import hypot

import tkinter as tk


class DrawLine:

   def __init__(self, canvas):
      self.start  = None
      self.end    = None  
      self.line   = None
      self.canvas = canvas
      
      # For scale feature:
      self.watch_for_scale = False
      self.scale_factor = None
      self.scale_unit = None


   def distance(self, beg, end):
      """
      Calculate distance in pixels between start and end (Pythagoras)
      """

      deltax = end[0] - beg[0]
      deltay = end[1] - beg[1]

      return hypot(deltax, deltay), deltax, deltay

   def onclick_handler(self, event):
      # Handle mouse click event by storing coordinates
      self.start = (event.x, event.y)
   





   def ondrag_handler(self, event):
      if self.start is not None:
         # Erase the old line before drawing new one
         if self.line is not None:
            self.canvas.delete(self.line)

         # Handle dragging by continuously redrawing line
         self.line = self.canvas.create_line(self.start[0], self.start[1], event.x, event.y)
      else:
         msg = "Something went wrong, the initial co-ordinates of the line"
         msg = msg + " have not been specified."
         raise TypeError(msg)


   def ondrag_handler_1d(self, event):
      
      
      if self.start is not None:
         # Erase the old line before drawing new one
         if self.line is not None:
            self.canvas.delete(self.line)




         # Handle dragging by continuously redrawing line
      
      
         # Calculate the current deltas to decide which coordinate to lock:
         x_temp_end, y_temp_end = self.calculate_current_end(event, lock=True)


         # draw the 1D-linie:
         self.line = self.canvas.create_line(self.start[0], self.start[1], x_temp_end, y_temp_end)
         
      
      
      else:
         msg = "Something went wrong, the initial co-ordinates of the line"
         msg = msg + " have not been specified."
         raise TypeError(msg)

































   def calculate_current_end(self, event, lock=False):
      """
      Calculate the current deltas to decide which coordinate to lock.
      """
      
      if not lock:
         return event.x, event.y

      x_temp_end, y_temp_end = event.x, event.y
      
      
      dist, dx, dy = self.distance(self.start, (x_temp_end, y_temp_end))

      if abs(dx) > abs(dy):
         # lock y as x is the dominant component 
         y_temp_end = self.start[1]
      else:
         x_temp_end = self.start[0]

      return x_temp_end, y_temp_end













   def reset_scale(self):
      # Reset scale:
      self.scale_factor = None
      self.scale_unit = None
      print("Scale has been resetted and removed.")


   def set_scale(self, dist):
      """
      Ask user to input the meaning of the measured distance
      (value and optional unit, seperated by '*') ,
      Check entry for validation and call this func recursive if not valid,
      if valid: calculate and store the scale_factor into the object.

      Args:
          dist (float): Measured distance in pixel.
      """
    
      self.watch_for_scale = False # Reset flag

      # =============================================================================
      #### # User-Input and Validation: ####
      # =============================================================================
      
      if dist == 0:
         self.reset_scale()
         return


      entry = input("\nGive the meaning (size > 0) of the last measured line, if you want with a unit after a '*' Symbol:\n> ")
      
      if "*" in entry:
         value, unit = entry.split("*")
      else:
         value = entry
         unit = "user_defined_unit"

      try:
         value = float(value)
         if value == 0:
            raise ValueError("value must not be 0")

      except ValueError:
         print("ERROR! The input  '{}' is not valid!".format(entry))
         self.set_scale(dist)
         return

      # if value == 0:
      #    self.reset_scale()
      #    return

      # Calculation of factor and reset:

      self.scale_factor = value / dist
      self.scale_unit = unit

      print("A new scale has been set: {} pixel complies to {} {} (scale_factor = {} {}/pixel)".format(
         dist, 
         value, unit, 
         self.scale_factor, unit,
         )
      )






   def get_scaled_meaning(self, dist:float) -> str:


      if not self.scale_factor:
         return ""
      
      converted_dist = self.scale_factor * dist
      
      text = ", distance corresponds to {:.3f} {}".format(converted_dist, self.scale_unit)

                                          
      return text
   



   def onrelease_handler_general(self, event, lock=False):

      if self.line is not None:
         self.canvas.delete(self.line)


      # Calculate the current deltas to decide which coordinate to lock:
      x_temp_end, y_temp_end = self.calculate_current_end(event, lock=lock)



      # Handle button release behaviour
      self.canvas.create_line(self.start[0], self.start[1], x_temp_end, y_temp_end)


      self.end = (x_temp_end, y_temp_end)

      dist, dx, dy = self.distance(self.start, self.end)
      # print("Distance: % 7.3f, delta X: % 4d, delta Y: % 4d" % (dist, dx, dy))

      if self.watch_for_scale:
         
         # self.input_required.set(True)  # Set the flag to require input
         
         self.set_scale(dist)

         # self.canvas.wait_variable(self.input_required)  # Wait for input


      
      # converted_for_scale = "Distance corresponds to {}".format(self.get_scaled_meaning(dist))


      text = "Distance: {: 7.3f}, delta X: {: 4d}, delta Y: {: 4d}{}".format(
         dist, dx, dy, self.get_scaled_meaning(dist)
      )

      print(text)         

   





   def onrelease_handler_1d(self, event):

      self.onrelease_handler_general(event, lock=True)



   def onrelease_handler(self, event):

      self.onrelease_handler_general(event, lock=False)
