from sentence_transformers import InputExample
from torch.utils.data import DataLoader
from sentence_transformers import losses
from sentence_transformers import SentenceTransformer, models
from transformers import AutoTokenizer, TFAutoModel
import tensorflow as tf
from pinecone import Pinecone

from scipy.spatial.distance import cosine

# PINECONE_API_KEY = "3b3a404c-6668-4006-a87b-1b71307db0b0"
# INDEX_NAME = "master-rad"
MODEL = "./paraphrase-multilingual-MiniLM-L12-v2-finetuned-squad-labels"

model = TFAutoModel.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)


# pc = Pinecone(api_key=PINECONE_API_KEY) 
# index = pc.Index(INDEX_NAME)

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = tf.cast(tf.tile(tf.expand_dims(attention_mask, -1), [1, 1, token_embeddings.shape[-1]]), tf.float32)
    return tf.math.reduce_sum(token_embeddings * input_mask_expanded, 1) / tf.math.maximum(tf.math.reduce_sum(input_mask_expanded, 1), 1e-9)


def encode(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='tf')
    model_output = model(**encoded_input, return_dict=True)
    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    embeddings = tf.math.l2_normalize(embeddings, axis=1)

    return embeddings

def cosine_similarity(vector1,vector2):
    return (1- cosine(vector1,vector2))

def query_pinecone(query: str, top_k: int):
    xq = encode(query).numpy().tolist()
    return index.query(vector=xq, top_k=top_k, include_metadata=True)


vocab_wrd2idx = tokenizer.vocab
vocab_idx2wrd = {v:k for k,v in vocab_wrd2idx.items()}

model_weights = model.get_weights()
vocab_weights = model_weights[0]



# query = ""

# while query != "stop":
#     query = input(">>>>")
#     print(query_pinecone(query, 2))

text1 = "Fakultet tehnickih nauka je najveci fakultet u Srbiji."
text2 = "Koji je najveci fakultet u Srbiji?"

while True:
    vector1 = encode(text1)
    vector2 = encode(text2)

    print(cosine_similarity(vector1[0], vector2[0]))

    text1 = input("text1 >>>")
    text2 = input("text2 >>>")
