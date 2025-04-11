# textbase/backend.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from textbase.textbase.message import Message
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import sys
import logging
from typing import List
import importlib
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

load_dotenv()
file_path = os.environ.get("FILE_PATH", "textbase/main.py")
main_dir = os.path.dirname(os.path.abspath(file_path))
if main_dir not in sys.path:
    sys.path.insert(0, main_dir)



app = FastAPI()

origins = [
    "https://chatbot-pro-41d70c5b0e1f.herokuapp.com/",
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:4000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    The `read_root` function reads and returns the contents of an HTML file specified by the path
    "textbase/frontend/index.html".
    :return: The content of the "index.html" file located in the "textbase/frontend" directory is being
    returned.
    """
    with open("textbase/textbase/Chatbot to send/build/index.html") as f:
        return f.read()

class Message(BaseModel):
    text: str
    sender: str  # "user" 或 "bot"

def get_module_from_file_path(file_path: str):
    """
    The function `get_module_from_file_path` takes a file path as input, loads the module from the file,
    and returns the module.

    :param file_path: The file path is the path to the Python file that you want to import as a module.
    It should be a string representing the absolute or relative path to the file
    :type file_path: str
    :return: the module that is loaded from the given file path.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
module = get_module_from_file_path(file_path)
on_message = getattr(module, "on_message", None)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = [Message(**m) for m in data.get("messages", [])]
    state = data.get("state", {})
    state2 = data.get("state2", {})

    result = on_message(messages, state, state2)
    if isinstance(result, tuple):
        response, new_state = result
        return {"botResponse": {"content": response}, "newState": new_state}
    else:
        return {"botResponse": {"content": result}}

# Mount the static directory (frontend files)
app.mount(
    "/",
    StaticFiles(directory="textbase/textbase/Chatbot to send/build", html=True),
    name="static",
)
