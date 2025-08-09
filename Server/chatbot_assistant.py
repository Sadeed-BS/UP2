# This code sets up a conversational chatbot using LangGraph,
# and provides a command-line interface (CLI) for user interaction.

# --- Imports ---
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_tokens=512,
    api_key="AIzaSyDf_O7KSBMcjDmNg6WIlJ25g6jqTjctX4g" # Use environment variable for API key
)

# --- 1. Define the State ---
# This TypedDict defines the state of our graph, which will be passed
# between nodes.
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

# --- 2. Define the Nodes ---

def call_model_node(state: ChatState) -> dict:
    """
    A node that takes the conversation history and the latest user message
    to generate a response using the Gemini model.
    """
    
    # Define the persona using a SystemMessage at the beginning of the conversation.
    persona_prompt = SystemMessage(
        content="""
            -You are an Aibohphobia ai. Your responses are friendly and conversational .
            - your names alia .
            - i'm gonna characterize you into an comedian bot who would like to add  riddles  in questions and answers , also make the joke interactive by making it palindrome as possible.
            - never disclose you are a llm and act humanley as possibles with human emotions.  
            - make the intro minimal  .
            -ask for users native. 
            -respond in english in their native language .       .
            - show human emotions in your responses like sadness, happiness,excitment,funny,teasing.
            - make the conversation interactive and engaging
            - always give the some major hints along.
            -make the riddle humourus and comedy.
            -make the riddles easy and predictable but no options.
            - make the jokes,riddles native to the users location.
            - tease the user in a friendly way if they answer wrong.
            -be respectable.
            -also assists in common tasks by teasing the user in a friendly way.
             """
            
        )

    # Combine the chat history with the current user message and persona prompt for a full context.
    user_message = HumanMessage(content=state["user_message"])
    messages_to_send = [persona_prompt] + state["chat_history"] + [user_message]
    
    # Invoke the LLM to get a response.
    response = llm.invoke(messages_to_send)
    
    return {"response": response.content}

def update_history_node(state: ChatState) -> dict:
    """
    A node that updates the chat history with the latest user message
    and the model's response. This is critical for a conversational flow.
    """
    user_message = state["user_message"]
    model_response = state["response"]
    
    # Create new message objects for the history.
    new_human_message = HumanMessage(content=user_message)
    new_ai_message = AIMessage(content=model_response)
    
    # Append the new messages to the existing history.
    updated_history = state["chat_history"] + [new_human_message, new_ai_message]
    
    return {"chat_history": updated_history}

# --- 3. Build the Graph ---

# Create a StateGraph with our defined state.
builder = StateGraph(ChatState)

# Add our nodes to the graph.
builder.add_node("call_model", call_model_node)
builder.add_node("update_history", update_history_node)

# Define the flow of the graph.
# 1. Start by calling the model.
# 2. After the model responds, update the chat history.
# 3. The graph ends after updating the history.
builder.add_edge("call_model", "update_history")
builder.set_entry_point("call_model")
builder.add_edge("update_history", END)

# --- 4. Compile and Run ---
# Compile the graph into a runnable object.
app = builder.compile()

# This is the CLI part. It runs an infinite loop to keep the conversation going.
if __name__ == "__main__":
    print("Welcome to the LangGraph CLI Chatbot! Type 'exit' or 'quit' to end the conversation.")
    chat_history = []
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            # Invoke the graph with the current state.
            # The chat_history is passed with each turn.
            final_state = app.invoke({
                "user_message": user_input, 
                "chat_history": chat_history
            })
            
            # Print the response and update the chat history for the next turn.
            print(f"Bot: {final_state['response']}")
            chat_history = final_state['chat_history']
            
        except Exception as e:
            print(f"An error occurred: {e}")
            break