import re
import streamlit as st
from helper_functions.llm import get_completion
from logics.library_search import generate_search_url

# Configure the page
st.set_page_config(layout="centered", page_title="Book Recommender")

st.title("✨Book Recommender")

# Genre selection
st.write("Select a genre or topic to receive book recommendations.")
genre_options = ["Biography", "Fiction", "Non-Fiction", "Science", "History", "Philosophy", "Mystery", "Fantasy"]
user_genre = st.selectbox("Select Genre:", genre_options)

# Display recommendations on button click
if st.button("Get Recommendations"):
    # Refine the prompt to avoid any introductory statements
    prompt = (
        "You are a helpful virtual librarian assistant. Recommend 2-3 popular books in the genre selected without any introductory statement or heading."
        " List each recommendation in the following format:\n"
        "<Title> - <Author>: <Description>\n\n"
        f"User's Selected Genre: {user_genre}\n"
    )

    # Call the LLM function to get recommendations
    response = get_completion(prompt)
    
    # Parse the response and display each book with its URL
    st.write("### Recommended Books:")
    books = response.strip().split("\n")  # Split by line
    
    for book in books:
        if book.strip():  # Ensure non-empty book detail
            try:
                # Extract title-author and description
                title_author, description = book.split(":", 1)
                
                # Clean up title_author by removing numbering, extra spaces, and asterisks
                title_author = re.sub(r"^\d+\.\s*|\*\*", "", title_author).strip()  # Remove numbering and bolding
                title_only = title_author.split(" - ")[0].strip()  # Extract <Title> only for URL
                
                # Generate the search URL for each title
                book_url = generate_search_url(title_only)
                
                # Display each book with its URL and other details
                st.write(f"- **{title_author}**: {description.strip()} [View Book on NLB Catalogue]({book_url})")
            except ValueError:
                st.write(f"- {book.strip()} (URL not available)")

    # Optionally add to session state for conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    st.session_state.conversation.append(f"User selected genre: {user_genre}")
    st.session_state.conversation.append(f"Assistant: {response}")
