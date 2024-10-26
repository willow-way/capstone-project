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
LibConnect leverages advanced **Natural Language Processing (NLP)** and **Large Language Models (LLM)**
          to provide users with an intuitive and intelligent interface for engaging with 
         library resources. This page outlines the methodology, data flow, and technical 
         details behind LibConnect’s functionality, emphasising how NLP and LLM capabilities 
         power dynamic query handling, prompt chaining, and multi-turn conversations.
""")

st.markdown("""
    #### Overall Methodology
    LibConnect uses Python, Streamlit, and OpenAI’s GPT-4 for its LLM-based 
    processing. Each use case involves specific data sources and processing logic. 
    Here's a breakdown of how NLP and LLM capabilities are applied in each use case:
            """)

st.image("data/methodology-chart.png", caption="Overall Methodology", width=500)

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

**Note**: NLP plays a crucial role in understanding and parsing user inputs, enabling the system to break down 
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

Each of the core use cases—Book Search, Library Location Search, and Membership Query involves 
            distinct processing logic and data sources, leveraging NLP and LLM capabilities as follows:
            """)

#Create tabs for easier nagivation
tab1, tab2, tab3 = st.tabs(["**Book Search**", "**Library Location Search**", "**Membership Query**"])

         
#Content for Book Search Tab
with tab1:
    st.markdown("""
    In the book search use case, users can ask questions about available books on specific topics, 
    and LibConnect returns relevant book recommendations and links to the library catalogue.     
        
    """)
    st.image("data/flowchart_booksearch.png", caption="Flowchart for Book Search", width=250)

#Content for Location Search Tab
with tab2:
        st.markdown("""
        Users can also request information about library branch locations. The system provides details 
                    such as the address and, optionally, a Google Maps link for directions.   
        """)

        st.image("data/flowchart_locationsearch.png", caption="Flowchart for Location Search", width=250)

#Content for Membership Query Tab
with tab3:
        st.markdown("""
        This use case allows users to inquire about membership options, fees, and benefits. 
        """)

        st.image("data/flowchart_membershipquery.png", caption="Flowchart for Memerbship Query", width=250)


st.markdown("""
    #### LLM Capabilities
LibConnect employs prompt engineering techniques to enable intelligent interactions. Here’s how the LLM capabilities are applied:

**Prompt Chaining**: For complex, multi-step queries, the LLM uses the output from one query as input for the next. This allows for sequential processing of requests, such as answering a question about membership and then recommending books based on the user's membership status.

**Context-Aware Conversations**: LibConnect maintains the context of previous user interactions. This enables multi-turn conversations, where the assistant builds on previous responses to provide more personalized and relevant information.

**Dynamic Query Handling**: The LLM is responsible for identifying the user’s intent (book search, location inquiry, membership) and generating accurate responses tailored to the query type.

            """)

