from transformers import AutoTokenizer, TFAutoModel
import tensorflow as tf
from scipy.spatial.distance import cosine

MODEL = "../paraphrase-multilingual-MiniLM-L12-v2-finetuned-squad-7-epochs"

class FineTunedModel:
    def __init__(self, model=MODEL) -> None:
        self.__auto_model = TFAutoModel.from_pretrained(model)
        self.__tokenizer = AutoTokenizer.from_pretrained(model)

    def __mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = tf.cast(tf.tile(tf.expand_dims(attention_mask, -1), [1, 1, token_embeddings.shape[-1]]), tf.float32)
        
        return tf.math.reduce_sum(token_embeddings * input_mask_expanded, 1) / tf.math.maximum(tf.math.reduce_sum(input_mask_expanded, 1), 1e-9)


    def encode(self, text):
        encoded_input = self.__tokenizer(text, padding=True, truncation=True, return_tensors='tf')
        model_output = self.__auto_model(**encoded_input, return_dict=True)
        embeddings = self.__mean_pooling(model_output, encoded_input['attention_mask'])
        embeddings = tf.math.l2_normalize(embeddings, axis=1)

        return embeddings