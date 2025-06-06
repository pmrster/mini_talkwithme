import streamlit as st
import random
import time
import json
from datetime import datetime

from model_tasks.model_tasks import AskModel
from functions.functions import StreamResponse
from prompts.prompts import thai_only_response

## set config
app_token = st.secrets["APP_TOKEN"]

st.set_page_config(
    page_title="talkwithme",
    page_icon="🥺",
    layout="wide"
)


# if "llm_model" no  in st.session_state:
#     st.session_state["llm_model"] = "meta-llama/llama-3.3-8b-instruct:free"
    
# if 'button_clicked' not in st.session_state:
#     st.session_state['button_clicked'] = False

if "messages" not in st.session_state:
    st.session_state.messages = []



#### page element
with st.sidebar:
    # user_input_api_key = st.text_input("Enter open router API Key",type="password")
    st.write(":gray[this app using open router api]")
    
    ## uncomment this if you run on local
    # is_ollama = st.radio(label="select server (local)",options=["open_router", "ollama"]) ##for local test
    
    ## uncomment this if you deploy on streamlit cloud
    is_ollama = st.radio(label="select server (streamlit cloud)",options=["open_router"]) ## for streamlit cloud
    
    st.write(":blue[openrouter will limited to 50 requests]")
    st.write(":red[_warning: ollama will available only for running on local only!_]")
    
    if is_ollama == "open_router":
        selected_llm = st.selectbox("select llm model you want to talk with",
                                    ("meta-llama/llama-3.3-8b-instruct:free",
                                    #  "google/gemma-3n-e4b-it:free",
                                    "deepseek/deepseek-v3-base:free",
                                    "google/gemma-3-12b-it:free",
                                    "google/gemma-3-4b-it:free",
                                    "google/gemma-3-27b-it:free",
                                    "meta-llama/llama-4-maverick:free",
                                    "deepseek/deepseek-r1:free",
                                    "qwen/qwen3-8b:free",
                                    "qwen/qwen3-14b:free",
                                    "qwen/qwen3-30b-a3b:free",
                                    "qwen/qwen3-32b:free",
                                    "qwen/qwen3-235b-a22b:free"
                                    )
                                    )
        st.write(f"selected llm -> {selected_llm}")
    elif is_ollama == "ollama":
        selected_llm = st.selectbox("select llm model you want to talk with",
                                    ("qwen3:1.7b",
                                     "gemma3:4b",
                                     "qwen3:4b",
                                     "qwen3:0.6b",
                                     "qwen3:8b",
                                     "scb10x/typhoon2.1-gemma3-4b:latest",
                                     "scb10x/llama3.1-typhoon2-8b-instruct:latest",
                                     "deepseek-r1:8b"
                                    )
                                    )
        st.write(f"selected llm -> {selected_llm}")
        
    
    reset_button = st.button("Reset session", type="primary")
    
    if reset_button:
        file_name = f"{datetime.now().strftime('%Y.%m.%d_%H%M%S')}_session_message_logs.json"
        with open(f"messages_logs/{file_name}", "w", encoding='utf-8') as f:
            json_string = json.dumps(st.session_state.messages, indent=4,ensure_ascii=False)
            f.write(json_string) 
        
        
        print(f"saved messages conversation after clear seesion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.session_state.messages = []
        print("cleared session!!")

    # model="meta-llama/llama-3.3-8b-instruct:free"

## chat area
st.title("chatwithme")
st.caption("update: 2025.06.07 1:09AM")
st.write(":gray[can using open router api or your local ollama]")

for message in st.session_state.messages:
    if message["role"] == "assistant":
        avatar = "🐣"
    elif message["role"] == "user":
        avatar = "🧑‍💻"
    with st.chat_message(message["role"],avatar=avatar):
        st.markdown(message["content"])

# Display assistant response in chat message container
if len(st.session_state.messages) == 0:
    print(len(st.session_state.messages))
    with st.chat_message("assistant", avatar="🐣"):
        response = st.write_stream(StreamResponse().greeting_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})        
        
# Accept user input
if prompt := st.chat_input("สอนวิธีทำออมเล็ตแบบง่ายๆหน่อย"):
    if prompt == "/quit":
        ## create file for save session on local device
        file_name = f"{datetime.now().strftime('%Y.%m.%d_%H%M%S')}_session_message_logs.json"
        with open(f"messages_logs/{file_name}", "w", encoding='utf-8') as f:
            json_string = json.dumps(st.session_state.messages, indent=4,ensure_ascii=False)
            f.write(json_string) 
        
        print(f"saved messages conversation after user say /quit : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("end of session")
        ## reset messages session to blank
        st.session_state.messages = []
        
    
    else:
    # Display user message in chat message container
        print(len(st.session_state.messages))
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar="🐣"):
            ## call iilm🤩🥺🐱🐔🐙🐥🐣🧐👻
            # get_instruct_prompt = thai_only_response(user_prompt=response)
            # st.session_state.messages.append({"role": "assistant", "content": get_instruct_prompt})  
            
            new_input_message = [ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages ]

            system_prompt  = [{"role": "system","content": thai_only_response()}]
            final_history = system_prompt + new_input_message
            with st.spinner("I'm thinking...", show_time=True):
                if is_ollama == "open_router":
                    try:
                        model_response = AskModel(model=selected_llm, prompt=final_history).ask_with_memory()
                        response = st.write_stream(StreamResponse(model_response.choices[0].message.content).text_stream_generator())
                    except Exception as e:
                        response = f"Error: {e}"
                        print(f"Error: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": response})
                elif is_ollama == "ollama":
                    try:
                        model_response = AskModel(model=selected_llm, prompt=final_history).ask_with_history_ollama()
                        # response = StreamResponse(model_response.message.content).write_stream()
                        response = st.write_stream(StreamResponse(model_response.message.content).text_stream_generator())
                    except Exception as e:
                        response = f"Error: {e}"
                        print(f"Error: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
        
    

