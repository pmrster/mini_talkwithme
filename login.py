import streamlit as st 
import time

app_token = st.secrets["APP_TOKEN"]

@st.dialog("Sign In")
def login_modal():
    st.write("Please sign in to use this feature")
    input_key = st.text_input("Enter your access key", type="password", help="ask admin")
        
    if st.button("Submit", key=3):
        st.session_state.login_key = input_key
        if input_key == app_token:
            st.write("Correct key, you can use this feature!")
            # time.sleep(5)
        else:
            st.write(":red[**Please enter access key**]")
            time.sleep(5)
        st.rerun()
