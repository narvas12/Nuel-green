# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from subprocess import Popen, PIPE

class CodeExecutionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json['code']

        # Execute the Python code and capture the result
        result = self.execute_code(code)

        # Send the result back to the WebSocket
        await self.send(text_data=json.dumps({
            'result': result
        }))

    def execute_code(self, code):
        try:
            # Use subprocess to run the Python code and capture the output
            process = Popen(['python', '-c', code], stdout=PIPE, stderr=PIPE, text=True)
            output, error = process.communicate()
            result = output + error
        except Exception as e:
            result = str(e)

        return result
