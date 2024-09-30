import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV data into a DataFrame
file_path = 'diemPython.csv'  # Đảm bảo file CSV này có trong cùng thư mục với script
df = pd.read_csv(file_path, index_col=0, header=0)

# Convert DataFrame to NumPy array
in_data = df.to_numpy()

# Total number of students
tongsv = in_data[:, 1]

# Grade statistics
loai_diem = {
    "A+": in_data[:, 2],
    "A": in_data[:, 3],
    "B+": in_data[:, 4],
    "B": in_data[:, 5],
    "C+": in_data[:, 6],
    "C": in_data[:, 7],
    "D+": in_data[:, 8],
    "D": in_data[:, 9],
    "F": in_data[:, 10],
}

# Average scores for L1, L2, TX1, TX2, and final score
l1_avg = np.mean(in_data[:, 11])
l2_avg = np.mean(in_data[:, 12])
tx1_avg = np.mean(in_data[:, 13])
tx2_avg = np.mean(in_data[:, 14])
cuoi_ky_avg = np.mean(in_data[:, 15])

# Create a figure for 3 subplots
plt.figure(figsize=(18, 12))

# Plot 1: Number of students achieving each grade (A+, A, B+, B, C+, C, D+, D, F)
plt.subplot(3, 1, 1)
labels = list(loai_diem.keys())
values = [np.sum(diem) for diem in loai_diem.values()]
plt.bar(labels, values, color='lightblue')
plt.xlabel('Phân loại điểm')
plt.ylabel('Số sinh viên')
plt.title('Số sinh viên đạt từng loại điểm')
plt.grid(axis='y')
plt.xticks(rotation=45)

# Plot 2: Average scores for L1 and L2
plt.subplot(3, 1, 2)
avg_labels_L1_L2 = ['L1', 'L2']
avg_values_L1_L2 = [l1_avg, l2_avg]
plt.bar(avg_labels_L1_L2, avg_values_L1_L2, color='orange')
plt.xlabel('Bài kiểm tra L1, L2')
plt.ylabel('Điểm trung bình')
plt.title('Điểm trung bình của các bài kiểm tra L1 và L2')
plt.grid(axis='y')

# Plot 3: Average scores for TX1, TX2, and final exam
plt.subplot(3, 1, 3)
avg_labels_TX1_TX2_CuoiKy = ['TX1', 'TX2', 'Cuối kỳ']
avg_values_TX1_TX2_CuoiKy = [tx1_avg, tx2_avg, cuoi_ky_avg]
plt.bar(avg_labels_TX1_TX2_CuoiKy, avg_values_TX1_TX2_CuoiKy, color='green')
plt.xlabel('Bài kiểm tra TX1, TX2 và Cuối kỳ')
plt.ylabel('Điểm trung bình')
plt.title('Điểm trung bình của các bài kiểm tra TX1, TX2 và Cuối kỳ')
plt.grid(axis='y')

# Adjust layout to avoid overlap
plt.tight_layout(pad=3.0, w_pad=0.5, h_pad=3.0)

# Show the plots
plt.show()
