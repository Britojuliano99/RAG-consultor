from openai import OpenAI
from typing import List, Optional
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from chaves import *
import pandas as pd

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from sentence_transformers import SentenceTransformer


def get_embeddings_lm6(sentences):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    return embeddings


def change_to_dict(valor):
    return {"texto": valor}
def get_embeddings(texts: List[str], model="text-embedding-3-small", **kwargs) -> List[List[float]]:
    # Replace newlines in each text, which can negatively affect performance.
    texts = [text.replace("\n", " ") for text in texts]

    response = client_OpenAI.embeddings.create(input=texts, model=model, **kwargs)

    return [data.embedding for data in response.data]

if os.path.exists('./df_split_langchain.parquet') == False:

    ### READ THE coments and using Recursive Character Text splitter to give a smaller text size to be embedded
    with open('all_coments.txt', 'r') as f:
        text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    sentences=text_splitter.split_text(text)

    client_OpenAI = OpenAI(api_key=OPENAI_API_KEY)



    # Assuming 'sentences' is a list of sentences
    batch_size = 100  # You can adjust this batch size according to your needs
    embeddings = []

    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i + batch_size]
        batch_embeddings = get_embeddings_lm6(batch)
        embeddings.extend(batch_embeddings)
        print(f"Processed batch {i // batch_size + 1}")

    df_split_langchain = pd.DataFrame()
    df_split_langchain['texto'] = sentences
    df_split_langchain['values'] = embeddings


    # Aplicar a função à série e atribuir à coluna 'metadata' do df_pinecone
    df_split_langchain['texto']=df_split_langchain.texto.replace('\n',' ')
    df_split_langchain['metadata'] = df_split_langchain['texto'].apply(change_to_dict)

    df_split_langchain.drop('texto', axis=1, inplace=True)

    df_split_langchain.reset_index( inplace=True)
    df_split_langchain.rename(columns={'index': 'id'}, inplace=True)

    df_split_langchain.head()

    df_split_langchain.to_parquet('df_split_langchain.parquet')

else:
    df_split_langchain = pd.read_parquet('df_split_langchain.parquet')

df_split_langchain.id = df_split_langchain.id.astype(str)
pc = Pinecone(api_key=API_KEY_PINECONE)

index_name = 'rag-embed-local' #Change the name according to your use


TEXT_EMBEDDING_SIZE=384 # this depends of you embedding model, the size of openAI textembedding small is 1536.
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=TEXT_EMBEDDING_SIZE,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 


index = pc.Index(index_name)

index.upsert_from_dataframe(df=df_split_langchain,batch_size=100)