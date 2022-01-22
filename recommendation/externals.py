from recommender.settings import BASE_DIR
import numpy as np
import joblib

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
    dataset = dataset.loc[dataset['Rank']<=rank[0]]
    recs = dataset.loc[dataset['city']==city_name]
    if recs['Rank'].count() < size:
        recs = recs.append(dataset.loc[dataset['city']!=city_name])
    return recs.iloc[:size,:]