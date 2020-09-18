# Thesis2020
Code for thesis 2020
Thế chia github thành 3 folder, gồm:
- folder Histogram_Calculate list of Jitter chứa code tìm danh sách các jitter trên 1 đoạn âm thanh (dùng lúc vẽ histogram)
- folder Principal Component Analysis chứa code vẽ PCA, trong folder này tách ra 2 folder nhỏ là PCA Jitter và PCA Shimmer nhé
- folder Library for Jitter and Shimmer Calculation chứa code của thư viện tính toán Jitter Shimmer mà Thế code bữa giờ
Trong từng source code, Thế note lại tại những hàm quan trọng (hàm đó dùng làm gì), hoặc những hàm nào cần truyền vào tham số thì phải giải thích tham số đó là gì
Ví dụ:
- Với source code jitter, Thế note lại ở chỗ các hàm lấy được list pulses và hàm tính ra được jitter giữa 2 chu kỳ liên tiếp
- Với source code PCA, Thế note lại ở chỗ hàm Standardlize, hàm chuyển 4 cột về 2 cột, hàm vẽ ra PCA chart
- Với source code thư viện demo, Thế note lại ở chỗ nào dùng để gọi hàm tính toán và cần truyền những tham số gì vào đó (ở main.py), chỗ hàm nào dùng để tính toán các loại jitter
và các loại shimmer
Khi nào xong hết, Thế nói Việt vào viết readme cho từng folder nhé
