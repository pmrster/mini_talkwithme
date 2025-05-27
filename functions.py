import random
import time


###stream
class StreamResponse:
    def __init__(self, text_to_stream=None):
        self.text_to_stream = text_to_stream


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
