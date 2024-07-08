from langchain.text_splitter import CharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.vectorstores import FAISS


class VectorSearch:
    def __init__(self, data:list, model_name:str) -> None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        self.data = data  #content extracted from the url
        self.model_name = model_name
        self.embeddings = HuggingFaceEmbeddings(model_name = self.model_name)
    
    def _split_data(self):
        
        text_splitter = CharacterTextSplitter(chunk_size=1500, separator='\n')
        self.docs, self.metadatas = [], []
        for page in self.data:
            splits = text_splitter.split_text(page['text'])
            self.docs.extend(splits)
            self.metadatas.extend([{"source": page['source']}] * len(splits))
        return self.docs, self.metadatas
    
    def _split_data_markdown(self):

        text_splitter = CharacterTextSplitter(chunk_size=1500, separator='\n')
        self.docs, self.metadatas = [], []
        for page in self.data:
            splits = text_splitter.split_text(page['text'].lower())
            self.docs.extend(splits)
            self.metadatas.extend([{"source": page['source']}] * len(splits))

        return self.docs, self.metadatas
    
    def _faiss_search(self):
        store = FAISS.from_texts(self.docs, self.embeddings, metadatas=self.metadatas)
        return store



        
        
    
        
