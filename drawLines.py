"""
Defines the class that does the line drawing with the callback functions
"""

from math import hypot


class DrawLine:

   def __init__(self, canvas):
      self.canvas = canvas
      self.start  = None
      self.end    = None  
      self.line   = None
      
      self.last_line = None
      self.last_label = None
      
      # For scale feature:
      self.watch_for_scale = False
      self.scale_factor = None
      self.scale_unit = None


      self.display_label = False

      self.screenshot_dir = None


      
   def distance(self, beg, end):
      """
      Calculate distance in pixels between start and end (Pythagoras)
      """

      deltax = end[0] - beg[0]
      deltay = end[1] - beg[1]

      return hypot(deltax, deltay), deltax, deltay
   



   def onclick_handler(self, event):
      """
      Handle mouse click event by storing coordinates
      """
      self.start = (event.x, event.y)
   



   def ondrag_handler(self, event, lock_dimension=False):
      """
      Callback-Function for event: dragging mouse while pressed button.
      Line should appear on the screen and connenct the current mouse location 
      with the start-position at the time of the click.

      Args:
          event: event
          lock_dimension (bool, optional): True if only horicontal OR vertical lines should be generated. Defaults to False.

      Raises:
          TypeError: when no start-point can be found.
      """
      
      if self.start is not None:
         # Erase the old line before drawing new one
         if self.line is not None:
            self.canvas.delete(self.line)

         # Handle dragging by continuously redrawing line
      
         # Calculate the current deltas to decide which coordinate to lock:
         x_temp_end, y_temp_end = self.calculate_current_end(event, lock_dimension=lock_dimension)

         # draw the linie:
         self.line = self.canvas.create_line(self.start[0], self.start[1], x_temp_end, y_temp_end)
         
      else:
         msg = "Something went wrong, the initial co-ordinates of the line"
         msg = msg + " have not been specified."
         raise TypeError(msg)

   



   def calculate_current_end(self, event, lock_dimension=False):
      """
      Calculate the current deltas to the last start-point 
      to decide which coordinate to lock.
      """
      
      if not lock_dimension:
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
      """
      Reset the current scale reference.
      """
      self.scale_factor = None
      self.scale_unit = None
      print("Scale has been resetted and removed.")




   def set_scale(self, dist):
      """
      Ask user to input the meaning of the measured distance
      (value and optional unit, seperated by single whitespace) ,
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


      entry = input("\nGive the meaning (size > 0) of the last measured line, if you want with a unit after a single whitespace:\n> ")
      
      if " " in entry:
         value, unit = entry.split(" ")
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

      # =============================================================================
      #### # Calculation of factor and printing: ####
      # =============================================================================
      

      self.scale_factor = value / dist
      self.scale_unit = unit

      print("A new scale has been set: {} pixel complies to {} {} (scale_factor = {} {}/pixel)".format(
         dist, 
         value, unit, 
         self.scale_factor, unit,
         )
      )






   def get_scaled_value(self, dist:float) -> float:
      """
      Use the current scale reference to convert the pixel distance to the user-defined-unit.
      

      Args:
          dist (float): distance (in pixel) to convert

      Returns:
          float: converted value
      """
      if not self.scale_factor:
         return dist
      

      return self.scale_factor * dist






   def get_scaled_meaning(self, dist:float) -> str:
      """
      Use the current scale reference to convert the pixel distance to the user-defined-unit.

      Args:
          dist (float): distance (in pixel) to convert

      Returns:
          str: Additional Text with distance in converted unit.
      """

      if not self.scale_factor:
         return ""
      
      converted_dist = self.get_scaled_value(dist)
      text = ", distance corresponds to {:.3f} {}".format(converted_dist, self.scale_unit)
      return text
   



   def onrelease_handler(self, event, lock_dimension=False):
      """
      Callback-function which is called when mouse-button is released.
      Calculate the current end points of the line, 
      create the line and calculate the distance in pixel 
      and (if scale reference has been provided) in the user defined unit.
      Print these results to terminal.

      Args:
          event: Tk-event
          lock_dimension (bool, optional): True if only horicontal OR vertical lines should be generated. Defaults to False.
      """

      if self.line is not None:
         self.canvas.delete(self.line)


      # Calculate the current deltas to decide which coordinate to lock:
      x_temp_end, y_temp_end = self.calculate_current_end(event, lock_dimension=lock_dimension)


      # Handle button release behaviour
      self.last_line = self.canvas.create_line(self.start[0], self.start[1], x_temp_end, y_temp_end)


      self.end = (x_temp_end, y_temp_end)

      dist, dx, dy = self.distance(self.start, self.end)

      if self.watch_for_scale:
         self.set_scale(dist)

      text = "Distance: {: 7.3f}, delta X: {: 4d}, delta Y: {: 4d}{}".format(
         dist, dx, dy, self.get_scaled_meaning(dist)
      )

      print(text)         

      if self.display_label:
         self.label_line(dist)



   def undo(self, event):
      """
      Remove the last drawned line from canvas without clearing everything.
      """
      if self.last_line:

         if self.last_label:
            self.canvas.delete(self.last_label)
         
         self.canvas.delete(self.last_line)
         print("removed last line from canvas...")

         self.last_line = None
         self.last_label = None






   def label_line(self, dist:float):
      """
      Add a text with the distance of the last line to the canvas.
      Use the value for the user-defined-unit if it has been provided by the user.

      Args:
          dist (float): value of the distance (in pixels)
      """

      # Calculate the middle of the line as the position to locate the label:
      x_start, y_start = self.start
      x_end, y_end = self.end

      x_mid = (x_end + x_start) / 2
      y_mid = (y_end + y_start) / 2


      x = x_mid
      y = y_mid

      # Build text with distance (scaled if provided) and unit (if provided)
      fractional_digits = 1 # Count of digits to display

      unit = ""
      if self.scale_unit:

         dist = self.get_scaled_value(dist)
         unit = " " + self.scale_unit

      label = str(round(dist, fractional_digits))
      label = "{}{}".format(label, unit)

      self.last_label = self.canvas.create_text(x, y, text=label, justify="center")



   def toggle_display_mode(self):
      """
      Invert the current mode for displaying labels with distance values on the canvas.
      """
      self.display_label = not self.display_label

      if self.display_label:
         notification_addition = "Display"
      else:
         notification_addition = "Do not display"

      print("Switched mode: {} distances for lines on canvas.".format(notification_addition))



   