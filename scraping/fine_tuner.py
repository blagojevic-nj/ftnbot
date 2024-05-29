from sentence_transformers import InputExample
from torch.utils.data import DataLoader
from sentence_transformers import losses
from sentence_transformers import SentenceTransformer, models
import tensorflow as tf

TRAINING_DATA = "./files/STS.news.sr.txt"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
FINE_TUNED_MODEL = "./paraphrase-multilingual-MiniLM-L12-v2-finetuned"


class FineTuner:
    def __init__(self) -> None:
        self.training_data : list[InputExample] = []
        self.model = None

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = tf.cast(tf.tile(tf.expand_dims(attention_mask, -1), [1, 1, token_embeddings.shape[-1]]), tf.float32)
        return tf.math.reduce_sum(token_embeddings * input_mask_expanded, 1) / tf.math.maximum(tf.math.reduce_sum(input_mask_expanded, 1), 1e-9)

    def normalize_label(self, label : float) -> float:
        return 2 * (label / 5.0) - 1.0
    
    def load_training_data(self, path: str) -> None:
        with open(path, 'r', encoding="UTF-8") as f:
            for line in f.readlines():
                line.replace("\n", "")
                tokens = line.split('\t')
                label = float(tokens[0])

                first_sen = tokens[6]
                second_sen = tokens[7]

                self.training_data.append(InputExample(texts=[first_sen, second_sen], label = self.normalize_label(label)))
    
    def fine_tune(self, model_path: str) -> None:
        word_embedding_model = models.Transformer(model_path)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
        self.model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

        train_dataloader = DataLoader(self.training_data, shuffle=True, batch_size=16)
        train_loss = losses.CosineSimilarityLoss(model=self.model)

        num_epochs = 10
        warmup_steps = int(len(train_dataloader) * num_epochs * 0.1)

        self.model.fit(train_objectives=[(train_dataloader, train_loss)],
                epochs=num_epochs,
                warmup_steps=warmup_steps)
    
    def save_model(self, path: str) -> None:
        self.model.save(path)

# if __name__ == "__main__":
#     tuner = FineTuner()
#     tuner.load_training_data(TRAINING_DATA)
#     tuner.fine_tune(MODEL)
#     tuner.save_model(FINE_TUNED_MODEL)