import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

csv_file = r'j_data.csv'

features = ['local', 'absolute', 'rap', 'ppq5', 'ddp']
column_name = ['local', 'absolute', 'rap', 'ppq5', 'ddp', 'target']

# Load dataset into Pandas DataFrame
data = pd.read_csv(csv_file, names=column_name)
data.plot(kind='bar')

print('\n')
print('Data: ')
print(data)
x = data.loc[:, features].values
# Separating out the target
y = data.loc[:, ['target']].values

plt.title('Histogram')

plt.show()
