from recommender.settings import BASE_DIR
import numpy as np
import joblib
""" import json
from web3 import Web3

url = 'https://rpc-mumbai.maticvigil.com'
web3 = Web3(Web3.HTTPProvider(url))
abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_rank","type":"uint256"}],"name":"addRank","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_ids","type":"uint256[]"},{"internalType":"uint256[]","name":"_ranks","type":"uint256[]"}],"name":"addRanks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_rank","type":"uint256"}],"name":"dislikeDoctor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ids","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_rank","type":"uint256"}],"name":"likeDoctor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ranks","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
address = '0x2604441A291eF0EEba319a4Fd959Fa8e96899e8E'
contract = web3.eth.contract(address=address, abi=abi) """

dataset = joblib.load(BASE_DIR / 'dataset.data')

model = joblib.load(BASE_DIR / 'lr.model')

def rankFilter(dataset, model, experience, fee, city_name, size):
    l=[]
    l.append(experience)
    l.append(fee)
    cities = [c for c in dataset['city'].value_counts().sort_values(ascending=False).index]
    for city in cities:
        if city == city_name:
            l.append(1.0)
        else:
            l.append(0.0)
    pred = np.array(l)
    rank = model.predict(pred.reshape(1,-1))

    """ for i in imrange(1,rank[0]+1):
        id = contract.functions.ids(i).call()
        entry = dataset.iloc[id,:]
        #entry = dataset.loc[dataset['Sr No.']==id] """

    dataset = dataset.loc[dataset['Rank']<=rank[0]]
    recs = dataset.loc[dataset['city']==city_name]
    if recs['Rank'].count() < size:
        recs = recs.append(dataset.loc[dataset['city']!=city_name])
    return recs.iloc[:size,:]