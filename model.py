import os
import pandas as pd
import numpy as np

import torch
from transformers import BertTokenizer,BertModel,BertForSequenceClassification,get_linear_schedule_with_warmup
from numpy import dot
from numpy.linalg import norm

from joblib import dump, load
from sklearn.decomposition import PCA

#%%
class EmbeddingModel:
    def __init__(self, model_name):
        if model_name == 'bert':
            output_dir = './model_save_bert/'
        elif model_name == 'roberta':
            output_dir = './model_save_roberta/'
            self.df = pd.read_csv('finetuned.csv')
            self.all_embeddings = np.load('finetuned_roberta_reduced.npy')
        self.pca = load('pca.joblib')
        self.model = BertModel.from_pretrained(output_dir)
        self.tokenizer = BertTokenizer.from_pretrained(output_dir)
        self.model.to('cpu')
        
    def embed_text(self,text):
        encoded_input = self.tokenizer.encode_plus(
                            text,                      # 输入文本
                            add_special_tokens = True, # 添加 '[CLS]' 和 '[SEP]'
                            max_length = 512,           # 填充 & 截断长度
                            pad_to_max_length = True,
                            return_attention_mask = True,   # 返回 attn. masks.
                            return_tensors = 'pt',     # 返回 pytorch tensors 格式的数据
                            )
        with torch.no_grad():
            output = self.model(**encoded_input)
        self.embeddings = output.last_hidden_state.squeeze(0)  # 去除batch维度
        return self.embeddings
    
    def cosine(self,list_1, list_2):
        list_1 = list_1.flatten()
        list_2 = list_2.flatten()
        cos_sim = dot(list_1, list_2) / (norm(list_1) * norm(list_2))
        return cos_sim
    
    def calculate_similarity(self,embedding):
        similarity = []
        for em in self.all_embeddings:
            similarity.append(self.cosine(embedding,em))
        return similarity
    
    def topk(self,text,k=3):
        embedding = self.embed_text(text)
        embedding = self.pca.transform([embedding.flatten().numpy()])
        similarity= self.calculate_similarity(embedding)
        return sorted(zip(similarity, self.df['JID']), reverse=True)[:k]
        