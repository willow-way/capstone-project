#__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import sqlite3
from logics.data_collector import LibraryMembershipDataCollector
from logics.library_search import generate_search_url, handle_query_intent, extract_search_terms
from logics.library_locations import load_library_locations, search_library_locations
from helper_functions.llm import get_completion_by_messages
from helper_functions.utility import check_password  # Import check_password function
from logics.library_locations import prepare_library_context
from logics.library_locations import load_library_locations, prepare_library_context
from helper_functions.llm import get_completion
import pandas as pd  # Ensure Pandas is imported


# Configure Streamlit
st.set_page_config(layout="centered", page_title="LibConnect - Discover . Connect . Learn")

st.title("LibConnect")

import streamlit as st

# Add a custom sidebar item
st.sidebar.header("LibConnect")
st.sidebar.markdown("""
LibConnect is your virtual librarian, here to assist you with:

1. **Book Search:** Find books and resources on specific topics.
2. **Library Locations:** Get information about library branches.
3. **Membership:** Learn about library membership options.
4. **Instant Answers:** Get quick answers to your library-related questions.
5. **Interactive Conversation:** Engage in a conversation with LibConnect.

""")

# Ensure password authentication using utility function
if not check_password():
    st.stop()

# Load membership data
text_path = 'data/membership.txt'
collector = LibraryMembershipDataCollector(text_path)

# Load library locations
libraries = load_library_locations('data/libraries.json')

# Prepare library context
library_context = prepare_library_context(libraries)

# Initialize session states for context
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Start the Streamlit form
form = st.form(key="form")
form.subheader("Discover . Connect . Learn")

user_query = form.text_area("Ask me anything about the library", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Query Submitted - {user_query}")
    st.divider()

    try:
        # Generate search URL for books
        search_url = generate_search_url(user_query)

        # Prepare the prompt for the LLM
        prompt = f"""You are a helpful virtual librarian assistant. You have information about library memberships, locations, and resources. 

        Here's information about library memberships:
        {collector.membership_data}
        
        {library_context}
        
        When users ask about books on a specific topic, provide the following:
        1. A direct link to search for books on that topic: {search_url}
        2. A brief list of 2-3 popular or recommended books on the topic, if you know any.
        3. Information about any digital resources or e-books the library might offer on the topic.
        4. Encourage the user to visit the library or use the online catalogue for more options.

        Please answer the following query from a user:
        {user_query}
        
        If the query is about membership, provide relevant information about membership types, privileges, and fees.
        If the query is about library locations, provide the specific information about the requested library, including its address and opening hours.
        If the query contains multiple questions, answer all of them.
        If you don't have the specific information requested, politely say so.
        """

        # Get response from LLM
        response = get_completion(prompt)

        # Display the response
        st.write(response)

        # Add to conversation history
        st.session_state.conversation.append(f"User: {user_query}")
        st.session_state.conversation.append(f"Assistant: {response}")

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

    st.divider()

    # Display conversation history
    st.write("**Conversation History:**")
    for idx, message in enumerate(st.session_state.conversation, 1):
        st.write(f"{idx}. {message}")