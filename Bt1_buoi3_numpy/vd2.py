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

# Create bar plot for grade distribution
plt.figure(figsize=(12, 10))

# Plot 1: Number of students achieving each grade
plt.subplot(2, 1, 1)
labels = list(loai_diem.keys())
values = [np.sum(diem) for diem in loai_diem.values()]
plt.bar(labels, values, color='skyblue')
plt.xlabel('Phân loại điểm')
plt.ylabel('Số sinh viên')
plt.title('Số sinh viên đạt từng loại điểm')
plt.grid(axis='y')
plt.xticks(rotation=45)

# Plot 2: Average scores for assessments
plt.subplot(2, 1, 2)
avg_labels = ['L1', 'L2', 'TX1', 'TX2', 'Cuối kỳ']
avg_values = [l1_avg, l2_avg, tx1_avg, tx2_avg, cuoi_ky_avg]
plt.bar(avg_labels, avg_values, color='lightgreen')
plt.xlabel('Bài kiểm tra')
plt.ylabel('Số sinh viên')
plt.title('Điểm trung bình các bài kiểm tra')
plt.grid(axis='y')

plt.tight_layout()
plt.show()
