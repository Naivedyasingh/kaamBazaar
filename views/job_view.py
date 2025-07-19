import streamlit as st

def render_job_view(user):
    st.title(f"Welcome, {user['name']} (Job Seeker) 👨‍🔧")
    st.write("📌 This is the Job Seeker Dashboard.")
    
    # Placeholder for future features
    st.success("You can browse job posts, express interest, and message employers.")
