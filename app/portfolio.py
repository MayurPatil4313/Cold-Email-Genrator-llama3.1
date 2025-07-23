import pandas as pd
import uuid
import chromadb

class Portfolio:
    def __init__(self , file_path='app/resource/my_portfolio.csv'):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('Vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name='portfolio')

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        print('qury executing in query_links')
        print('skills in query_links => ', skills)
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])


if __name__ == "__main__":
    print('IN portfolio.py file')