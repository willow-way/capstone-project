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
LibConnect uses advanced Natural Language Processing and Machine Learning to provide
          intelligent library assistance. It understands user queries, offers relevant 
         recommendations, and provides instant answers by leveraging its knowledge of library data. 
         LibConnect's methodology enables interactive conversations and continuous learning to 
         adapt to users' needs.
""")

# Add images of the methodology
st.subheader("Methodology")

# Display static images
#st.image("data/image1.jpg", caption="Methodology Image 1", use_column_width=True)
#st.image("data/image2.jpg", caption="Methodology Image 2", use_column_width=True)
# Add more images as needed
