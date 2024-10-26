import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="LibConnect - Discover . Connect . Learn"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")

# Add the LibConnect description
st.write("""
LibConnect leverages advanced Natural Language Processing (NLP) and Large Language Models (LLM)
          to provide users with an intuitive and intelligent interface for engaging with 
         library resources. This page outlines the methodology, data flow, and technical 
         details behind LibConnect’s functionality, emphasizing how NLP and LLM capabilities 
         power dynamic query handling, prompt chaining, and multi-turn conversations.
""")

# Add images of the methodology
#st.title("")
st.write("""
#### Data Flow Overview
The data flow in LibConnect revolves around three key components:

**1. User Input**: The user submits a question or query through the app.\n
**2. Natural Language Processing (NLP)**: The system uses NLP to analyze the query and detect 
         its intent (e.g., book search, library location, or membership inquiry).\n
**3. LLM-Driven Response Generation**: Based on the detected query intent, the LLM generates a 
         context-aware response, retrieving static data, and combining it with contextual 
         information to deliver accurate results.

NLP plays a crucial role in understanding and parsing user inputs, enabling the system to break down 
         complex queries and detect multiple intents within a single user prompt.

""")
st.image("data/dataflow_booksearch.png", caption="Data Flow for Single Query (Book Search)", use_column_width=True)

st.write("""
In addition to handling single-step queries, LibConnect also supports **Multi-Step Queries** (or **Prompt 
         Chaining**). This functionality allows the system to remember previous user interactions and 
         generate responses based on the ongoing context.
""")

st.image("data/dataflow_multichain.png", caption="Data Flow for Multi-Step Query", use_column_width=True)



st.markdown("""
#### Key Implementation Details
LibConnect uses Python, Streamlit, and OpenAI’s GPT-4 for its LLM-based 
processing. Each use case involves specific data sources and processing logic. 
Here's a breakdown of how NLP and LLM capabilities are applied in each use case:

##### 1. Book Seach Use Case
In the book search use case, users can ask questions about available books on specific topics, 
and LibConnect returns relevant book recommendations and links to the library catalog.     
    
""")
st.image("data/flowchart_booksearch.png", caption="Flowchart for Book Search Use Case", width=250)


# Display static images
st.image("data/methodology-chart.png", caption="Overall Methodology", width=500)
#st.image("data/image2.jpg", caption="Methodology Image 2", use_column_width=True)
# Add more images as needed
