import cv2
import face_recognition
import os
import csv
from datetime import datetime, timedelta
import sys

# Load known face encodings and names
known_face_encodings = []
known_face_names = []

# Get all image files from the "known_faces" directory
known_faces_dir = "known_faces"
image_files = [f for f in os.listdir(known_faces_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Load each image and get its encoding and name (filename without extension)
for image_file in image_files:
    image_path = os.path.join(known_faces_dir, image_file)

    # Load the image
    image = face_recognition.load_image_file(image_path)

    # Get face encoding
    encoding = face_recognition.face_encodings(image)

    if encoding:  # If at least one face is found
        known_face_encodings.append(encoding[0])  # Use the first face encoding
        # Get the name from the filename (without extension)
        name = os.path.splitext(image_file)[0]
        known_face_names.append(name)

# Initialize webcam
video_capture = cv2.VideoCapture(0)  # Try using 0 or 1 if needed

# Check if the camera is opened successfully
if not video_capture.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Open the CSV file for logging face recognition
log_file = "face_recognition_log.csv"

# If the log file doesn't exist, create it and write headers
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Timestamp"])

# Dictionary to track the last logged time and marking status for each person
last_logged_times = {}
marking_status = {}

# Function to start face recognition
def start_recognition():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Ensure the frame is not None
        if frame is None:
            print("Received empty frame!")
            break

        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            marked = False  # To track if the person is marked in the log

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Get current time
                current_time = datetime.now()

                # Check if the name has been logged within the last 5 minutes
                if name not in last_logged_times or current_time - last_logged_times[name] >= timedelta(minutes=5):
                    # Log the name and timestamp to the CSV file
                    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                    with open(log_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([name, timestamp])

                    # Update the last logged time and marking status for the person
                    last_logged_times[name] = current_time
                    marking_status[name] = True  # Set marking status to True
                else:
                    marking_status.setdefault(name, False)  # Default to False if not logged

            # Determine the color and label based on marking status
            if marking_status.get(name, False):
                label = f"{name} - Marked"
                color = (0, 255, 0)  # Green for marked
            else:
                label = name
                color = (0, 0, 255)  # Red for unmarked

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Display the name and status
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Display the resulting frame
        cv2.imshow("Video", frame)

        # Break the loop when the 'q' key is pressed or window is closed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Check if the window was closed
        if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
            print("Window closed by user.")
            break

    # Release the webcam and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()
    sys.exit(0)  # Exit the program immediately

if __name__ == "__main__":
    start_recognition()
