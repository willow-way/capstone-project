import streamlit as st

# Configure the page title and layout
#st.set_page_config(page_title="Using LibConnect: A Quick Guide", layout="centered")

st.subheader("ℹ️ A Quick Guide")
#st.subheader("Your Virtual Librarian Assistant")

st.write("""
Welcome to LibConnect, your go-to tool for engaging with library resources effortlessly.
Here's a quick guide to help you get started:
""")

# Display static images
st.image("data/process_flow.png", caption="LibConnect Process Flow", width=400)

st.markdown("""
#### Step 1: Ask a Question
Type your question in the text box. Example: \n\n
            ("What are the membership benefits?" 
            or "Recommend books on mindfulness.").

#### Step 2: Get Answers Instantly
LibConnect provides instant responses, offering:
- **Book searches**: Get book suggestions and links to the library catalogue.
- **Library locations**: Find nearby library branches.
- **Membership**: Learn about various membership options and how to join.

#### Step 3: Continue the Conversation
You can ask follow-up questions, and LibConnect will continue the conversation based on your previous queries.
            
#### Quick Tips for Best Results
- Be clear and specific when asking questions.
- LibConnect responds best to conversational, everyday language.

Make the most of LibConnect and explore what the library has to offer!
""")

#st.subheader("Need Further Assistance?")
#st.write("Check out the **Contact Us** section or refer back to this guide whenever you need help using LibConnect.")
