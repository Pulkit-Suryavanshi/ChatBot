import json
from nltk_down import tokenize, stem, bagOfWords
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# to load the json file
with open('intents.json', 'r') as f:
    intents = json.load(f)

# print(intents)

allWords = []  # empty list
tags = []  # for tags
xy = []  # later holds all words and tags

for intent in intents['intents']:
    tag = intent['tag']  # key tag as in the json file
    tags.append(tag)  # then we will be appending it in out tag array and
    for pattern in intent['patterns']:  # loop through every pattern with this tag in the json file
        tknize = tokenize(pattern)
        allWords.extend(tknize)  # append it into the all word array
        xy.append((tknize, tag))  # so it will know the pattern and the corresponding tag

# Now excluding the punctuation characters, Later Implication: Removing all the stopwords later down the road if
# needed, but for now this works

ignoreWords = ['?', '!', '.', ',']  # Array of punctuation characters. We Will not be needing them for our BOW model
allWords = [stem(w) for w in allWords if w not in ignoreWords]  # do Stemming
print(allWords)  # This will give a tokenized and stemmed word and removed the special characters
allWords = sorted((set(allWords)))  # sort and remove all the duplicate words
tags = sorted((set(tags)))  # removing and sort all the tag duplicates
print(tags)

aTrain = []  # bag of words
bTrain = []  # associated number for each tags

# loop over our xy array
for (tknize, tag) in xy:
    # calling from the nltk_down so here tknize is already tokenized
    bag = bagOfWords(tknize, allWords)
    # then append it into train array
    aTrain.append(bag)
    # numbers for our labels as in 0,1,2,....n
    lable = tag.index(tag)
    bTrain.append(lable)  # CorssEntropyLoss that is why not doing 1 hot encoding

# after this we have to convert it into numpy array
aTrain = np.array(aTrain)
bTrain = np.array(bTrain)


# PyTorch model and training

class CDataset(Dataset):  # ChatDataset
    def __int__(self):
        self.n_samples = len(aTrain) #store number of samples a train array
        self.adata = aTrain
        self.bdata = bTrain

        # dataset[index]
        def __getitem__(self, index): #
            return self.adata[index], self.bdata[index]

        def __len__(self):
            return self.n_samples


#hyperparameters
batch_size=8;

dataset=CDataset()
# create a data loader here
# batch size=8 (lets)
# number of workers =2 --> it is for multiprocessing so that it works faster
train_loader=DataLoader(dataset=CDataset, batch_size=8, shuffle=True , num_workers=2)
# num_workers sometimes throws an error in windows so if that is the case just set it to 0
# We can automatically iterate over it and can get a batch training

# now let go for the training look for the Training.

