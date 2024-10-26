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
LibConnect is a virtual library assistant developed to offer users an intuitive, conversational 
         interface for exploring library resources. By utilizing Large Language Model (LLM), LibConnect allows users to easily search for books, find nearby 
         library branches, explore membership options, and obtain quick answers to library-related 
         queries. Built with Python and Streamlit, LibConnect combines the power of conversational 
         AI with a user-friendly design, delivering a smooth, personalized experience that enhances 
         how users connect with their library.
""")

# Objectives Section
st.subheader("Objectives")
st.write("""
LibConnect aims to simplify access to library resources by enabling intuitive, natural language 
         interactions. It empowers users with an accessible platform that understands complex queries, 
         maintains context across conversations, and provides reliable, data-driven responses. 
         The main objectives include:        

1. **Enhanced User Access**: Simplify the process for users to quickly retrieve essential library 
         information, such as book searches, branch locations, and membership details in a single 
         user-friendly interface.

2. **Contextual Inteactions**: The assistant is designed to support context-aware conversations, 
         creating personalized and relevant responses that improve with each interaction.

3. **Efficient Query Handling**: Ensure that the assistant can accurately identify and respond to a 
         diverse range of user queries, from book searches to membership information and branch locations, offering precise 
         and relevant results.

4. **User-Friendly Interface**: Deliver a seamless and intuitive interface where users can submit queries,
         easily view responses, and track their conversation history, enhancing the overall user 
         experience.

""")

# Features Section
st.subheader("Features")
st.write("""
1. **Book Search**\n
With LibConnect’s Book Search feature, users can effortlessly discover books on a range of topics 
by simply typing in their queries. Unlike traditional catalog searches, this feature interprets 
user requests and provides customized book recommendations and search links, making it easy to 
         navigate the library’s extensive catalogue.

2. **Library Location Finder**\n
Users can find nearby library branches with ease. This feature offers detailed information on each 
location, including addresses, operating hours, and direct links to Google Maps, allowing 
users to plan visits conveniently.

3. **Library Membership Information**\n
LibConnect offers comprehensive guidance on library membership options, covering aspects such as 
         membership benefits, eligibility, and pricing. This allows users to make informed decisions 
         about joining the library and taking full advantage of available resources.

4. **Book Recommender** \n
Book Recommender allows users to receive personalised book recommendations 
         based on their chosen genre, like Fiction or Biography. The feature 
         generates tailored suggestions and provides direct links to the 
         library catalogue, simplifying book discovery and enhancing user 
         engagement with library resources.
         
5. **Instant Answers**\n
LibConnect responds instantly to various library-related queries, from general questions to specific 
         needs like locating resources. By handling a wide array of question types, the assistant 
         serves as a versatile, go-to source for library information.

6. **Conversational History**\n
The assistant keeps a session-based conversation history, allowing users to ask follow-up questions 
         and continue the dialogue without needing to rephrase or re-explain their queries. This feature 
         enhances the experience by enabling multi-turn conversations.
""")

# Data Sources Section
st.subheader("Data Sources")
st.write("""
LibConnect operates on a combination of static data and user input to provide accurate and relevant information. The primary data sources include:

- **Curated Library Data:** Manually collected data such as library membership details, branch locations, 
         and book categories (stored in files like membership.txt and libraries.json).\n
- **User Input:** The platform uses user-entered queries as the primary driver for interactions, 
         analyzing the content to determine the most relevant responses.\n
- **Embedded Knowledge:** Using embeddings, LibConnect processes both the user’s input and the library’s 
         data to retrieve the most relevant information for each query.\n
- **Conversation Context:** LibConnect maintains a history of the user’s previous interactions within 
         a session, allowing the assistant to respond in a way that accounts for the ongoing conversation.
""")

