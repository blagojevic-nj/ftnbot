from pinecone import Pinecone
from fine_tuned_model import FineTunedModel

PINECONE_API_KEY = "3b3a404c-6668-4006-a87b-1b71307db0b0"
INDEX_NAME = "master-rad"


class DatabaseAdapter:
    def __init__(self) -> None:
        self.pc = Pinecone(api_key=PINECONE_API_KEY) 
        self.index = self.pc.Index(INDEX_NAME)
        self.model = FineTunedModel()
    
    def query_database(self, query: str = "", top_k: int = 2):
        vector = self.model.encode(query).numpy().tolist()
        return self.index.query(vector=vector, top_k=top_k, include_metadata=True)
    
    def add_context(self, context: str):
        idx  = self.index.describe_index_stats()['total_vector_count']
        context_info=(str(idx+1),
                self.model.encode(context).numpy().tolist()[0],
                {'title': "ftn-info",'context': context})
        
        self.index.upsert(vectors=[context_info])

    def delete_context(self, id: str):
        self.index.delete(ids=[id])

    def update_context(self, context): 
        context_info = (context['id'],
                        self.model.encode(context['text']).numpy().tolist()[0],
                        {'title': 'ftn-info', 'context': context['text']})
        
        self.index.upsert(vectors=[context_info])

