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

   def onrelease_handler(self, event):
      if self.line is not None:
         self.canvas.delete(self.line)
      # Handle button release behaviour
      self.canvas.create_line(self.start[0], self.start[1], event.x, event.y)
      
      self.end = (event.x, event.y)

      dist, dx, dy = self.distance(self.start, self.end)
      print("Distance: % 7.3f, delta X: % 4d, delta Y: % 4d" % (dist, dx, dy))

