import streamlit as st
from rag_model import *

INDEX_NAME=''


choice = st.radio('Qual modelo',['Llamma 3-rag','Llamma 3-puro','ChatGPT4o'])
choice2=st.radio('Qual Area',['Carros','Juridica'])

if choice2=='Carros':
      INDEX_NAME='ragconsultor'
elif choice2=='Juridica':
      INDEX_NAME='rag-comprimento-sentenca-large'

if choice == 'Llamma 3-rag':
        st.write('LLAMA 3')
        prompt = st.chat_input("Fale alguma coisa",key='Chat')
        if prompt:
            st.write(f" {prompt}")

            message = st.chat_message("assistant")
            message.write("Ola vou ajudar com sua pergunta")


            resposta = chat_llama_rag(prompt)

            message.write(resposta)

if choice == 'Llamma 3-puro':
        st.write('LLAMA 3')
        prompt = st.chat_input("Fale alguma coisa",key='Chat')
        if prompt:
            st.write(f" {prompt}")

            message = st.chat_message("assistant")
            message.write("Ola vou ajudar com sua pergunta")


            resposta = chat_llama_sem_rag(prompt)

            message.write(resposta)


if choice == 'ChatGPT4o':
        st.write('ChatGPT4o')
        prompt = st.chat_input("Fale alguma coisa",key='Chat')
        if prompt:
            st.write(f" {prompt}")

            message = st.chat_message("assistant")
            message.write("Ola vou ajudar com sua pergunta")


            resposta = chat_gpt_rag(prompt)

            message.write(resposta)