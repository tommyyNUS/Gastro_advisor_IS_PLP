# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 00:44:00 2020

@author: Ritesh Munjal
"""

import torch
from transformers import AutoTokenizer, AutoConfig
from modeling import BertForSentimentClassification
from arguments import args
import pandas as pd

def classify_sentiment(sentence):
    with torch.no_grad():
        tokens = tokenizer.tokenize(sentence)
        tokens = ['[CLS]'] + tokens + ['[SEP]']
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_ids = torch.tensor(input_ids)
        input_ids = input_ids.unsqueeze(0)
        attention_mask = (input_ids != 0).long()
        logit = model(input_ids=input_ids, attention_mask=attention_mask)
        prob = torch.sigmoid(logit.unsqueeze(-1))
        prob = prob.item()
        soft_prob = prob > 0.5
        if soft_prob == 1:
            print( sentence +','+ "Positive" +','+ "%.2f" %(prob*100) + '%') 
        else:
            print( sentence + ',' + "Negative" + ',' + "%.2f" %(100 - prob*100) +'%')


if __name__ == "__main__":
    if args.model_name_or_path is None:
        args.model_name_or_path = './models/my_model_bert'

    #Configuration for the desired transformer model
    config = AutoConfig.from_pretrained(args.model_name_or_path)

    print('Please wait while the model is loading')

    #Create the model with Bert model
    if config.model_type == 'bert':
        model = BertForSentimentClassification.from_pretrained(args.model_name_or_path)
    else:
        raise ValueError('Model does not exist')
   
    model.eval()

    #Initialize the tokenizer for the desired transformer model
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    
    #Upload the reviews to get the sentiment score
    df = pd.read_csv('./reviews_with_aspects_full.csv', engine='python')
    df1 = df[:200]['Review']
    print(df1)
    for sentence in df1:
        classify_sentiment(sentence)
