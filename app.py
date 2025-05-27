import streamlit as st
import random
import time

from model_tasks import ask_with_memory
from functions import StreamResponse
from prompts import thai_only_response

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
    selected_llm = st.selectbox("select llm model you want to talk with",
                                ("meta-llama/llama-3.3-8b-instruct:free",
                                #  "google/gemma-3n-e4b-it:free",
                                 "deepseek/deepseek-v3-base:free",
                                 "google/gemma-3-12b-it:free",
                                 "google/gemma-3-4b-it:free",
                                 "google/gemma-3-27b-it:free",
                                 "meta-llama/llama-4-maverick:free",
                                 "deepseek/deepseek-r1:free" 
                                 )
                                )
    st.write(f"selected llm -> {selected_llm}")
    
    reset_button = st.button("Reset session", type="primary")
    
    if reset_button:
        st.session_state.messages = []
        

    # model="meta-llama/llama-3.3-8b-instruct:free"

## chat area
st.title("chatwithme")
st.caption("update: 2025.05.26 2:49PM")
st.write(":gray[this app using open router api]")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display assistant response in chat message container
if len(st.session_state.messages) == 0:
    print(len(st.session_state.messages))
    with st.chat_message("assistant"):
        response = st.write_stream(StreamResponse().greeting_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})        
        
# Accept user input
if prompt := st.chat_input("What is up?"):
    if prompt == "/quit":
        print("end of session")
        st.session_state.messages = []
    
    else:
    # Display user message in chat message container
        print(len(st.session_state.messages))
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            ## call iilm
            # get_instruct_prompt = thai_only_response(user_prompt=response)
            # st.session_state.messages.append({"role": "assistant", "content": get_instruct_prompt})  
            
            new_input_message = [ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages ]
            system_prompt  = [{"role": "system","content": thai_only_response()}]
            final_history = system_prompt + new_input_message
            model_response = ask_with_memory(history=final_history, model=selected_llm)
            response = st.write_stream(StreamResponse(model_response.choices[0].message.content).text_stream_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})
    

