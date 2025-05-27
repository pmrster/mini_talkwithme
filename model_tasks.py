from openai import OpenAI
import os
import streamlit as st

openrouter_api_key= st.secrets["OPENROUTER_API_KEY"]
openrouter_base_url= st.secrets["OPENROUTER_BASE_URL"]


## model - without memory
def simple_ask(prompt,model):
    client = OpenAI(
        base_url=openrouter_base_url,
        api_key=openrouter_api_key,
    )

    completion = client.chat.completions.create(
    model=model,
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ]
    )
    print(completion.choices[0].message.content)
    return completion



### ส่ง history เก็บเป็น session ของ streamlit แล้วส่งเข้ามาในนี้
## https://platform.openai.com/docs/guides/conversation-state?api-mode=chat
def ask_with_memory(history, model):
    client = OpenAI(
        base_url=openrouter_base_url,
        api_key=openrouter_api_key,
    )
    ## add system promp
    ### ask
    ask_with_history = client.chat.completions.create(
    model=model,
    messages=history,
    )
    #stream=True
    print(ask_with_history.choices[0].message.content)
    return ask_with_history

def prepare_history_msg(previous_response, prompt):
    new_input_message = previous_response.append({ "role": "user", "content": prompt })
    return new_input_message