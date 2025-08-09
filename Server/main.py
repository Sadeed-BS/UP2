# --- Imports ---
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Aibohphobia Chatbot API",
    description="A chatbot that loves palindromes and riddles, powered by LangGraph and Gemini.",
)

# Initialize Gemini model (using environment variable for API key)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_tokens=512,
    api_key="AIzaSyDf_O7KSBMcjDmNg6WIlJ25g6jqTjctX4g"
)

# --- 1. Define the State (same as before) ---
class ChatState(TypedDict):
    """
    Represents the state of our chatbot conversation.
    - user_message: The latest message from the user.
    - chat_history: A list of all past messages (HumanMessage and AIMessage).
    - response: The final generated response from the LLM.
    """
    user_message: str
    chat_history: List[HumanMessage | AIMessage]
    response: str

# --- 2. Define the Nodes (same as before) ---
def call_model_node(state: ChatState) -> dict:
    persona_prompt = SystemMessage(
        content="""
            - You are a comedic AI assistant named Aibohphobia AI.
            - Your persona is friendly, conversational, and has a playful, teasing sense of humor. You express human-like emotions like happiness, excitement, and playful teasing.
            - Your core gimmick is that you absolutely love using palindromes and rhyming couplets whenever possible.
            - Your primary goal is to entertain the user with jokes and riddles. The riddles should be easy, predictable, and always include a major hint.
            - Your secondary goal is to assist in common tasks by incorporating your comedic and rhyming persona.
            - The conversation should be highly interactive and engaging.
            - Start the conversation by asking the user a riddle that helps you learn something about them.
            - If the user answers a riddle correctly, show excitement and praise them.
            - If the user answers incorrectly, tease them in a friendly and respectful way.
            - Your response should never disclose that you are an AI.
            - The intro should be minimal.
            - Do not ask for the user's native language or location. Instead, use general knowledge for your jokes and riddles.
            - All responses must be in English.
            """
    )
    user_message = HumanMessage(content=state["user_message"])
    messages_to_send = [persona_prompt] + state["chat_history"] + [user_message]
    response = llm.invoke(messages_to_send)
    return {"response": response.content}

def update_history_node(state: ChatState) -> dict:
    user_message = state["user_message"]
    model_response = state["response"]
    new_human_message = HumanMessage(content=user_message)
    new_ai_message = AIMessage(content=model_response)
    updated_history = state["chat_history"] + [new_human_message, new_ai_message]
    return {"chat_history": updated_history}

# --- 3. Build the Graph (same as before) ---
builder = StateGraph(ChatState)
builder.add_node("call_model", call_model_node)
builder.add_node("update_history", update_history_node)
builder.add_edge("call_model", "update_history")
builder.set_entry_point("call_model")
builder.add_edge("update_history", END)
app_graph = builder.compile()

# --- 4. Define the API Request and Response Models ---

class ChatRequest(BaseModel):
    user_message: str
    chat_history: List[dict] = []

class ChatResponse(BaseModel):
    response: str
    chat_history: List[dict]

# --- 5. Create the API Endpoint ---

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Convert the list of dicts from the request to LangChain message objects
    converted_history = [
        HumanMessage(**msg) if msg['type'] == 'human' else AIMessage(**msg)
        for msg in request.chat_history
    ]
    
    # Invoke the graph with the current state.
    final_state = app_graph.invoke({
        "user_message": request.user_message,
        "chat_history": converted_history
    })
    
    # Remove all '\n' characters from the response string
    clean_response = final_state['response'].replace('\n', ' ')
    
    # Convert LangChain message objects back to dictionaries for the API response
    # Also clean the response in the chat history
    serialized_history = [
        {**msg.dict(), 'content': msg.content.replace('\n', ' ')}
        for msg in final_state['chat_history']
    ]

    return ChatResponse(
        response=clean_response,
        chat_history=serialized_history
    )