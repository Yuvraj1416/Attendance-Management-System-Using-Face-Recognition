import cv2
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Directory to save new student photos
known_faces_dir = "known_faces"
os.makedirs(known_faces_dir, exist_ok=True)

class NewStudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("New Student Photo Capture")
        self.root.geometry("1000x600")  # Larger window size to accommodate camera and controls
        self.root.config(bg="#2e2e2e")  # Dark background

        # Variables
        self.student_name = tk.StringVar()
        self.video_capture = None
        self.photo_count = 0
        self.canvas = None
        self.photo_image = None

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Arial", 14),
                             padding=10,
                             relief="flat",
                             background="#4CAF50",
                             foreground="black",  # Default text color black
                             focuscolor="#4CAF50")
        self.style.configure("TEntry",
                             font=("Arial", 14),
                             padding=10,
                             relief="flat",
                             foreground="black",  # Default text color for entry
                             background="#f2f2f2",  # Lighter background color for input fields
                             fieldbackground="#f2f2f2")
        self.style.configure("TLabel",
                             font=("Arial", 16, "bold"),  # Bold and slightly larger font for labels
                             background="#2e2e2e",  # Dark background for labels
                             foreground="#f7f7f7")  # Light text color
        self.style.configure("TFrame", background="#2e2e2e")

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Main frame that holds both camera feed and buttons
        self.main_frame = tk.Frame(self.root, width=1000, height=600, bg="#2e2e2e")
        self.main_frame.pack(padx=20, pady=20)  # Added padding to the whole frame

        # Left side - Camera feed
        self.canvas_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.canvas_frame.pack(side="left", padx=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=480, height=360, bg="black", bd=5, relief="ridge")
        self.canvas.pack(padx=5, pady=5)

        # Right side - Controls (student name, buttons)
        self.control_frame = tk.Frame(self.main_frame, bg="#333333", padx=20, pady=20, relief="ridge", bd=2)
        self.control_frame.pack(side="left", padx=20)

        ttk.Label(self.control_frame, text="New Student Photo Capture", style="TLabel").pack(pady=20)

        ttk.Label(self.control_frame, text="Enter Student Name:", style="TLabel").pack(pady=5)
        self.name_entry = ttk.Entry(self.control_frame, textvariable=self.student_name, style="TEntry", width=25)
        self.name_entry.pack(pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Start Camera", style="TButton", command=self.start_camera)
        self.start_button.pack(pady=10, fill="x")

        self.capture_button = ttk.Button(self.control_frame, text="Capture Photo", style="TButton", command=self.capture_photo, state="disabled")
        self.capture_button.pack(pady=10, fill="x")

        self.stop_button = ttk.Button(self.control_frame, text="Stop Camera", style="TButton", command=self.stop_camera, state="disabled")
        self.stop_button.pack(pady=10, fill="x")

        # Add hover effect to buttons
        self.add_hover_effect(self.start_button, "#45a049", "#4CAF50")
        self.add_hover_effect(self.capture_button, "#45a049", "#4CAF50")
        self.add_hover_effect(self.stop_button, "#45a049", "#4CAF50")

        # Add text color change effect for buttons
        self.add_text_hover_effect(self.start_button)
        self.add_text_hover_effect(self.capture_button)
        self.add_text_hover_effect(self.stop_button)

        # Add interactivity to the name entry input
        self.add_interactivity_to_entry(self.name_entry)

    def add_hover_effect(self, button, hover_color, normal_color):
        """Function to add hover effect to buttons"""
        button.bind("<Enter>", lambda e: self.on_hover(button, hover_color))
        button.bind("<Leave>", lambda e: self.on_leave(button, normal_color))
        button.bind("<ButtonPress-1>", lambda e: self.on_click(button))
        button.bind("<ButtonRelease-1>", lambda e: self.on_leave(button, normal_color))

    def on_hover(self, button, color):
        """Change button color on hover"""
        button.config(background=color)

    def on_leave(self, button, color):
        """Change button color when hover ends"""
        button.config(background=color)

    def on_click(self, button):
        """Change button text style on click"""
        button.config(foreground="black", font=("Arial", 14, "bold"))  # Bold and black text

    def add_text_hover_effect(self, button):
        """Function to change text color on hover"""
        button.bind("<Enter>", lambda e: self.on_text_hover(button))
        button.bind("<Leave>", lambda e: self.on_text_leave(button))

    def on_text_hover(self, button):
        """Change button text color to blue on hover"""
        button.config(foreground="blue", font=("Arial", 14))

    def on_text_leave(self, button):
        """Revert text color to black when hover ends"""
        button.config(foreground="black", font=("Arial", 14))

    def add_interactivity_to_entry(self, entry):
        """Function to add interactivity to the input box"""
        # Add focus and hover effect to the input box
        entry.bind("<FocusIn>", lambda e: self.on_focus_in(entry))
        entry.bind("<FocusOut>", lambda e: self.on_focus_out(entry))
        entry.bind("<Enter>", lambda e: self.on_entry_hover(entry))
        entry.bind("<Leave>", lambda e: self.on_entry_leave(entry))

    def on_focus_in(self, entry):
        """Change border color when focused"""
        entry.config(style="TEntry")
        entry.config(background="#e7f3fe", relief="solid")

    def on_focus_out(self, entry):
        """Reset border and background color when focus is lost"""
        entry.config(background="#f2f2f2", relief="flat")

    def on_entry_hover(self, entry):
        """Change background color when hovered"""
        entry.config(background="#f0f8ff")

    def on_entry_leave(self, entry):
        """Reset background color when hover ends"""
        entry.config(background="#f2f2f2")

    def start_camera(self):
        if not self.student_name.get().strip():
            messagebox.showerror("Error", "Student name cannot be empty!")
            return

        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        self.photo_count = 0
        self.start_button.config(state="disabled")
        self.capture_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.show_camera_feed()

    def show_camera_feed(self):
        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                # Convert the frame to RGB (OpenCV uses BGR by default)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert to Image
                image = Image.fromarray(frame_rgb)
                self.photo_image = ImageTk.PhotoImage(image=image)

                # Update canvas with the new image
                self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")

            # Keep updating the feed in a loop
            self.root.after(10, self.show_camera_feed)

    def capture_photo(self):
        if not self.video_capture or not self.video_capture.isOpened():
            messagebox.showerror("Error", "Camera is not running.")
            return

        ret, frame = self.video_capture.read()
        if ret:
            student_name = self.student_name.get().strip()
            photo_path = os.path.join(known_faces_dir, f"{student_name}.jpg")
            cv2.imwrite(photo_path, frame)
            messagebox.showinfo("Success", f"Photo saved at {photo_path}.")
        else:
            messagebox.showerror("Error", "Failed to capture photo.")

    def stop_camera(self):
        if self.video_capture and self.video_capture.isOpened():
            self.video_capture.release()
            cv2.destroyAllWindows()

        # Clear the student name input
        self.student_name.set("")  # Clears the text in the input field

        # Disable and enable appropriate buttons
        self.start_button.config(state="normal")
        self.capture_button.config(state="disabled")
        self.stop_button.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = NewStudentApp(root)
    root.mainloop()
