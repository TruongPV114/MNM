import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class XRayEnhancementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-Ray Image Enhancement")

        self.img = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        # Button to select an image
        btn_select_image = Button(self.root, text="Select X-Ray Image", command=self.select_image)
        btn_select_image.pack(side="top", padx=10, pady=10)

        # Button to sharpen the image
        btn_sharpen_image = Button(self.root, text="Sharpen Image", command=self.sharpen_image)
        btn_sharpen_image.pack(side="top", padx=10, pady=10)

        # Button to save the image
        btn_save_image = Button(self.root, text="Save Enhanced Image", command=self.save_image)
        btn_save_image.pack(side="top", padx=10, pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # Read X-ray image as grayscale
            if self.img is None:
                messagebox.showerror("Error", "Unable to load image.")
            else:
                self.processed_image = self.img.copy()  # Initialize processed image
                self.display_image(self.img)

    def sharpen_image(self):
        if self.img is not None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
            self.processed_image = cv2.filter2D(self.img, -1, kernel)
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Success", f"Enhanced image saved at {file_path}")
        else:
            messagebox.showwarning("Warning", "No processed image to save.")

    def display_image(self, img):
        # Create a new window for displaying the image
        image_window = Toplevel(self.root)
        image_window.title("Image Display")

        # Resize the image to fit the window
        height, width = img.shape
        aspect_ratio = width / height
        new_width = 600  # Set a fixed width for the window
        new_height = int(new_width / aspect_ratio)

        # Resize the image
        img_resized = cv2.resize(img, (new_width, new_height))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB)  # Convert to RGB
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        # Create a label to display the image
        label = Label(image_window, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.pack()

        # Set window size to fit the resized image
        image_window.geometry(f"{new_width}x{new_height}")


if __name__ == "__main__":
    root = Tk()
    app = XRayEnhancementApp(root)
    root.mainloop()
