import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import joblib
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("/home/canberk/Desktop/lEncodeddata.csv")

'''
# Dataframedeki virgulleri silme kodu
for i in df.columns:
	for j in range(0,len(df.index)):
		if(isinstance(df[i][j],str) == 1):
			df[i][j] = df[i][j].replace(',', '')
df.to_csv("data.csv")
'''

<<<<<<< HEAD
# print(df.Genres)

=======
>>>>>>> a5140502f5a27cfff177a4700946bd458e484eb8
'''
labelenc = LabelEncoder()
df.genres = labelenc.fit_transform(df.genres)
df.to_csv("lEncodeddata.csv")
'''

<<<<<<< HEAD
df_pivot = df.pivot(index="index", columns="Genres", values="rating").fillna(0)
=======

df_pivot = df.pivot(index = "book_id", columns = "genres", values = "rating").fillna(0)
>>>>>>> a5140502f5a27cfff177a4700946bd458e484eb8

# print(df.head())
matrix = csr_matrix(df_pivot.values)

knn = joblib.load('knn.h5')

<<<<<<< HEAD
# knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
=======
>>>>>>> a5140502f5a27cfff177a4700946bd458e484eb8
knn.fit(matrix)

<<<<<<< HEAD
query_index = np.random.choice(df_pivot.shape[0])
distances, indices = knn.kneighbors(df_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors=6)

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {}:\n'.format(df.title[df.title.index[query_index]]))
    else:
        print('{}: {}'.format(i, df.title[df.title.index[indices.flatten()[i]]]))
=======

genre = a  # BURAYA KULLANICININ GIRDIGI KITAP TURU (GENRE) GELECEK (INTEGER OLARAK)
query_index = 0
filter1 = df.genres == genre
ids = df.book_id.where(filter1)
for i in ids:
	if type(i) == float and pd.isna(i):
		pass
	else:
		query_index = int(i)

distances, indices = knn.kneighbors(df_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 6)

for i in range(0, len(distances.flatten())):
	if i == 0:
		print('Recommendations for {}:\n'.format(df.genres[df.title.index[query_index]]))
	else:
			print('{}: {}'.format(i, df.genres[df.title.index[indices.flatten()[i]]]))
>>>>>>> a5140502f5a27cfff177a4700946bd458e484eb8
