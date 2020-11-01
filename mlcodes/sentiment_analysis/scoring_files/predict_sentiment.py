# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 00:44:00 2020

@author: Ritesh Munjal, Paul S.R
"""

import torch
from transformers import AutoTokenizer, AutoConfig
from model.modeling import BertForSentimentClassification
from model.arguments import args

class BertSentiment:

    _bert = None
    _tokenizer = None

    def classify_sentiment(self,sentence):
        with torch.no_grad():
            # prepare tokens and input
            tokens = self._tokenizer.tokenize(sentence)
            tokens = ['[CLS]'] + tokens + ['[SEP]']
            input_ids = self._tokenizer.convert_tokens_to_ids(tokens)
            input_ids = torch.tensor(input_ids)
            input_ids = input_ids.unsqueeze(0)
            attention_mask = (input_ids != 0).long()
            
            # invoke BERT
            logit = self._bert(input_ids=input_ids, attention_mask=attention_mask)
            prob = torch.sigmoid(logit.unsqueeze(-1))
            
            # print probability
            prob = prob.item()
            #print(sentence, "::", prob)

            if prob > 0.5:
                print( sentence +','+ "Positive" +','+ "%.2f" %(prob*100) + '%') 
            else:
                print( sentence + ',' + "Negative" + ',' + "%.2f" %(100 - prob*100) +'%')

            return prob

    def __init__(self):
        if self._bert is None:
            args.model_name_or_path = './model/fine_tuned_bert'
        
            #Configuration for the desired transformer model
            config = AutoConfig.from_pretrained(args.model_name_or_path)
        
            print('Please wait while the model is loading')
        
            #Create the model with Bert model
            if config.model_type == 'bert':
                self._bert = BertForSentimentClassification.from_pretrained(args.model_name_or_path)
            else:
                raise ValueError('Model does not exist')
           
            self._bert.eval()
            print('Model has been loaded successfully')
        
            # initialize the tokenizer for the desired transformer model
            self._tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
        
        
if __name__ == "__main__":
    
    try:
        # create BERT model for Sentiment Analysis
        bert_sentiment = BertSentiment()
    
        df = ["The food was fine", 
               "The food was good", 
               "The food was excellent", 
               "The food was bad", 
               "It is just food"]
        for sentence in df:
            bert_sentiment.classify_sentiment(sentence)
            
    except:
        print("\n<<< An exception occurred >>>") 
        raise

