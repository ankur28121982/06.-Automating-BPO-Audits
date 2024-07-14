import cv2
import numpy as np
import pygetwindow as gw
from PIL import Image, ImageGrab, ImageTk
import datetime
import tkinter as tk

def capture_window(window_title):
    window = gw.getWindowsWithTitle(window_title)[0]
    window.activate()
    bbox = (window.left, window.top, window.right, window.bottom)
    screenshot = ImageGrab.grab(bbox)
    return np.array(screenshot)

def draw_roi_with_mouse(image):
    # Create a tkinter window
    root = tk.Tk()
    root.title("Draw ROI with Mouse")

    # Convert image to PhotoImage format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    photo_image = ImageTk.PhotoImage(image)

    # Create canvas to display image
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

    # Variables to store ROI coordinates
    roi_selected = False
    roi_coords = []

    def on_mouse_down(event):
        nonlocal roi_selected, roi_coords
        roi_coords.clear()
        roi_coords.extend([event.x, event.y, event.x, event.y])
        canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2, tag='roi')
        roi_selected = False

    def on_mouse_move(event):
        nonlocal roi_selected, roi_coords
        if roi_selected:
            canvas.coords('roi', roi_coords[0], roi_coords[1], event.x, event.y)
        else:
            canvas.coords('roi', roi_coords[0], roi_coords[1], event.x, event.y)

    def on_mouse_up(event):
        nonlocal roi_selected, roi_coords
        roi_coords[2:] = [event.x, event.y]
        roi_selected = True
        canvas.coords('roi', roi_coords[0], roi_coords[1], event.x, event.y)
        root.destroy()  # Close the tkinter window after ROI selection

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    # Start tkinter main loop
    root.mainloop()

    # Return ROI coordinates (x1, y1, x2, y2)
    return roi_coords

def highlight_differences(imageA, imageB, output_path, roi, min_contour_size=100):
    if imageA.shape != imageB.shape:
        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))

    diff = cv2.absdiff(imageA, imageB)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Create a binary mask where differences are marked
    _, binary_mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    differences = []

    # Highlight differences within the specified ROI with a rectangle
    for c in contours:
        if cv2.contourArea(c) >= min_contour_size:
            (x, y, w, h) = cv2.boundingRect(c)
            difference_rect = (x, y, x + w, y + h)

            # Check if the difference rectangle overlaps with the ROI
            if overlap(roi, difference_rect):
                differences.append(difference_rect)
                cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save image with differences highlighted
    cv2.imwrite(output_path, imageA)

    return differences

def overlap(rect1, rect2):
    # Function to check if two rectangles overlap
    (x1, y1, x2, y2) = rect1
    (x3, y3, x4, y4) = rect2
    return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

def log_changes(window_title, differences, log_file):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Window: {window_title}, Differences:\n"

    for idx, (x1, y1, x2, y2) in enumerate(differences, start=1):
        log_entry += f"    Difference {idx}: (x1={x1}, y1={y1}, x2={x2}, y2={y2})\n"

    log_entry += "\n"

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def main():
    reference_image_path = "C:/Users/Dell/Desktop/bpo_audit/image.JPG"
    captured_image_path = "C:/Users/Dell/Desktop/bpo_audit/captured_window.jpg"
    differences_image_path = "C:/Users/Dell/Desktop/bpo_audit/differences_highlighted.jpg"
    log_file = "C:/Users/Dell/Desktop/bpo_audit/log.txt"

    try:
        windows = gw.getAllTitles()
        if not windows:
            print("No windows found.")
            return

        print("Open windows:")
        for i, window in enumerate(windows):
            print(f"{i}: {window}")

        while True:
            window_index = input("Select the window index to capture (press Enter to exit): ")
            if window_index == "":
                return  # Exit if Enter is pressed without input

            try:
                window_index = int(window_index)
                if window_index < 0 or window_index >= len(windows):
                    raise ValueError
                break  # Break the loop if valid index is provided
            except ValueError:
                print("Invalid input. Please enter a valid index.")

        selected_window_title = windows[window_index]

        captured_image = capture_window(selected_window_title)
        if captured_image.size == 0:
            print("Error: Captured image is empty")
            return

        print(f"Captured image dimensions: {captured_image.shape}")

        cv2.imwrite(captured_image_path, captured_image)

        reference_image = cv2.imread(reference_image_path)
        if reference_image is None:
            print(f"Error: Unable to open reference image at {reference_image_path}")
            return

        captured_image = cv2.imread(captured_image_path)
        if captured_image is None:
            print(f"Error: Unable to open captured image at {captured_image_path}")
            return

        # Draw ROI with mouse using tkinter
        roi = draw_roi_with_mouse(captured_image)
        if len(roi) != 4:
            print("ROI selection cancelled.")
            return

        # Adjust minimum contour size for significance here (e.g., 100 pixels)
        min_contour_size_input = input("Enter the minimum contour size for significance (default is 100): ").strip()
        min_contour_size = int(min_contour_size_input) if min_contour_size_input else 100

        differences = highlight_differences(captured_image, reference_image, differences_image_path, roi, min_contour_size)
        print(f"Number of significant differences found within the selected rectangle: {len(differences)}")

        # Log the changes
        log_changes(selected_window_title, differences, log_file)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
