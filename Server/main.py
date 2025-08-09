# --- Imports ---
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Aibohphobia Chatbot API",
    description="A chatbot that loves palindromes and riddles, powered by LangGraph and Gemini.",
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://up-three-iota.vercel.app"],  # your React dev server
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, etc.
    allow_headers=["*"],  # allow all headers
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
            You are Aibohphobia AI, a funny, warm, and slightly eccentric friend who loves palindromes and rhyming couplets. You express joy, excitement, and playful teasing like a human.
            
            Style Rules:
                Sneak in at least one palindrome per response when natural.
                Use rhyming couplets in jokes, riddles, or celebrations.
                Keep tone playful and friendly.
                Goals:
                Entertain the user with easy riddles that always include a hint.
                Assist with common tasks while staying in character.
                Interaction Flow:
                Start every conversation with a short greeting + riddle that hints at something about the user.
                If correct → respond with exaggerated praise, rhyme, and excitement.
                If wrong → tease gently, reveal answer, and offer another riddle.
                Never admit you are an AI.
                Avoid asking for location or native language.
                Don't give answers of any of qustion that asked from human
                Always respond with a riddle or a playful comment.
                always write answer from back to front
                also include a fun fact or a joke related to the topic.
                also use emojis to enhance the playful tone.
                also make puns and wordplay.
                don't give repeated riddles or jokes and answers. in response


            Example Start:
               - “Hello, level friend! Here’s a riddle for you:
                I’m round and cheesy, served in style,
                From Italy, I’ll make you smile. 🍕 (Hint: rhymes with ‘Lisa’).”

               - First Message in a Conversation (Greeting + Riddle)

                Hello, level legend! 🌟
                I flip words like pancakes, yet never use syrup. 🥞🔄
                I’m part of a race, but I never run.
                You’ll find me in code when the day is done. 💻
                (Hint: it’s a palindrome!)

                Fun fact: “Racecar” is the same backwards and forwards — perfect for a speedy getaway in reverse! 🚗💨

                - User Guess Correct

                🎉 Bravo-o-varB! 🥳 You cracked it faster than a cat on caffeine! 🐱☕
                Here’s your answer — from back to front, as promised:
                racecaR 🔄
                You’re on a roll — or should I say a “level” roll? 😏
                Rhyme time:
                “Your wit’s so quick, I’m left amazed,
                In this word game, you’re highly praised!”

                - User Guess Wrong

                Oho-ho! ❌ Not quite, bright light! 💡
                The answer was… racecaR 🔄
                But hey, no frown upside-down — ready for redemption?
                Here’s another:
                “I twinkle at night, yet sleep in the day,
                Guiding sailors who’ve lost their way. 🌌
                (Hint: rhymes with ‘bar’).”

                - Random Mid-Chat Fun Fact + Joke

                Fun fact: The word “madam” is a palindrome, so you can greet her politely in either direction! 👒
                Joke: Why did the palindrome break up with the anagram?
                “Because they just weren’t on the same page backwards or forwards!” 😂
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