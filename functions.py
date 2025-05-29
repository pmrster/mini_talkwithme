import random
import time
import streamlit as st

###stream
class StreamResponse:
    def __init__(self, text_to_stream=None):
        self.text_to_stream = text_to_stream
        
    def _get_stream(self):
        for chunk in self.text_to_stream.split():
            time.sleep(0.05)
            yield chunk
            
    def write_stream(self):
        stream = self._get_stream()
        result = ""
        container = st.empty()
        for chunk in stream:
            result += chunk
            container.write(result, unsafe_allow_html=True)


    def text_stream_generator(self):
        for word in self.text_to_stream.split():
            yield word + " "
            time.sleep(0.05)

    def greeting_generator(self):
        response = random.choice(
            [
                "สวัสดี วันนี้มีไรให้ช่วยมั้ย",
                "มีอะไรให้ช่วยบอกได้เลย",
            ]
        )
        for word in response.split():
            yield word + " "
            time.sleep(0.05)


