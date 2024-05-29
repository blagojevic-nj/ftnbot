from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, models, InputExample, losses
from sklearn.model_selection import train_test_split
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
import json
import csv
from sklearn.model_selection import train_test_split

class FineTunerWithLabels:
    def __init__(self) -> None:
        self.score_dict = {}
        self.dataset_examples = []
    
    def load_labels(self):
        with open("./squad-with-labels.csv", newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            idx = row['id']
            score = row['score']
            self.score_dict[idx] = score
    
    def create_dataset_examples(self):
        with open("./squad-sr-lat.json", 'r', encoding="UTF-8") as f:
            data = json.loads(f.read())

        for d in data['data']:
            for parag in d['paragraphs']:
                for question in parag["qas"]:
                    idx = question['id']
                    if idx in self.score_dict:
                        self.dataset_examples.append(InputExample(texts=[question["question"], parag["context"]], label=float(self.score_dict[idx])))

    def fine_tune(self):
        word_embedding_model = models.Transformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

        train_examples, val_examples = train_test_split(self.dataset_examples, test_size=0.2, random_state=42)

        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

        train_loss = losses.CosineSimilarityLoss(model=model)
        evaluator = EmbeddingSimilarityEvaluator.from_input_examples(val_examples, name='val-eval')

        num_epochs = 10
        warmup_steps = int(len(train_dataloader) * num_epochs * 0.1)

        model.fit(train_objectives=[(train_dataloader, train_loss)],
                evaluator=evaluator,
                evaluation_steps=int(len(train_dataloader) * 0.1),
                epochs=num_epochs,
                warmup_steps=warmup_steps,
                output_path="./paraphrase-multilingual-MiniLM-L12-v2-finetuned-squad")
        

if __name__ == '__main__':
    ft = FineTunerWithLabels()
    ft.load_labels()
    ft.create_dataset_examples()
    ft.fine_tune()