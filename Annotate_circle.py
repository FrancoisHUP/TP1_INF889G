import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from math import sqrt

class CircleAnnotationApp:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.load_image(image_path)
        self.annotations = []

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.undo_button = tk.Button(root, text="Undo", command=self.undo)
        self.undo_button.pack()


    def load_image(self, image_path):
        # Load the image
        self.image = Image.open(image_path)
        
        # Calculate the new size preserving the aspect ratio
        original_width, original_height = self.image.size
        target_width = 1200
        target_height = 900
        ratio = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Check for the best available resampling method
        try:
            # For Pillow versions 8.0.0 and later
            resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            try:
                # For versions between 7.0.0 (inclusive) and 8.0.0 (exclusive)
                resample_method = Image.LANCZOS
            except AttributeError:
                # For versions before 7.0.0
                resample_method = Image.ANTIALIAS
        
        # Resize the image using the determined resampling method
        self.image = self.image.resize((new_width, new_height), resample_method)
        self.photo = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(self.root, width=new_width, height=new_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.start_x = None
        self.start_y = None
        self.current_circle = None
        self.current_center = None


    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Remove the previous circle
        if self.current_circle:
            self.canvas.delete(self.current_circle)

        if self.current_center:
            self.canvas.delete(self.current_center)
        
        # Calculate the radius
        radius = sqrt((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2)

        # Draw the new circle
        self.current_circle = self.canvas.create_oval(
            self.start_x - radius, self.start_y - radius, 
            self.start_x + radius, self.start_y + radius,
            outline='red'
        )

        # Draw the center point of the circle
        center_size = 4  # Size of the center point, adjust as needed
        self.current_center = self.canvas.create_oval(
            self.start_x - center_size, self.start_y - center_size,
            self.start_x + center_size, self.start_y + center_size,
            fill='blue'
        )

    def on_release(self, event):
        # Calculate the final radius and add the annotation
        radius = sqrt((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) 
        
        # Normalize the coordinates and radius
        norm_start_x = self.start_x / 1200  # Assuming 1200 is the width of the canvas
        norm_start_y = self.start_y / 900   # Assuming 900 is the height of the canvas
        norm_radius = radius / 1200         # Normalize based on the max dimension for aspect ratio

        # Append the normalized annotation
        self.annotations.append((self.current_circle, self.current_center, norm_start_x, norm_start_y, norm_radius))

        # self.annotations.append((self.start_x, self.start_y, radius))
        # Reset current circle
        self.current_circle = None
        self.current_center = None
        print("Annotations:", self.annotations)

    def undo(self, event=None):
        if self.annotations:
            last_annotation = self.annotations.pop()
            self.canvas.delete(last_annotation[0])  # Delete the circle from the canvas
            if len(last_annotation) > 1:
                # If you're storing the center point separately and want to delete it too
                self.canvas.delete(last_annotation[1])
            print("Undo: Removed last annotation.")

    def close_and_save(self):
        # Save the annotations to a file
        with open("annotations.txt", "w") as file:
            for annotation in self.annotations:
                file.write(f"{annotation[2]},{annotation[3]},{annotation[4]}\n")
        print("Annotations saved to annotations.txt")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    # Prompt the user to select an image file
    image_path = filedialog.askopenfilename(title="Select an image file")
    if image_path:
        app = CircleAnnotationApp(root, image_path)
        root.protocol("WM_DELETE_WINDOW", app.close_and_save)  # Save on window close
        root.mainloop()
    else:
        print("No image selected.")
