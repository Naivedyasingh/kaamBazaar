# login.py
import streamlit as st
from utils import authenticate_user, read_json

def login_user(role):
    st.title(f"🔑 {'Job Seeker' if role == 'job' else 'Employer'} Login")
    
    # # Add welcome message with role-specific info
    # if role == "job":
    #     st.info("🔍 **Welcome back, Job Seeker!** Login to continue your job search journey.")
    #     st.write("After login, you can:")
    #     st.write("• Browse the latest job opportunities")
    #     st.write("• Apply to positions that match your skills")
    #     st.write("• Track your application status")
    #     st.write("• Update your profile and preferences")
    # else:
    #     st.info("🏢 **Welcome back, Employer!** Login to manage your hiring process.")
    #     st.write("After login, you can:")
    #     st.write("• Post new job openings")
    #     st.write("• Review and manage applications")
    #     st.write("• Contact potential candidates")
    #     st.write("• Manage your company profile")
    
    st.markdown("---")
    st.subheader("🔐 Login Credentials")
    
    # Login form in columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        login_method = st.radio("Login with:", ["Full Name", "Phone Number"], key=f"login_method_{role}")
    
    with col2:
        show_password = st.checkbox("Show Password", key=f"show_password_{role}")
    
    # Input fields based on selected method
    if login_method == "Full Name":
        identifier = st.text_input("📛 Full Name", 
                                 placeholder="Enter your full name as registered", 
                                 key=f"login_name_{role}")
    else:
        identifier = st.text_input("📱 Phone Number", 
                                 placeholder="Enter your 10-digit phone number", 
                                 key=f"login_phone_{role}")
    
    password = st.text_input("🔒 Password", 
                           type="text" if show_password else "password",
                           placeholder="Enter your password", 
                           key=f"login_password_{role}")
    
    # Remember me option
    remember_me = st.checkbox("🔄 Remember me", key=f"remember_{role}")
    
    # Login button with enhanced styling
    if st.button("🚀 Login to Account", key=f"login_btn_{role}", 
                 type="primary", use_container_width=True):
        
        if not identifier or not password:
            st.error("❌ Please fill in all fields to continue.")
            return
        
        # Authenticate based on login method
        if login_method == "Full Name":
            user = authenticate_user(identifier.strip(), password.strip(), role)
        else:
            # Validate phone format first
            if not identifier.isdigit() or len(identifier) != 10:
                st.error("❌ Please enter a valid 10-digit phone number.")
                return
            user = authenticate_user(identifier.strip(), password.strip(), role)
        
        if user:
            st.success(f"🎉 Welcome back, {user['name']}!")
            st.balloons()
            
            # Store user info in session state
            st.session_state.current_user = user
            st.session_state.remember_login = remember_me
            st.session_state.page = "dashboard"
            
            # Show quick stats about their profile
            if role == "job":
                st.info(f"✨ Profile Summary: {user.get('experience', 'Experience not specified')} | Skills: {', '.join(user.get('work_type', ['Not specified']))}")
            else:
                st.info(f"🏢 Company: {user.get('company_name', 'Company name not specified')} | Type: {user.get('company_type', 'Not specified')}")
            
            # Auto redirect after 2 seconds
            with st.spinner("Redirecting to dashboard..."):
                import time
                time.sleep(1.5)
                st.rerun()
        else:
            st.error("❌ Invalid credentials. Please check your information and try again.")
            
            # Show helpful hints
            with st.expander("💡 Having trouble logging in?"):
                st.write("**Common issues:**")
                st.write("• Make sure you're using the correct login method (Name vs Phone)")
                st.write("• Check that you selected the right role (Job Seeker vs Employer)")
                st.write("• Ensure your password is entered correctly")
                st.write("• If you used phone to register, use phone to login")
                
                # Show registration statistics for encouragement
                users = read_json("data/users.json")
                job_seekers = len([u for u in users if u.get('role') == 'job'])
                employers = len([u for u in users if u.get('role') == 'hire'])
                
                if job_seekers > 0 or employers > 0:
                    st.write(f"**Platform Stats:** {job_seekers} Job Seekers • {employers} Employers registered")
    
    # Additional options
    st.markdown("---")
    st.subheader("🔗 Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Don't have an account? Register", key=f"go_to_register_{role}", 
                     use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
    
    with col2:
        if st.button("🔑 Forgot Password?", key=f"forgot_password_{role}", 
                     use_container_width=True):
            st.info("🚧 Password recovery feature coming soon! Please contact support if needed.")
    
    # Show recent activity stats
    users = read_json("data/users.json")
    if users:
        recent_registrations = len([u for u in users if u.get('role') == role])
        if recent_registrations > 0:
            st.success(f"🎯 {recent_registrations} {role.replace('job', 'Job Seeker').replace('hire', 'Employer')}s have joined our platform!")
    
    # Back button with better styling
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Login/Register Choice", key=f"back_to_auth_{role}", 
                     use_container_width=True):
            st.session_state.page = "auth_choice"
            st.rerun()