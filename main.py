import streamlit as st
import os
from openai import AzureOpenAI
from PIL import Image
import time

# Environment variables for Azure OpenAI
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Adding a custom title and logo
st.set_page_config(page_title="Nurse Assistant", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# Load and display the logo
# logo = Image.open('nurse.231x256.png')
logo = Image.open('transparent-nurse-icon-healthcare-and-medical-icon-medicine-ic-5fb5e6d93162a6.0809276416057566332023.png')
col1, col2 = st.columns([1, 4])
with col2:
    st.title("Nurse Assistant Chatbot")


# Set up color scheme and modern UI elements
st.markdown(
     """
    <style>
        div[data-testid="stImage"] {margin: 0 auto;}
        button[data-testid="StyledFullScreenButton"] {
        display: none;
        }
        div[data-testid="stMarkdownContainer"] { color:white;}

        body {
            background-color: black;
        }
        .stApp {
            font-family: "Arial", sans-serif;
            background-color: black;
            border-radius: 15px;
            padding: 20px;
            max-width: 95%;
            margin: auto;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            transition-duration: 0.4s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .header {
            font-size: 32px;
            font-weight: bold;
            color: #1f77b4;
            margin-top: 10px;
            margin-bottom: 30px;
        }
        .stMarkdown {
            color: #333333;
        }
        .stTextInput>div>input {
            color: #333333;
            background-color: #ffffff;
        }
        @media screen and (max-width: 768px) {
            .header {
                font-size: 24px;
            }
            .stButton>button {
                font-size: 14px;
                padding: 8px 16px;
            }
        }
        @media screen and (max-width: 480px) {
            .header {
                font-size: 20px;
            }
            .stButton>button {
                font-size: 12px;
                padding: 6px 12px;
            }
            .stApp {
                padding: 10px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for additional information
with st.sidebar:
    st.image(logo, width=100)
    st.header("AI Nursing Assistant")
    st.markdown("**Select an option:**")
    option = st.radio("Select an option:", ["Admission Assistance", "Clinical History Query"], label_visibility='collapsed')

# Main chat UI
def main():
    if 'client' not in st.session_state:
        st.session_state.client = None

    if option == "Admission Assistance":
        if st.session_state.client is None:
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=subscription_key,
                api_version="2024-05-01-preview",
            )
            st.write("Client initialized")
        else:
            st.write("Client already initialized")

        # Code for Admission Assistance
        st.markdown("<div class='header'>Nursing Admission Assistant with Azure OpenAI</div>", unsafe_allow_html=True)
        st.text("Try it using some of the following queries:")
        st.table([
            'What are the steps for admission?',
            'What should I do if the patient has a fever?',
            'What are the admission procedures for a patient with a history of hypertension?',
            'Man 55 years chest pain'
        ])

        consulta = st.text_input("Ask me a question regarding patient admissions:", placeholder="Enter your question here")

        if consulta:
            with st.spinner('Generating response...'):
                time.sleep(0.5)  # Simulate delay
                # Make the query to OpenAI model
                completion = client.chat.completions.create(
                    model=deployment,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an AI Nursing assistant that helps nurses with admission. Based on nurse_protocol.pdf. ALWAYS your answers should be only max 10 steps to proceed. No additional text"
                        },
                        {
                            "role": "user",
                            "content": str(consulta)
                        }
                    ],
                    max_tokens=500,
                    temperature=0.4,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    stream=False,
                    extra_body={
                        "data_sources": [{
                            "type": "azure_search",
                            "parameters": {
                                "filter": None,
                                "endpoint": f"{search_endpoint}",
                                "index_name": "index-nurse-1",
                                "semantic_configuration": "vector-1726896547803-semantic-configuration",
                                "authentication": {
                                    "type": "api_key",
                                    "key": f"{search_key}"
                                },
                                "query_type": "simple",
                                "in_scope": True,
                                "role_information": "You are an AI Nursing assistant that helps nurses with admission. Based on nurse_protocol.pdf. ALWAYS your answers should be only max 10 steps to proceed. No additional text",
                                "strictness": 3,
                                "top_n_documents": 5
                            }
                        }]
                    }
                )
                message_content = completion.choices[0].message.content
                st.subheader("Assistant Response:")
                st.markdown(message_content)

    elif option == "Clinical History Query":
        if st.session_state.client is None:
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=subscription_key,
                api_version="2024-05-01-preview",
            )
            st.write("Client initialized")
        else:
            st.write("Client already initialized")

        # Code for Clinical History Query
        st.markdown("<div class='header'>Clinical History Query</div>", unsafe_allow_html=True)
        st.text("Try it using some of the following patient names:")
        st.table([
            'María Fernandez',
            'Jorge Ramírez',
            'Pablo Lopez',
            'Ana García'
        ])

        consulta_ch = st.text_input("Enter the name of a patient to find the history:", placeholder="Patient name")
        if consulta_ch:
            with st.spinner('Generating response...'):
                time.sleep(0.5)  # Simulate delay
                completion = client.chat.completions.create(
                    model=deployment,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an AI nursing assistant that helps people find information about clinic history in retrieved data. ALWAYS your answers should be only a resume of the clinic history. All translated to English. No additional text"
                        },
                        {
                            "role": "user",
                            "content": f"Necesito busques la historía clínica del paciente: {consulta_ch}"
                        }
                    ],
                    max_tokens=800,
                    temperature=0.5,
                    top_p=0.78,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    stream=False,
                    extra_body={
                        "data_sources": [{
                            "type": "azure_search",
                            "parameters": {
                                "filter": None,
                                "endpoint": f"{search_endpoint}",
                                "index_name": "great-nut-723ncdwd3g",
                                "semantic_configuration": "azureml-default",
                                "authentication": {
                                    "type": "api_key",
                                    "key": f"{search_key}"
                                },
                                "embedding_dependency": {
                                    "type": "endpoint",
                                    "endpoint": "https://openaiavisco.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-07-01-preview",
                                    "authentication": {
                                        "type": "api_key",
                                        "key": "70eccac0e4ed42409ac26781cfff474a"
                                    }
                                },
                                "query_type": "vector_simple_hybrid",
                                "in_scope": True,
                                "role_information": "You are an AI nursing assistant that helps people find information about clinic history in retrieved data. ALWAYS your answers should be only a resume of the clinic history. All translated to English. No additional text",
                                "strictness": 3,
                                "top_n_documents": 6
                            }
                        }]
                    }
                )
                message_content = completion.choices[0].message.content
                st.subheader("Assistant Response:")
                st.markdown(message_content)

    if st.button("Clear Chat"):
        st.session_state['responses'] = []

# Placeholder function for chatbot response
# This function is retained for testing purposes

def get_response(user_input):
    return f"This is a response to '{user_input}'"

if __name__ == '__main__':
    main()
