import cv2
import numpy as np
from tkinter import Tk, filedialog
from tkinter import messagebox


# Hàm để thay đổi kích thước hình ảnh cho vừa cửa sổ
def resize_image(image, window_width=800, window_height=600):
  h, w = image.shape[:2]
  scale_w = window_width / w
  scale_h = window_height / h
  scale = min(scale_w, scale_h)
  new_w = int(w * scale)
  new_h = int(h * scale)
  resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
  return resized_image


# Hàm làm nét hình ảnh
def sharpen_image(img):
  # Kernel làm nét
  kernel_sharpen = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
  sharpened_img = cv2.filter2D(img, -1, kernel_sharpen)
  return sharpened_img


# Hàm tải hình ảnh từ máy tính
def load_image():
  Tk().withdraw()  # Ẩn cửa sổ Tkinter gốc
  file_path = filedialog.askopenfilename(title="Select X-ray Image", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
  if file_path:
    img = cv2.imread(file_path)
    if img is None:
      messagebox.showerror("Error", "Could not load the image!")
      return

    # Thay đổi kích thước hình ảnh
    resized_img = resize_image(img)

    # Hiển thị hình ảnh gốc
    cv2.imshow('Original X-ray Image', resized_img)

    # Áp dụng làm nét
    sharpened_img = sharpen_image(resized_img)

    # Hiển thị hình ảnh sau khi làm nét
    cv2.imshow('Sharpened X-ray Image', sharpened_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
  else:
    messagebox.showwarning("Warning", "No file was selected!")


if __name__ == "__main__":
  load_image()
