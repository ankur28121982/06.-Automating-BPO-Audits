# Project Title
BPO Data Entry Image Comparator

## Project Description
This tool compares screenshots taken during data entry (active window) against a reference image (`image.JPG`). It highlights differences within a user-selected rectangle on the screen and logs these differences in a text file (`log.txt`). The application is designed to aid quality assurance in the BPO industry by ensuring accuracy in data entry tasks.

## Quick Steps to Run the Project:
1. Save the Python file (`window_comparator.py`) in a directory/folder.
2. Ensure that the required packages are installed (see Requirements).
3. Run the script to capture the active window screenshot and compare it with the reference image.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- PyGetWindow
- PIL (Pillow)
- tkinter

## Installation
To set up the environment and install the required packages, follow these steps:

1. Clone the repository:

   git clone https://github.com/ankur28121982/06.-Automating-BPO-Audits
   cd bpo-data-entry-comparator
   

2. Create and activate a virtual environment (optional but recommended):

   
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   

3. Install the required packages:

      pip install opencv-python-headless
   pip install numpy
   pip install pygetwindow
   pip install pillow
   ```

## Running the Script

To run the script, use the following command:


python window_comparator.py


## Script Overview

### `window_comparator.py`


import cv2
import numpy as np
import pygetwindow as gw
from PIL import Image, ImageGrab, ImageTk
import datetime
import tkinter as tk

def capture_window(window_title):
    # Function to capture the screenshot of the specified window
    ...

def draw_roi_with_mouse(image):
    # Function to allow user to draw a rectangle ROI with the mouse
    ...

def highlight_differences(imageA, imageB, output_path, roi, min_contour_size=100):
    # Function to highlight differences within the specified ROI
    ...

def log_changes(window_title, differences, log_file):
    # Function to log the differences found within the ROI
    ...

def main():
    # Main function to control the flow of the script
    ...

if __name__ == "__main__":
    main()
```


## Author

## Author
Dr. Ankur Chaturvedi
ankur1122@gmail.com

Dr. Ankur Chaturvedi is a seasoned Transformation Specialist with expertise in Consulting, Data Science, and Quality Management. He has a profound background in LEAN and Agile Transformation, having managed and optimized processes for teams of up to 3000 FTEs. Dr. Chaturvedi is currently a Senior Manager at Infosys BPM, where he spearheads process excellence, quality consulting, and organizational improvements. His skill set includes deploying data analytics, robotics, and mindset & behavior tools to drive efficiency and transformation across various domains.
