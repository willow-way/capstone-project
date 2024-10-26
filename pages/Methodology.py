# Import Streamlit library
import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="LibConnect - Discover . Connect . Learn"
)
# endregion <--------- Streamlit App Configuration --------->

# **App Title**: Set the main title of the "Methodology" page
st.title("Methodology")

# Add the LibConnect description
st.write("""
LibConnect leverages Large Language Model (LLM) to provide users with an intuitive and 
         intelligent interface for engaging with library resources. This page outlines the methodology, data flow, and technical 
         details behind LibConnect’s functionality, emphasising how LLM capabilities power 
         dynamic query handling, prompt chaining, and multi-turn conversations.
""")

# **Methodology Section**: Provide an overview of the methodology behind LibConnect
st.markdown("""
    #### Overall Methodology
    LibConnect uses Python, Streamlit, and OpenAI’s GPT-4 for its LLM-based 
    processing. Each use case involves specific data sources and processing logic. 
    Here's a breakdown of how LLM capabilities are applied in each use case:
            """)

st.image("data/methodology-chart.png", caption="Overall Methodology for LibConnect", use_column_width=True)
st.image("data/multistep_context.png", caption="Multi-Step Query Handling and Contextual Response Generation)", use_column_width=True)
st.image("data/flowchart_bookrecommender.png", caption="Overall Methodology for Book Recommender", use_column_width=True)



st.write("""
#### Data Flow Overview
The data flow in LibConnect revolves around three key components:

**1. User Input**: The user submits a question or query through the app.\n
**2. Intent Detection via Keyword Matching**: The system uses a keyword-based approach to analyze 
         user queries and identify their intent, such as book search, library location inquiries, 
         or membership-related questions. By scanning for specific terms associated with each intent, 
         the system efficiently categorizes queries without relying on complex language models.\n
**3. LLM-Driven Response Generation**: Based on the detected query intent, the LLM generates a 
         context-aware response, retrieving static data, and combining it with contextual 
         information to deliver accurate results.

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
            distinct processing logic and data sources, leveraging LLM capabilities as follows:
            """)

#Create tabs for easier nagivation
tab1, tab2, tab3, tab4 = st.tabs(["**Book Search**", "**Library Location Search**", "**Membership Query**", "**Book Recommender**"])

         
#Content for Book Search Tab
with tab1:
    st.markdown("""
    In the book search use case, users can ask questions about available books on specific topics, 
    and LibConnect returns relevant book recommendations and links to the library catalogue.     
        
    """)
    st.image("data/flowchart_booksearch.png", caption="Flowchart for Book Search", use_column_width=True)

#Content for Location Search Tab
with tab2:
        st.markdown("""
        Users can also request information about library branch locations. The system provides details 
                    such as the address and, optionally, a Google Maps link for directions.   
        """)

        st.image("data/flowchart_locationsearch.png", caption="Flowchart for Location Search", use_column_width=True)

#Content for Membership Query Tab
with tab3:
        st.markdown("""
        This use case allows users to inquire about membership options, fees, and benefits. 
        """)

        st.image("data/flowchart_membershipquery.png", caption="Flowchart for Memerbship Query", use_column_width=True)

with tab4:
        st.markdown("""
        This use case allows users to receive personalised book recommendations based on their chosen genre, like Fiction or Biography. 
        """)
        st.image("data/flowchart_bookrecommender.png", caption="Flowchart for Book Recommender", use_column_width=True)

st.markdown("""
    #### LLM Capabilities
LibConnect employs prompt engineering techniques to enable intelligent interactions. Here’s how the LLM capabilities are applied:

**Prompt Chaining**: For complex, multi-step queries, the LLM uses the output from one query as input for the next. This allows for sequential processing of requests, such as answering a question about membership and then recommending books based on the user's membership status.

**Context-Aware Conversations**: LibConnect maintains the context of previous user interactions. This enables multi-turn conversations, where the assistant builds on previous responses to provide more personalized and relevant information.

**Dynamic Query Handling**: The LLM is responsible for identifying the user’s intent (book search, location inquiry, membership) and generating accurate responses tailored to the query type.

            """)

