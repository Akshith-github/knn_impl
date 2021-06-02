#import
from flask import  jsonify
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pd,os,pickle
try:
    from sklearn.externals import joblib
except:
    try:
        import joblib
    except:
        print("action to import joblib failed ")
from random import randint
from knn_model_build import test_model_output 

# print(__file__)
#dataset 
base_loc = os.path.join(os.path.dirname(__file__), os.path.join('data'))
us_canada_user_rating_pivot = pd.read_csv(base_loc+"/us_canada_user_rating_pivot.csv")
us_canada_user_rating_pivot_idx = us_canada_user_rating_pivot.set_index("bookTitle")
return_data_csv=pd.read_csv(base_loc+"/Book_details_filtered_us_canada.csv")
# print(us_canada_user_rating_pivot.head())
model_loc = os.path.join(os.path.dirname(__file__), os.path.join('models')) 
# pd.DataFrame(us_canada_user_rating_pivot["bookTitle"]).to_csv(base_loc+"\\popular_usa_books.csv")
titles=us_canada_user_rating_pivot["bookTitle"].str.lower()
isbns=return_data_csv["ISBN"].apply(lambda x: str(x).lower())
print(us_canada_user_rating_pivot.columns)
#load model
def load_model():
    loaded_model = None
    try:
        with open(model_loc+'/knnpickle_file', 'rb') as knnPickle:
            loaded_model = pickle.load(knnPickle)
        print("loaded model (1)")
    except:
        try:
            loaded_model = joblib.load( model_loc+'/model_knn.pkl' , mmap_mode ='r')
            print("loaded model (2)")
        except:
            print("\nUnable to load model :(\n")
    finally:
        return loaded_model
def get_data(indices,distances):
    # a=[ (i,*[str(i) for i in return_data_csv.iloc[indices.flatten()[i],:].to_list()],
    #             distances.flatten()[i])
    #         for i in range(0, len(distances.flatten()))]
    b=dict()
    for j in range(0, len(distances.flatten())):
        a= {'distance':distances.flatten()[j] }
        for i in return_data_csv.iloc[indices.flatten()[j],:].to_dict().items():
            a[i[0]]= str(i[1]) 
        b[j]=a.copy()
    return b
# print(load_model())
def run_random_recommend(n_neighbors,query_index=-1):
    if query_index == -1 :
        query_index = randint(0,us_canada_user_rating_pivot.shape[0]-1)
    # print(query_index)
    model_knn=load_model()
    # print(us_canada_user_rating_pivot_idx.iloc[query_index,1:].values.reshape(1, -1))
    distances, indices = model_knn.kneighbors(us_canada_user_rating_pivot_idx.iloc[query_index,:].values.reshape(1, -1), n_neighbors = n_neighbors)
    # for i in range(0, len(distances.flatten())):
    #     if i == 0:
    #         print('Recommendations for {0}:\n'.format(us_canada_user_rating_pivot_idx.index[query_index]))
    #     else:
    #         print('{0}: {1}, with distance of {2}:'.format(i, us_canada_user_rating_pivot_idx.index[indices.flatten()[i]], distances.flatten()[i]))
    
    a=get_data(indices,distances)
    # print(a)
    return a

def recommend_for_book_isbn(isbn:str,n_neighbors=6):
    isbn_idx = isbns[isbns==isbn.lower()]
    print(isbn_idx.shape[0])
    query_index = -1  if(not isbn_idx.shape[0]) else int(isbn_idx.index.values[0])
    print(isbn_idx.shape)
    return run_random_recommend(n_neighbors,query_index)


def recommend_for_book(book_name:str,n_neighbors=6):
    title_idx = titles[titles==book_name.lower()]
    print(title_idx.shape[0])
    # if(title_idx.shape[0]>1):
    #     title_idx = title_idx.iloc[0]
    query_index = -1  if(not title_idx.shape[0]) else int(title_idx.index.values[0])
    # print(title_idx.shape)
    return run_random_recommend(n_neighbors,query_index)
    
if __name__ == "__main__":
    run_random_recommend()
    recommend_for_book(input("Enter book name :"))