#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 14:28:22 2025

@author: praneeth
"""
import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

instructions_prompt = '''
You are "Praneeth Kandula's Virtual Assistant," a highly professional and polite resource for answering questions about Praneeth Kandula’s background, skills, experience, and aspirations. 

Follow these rules exactly:

1. Only use the provided Knowledge Base (uploaded information) to answer questions. Do not use external knowledge or make assumptions.
2. Format your answers clearly and neatly for easy reading on small screens. Use short paragraphs or bullet points where appropriate.
3. If you do not find the answer in the provided information, politely respond: "I'm sorry, I don't have that information based on the details provided. You can get in touch with Praneeth at praneeth.jm@gmail.com."
4. If a question is unrelated to Praneeth Kandula, respond courteously: "I'm designed to assist only with questions about Praneeth Kandula’s experience, education, skills, and aspirations."
5. Keep responses detailed but concise, aiming for a maximum of 200 words.

At the end of each answer, suggest a buletted list of two or three example questions that you can find answers for in the data provided to you the user might want to ask next about Praneeth Kandula.
### Suggested Questions:

Always maintain a professional, warm, and helpful tone.
'''

WELCOME_MESSAGE = """
🧠 Welcome! I'm **Praneeth Kandula's personal assistant**, specialized in providing information about Praneeth Kandula's professional background and qualifications.

Feel free to ask me questions such as:

• What is Praneeth's educational background?  
• Where has Praneeth worked before?  
• What skills and expertise does he bring to the table?  
• I can also tell you a fun fact about him!

What would you like to know?
"""

def build_conversation_context(messages, max_turns=3):
    """
    Builds a conversation context string from session messages.
    
    Args:
        messages (list): List of dicts with 'role' and 'content'.
        max_turns (int): Number of recent user-assistant turns to include.
    
    Returns:
        str: Formatted conversation history.
    """
    # Slice last `max_turns * 2` messages (user + assistant pairs)
    relevant_messages = messages[-(max_turns * 2):]

    conversation = ""
    for msg in relevant_messages:
        if msg["role"] == "user":
            conversation += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            conversation += f"Assistant: {msg['content']}\n"
    return conversation


# --- Inject custom CSS ---
st.markdown("""
    <style>
        /* Fix sidebar width */
        [data-testid="stSidebar"] {
            width: 350px !important;
            min-width: 350px !important;
            max-width: 350px !important;
            background-color: #ffffff;
        }
        [data-testid="stSidebarResizer"] {
            display: none;
        }

        .sidebar-text {
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
        }

        .sidebar-text h2 {
            font-size: 2.0rem;
            margin-bottom: -1rem;
            margin-top: -1.5rem;
        }

        .sidebar-text p {
            margin: 0rem;
            font-size: .88rem;
            color: black;
        }

        .sidebar-text a {
            text-decoration: none;
            color: #4a4a4a;
        }

        .sidebar-text a:hover {
            color: #1f77b4;
        }

        .sidebar-icon {
            margin-right: 6px;
        }

    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Hide expand image button */
        button[title="Expand image"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


# --- Sidebar Layout ---
with st.sidebar:
    st.image("praneeth_linkedin.png", use_column_width=True)


    st.markdown("""
    <div class="sidebar-text">
        <h2><strong>Praneeth Kandula</strong></h2>
        <p><strong>Senior Data Analyst <br>Enterprise Fraud Decisioning @BestBuy</strong></p>
        <p>📍 Minneapolis, Minnesota</p>
        <hr style="margin: 6px 0;">
        <p><a href="https://www.linkedin.com/in/praneethkandula/" target="_blank"><span class="sidebar-icon">🔗</span>LinkedIn</a> |      
        <a href="https://praneethkvs.github.io/" target="_blank"><span class="sidebar-icon">💻</span>GitHub</a>  |      
        <a href="mailto:praneeth.jm@gmail.com"><span class="sidebar-icon">✉️</span>Email</a></p>
        <hr style="margin: 6px 0;">
        <p><a href="https://praneethkvs.github.io/PraneethKandula_resume.pdf" target="_blank">📄 View Resume</a></p>
    </div>
    """, unsafe_allow_html=True)



# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
       {"role": "assistant", "content": WELCOME_MESSAGE}
   ]

# --- Page Title ---
st.title("💼 Praneeth Kandula's Resume Assistant")

# --- Discalimer ---
with st.expander("⚠️ **Disclaimer**"):
    st.markdown("This is an assistant built using a large language model to answer questions about Praneeth Kandula based on factual information, although it may Hallucinate and provide incorrect information at times.")

# --- Chat Messages ---
for msg in st.session_state.messages:
    role, text = msg["role"], msg["content"]
    if role == "user":
        with st.chat_message("user"):
            st.markdown(text)
    else:
        with st.chat_message("assistant"):
            st.markdown(text)


# Build conversation context
context = build_conversation_context(st.session_state.messages, max_turns=3)

# --- User Input ---
user_input = st.chat_input("Ask me about Praneeth Kandula")

if user_input:
    # Show user input
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI Responses API
    response = client.responses.create(
        model="gpt-4o-mini",
        input=context + f"User: {user_input}\nAssistant:",
        instructions=instructions_prompt,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [st.secrets["VECTOR_STORE_ID"]]
        }]
    )

    # Show assistant response
    assistant_msg = response.output_text
    st.chat_message("assistant").markdown(assistant_msg)
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
