import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="LibConnect - Discover . Connect . Learn"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About us")

# Add the LibConnect description
st.write("""
"LibConnect: Your Gateway to Library Resources"

LibConnect is your platform for exploring and accessing library resources easily. Whether you’re searching for a book or looking for information on upcoming events, LibConnect helps you find what you need. With simple guidance and a user-friendly interface, LibConnect connects you to your library effortlessly.
""")


with st.expander("How to use this App"):
    st.write("1. Enter your prompt in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate a text completion based on your prompt.")
