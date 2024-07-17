from openai import OpenAI
from typing import List, Optional
from groq import Groq
from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import streamlit as st
from app import INDEX_NAME
#rom chaves import *


API_KEY_PINECONE = st.secrets['API_KEY_PINECONE']
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
GROQ_API_KEY= st.secrets['GROQ_API_KEY']

client_OpenAI = OpenAI(api_key=OPENAI_API_KEY)

pc = Pinecone(api_key=API_KEY_PINECONE)



client_Groq = Groq(
    api_key=GROQ_API_KEY,
)

def get_embedding(text: str, model="text-embedding-3-large", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = client_OpenAI.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding
def get_embedding_small(text: str, model="text-embedding-3-small", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = client_OpenAI.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding


def similares(text):
    try:
        
        index = pc.Index(INDEX_NAME)
        if INDEX_NAME=='rag-comprimento-sentenca-large':
            embeddings=get_embedding(text)
        elif INDEX_NAME=='ragconsultor':
            embeddings=get_embedding_small(text)
        
        query=index.query(
            vector=embeddings,
            top_k=3,
            include_metadata=True
        )

        textos_similares=[]
        for matches in query['matches']:
            textos_similares.append(str(matches['metadata']['texto']))
        
        
        return textos_similares

    except Exception as e:
        print(e)




def chat_llama_rag(text):

    textos_similares=similares(text)
    
    chat_completion = client_Groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                'content':'Os textos abaixos são sentenças em segunda instancias sobre processos que podem ser relevantes para a pergunta do usuario.',
                'content':textos_similares[0],
                'content':textos_similares[1],
                'content':textos_similares[2],
                'content':'Dado esses contextos acima responda a pergunta?',
            },
            {
                'role':'user',
                'content':text
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def chat_llama_sem_rag(text):

   
    
    chat_completion = client_Groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": 'Eu sou um assistente oque posso ajudar?'
            },
            {
                'role':'user',
                'content':text
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def chat_gpt_rag(text):
    # Função fictícia que retorna textos semelhantes
    textos_similares = similares(text)
    
    # Preparando as mensagens para o chat
    messages = [
        {"role": "system", "content": 'Os textos abaixos são sentenças em segunda instancias sobre processos que podem ser relevantes para a pergunta do usuario.'},
        {"role": "system", "content": textos_similares[0]},
        {"role": "system", "content": textos_similares[1]},
        {"role": "system", "content": textos_similares[2]},
        {"role": "system", "content": "Dado esses contextos acima responda a pergunta?"},
        {"role": "user", "content": text}
    ]
    
    completion = client_OpenAI.chat.completions.create(
    model="gpt-4o",
    messages=messages
)   
    return completion.choices[0].message.content
   