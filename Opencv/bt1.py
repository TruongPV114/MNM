import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Biến lưu trữ ảnh đã xử lý
processed_image = None

# Hàm chọn ảnh
def select_image():
    global img, original_image
    file_path = filedialog.askopenfilename()
    if len(file_path) > 0:
        img = cv2.imread(file_path)
        original_image = img.copy()
        display_image_in_new_window(img, "Original Image")

# Hàm hiển thị ảnh trong cửa sổ mới
def display_image_in_new_window(img, title):
    global processed_image
    processed_image = img  # Cập nhật ảnh đã xử lý
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB

    # Thay đổi kích thước hình ảnh
    height, width = img_rgb.shape[:2]
    max_height = 400  # Chiều cao tối đa cho cửa sổ
    scale = max_height / height
    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_img = cv2.resize(img_rgb, (new_width, new_height))  # Thay đổi kích thước ảnh

    img_pil = Image.fromarray(resized_img)  # Chuyển sang định dạng PIL
    img_tk = ImageTk.PhotoImage(img_pil)

    new_window = Toplevel()  # Tạo cửa sổ mới
    new_window.title(title)
    panel = Label(new_window, image=img_tk)
    panel.image = img_tk  # Giữ tham chiếu ảnh
    panel.pack()



# Các bộ lọc
def apply_blur():
    if img is not None:
        blurred = cv2.GaussianBlur(img, (9, 9), 0)
        display_image_in_new_window(blurred, "Blurred Image")

def apply_sharpen():
    if img is not None:
        kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(img, -1, kernel_sharpen)
        display_image_in_new_window(sharpened, "Sharpened Image")

def apply_grayscale():
    if img is not None:
        grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        display_image_in_new_window(cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR), "Grayscale Image")

def apply_negative():
    if img is not None:
        negative = cv2.bitwise_not(img)
        display_image_in_new_window(negative, "Negative Image")

def flip_image():
    if img is not None:
        flipped = cv2.flip(img, 1)  # Lật ngang ảnh
        display_image_in_new_window(flipped, "Flipped Image")

# Hàm lưu ảnh
def save_image():
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, processed_image)
            print(f"Image saved at {file_path}")


def remove_background():
    global processed_image
    if processed_image is not None:
        # Chuyển ảnh sang chế độ RGB
        img_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

        # Tạo một vùng chữ nhật bao quanh đối tượng chính
        mask = np.zeros(img_rgb.shape[:2], np.uint8)

        # Hiển thị ảnh và chọn ROI
        cv2.imshow("Select ROI", img_rgb)
        cv2.resizeWindow("Select ROI", 400, 400)  # Điều chỉnh kích thước cửa sổ

        rect = cv2.selectROI("Select ROI", img_rgb, fromCenter=False, showCrosshair=True)

        # Tạo ma trận để GrabCut hoạt động
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # Áp dụng thuật toán GrabCut
        cv2.grabCut(img_rgb, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        # Đặt pixel nền về 0 và đối tượng chính về 1
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img_rgb_nobg = img_rgb * mask2[:, :, np.newaxis]

        # Hiển thị ảnh đã xóa nền
        display_image_in_new_window(cv2.cvtColor(img_rgb_nobg, cv2.COLOR_RGB2BGR), "Image without Background")


def smooth_skin():
    global processed_image
    if processed_image is not None:
        # Chuyển ảnh sang chế độ RGB
        img_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

        # Áp dụng bộ lọc Gaussian
        smoothed = cv2.GaussianBlur(img_rgb, (7, 7), 1.5)

        # Hiển thị ảnh đã làm mịn
        display_image_in_new_window(cv2.cvtColor(smoothed, cv2.COLOR_RGB2BGR), "Smoothing Skin")


def blur_background():
    global processed_image
    if processed_image is not None:
        # Chuyển ảnh sang chế độ RGB
        img_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

        # Tạo một vùng chữ nhật bao quanh đối tượng chính
        mask = np.zeros(img_rgb.shape[:2], np.uint8)

        # Hiển thị ảnh và chọn ROI để xác định đối tượng chính
        cv2.imshow("Select ROI", img_rgb)
        cv2.resizeWindow("Select ROI", 400, 400)  # Điều chỉnh kích thước cửa sổ
        rect = cv2.selectROI("Select ROI", img_rgb, fromCenter=False, showCrosshair=True)

        # Tạo ma trận để GrabCut hoạt động
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # Áp dụng thuật toán GrabCut
        cv2.grabCut(img_rgb, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        # Đặt pixel nền về 0 và đối tượng chính về 1
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Tạo ảnh nền đã làm mờ bằng Gaussian Blur
        blurred_background = cv2.GaussianBlur(img_rgb, (21, 21), 10)

        # Giữ nguyên đối tượng chính và áp dụng nền mờ
        img_combined = img_rgb * mask2[:, :, np.newaxis] + blurred_background * (1 - mask2[:, :, np.newaxis])

        # Hiển thị ảnh có phông nền đã làm mờ
        display_image_in_new_window(cv2.cvtColor(img_combined, cv2.COLOR_RGB2BGR), "Image with Blurred Background")


# Tạo cửa sổ chính
root = Tk()
root.title("Image Processing App")

# Các nút chọn ảnh và các bộ lọc
btn_select_image = Button(root, text="Select Image", command=select_image)
btn_select_image.pack(side="top", padx=10, pady=10)

btn_blur = Button(root, text="Blur", command=apply_blur)
btn_blur.pack(side="left", padx=5, pady=5)

btn_sharpen = Button(root, text="Sharpen", command=apply_sharpen)
btn_sharpen.pack(side="left", padx=5, pady=5)

btn_grayscale = Button(root, text="Grayscale", command=apply_grayscale)
btn_grayscale.pack(side="left", padx=5, pady=5)

btn_negative = Button(root, text="Negative", command=apply_negative)
btn_negative.pack(side="left", padx=5, pady=5)

btn_flip = Button(root, text="Flip", command=flip_image)
btn_flip.pack(side="left", padx=5, pady=5)

btn_remove_bg = Button(root, text="Remove Background", command=remove_background)
btn_remove_bg.pack(side="left", padx=5, pady=5)

btn_smooth_skin = Button(root, text="Smooth Skin", command=smooth_skin)
btn_smooth_skin.pack(side="left", padx=5, pady=5)

btn_smooth_skin = Button(root, text="Blur Backgound", command=blur_background)
btn_smooth_skin.pack(side="left", padx=5, pady=5)

# Nút lưu ảnh
btn_save_image = Button(root, text="Save Image", command=save_image)
btn_save_image.pack(side="bottom", padx=10, pady=10)

# Chạy ứng dụng
root.mainloop()
