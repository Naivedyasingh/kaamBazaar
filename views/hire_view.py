import streamlit as st

def render_hire_view(user):
    st.title(f"Welcome, {user['name']} (Employer) 👷‍♂️")
    st.write("📌 This is the Hire Dashboard.")
    
    # Placeholder for future features
    st.success("You can post jobs, view job seekers, and send messages.")
