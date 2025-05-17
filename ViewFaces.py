from tkinter import Label
import os
from PIL import Image, ImageTk

# Global variable to track the state of face display
faces_displayed = False  # Initially, faces are not displayed

def toggle_show_all_faces(canvas_frame, show_faces_button):
    global faces_displayed  # Track the state

    if not faces_displayed:
        # Show all faces
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        # Get all image files from the "known_faces" directory
        known_faces_dir = "known_faces"
        image_files = [f for f in os.listdir(known_faces_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

        # Number of columns fixed at 6
        num_columns = 6
        row, col = 0, 0

        # Loop through the image files and display them
        for image_file in image_files:
            image_path = os.path.join(known_faces_dir, image_file)

            # Load the image and resize to fit within the fixed grid size
            img = Image.open(image_path)
            img.thumbnail((150, 150))  # Resize image to fit within the grid
            img = ImageTk.PhotoImage(img)

            # Create a label for the image
            image_label = Label(canvas_frame, image=img, bg="#2b2b2b")
            image_label.image = img  # Keep a reference to avoid garbage collection
            image_label.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Create a label for the image name
            name_label = Label(canvas_frame, text=os.path.splitext(image_file)[0], bg="#2b2b2b", fg="white", font=("Helvetica", 10))
            name_label.grid(row=row + 1, column=col, padx=10, pady=5, sticky="nsew")

            # Update the grid position
            col += 1
            if col >= num_columns:  # If 6 images are placed in a row, move to the next row
                col = 0
                row += 2

        faces_displayed = True  # Set the flag to True after displaying faces
        show_faces_button.config(text="Hide All Faces")  # Change button text to "Hide All Faces"

    else:
        # Hide all faces
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        faces_displayed = False  # Reset the flag
        show_faces_button.config(text="Show All Faces")  # Reset button text to "Show All Faces"
