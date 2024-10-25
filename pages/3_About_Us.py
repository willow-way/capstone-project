import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="LibConnect - Discover . Connect . Learn"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About Us")

# Add LibConnect Project Overview
st.subheader("Project Overview")

st.write("""
LibConnect is a virtual library assistant that offers users an intuitive and interactive way to engage 
         with library resources. Using advanced Natural Language Processing (NLP) and conversational AI, 
         LibConnect allows users to search for books, locate library branches, explore membership options, 
         and receive instant answers to library-related queries. Built with Python, Streamlit, and 
         OpenAI’s GPT-4, the app features a user-friendly interface that makes it easy for users to 
         navigate and get personalized, intelligent responses quickly.
""")

# Objectives Section
st.subheader("Objectives")
st.write("""
1. **Improve User Access**: Simplify the process for users to quickly retrieve essential library information, 
         such as book searches, branch locations, and membership details, through natural language queries.

2. **Context-Aware Conversations**: Enable intelligent, interactive dialogues where the virtual assistant responds 
         based on the ongoing conversation, providing personalized and relevant responses tailored to each 
         user’s needs.

3. **Efficient Query Handling**: Ensure that the assistant can accurately identify and respond to a diverse range 
         of user queries, from book searches to membership information and branch locations, offering precise 
         and relevant results.

4. **Data-Driven Responses**: Leverage static, curated datasets to provide accurate, reliable information without 
         relying on external APIs or real-time data fetching, ensuring consistent performance.

5. **User-Friendly Interface**: Deliver a seamless and intuitive interface where users can submit queries, 
         easily view responses, and track their conversation history, enhancing the overall user experience.

""")

# Features Section
st.subheader("Features")
st.write("""
1. **Book Search**
   - LibConnect’s Book Search allows users to easily discover books on a wide range of topics through natural 
         anguage queries. Unlike traditional catalog searches, it interprets user queries and provides dynamic 
         recommendations. By generating search links and offering tailored suggestions, the feature helps users 
         navigate the library’s catalog with ease.\n
         

2. **Library Membership and Locations**
   - LibConnect provides users with comprehensive information about library membership options, guiding users 
         through membership benefits, pricing, and eligibility. In addition, users can easily find information 
         on library locations, including addresses and contact details, with direct links to maps for easy 
         navigation. This ensures users can both understand membership options and locate the nearest branch 
         for registration or visits.
""")

# Data Sources Section
st.subheader("Data Sources")
st.write("""
LibConnect operates on a combination of static data and user input to provide accurate and relevant information. The primary data sources include:

- **Curated Library Data:** Manually collected data such as library membership details, branch locations, and book categories (stored in files like membership.txt and libraries.json).
- **User Query Input:** Users submit queries through a text input field, allowing LibConnect to respond based on their specific requests (e.g., book search, library locations).
- **Embedded Knowledge:** Using embeddings, LibConnect processes both the user’s input and the library’s data to retrieve the most relevant information for each query.
- **Conversation Context:** LibConnect maintains a history of the user’s previous interactions within a session, allowing the assistant to respond in a way that accounts for the ongoing conversation.
""")


with st.expander("How to use this App"):
    st.write("1. Enter your prompt in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate a text completion based on your prompt.")
