import textbase
from textbase.textbase.message import Message
from textbase.textbase import models
import os
from typing import List
import openai
import json
import datetime
import re
import requests

# Load your OpenAI API key
models.OpenAI.api_key = "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" #api
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-40 Turbo
SYSTEM_PROMPT = """You are chatting with a Medical Assistant. I can provide information on medical topics and answer health-related questions. Please remember that I'm not a substitute for professional medical advice. If you have a medical emergency, please call emergency services immediately.
"""
diagnosis_api_url = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/table/diagnosis"
disease_api_url = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/table/diabetes"


def aggregate_conversation_history(message_history: List[Message]) -> str:
    return "\n".join([f"{msg.sender.capitalize()}: {msg.text}" for msg in message_history])

def build_patient_context(patient_id: str, age: int, chronic_diseases: list) -> str:
    """
    Create a string or text block summarizing key patient info.
    This text can then be included in the system prompt or user prompt for GPT.
    """
    diseases_str = ", ".join(chronic_diseases) if chronic_diseases else "None"
    return (
        f"patient_id: {patient_id}\n"
        f"Age: {age}\n"
        f"Known Chronic Diseases: {diseases_str}\n"
    )

def extract_patient_id_from_history(message_history: List[Message]) -> str:
    name_pattern_1 = re.compile(r"(my\s+id\s*(is|=|:)?\s*)(\d+)", re.IGNORECASE)

    for msg in message_history:
        if msg.sender.lower() == "user":
            match1 = name_pattern_1.search(msg.text)
            if match1:
                return match1.group(3).strip()
    return ""

def extract_patient_symptom_from_history(message_history: List[Message]) -> str:
    name_pattern_1 = re.compile(r"(my\s+id\s*(is|=|:)?\s*)(\d+)", re.IGNORECASE)

    for msg in message_history:
        if msg.sender.lower() == "user":
            match1 = name_pattern_1.search(msg.text)
            if match1:
                return match1.group(3).strip()
    return ""

@textbase.textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None, state2: dict = None):
    """Medical Assistant Chatbot logic
#     message_history: List of user messages
#     state: A dictionary to store any stateful information

#     Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
#     """

    if state2 is None:
        state2 = {}
    if "patient_id" not in state2 or not state2["patient_id"]:
        patient_id_str = extract_patient_id_from_history(message_history)
        print(patient_id_str)
        if patient_id_str:
            state2["patient_id"] = int(patient_id_str)
    if "patient_id" in state2 and state2["patient_id"]:
        patient_data = requests.get(disease_api_url)
        table_data = patient_data.json()
        patient_data2 = requests.get(diagnosis_api_url)
        table_data2 = patient_data2.json()
        for row in table_data2:
            if row['patient_id'] == state2["patient_id"]:
                state2['Disease'] = row['description']
        for row in table_data:
            if row['patient_id'] == state2["patient_id"]:
                state2['Age'] = row['Age']
                state2['BMI'] = row['BMI']
                state2['BloodPressure'] = row['BloodPressure']
    print(state2)
    patient_context = ""
    if "BloodPressure" in state2:
        patient_context += f"BloodPressure: {state2['BloodPressure']}\n"
    if "BMI" in state2:
        patient_context += f"BMI: {state2['BMI']}\n"
    if "Age" in state2:
        patient_context += f"Age: {state2['Age']}\n"
    if "Disease" in state2:
        patient_context += f"Disease: {state2['Disease']}\n"

    print(patient_context)
    SYSTEM_PROMPT2 = """You are chatting with a Medical Assistant. 
    I can provide information on patient. I want you to give me some advice based on the information that 
    I give to you. Your response should look like this (example):1.Patient Overview:  2.Diagnosis:  3.Advice:
Each section should be labeled with a number, followed by a period, then a newline. No markdown, no asterisks, no pound/hash signs, no bullet points. Please include the reasoning behind the suggestion.
    """
    system_prompt_with_context = (
        SYSTEM_PROMPT2
        + "\n\n"
        + "Important Patient Information:\n"
        + patient_context
    )
    print(system_prompt_with_context)
    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    converted_history = []
    for msg in message_history:

        role = "assistant" if msg.sender.lower() == "bot" else "user"
        converted_history.append({"role": role, "content": msg.text})
    converted_history.append({
        "role": "user",
        "content": (
            "Please respond in **valid JSON** with these keys only:\n"
            "\"patient_overview\", \"diagnosis\", and \"advice\".\n\n"
            "Under 'patient_overview', you MUST include every item from the system prompt's patient data, "
        "including Age, BMI, BloodPressure, and any other context. "
            "Example:\n"
            "{\n"
            "  \"patient_overview\": \"...\",\n"
            "  \"diagnosis\": \"...\",\n"
            "  \"advice\": \"...\"\n"
            "}"
        )
    })
    bot_response = models.OpenAI.generate(
        system_prompt=system_prompt_with_context,
        message_history=converted_history,
        model="gpt-4o-mini",
    )
    return bot_response, state
