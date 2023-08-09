import streamlit as st
import openai
import time

st.title('Chat With TomBot from GPT 🚀')
st.write('## **Try something simple with my new GPT!** ☁')
st.write('### **Try asking any fucking question...!** 😛')
st.divider()

# Set OpenAi API key with streamlit secrets
openai.api_key = st.secrets['OPENAI_API_KEY']

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Create Chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat from history when app is rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# Accept user input for chat
if prompt := st.chat_input("What's up?"):
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # Display user message in chat container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Display assistant response in chat container
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        # Generate stream of responses from the model
        for response in openai.ChatCompletion.create(
                model=st.session_state['openai_model'],
                messages=[
                    {'role': m['role'], 'content': m['content']}
                    for m in st.session_state.messages
                ],
                stream=True,
        ):
            full_response += response.choices[0].delta.get('content', '')
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({'role': 'assistant', 'content': full_response})

st.write("**Disclaimer: Please we do not use, save or keep anyone's data**")