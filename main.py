from tkinter import Label, PhotoImage, messagebox, ttk
import tkinter as tk
from ViewFaces import toggle_show_all_faces  # Import the toggle function
from face_recognition_module import start_recognition  # Importing the function from the face recognition module
import pandas as pd
from newStudent import NewStudentApp

# Function for logging
def start_recognition_thread():
    import threading
    recognition_thread = threading.Thread(target=start_recognition, daemon=True)
    recognition_thread.start()

def open_new_student_app():
    new_student_window = tk.Toplevel(root)  # Create a new top-level window
    app = NewStudentApp(new_student_window)  # Create the NewStudentApp inside this window

def show_logs():
    try:
        # Read the CSV file
        df = pd.read_csv('face_recognition_log.csv')

        # Create a new window for displaying the logs
        logs_window = tk.Toplevel(root)
        logs_window.title("Face Recognition Logs")
        logs_window.geometry("900x500")
        logs_window.config(bg="#2b2b2b")  # Dark theme background

        # Header Label
        header = tk.Label(
            logs_window,
            text="Face Recognition Logs",
            font=("Helvetica", 16, "bold"),
            bg="#2b2b2b",
            fg="#f0f0f0"
        )
        header.pack(pady=10)

        # Frame for Treeview and scrollbar
        frame = tk.Frame(logs_window, bg="#2b2b2b")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create a Treeview widget to display the table
        tree = ttk.Treeview(
            frame,
            columns=list(df.columns),
            show='headings',
            height=20,
            style="Custom.Treeview"
        )

        # Configure Treeview style
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="#333333",
            foreground="#ffffff",
            rowheight=25,
            fieldbackground="#333333",
            font=("Helvetica", 11)
        )
        style.map("Custom.Treeview", background=[("selected", "#4CAF50")])

        # Configure the columns
        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=150)

        # Insert rows into the Treeview
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Add a horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

        # Pack the Treeview
        tree.pack(fill="both", expand=True)

        # Add a close button
        close_button = tk.Button(
            logs_window,
            text="Close",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            relief="flat",
            command=logs_window.destroy
        )
        close_button.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "The log file 'face_recognition_log.csv' does not exist.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the logs: {e}")

# Function for clearing the logs (optional)
def clear_logs():
    try:
        # Delete the CSV file
        import os
        os.remove('face_recognition_log.csv')
        messagebox.showinfo("Logs Cleared", "All logs have been successfully cleared.")
    except FileNotFoundError:
        messagebox.showinfo("No Logs Found", "There are no logs to clear.")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while clearing logs: {e}")


# Tkinter GUI setup
root = tk.Tk()
root.title("Face Recognition Interface")

# Setting up the window size and background color
root.geometry("1070x850")  # Larger initial size to accommodate buttons and images
root.config(bg="#2b2b2b")  # Dark background color

# Font styling
font_style = ("Helvetica", 12, "bold")
# Add "DPA" text at the top-left corner
dpa_label = tk.Label(root, text="DPA", font=("Helvetica", 14, "bold"), bg="#2b2b2b", fg="#f0f0f0")
dpa_label.place(x=10, y=10)  # Adjust x and y as needed for positioning

# Create a frame to hold the buttons for a more organized layout
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(padx=20, pady=30, fill="both", expand=False)

# Header Label
header_label = tk.Label(root, text="Face Recognition System Using face_recognition", font=("Helvetica", 16, "bold"), bg="#2b2b2b", fg="#f0f0f0")
header_label.pack(pady=10, fill="x")

# Add a separator line for better visual separation
separator = tk.Frame(root, height=2, bg="#f0f0f0")
separator.pack(fill="x", padx=20, pady=10)

# Create a frame for the images and buttons to be arranged horizontally
button_frame = tk.Frame(frame, bg="#2b2b2b")
button_frame.pack(pady=10, fill="both", expand=True)

# Configure grid to resize dynamically with the window
button_frame.columnconfigure(0, weight=1, uniform="group")
button_frame.columnconfigure(1, weight=1, uniform="group")
button_frame.columnconfigure(2, weight=1, uniform="group")
button_frame.columnconfigure(3, weight=1, uniform="group")

# Function to create a button with an image above it
def create_button_with_image(image_path, text, command, column):
    # Load the image
    image = PhotoImage(file=image_path)
    image = image.subsample(3, 3)  # Adjust size if necessary

    # Create an image label
    image_label = tk.Label(button_frame, image=image, bg="#2b2b2b")
    image_label.image = image  # Keep a reference to avoid garbage collection
    image_label.grid(row=0, column=column, padx=20, pady=10, sticky="nsew")  # Place image above button

    # Create the button
    button = tk.Button(
        button_frame,
        text=text,
        font=font_style,
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        command=command,
        relief="flat",
        bd=0,
        activebackground="#45a049"
    )
    button.grid(row=1, column=column, padx=20, pady=10, sticky="nsew")  # Place button below the image

# Create buttons with images above them in a horizontal layout
create_button_with_image("pics/start.png", "Take Attendence", start_recognition_thread, 0)
show_faces_button = create_button_with_image("pics/list.png", "Show All Faces", lambda: toggle_show_all_faces(canvas_frame, show_faces_button), 1)
create_button_with_image("pics/log.png", "View Logs", show_logs, 2)

# Adding the Add New Student button with an image
create_button_with_image("pics/addNew.png", "Register new Face", open_new_student_app, 3)




# Create a canvas to hold the image frame for scrolling
canvas = tk.Canvas(root, bg="#2b2b2b")
canvas.pack(fill="both", expand=True, padx=20, pady=20)

# Create scrollbars
v_scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
v_scrollbar.pack(side="right", fill="y")

h_scrollbar = tk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
h_scrollbar.pack(side="bottom", fill="x")

canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Create a frame inside the canvas to hold the images
canvas_frame = tk.Frame(canvas, bg="#2b2b2b")
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

# Configure the canvas to resize with the window
canvas_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Configure fixed grid size for canvas_frame
for i in range(6):  # 6 columns
    canvas_frame.columnconfigure(i, weight=0, minsize=160)  # Fixed width for each column (160px)

# Configure rows for a fixed height for images and names
canvas_frame.rowconfigure(0, weight=0, minsize=160)  # Fixed height for image rows
canvas_frame.rowconfigure(1, weight=0, minsize=40)   # Fixed height for name rows

# Start the Tkinter event loop
root.mainloop()
