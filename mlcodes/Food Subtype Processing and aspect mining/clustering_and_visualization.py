# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import normalize
import seaborn as sns
import matplotlib.patches as mpatches
import os
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn import metrics
import re
import string
import time
import seaborn as sns
import matplotlib.patches as mpatches


##Constants
mystopwords=stopwords.words("english")+['singapore', 
'holiday', 'sister', 'brother', 'kid', 'generally', 'european', 
'typically', 'recommend', 'recommended', 'reasonable', 'like', 'liked',
'french', 'quite', 'back', 'definitely', 'place', 'food', 'sand', 'bay', 
'afternoon', 'home', 'lunch', 'dinner', 'roof', 'layout', 'restaurant',
'situation', 'set', 'email', 'rooftop', 'bar', 'really', 'good',
'work', 'music', 'marriot', 'skyline', 'hotel', 'impeccable', 'fullerton',
'classy', 'feel', 'presented', 'present', 'well', 'explaining', 'decoration',
'wife', 'husband', 'friend', 'perfectly', 'limited', 'called', 'call',
'delight', 'arrive', 'otherwise', 'unfortunately', 'enjoyable',
'seemed', 'managed', 'read', 'indeed', 'stay', 'great', 'plus',
'better', 'front', 'recently', 'floor', 'friday', 'monday', 'tuesday',
'wednesday', 'thursday', 'saturday', 'sunday', 'weekend', 'weekends',
'weekdays', 'weekday', 'often', 'wait', 'waited','seat', 'seated',
'week', 'ordering', 'something', 'next', 'know', 'known',
'helped', 'entrance', 'also', 'enough', 'reservation', 'going',
'go', 'need', 'coming', 'etc', 'sit', 'disappointing', 'certainly',
'able', 'gave', 'give', 'including', 'seems', 'table', 'must',
'try', 'time', 'would', 'will', 'even', 'many', 'especially', 'though',
'although', 'must try', 'year', 'outside', 'however', 'around', 'group',
'want', 'take', 'overall', 'took', 'surprised', 'recommendation',
'okay', 'let', 'either', 'bring', 'helpful', 'crowd', 'yes', 'no',
'except', 'soon', 'remember', 'business', 'queue', 'everyone',
'chose', 'station', 'fact', 'keep', 'anything', 'within','sgd',
'saw', 'expectation', 'due', 'stop', 'counter', 'corner', 'mine',
'check', 'hit', 'similar', 'despite', 'note', 'reasonably', 'impressed',
'impress', 'particularly', 'highlight', 'later', 'late', 'based',
'totally', 'heard', 'city', 'colleague', 'across', 'space', 'leave',
'world', 'avoid','various','tell', 'told', 'ended', 'town', 'change',
'personally', 'making', 'make', 'typical', 'help', 'outstanding',
'surprisingly', 'surprised', 'upon', 'into','nearby', 'please',
'pleased', 'pleasing', 'disappoint','followed','sharing', 'taken',
'took', 'take', 'among', 'amongst', 'sitting', 'sell', 'deal', 'party',
'one', 'two', 'menu','visit','get','view', 'marina', 'amazing',
'amaze', 'amazed', 'child', 'class', 'boy', 'complain', 'could',
'busy', 'choose', 'came', 'arrival', 'departure', 'could get',
'court', 'complimentary', 'boyfriend', 'girlfriend', 'charged',
'booking', 'book', 'brought', 'actually', 'absolutely', 'accompanied',
'addition', 'across', 'long', 'always', 'absolute', 'advance',
'acceptable', 'bright', 'ask', 'asking', 'base', 'almost', 'anyone',
'compare', 'compared', 'behind', 'case', 'country', 'away', 'arrangement',
'concept', 'apparently', 'anywhere', 'compliment', 'certain', 'available',
'charming', 'catch', 'attended', 'comfortable', 'ceiling', 'basically',
'booked', 'charge', 'card', 'combination', 'common', 'celebration', 
'closed', 'clarke', 'quay', 'chain', 'arrived', 'cheerful', 'clarke quay',
'average', 'carte', 'craving', 'branch', 'credit card', 'bought', 'bad',
'constantly', 'considering', 'believe', 'best', 'celebrate',
'chope', 'beautiful', 'buy', 'asked', 'anyway', 'ambiance', 'anniversary'
'ahead', 'additional', 'advice', 'abit',
'adult', 'alright', 'another', 'checking', 'birthday', 'bother',
'credit', 'compare', 'centre', '']

WNlemma = nltk.WordNetLemmatizer()
num_clusters = 5
vectorizer = TfidfVectorizer(max_df=0.3, max_features=6000,
                             min_df=5, stop_words=mystopwords,
                             use_idf=True, ngram_range=(1,3))
clusterHolder1 = []
clusterHolder2 = []

##Functions
def pre_process(text):
    tokens = nltk.word_tokenize(text)
    tokens=[ WNlemma.lemmatize(t.lower()) for t in tokens]
    tokens=[ t for t in tokens if t not in mystopwords]
    tokens=[ t for t in tokens if False == t.isdigit()]
    tokens=[ t for t in tokens if False == containsNumeric(t)]
    tokens=[ t for t in tokens if True == t.isalpha()]
    tokens=[ t for t in tokens if t not in string.punctuation]
    tokens = [ t for t in tokens if len(t) >= 3 ]
    text_after_process=" ".join(tokens)
    return(text_after_process)

def print_terms(cm, num):
    original_space_centroids = cm.cluster_centers_
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(num):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()

def containsNumeric(text):
    if text is not None:
        return any(str.isdigit(c) for c in text)
    else:
        return True

def saveClusterValues(model, clusterNum, array):
    original_space_centroids = model.cluster_centers_
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for ind in order_centroids[clusterNum, :]:
        array.append(terms[ind])
        
data = pd.read_csv('..\\..\\data\\data.csv', encoding='latin1')
data.groupby('restaurant')
text = data['Review']
tokens = text.apply(pre_process)
print(data.head())

X = vectorizer.fit_transform(tokens)
km1 = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=1000)

print("Fitting to k-means model...")
time_start = time.time()

km1.fit(X)
print('Fitting done! Time elapsed: {} seconds'.format(time.time()-time_start))

print("Coefficient for "+str(num_clusters)+" clusters: %0.3f"
     % metrics.silhouette_score(X, km1.labels_))

labels, counts = np.unique(km1.labels_[km1.labels_>=0], return_counts=True)
print (labels)
print (counts)
print_terms(km1, num_clusters)

df2 = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
labels = km1.labels_
X2 = X.todense()
colormap = { 0: 'red', 1: 'green', 2: 'blue', 3: 'cyan', 4: 'magenta' }

reduced_data = PCA(n_components=2).fit_transform(X2)
fig, ax = plt.subplots()
for index, instance in enumerate(reduced_data):
    pca_comp_1, pca_comp_2 = reduced_data[index]
    color = colormap[labels[index]]
    ax.scatter(pca_comp_1, pca_comp_2, c=color)
plt.show()
