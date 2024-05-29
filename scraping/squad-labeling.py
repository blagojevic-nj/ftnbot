from datasets import load_dataset
import pandas as pd
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, models, InputExample, losses
from sklearn.model_selection import train_test_split
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from transformers import AutoTokenizer, TFAutoModel
import tensorflow as tf
from scipy.spatial.distance import cosine
import json
import csv
from final.fine_tuned_model import FineTunedModel
import time

def cosine_similarity(vector1, vector2):
    return (1- cosine(vector1, vector2))

def save_dataset():
    with open("./squad-en-with-labels.csv", 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writerows(updated_rows)

model = FineTunedModel(model="./all-MiniLM-L6-v2")
updated_rows = []

counter = 0
with open("./train_dataset.csv", newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)

    fieldnames = csvreader.fieldnames + ['score']
    
    start = time.time()
    for row in csvreader:
        # Extract the context and question from each row
        context = row['context']
        if row['question'].strip() != "":
            vector1 = model.encode(context)
            vector2 = model.encode(row['question'])
            row['score'] = cosine_similarity(vector1[0], vector2[0])
            updated_rows.append(row)
            if counter == 100:
                print(counter)
            
            if counter % 5000 == 0:
                save_dataset()
                updated_rows = []
        counter += 1

with open("./squad-en-with-label.csv", 'a', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writerows(updated_rows)