import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os


class WebcamApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")

        # Open the webcam (0 or 1 can be used for default webcams, 2 is often an external webcam)
        self.video_capture = cv2.VideoCapture(0)  # Adjust the camera index if needed

        # Check if the video capture is successful
        if not self.video_capture.isOpened():
            print("Error: Could not open webcam")
            self.window.quit()

        self.current_image = None
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        self.download_button = tk.Button(window, text="Capture", command=self.download_image)
        self.download_button.pack()

        self.update_webcam()  # Start webcam feed

    def update_webcam(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Convert the frame to RGB (from BGR which OpenCV uses)
            self.current_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Convert the Image object into ImageTk object
            self.photo = ImageTk.PhotoImage(image=self.current_image)

            # Display the image on canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # Call update_webcam after 15 ms
            self.window.after(15, self.update_webcam)

    def download_image(self):
        if self.current_image is not None:
            # Get the path for the Downloads folder dynamically
            download_folder = os.path.expanduser("~/Downloads")
            file_path = os.path.join(download_folder, "captured_image.jpg")

            # Save the image to the specified path
            self.current_image.save(file_path)

            # Open the file with the default image viewer
            os.startfile(file_path)


# Create the Tkinter window
root = tk.Tk()

# Initialize the webcam app
app = WebcamApp(root)

# Start the Tkinter event loop
root.mainloop()
