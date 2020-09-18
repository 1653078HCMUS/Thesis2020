import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

csv_file = r'j_data.csv'

features = ['local', 'absolute', 'rap', 'ppq5', 'ddp']
column_name = ['local', 'absolute', 'rap', 'ppq5', 'ddp', 'target']

# Load dataset into Pandas DataFrame
data = pd.read_csv(csv_file, names=column_name)

print('\n')
print('Data: ')
print(data)

# Separating out the features
x = data.loc[:, features].values
# Separating out the target
y = data.loc[:, ['target']].values
# Standardizing the features
x = StandardScaler().fit_transform(x)

print('\n')
print('Standardizing: ')
print(x)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data=principalComponents,
                           columns=['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, data[['target']]], axis=1)

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
targets = ['normal', 'patient']
colors = ['g', 'r']
for target, color in zip(targets, colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
               finalDf.loc[indicesToKeep, 'principal component 2'],
               c=color, s=50)
ax.legend(targets)
ax.grid()
plt.show()
