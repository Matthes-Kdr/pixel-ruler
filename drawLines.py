"""
Defines the class that does the line drawing with the callback functions
"""

from math import hypot

class drawLine:

   def __init__(self, canvas):
      self.start  = None
      self.end    = None  
      self.line   = None
      self.canvas = canvas

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
         self.line = self.canvas.create_line(self.start[0], self.start[1], 
                                                         event.x, event.y)
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















   def onrelease_handler_general(self, event, lock=False):

      if self.line is not None:
         self.canvas.delete(self.line)


      # Calculate the current deltas to decide which coordinate to lock:
      x_temp_end, y_temp_end = self.calculate_current_end(event, lock=lock)



      # Handle button release behaviour
      self.canvas.create_line(self.start[0], self.start[1], x_temp_end, y_temp_end)


      self.end = (x_temp_end, y_temp_end)

      dist, dx, dy = self.distance(self.start, self.end)
      print("Distance: % 7.3f, delta X: % 4d, delta Y: % 4d" % (dist, dx, dy))
   





   def onrelease_handler_1d(self, event):

      self.onrelease_handler_general(event, lock=True)



   def onrelease_handler(self, event):

      self.onrelease_handler_general(event, lock=False)
