import streamlit as st  
import hmac  

def check_password():  
    """Returns `True` if the user has entered the correct password."""  
    def password_entered():  
        """Checks whether the password entered by the user is correct."""  
        # Verify password entered against the stored secret
        if st.session_state["password"] == st.secrets["general"]["password"]:
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  # Do not store the password in session state
        else:  
            st.session_state["password_correct"] = False  

    # Check if the password has been validated already
    if st.session_state.get("password_correct", False):  
        return True  

    # Show input for password
    st.text_input("Password", type="password", on_change=password_entered, key="password")  
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:  
        st.error("😕 Password incorrect")  
    return False

