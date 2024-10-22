import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests

# Khởi tạo biến toàn cục
captured_frame = None
original_frame = None  # Khung hình gốc
start_point = None  # Điểm bắt đầu cho vùng chọn
end_point = None  # Điểm kết thúc cho vùng chọn
rect_drawing = False  # Cờ cho việc kéo thả chuột để chọn vùng

# Các kernel để áp dụng
kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
kernel_3x3 = np.ones((3, 3), np.float32) / 9
kernel_5x5 = np.ones((5, 5), np.float32) / 25

# Biến để lưu kernel đã chọn
selected_kernel = kernel_identity

def display_image(cv_img, label):
    """Hiển thị ảnh trong GUI"""
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    img_tk = ImageTk.PhotoImage(image=img_pil)
    label.config(image=img_tk)
    label.image = img_tk  # Giữ tham chiếu để tránh bị xoá ảnh

def load_image_from_file():
    """Chọn ảnh từ máy tính"""
    global captured_frame, original_frame
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        captured_frame = cv2.imread(file_path)
        original_frame = captured_frame.copy()  # Lưu ảnh gốc
        display_image(captured_frame, lbl_original)

def load_image_from_url():
    """Tải ảnh từ URL"""
    global captured_frame, original_frame
    url = filedialog.askstring("Input URL", "Enter the image URL:")
    if url:
        try:
            response = requests.get(url)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            captured_frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            original_frame = captured_frame.copy()  # Lưu ảnh gốc
            display_image(captured_frame, lbl_original)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image from URL: {e}")

def apply_kernel(frame, kernel):
    """Áp dụng kernel lên ảnh"""
    return cv2.filter2D(frame, -1, kernel)

def update_result():
    """Cập nhật kết quả khi thay đổi kernel hoặc thanh trượt"""
    global captured_frame, selected_kernel
    if captured_frame is not None:
        processed_frame = apply_kernel(captured_frame, selected_kernel)
        display_image(processed_frame, lbl_result)

def select_kernel(kernel_type):
    """Chọn kernel để áp dụng"""
    global selected_kernel
    if kernel_type == 'identity':
        selected_kernel = kernel_identity
    elif kernel_type == '3x3':
        selected_kernel = kernel_3x3
    elif kernel_type == '5x5':
        selected_kernel = kernel_5x5
    update_result()

def process_selection():
    """Xử lý vùng chọn để làm nét và hiển thị kết quả"""
    global captured_frame, start_point, end_point
    if captured_frame is not None and start_point and end_point:
        x1, y1 = start_point
        x2, y2 = end_point

        # Lấy vùng quét từ ảnh gốc
        selected_region = captured_frame[y1:y2, x1:x2]

        # Làm nét phần được quét
        sharpened_region = apply_kernel(selected_region, selected_kernel)

        # Tạo bản sao của ảnh gốc và thay thế vùng đã quét bằng vùng đã làm nét
        sharpened_frame = captured_frame.copy()
        sharpened_frame[y1:y2, x1:x2] = sharpened_region

        # Hiển thị cả hai bản: một bản quét nguyên bản và một bản đã làm nét
        combined = np.hstack((captured_frame, sharpened_frame))
        display_image(combined, lbl_result)

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
        process_selection()

def redraw_image_with_rectangle():
    """Vẽ lại ảnh và vùng chọn hình chữ nhật khi kéo chuột"""
    if captured_frame is not None and start_point and end_point:
        img_copy = captured_frame.copy()
        cv2.rectangle(img_copy, start_point, end_point, (0, 255, 0), 2)
        display_image(img_copy, lbl_original)

# Giao diện người dùng
root = tk.Tk()
root.title("Image Filtering and Background Removal")

# Khung hiển thị ảnh
lbl_original = tk.Label(root)
lbl_original.pack(side=tk.LEFT)

lbl_result = tk.Label(root)
lbl_result.pack(side=tk.LEFT)

# Nút chọn ảnh từ máy tính
btn_load_file = tk.Button(root, text="Load Image from File", command=load_image_from_file)
btn_load_file.pack()

# Nút tải ảnh từ URL
btn_load_url = tk.Button(root, text="Load Image from URL", command=load_image_from_url)
btn_load_url.pack()

# Nút chọn kernel
btn_identity = tk.Button(root, text="Apply Identity Kernel", command=lambda: select_kernel('identity'))
btn_identity.pack()

btn_3x3 = tk.Button(root, text="Apply 3x3 Kernel", command=lambda: select_kernel('3x3'))
btn_3x3.pack()

btn_5x5 = tk.Button(root, text="Apply 5x5 Kernel", command=lambda: select_kernel('5x5'))
btn_5x5.pack()

# Thanh trượt để thay đổi độ mạnh của bộ lọc
scale_strength = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, label="Kernel Strength")
scale_strength.pack()

# Kết nối sự kiện cho việc chọn vùng bằng chuột
lbl_original.bind("<ButtonPress-1>", start_rect_selection)
lbl_original.bind("<B1-Motion>", update_rect_selection)
lbl_original.bind("<ButtonRelease-1>", end_rect_selection)

root.mainloop()
