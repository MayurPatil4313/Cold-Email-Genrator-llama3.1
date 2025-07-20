import pandas as pd
import uuid
import chromadb
# from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


class Portfolio:
    def __init__(self , file_path='D:/Learnbay\Cold Email Genrator llama3.1/app/venv/resource/generated_techstack_portfolio.csv'):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

        # embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.chroma_client = chromadb.PersistentClient('Vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name='portfolio')

    def load_portfolio(self):
        print('inside load_portfolio')
        if not self.collection.count():
            for idx , row in self.df.iterrows():
                # self.collection.add(
                #     documents=row['Techstack'],
                #     metadatas={'links': row['Links']},
                #     ids=[str(uuid.uuid4())]
                # )
                self.collection.add(
                    documents=[row['Techstack']],  # wrap in list!
                    metadatas=[{'links': row['Links']}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        print('qury executing in query_links')
        print('skills in query_links => ', skills)
        return self.collection.query(query_texts=skills, n_results=2).get(metadatas='metadatas')


if __name__ == "__main__":
    print('IN portfolio.py file')
    
    
