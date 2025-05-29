from openai import OpenAI
import os
import streamlit as st
from ollama import Client
from datetime import datetime

openrouter_api_key= st.secrets["OPENROUTER_API_KEY"]
openrouter_base_url= st.secrets["OPENROUTER_BASE_URL"]
ollama_host = st.secrets["OLLAMA_HOST"]


class AskModel:
    
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt

    ## model - without memory
    def simple_ask(self):
        client = OpenAI(
            base_url=openrouter_base_url,
            api_key=openrouter_api_key,
        )

        completion = client.chat.completions.create(
        model=self.model,
        messages=[
            {
            "role": "user",
            "content": self.prompt
            }
        ]
        )
        print(completion.choices[0].message.content)
        return completion



    ### ส่ง history เก็บเป็น session ของ streamlit แล้วส่งเข้ามาในนี้
    ## https://platform.openai.com/docs/guides/conversation-state?api-mode=chat
    def ask_with_memory(self):
        client = OpenAI(
            base_url=openrouter_base_url,
            api_key=openrouter_api_key,
        )
        ## add system promp
        ### ask
        ask_with_history = client.chat.completions.create(
        model=self.model,
        messages=self.prompt,
        )
        #stream=True
        print(ask_with_history.choices[0].message.content)
        return ask_with_history
    
    ## ask using local moedl (on local device)
    def ask_with_history_ollama(self):
        print(f"start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        ## model= "qwen3:4b", "qwen3:4b"
        client = Client(
        host=ollama_host,
        # headers={'x-some-header': 'some-value'}
        )
        ask_with_history = client.chat(model=self.model, messages=self.prompt)
        
        print(f"end chat time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(ask_with_history.message.content)
        return ask_with_history




def prepare_history_msg(previous_response, prompt):
    new_input_message = previous_response.append({ "role": "user", "content": prompt })
    return new_input_message