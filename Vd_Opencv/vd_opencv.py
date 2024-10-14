import cv2

# Đọc ảnh từ file
image = cv2.imread('image.jpg')

# Kiểm tra xem ảnh có đọc thành công không
if image is None:
    print("Không thể mở hoặc tìm thấy ảnh")
else:
    # Hiển thị ảnh
    cv2.imshow('Hình ảnh', image)

    # Đợi cho đến khi nhấn phím bất kỳ để đóng cửa sổ hiển thị
    cv2.waitKey(0)

    # Đóng tất cả cửa sổ hiển thị
    cv2.destroyAllWindows()
