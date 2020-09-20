# Code for thesis 2020

## **1.Bao gồm:**
Source code bao gồm 3 folder:
- Folder Histogram_Calculate list of Jitter chứa code tìm danh sách các jitter trên 1 đoạn âm thanh và vẽ Histogram của đoạn âm thanh đó.
- Folder Principal Component Analysis chứa code vẽ PCA, trong folder này tách ra 2 folder nhỏ là PCA Jitter và PCA Shimmer.
- folder Library for Jitter and Shimmer Calculation chứa code của thư viện tính toán Jitter Shimmer và file script dùng để gọi các hàm tính toán từ thư viện.

## **2.Giải thích:**
##### **a.Vẽ Histogram:**
- j_Histogram là script vẽ ra histogram từ danh sách các Jitter trên 1 đoạn âm thanh được chứa trong 1 file csv.
Code phân loại các khung dữ liệu:
```
features = ['local', 'absolute', 'rap', 'ppq5', 'ddp']
column_name = ['local', 'absolute', 'rap', 'ppq5', 'ddp', 'target']
```
Code đọc từ file csv:
```
data = pd.read_csv(csv_file, names=column_name)
data.plot(kind='bar')
```

##### **b.PCA:**
Hàm Standardlize:
```
x = StandardScaler().fit_transform(x)
```
Hàm chuyển 4 cột thành 2 cột:
```
pca = PCA(n_components=2)
#Set number of components for PCA
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data=principalComponents,
                           columns=['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, data[['target']]], axis=1)
```
Hàm vẽ Chart
```
fig = plt.figure(figsize=(12, 7))
#Size of figure
ax = fig.add_subplot(1, 1, 1)
#Add number of rows, columns and indexs to figure
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
#Set labels and title for the figure
targets = ['normal', 'patient']
colors = ['g', 'r']
for target, color in zip(targets, colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
               finalDf.loc[indicesToKeep, 'principal component 2'],
               c=color, s=50)
ax.legend(targets)
#Put target into figure
```
##### **c.Thư viện tính toán:**
Các hàm thường dùng

