import streamlit as st
from rag_model import *

prompt = st.chat_input("Fale alguma coisa")
choice = st.radio('Qual modelo',['Llamma 3','ChatGPT4o'])

if choice == 'Llamma 3':
        st.write('LLAMA 3')
        if prompt:
            st.write(f" {prompt}")

            message = st.chat_message("assistant")
            message.write("Ola vou ajudar com sua pergunta")


            resposta = chat_llama_rag(prompt)

            message.write(resposta)

if choice == 'ChatGPT4o':
        st.write('ChatGPT4o')
        if prompt:
            st.write(f" {prompt}")

            message = st.chat_message("assistant")
            message.write("Ola vou ajudar com sua pergunta")


            resposta = chat_gpt_rag(prompt)

            message.write(resposta)