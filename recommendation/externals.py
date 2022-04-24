from recommender.settings import BASE_DIR
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from web3 import Web3

url = 'https://rpc-mumbai.maticvigil.com'
web3 = Web3(Web3.HTTPProvider(url))
abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"dislikeDoctor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAllDetails","outputs":[{"internalType":"uint256[]","name":"details","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"likeDoctor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"numOfLikes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
address = '0x14A2C0C3245F9D86f69f7942AC3f1d3e646F2653'
contract = web3.eth.contract(address=address, abi=abi)

dataset = joblib.load(BASE_DIR / 'dataset.data')

def getAllHospitals():
    return dataset["Hospital"].unique()

combined_features = dataset["Experience"].astype('str') + " " + dataset["Fee"].astype('str') + " " + dataset["city"].astype('str')
def recommend(experience, fee, city, size):
    query = str(experience) + " " + str(fee) + " " + str(city)
    datasetVectorizer = TfidfVectorizer().fit_transform(np.append(combined_features, [query]))
    sim_matrix = cosine_similarity(datasetVectorizer)
    similars = np.delete(sim_matrix[-1], -1)
    similars_enumerated = np.array(list(enumerate(similars)))
    similars_enumerated_sort = np.array(sorted(similars_enumerated, key = lambda x:x[1], reverse = True))
    tempDS = dataset.iloc[similars_enumerated_sort[:,0].astype('int'), :]
    tempDS1 = tempDS.loc[tempDS["city"]==city]
    if len(tempDS1) > size:
        tempDS1.append(tempDS.loc[tempDS["city"]!=city])
    ids = tempDS1.iloc[:size,:]["id"]
    likesList_enumerated = []
    for i in ids:
        likes = contract.functions.numOfLikes(i).call()
        likesList_enumerated.append([i, likes])
    likesList_enumerated_sorted = np.array(sorted(likesList_enumerated, key = lambda x:x[1], reverse = True))
    tempDS2 = dataset.iloc[likesList_enumerated_sorted[:,0].astype('int'), :]
    return tempDS2.iloc[:size,:]

def getDocsByIds(array):
    return dataset.iloc[array, :]

def getTopDocs(size):
    likesList = np.array([], dtype='int')
    for i in range(0, 10):#len(dataset)
        likes = contract.functions.numOfLikes(i).call()
        likesList = np.append(likesList, likes)
    likesList_enumerated = np.array(list(enumerate(likesList)))
    likesList_enumerated_sorted = np.array(sorted(likesList_enumerated, key = lambda x:x[1], reverse = True))
    tempDS = getDocsByIds(likesList_enumerated_sorted[:,0].astype('int'))
    return tempDS.iloc[:size,:]