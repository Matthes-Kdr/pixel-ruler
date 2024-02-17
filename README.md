# Pixel Ruler




> This project is based on following repositiy: https://github.com/Kitchi/pixruler.git by Kitchi and has been modified to implement more functions.


# Introduction


A simple pixel ruler written in ('pure') Python, using Tk without further dependencies or third-party-libraries.


# Usage

## General Usage
When executing the script a new window opens. As this window is transparent it can be placed on top of other windows without preventing the visibility of the actual relevant parts on the screen.
Resize this Pixel-Ruler-window to cover the region of interest and drag
your mouse pointer across whatever you want to measure. The length of
the drawned line will be printed on the terminal. 


## Additional Functions

- Create horicontal or vertical lines
  -  Hold the **'Shift'-Key** while drawing to lock one dimension. This allows you to easily create horicontal or vertical lines. 
  -  Which dimension will be locked depends on the current deltaX and deltaY in relation to the starting point: When deltaX is greater than deltaY the Y-coordinate will be locked which allows you to create horicontal lines. Otherwise the X-coordinate will be locked which allows you to create vertical lines.
  
- Use a scale as reference to determine real dimensions
    - Press the **'F5'-Key** for draw a line as a reference scale. After drawing this line prompt the desired 'real' distance for this line into the terminal (e.g. "50"). Optional you can also promt an unit for this value by append this desired unit after a single whitespace (e.g. "50 mm"). For all further measurements this scale-reference will be used to calculate the converted  distance so that additional to the pixel distance this converted distance will be printed to the terminal, too.
  - To update this scale: Press 'F5'-Key again and draw a new line as reference.
  - To reset (remove) this scale: Press 'F5'-Key again and just click on the window.


## Usage screenshots

**Basic Usage:**

![basic usage (window)](screenshots/basic_usage_window.png)

The output in the terminal for these lines is:

![basic usage (terminal)](screenshots/basic_usage_terminal.png)

**Usage with scale reference:**

![scale reference usage (window)](screenshots/scale_reference_window.png)

The output in the terminal for these (yellow highlighted) lines is:

![scale reference usage (terminal)](screenshots/scale_reference_terminal.png)


- So the bridge over the Rhein is about 347.576 m long.
- The following lines have been drawned from Maritim Hotel Köln to the Rhein.


# Installation and Prerequisites

There is no need to install third-party-packages.

To start the script navigate to the folder with the files and run pixruler.

    python pixruler.py


# Further extension options

- Function to clear window from all drawned lines

- Function to sum the distances of multiple lines

- Function to label each line with its distance


