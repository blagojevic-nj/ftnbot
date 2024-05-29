from fine_tuned_model import FineTunedModel
from pinecone import Pinecone

PINECONE_API_KEY = "3b3a404c-6668-4006-a87b-1b71307db0b0"
INDEX_NAME = "master-rad"


FINAL_FILE_LAT = "./files/full_text.txt"

class DatabasePopulator:
    def __init__(self) -> None:
        self.text_chunks: list[str] = []
        self.pc = Pinecone(api_key=PINECONE_API_KEY) 
        self.index = self.pc.Index(INDEX_NAME)
        self.model = FineTunedModel()
        self.plain_text = ""

    def load_text(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            self.plain_text = f.read()

    def split_text(self) -> None:
        for chunk in self.plain_text.split("<br>"):
            self.text_chunks.append(' '.join(chunk.split()))

    def add_data(self, data) -> None:
        print(len(data))
        idx  = self.index.describe_index_stats()['total_vector_count']
        for i in range(len(data)):
            print("Added ", i, ". chunk")
            context_info=(str(idx+i),
                    self.model.encode(data[i]).numpy().tolist()[0],
                    {'title': "ftn-info",'context': data[i]})
            
            self.index.upsert(vectors=[context_info])
        


if __name__ == "__main__":
    dp = DatabasePopulator()
    
    dp.load_text(FINAL_FILE_LAT)
    dp.split_text()

    dp.add_data(dp.text_chunks)