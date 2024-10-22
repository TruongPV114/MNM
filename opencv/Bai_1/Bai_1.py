import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Khởi tạo biến toàn cục
captured_frame = None
original_frame = None  # Khung hình gốc
start_point = None  # Điểm bắt đầu cho vùng chọn
end_point = None  # Điểm kết thúc cho vùng chọn
rect_drawing = False  # Cờ cho việc kéo thả chuột để chọn vùng


def apply_filter(filter_type, frame=None):
  global img, captured_frame
  if frame is None:
    frame = captured_frame  # Nếu không có khung hình từ camera, dùng khung hình đã chụp

  if filter_type == 'Identity':
    kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    output = cv2.filter2D(frame, -1, kernel_identity)
  elif filter_type == 'Gaussian':
    output = cv2.GaussianBlur(frame, (5, 5), 0)
  elif filter_type == 'Sharpen':
    kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    output = cv2.filter2D(frame, -1, kernel_sharpen)
  elif filter_type == 'Blur':
    output = cv2.GaussianBlur(frame, (15, 15), 0)
  elif filter_type == 'Grayscale':
    output = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  elif filter_type == 'Cartoon':
    output = cartoonize(frame)

  display_image(output, is_grayscale=(filter_type == 'Grayscale'))


def cartoonize(frame):
  """Chuyển đổi ảnh thành phong cách hoạt hình"""
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.medianBlur(gray, 7)

  edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
  color = cv2.bilateralFilter(frame, 9, 300, 300)

  cartoon = cv2.bitwise_and(color, color, mask=edges)
  return cartoon


def display_image(cv_img, is_grayscale=False):
  """Hiển thị ảnh trong GUI"""
  if is_grayscale:
    img_pil = Image.fromarray(cv_img)
  else:
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

  img_tk = ImageTk.PhotoImage(image=img_pil)
  lbl_img.config(image=img_tk)
  lbl_img.image = img_tk  # Giữ tham chiếu để tránh bị xoá ảnh


def capture_image_from_stream():
  """Chụp ảnh từ camera động"""
  global captured_frame, original_frame
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
    messagebox.showerror("Error", "Cannot access the camera.")
    return

  while True:
    ret, frame = cap.read()
    if not ret:
      break

    cv2.imshow('Camera Stream', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
      captured_frame = frame
      original_frame = frame.copy()  # Lưu ảnh gốc
      display_image(captured_frame)
      break
    elif key == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()


def load_image_from_file():
  """Chọn ảnh từ máy tính"""
  global captured_frame, original_frame
  file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
  if file_path:
    captured_frame = cv2.imread(file_path)
    original_frame = captured_frame.copy()  # Lưu ảnh gốc
    display_image(captured_frame)


def apply_cartoon_effect():
  if captured_frame is None:
    messagebox.showerror("Error", "No image captured. Please capture an image first.")
  else:
    apply_filter('Cartoon', captured_frame)


def apply_sharpen_effect():
  if captured_frame is None:
    messagebox.showerror("Error", "No image captured. Please capture an image first.")
  else:
    apply_filter('Sharpen', captured_frame)


def apply_blur_effect():
  if captured_frame is None:
    messagebox.showerror("Error", "No image captured. Please capture an image first.")
  else:
    apply_filter('Blur', captured_frame)


def apply_grayscale_effect():
  if captured_frame is None:
    messagebox.showerror("Error", "No image captured. Please capture an image first.")
  else:
    apply_filter('Grayscale', captured_frame)


def start_rect_selection(event):
  """Xử lý khi nhấn chuột để bắt đầu chọn vùng"""
  global start_point, rect_drawing
  start_point = (event.x, event.y)
  rect_drawing = True


def update_rect_selection(event):
  """Cập nhật khi kéo chuột để vẽ vùng chọn"""
  global end_point
  end_point = (event.x, event.y)
  redraw_image_with_rectangle()


def end_rect_selection(event):
  """Kết thúc chọn vùng khi nhả chuột"""
  global rect_drawing
  rect_drawing = False
  if start_point and end_point:
    remove_selected_area()


def redraw_image_with_rectangle():
  """Vẽ lại ảnh và vùng chọn hình chữ nhật khi kéo chuột"""
  if captured_frame is not None and start_point and end_point:
    img_copy = captured_frame.copy()
    cv2.rectangle(img_copy, start_point, end_point, (0, 255, 0), 2)
    display_image(img_copy)


def remove_selected_area():
  """Xóa vùng đã được chọn bằng cách làm mờ hoặc tô màu"""
  global captured_frame, start_point, end_point
  if captured_frame is not None and start_point and end_point:
    x1, y1 = start_point
    x2, y2 = end_point
    # Làm mờ vùng đã chọn
    selected_area = captured_frame[y1:y2, x1:x2]
    blurred_area = cv2.GaussianBlur(selected_area, (15, 15), 0)
    captured_frame[y1:y2, x1:x2] = blurred_area
    display_image(captured_frame)


def remove_background():
  """Xóa phông nền của ảnh"""
  global captured_frame
  if captured_frame is None:
    messagebox.showerror("Error", "No image captured. Please capture an image first.")
    return

  # Chuyển đổi sang không gian màu HSV
  hsv = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2HSV)

  # Định nghĩa khoảng màu để xóa phông
  lower_bound = np.array([0, 0, 0])
  upper_bound = np.array([180, 255, 30])  # Giới hạn màu để xóa phông

  # Tạo mặt nạ
  mask = cv2.inRange(hsv, lower_bound, upper_bound)

  # Xóa phông
  result = cv2.bitwise_and(captured_frame, captured_frame, mask=~mask)

  display_image(result)


def reset_image():
  """Trở lại ảnh gốc đã chụp"""
  global captured_frame, original_frame
  if original_frame is None:
    messagebox.showerror("Error", "No original image to reset to.")
  else:
    captured_frame = original_frame.copy()
    display_image(captured_frame)


# Giao diện người dùng
root = tk.Tk()
root.title("Image Filtering and Background Removal")

# Khung hiển thị ảnh
lbl_img = tk.Label(root)
lbl_img.pack()

# Nút chọn ảnh từ máy tính
btn_load = tk.Button(root, text="Load Image from File", command=load_image_from_file)
btn_load.pack()

# Nút chụp ảnh từ camera động
btn_capture = tk.Button(root, text="Capture Image from Camera Stream", command=capture_image_from_stream)
btn_capture.pack()

# Nút áp dụng bộ lọc hoạt hình
btn_cartoon = tk.Button(root, text="Apply Cartoon Effect", command=apply_cartoon_effect)
btn_cartoon.pack()

# Nút áp dụng bộ lọc làm nét
btn_sharpen = tk.Button(root, text="Apply Sharpen Effect", command=apply_sharpen_effect)
btn_sharpen.pack()

# Nút áp dụng bộ lọc làm mờ
btn_blur = tk.Button(root, text="Apply Blur Effect", command=apply_blur_effect)
btn_blur.pack()

# Nút tạo ảnh đen trắng
btn_grayscale = tk.Button(root, text="Convert to Grayscale", command=apply_grayscale_effect)
btn_grayscale.pack()

# Nút xóa phông nền
btn_remove_bg = tk.Button(root, text="Remove Background", command=remove_background)
btn_remove_bg.pack()

# Nút trở lại ảnh gốc
btn_reset = tk.Button(root, text="Reset to Original", command=reset_image)
btn_reset.pack()

# Kết nối sự kiện chuột
lbl_img.bind("<ButtonPress-1>", start_rect_selection)
lbl_img.bind("<B1-Motion>", update_rect_selection)
lbl_img.bind("<ButtonRelease-1>", end_rect_selection)

root.mainloop()
