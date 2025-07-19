# main.py
import streamlit as st
from auth.register import register_user
from auth.login import login_user
from utils import read_json

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

def landing_page():
    # Hero section with beautiful styling
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #1f77b4; font-size: 3rem; margin-bottom: 0.5rem;'>
            🏢 KaamBazaar 
        </h1>
        <h3 style='color: #666; font-weight: 300; margin-bottom: 2rem;'>
            Connecting Dreams with Opportunities
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics Section
    users = read_json("data/users.json")
    job_seekers = [u for u in users if u.get('role') == 'job']
    employers = [u for u in users if u.get('role') == 'hire']
    
    st.markdown("### 📊 Platform Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Job Seekers", len(job_seekers), delta="Active")
    with col2:
        st.metric("🏢 Employers", len(employers), delta="Hiring")
    with col3:
        # Calculate total connections/applications (placeholder)
        total_connections = len(job_seekers) * 2  # Estimated
        st.metric("🤝 Connections", total_connections, delta="+12%")
    with col4:
        success_rate = "85%" if len(users) > 5 else "Growing"
        st.metric("✅ Success Rate", success_rate, delta="High")
    
    # Before & After Impact Section
    st.markdown("---")
    st.markdown("### 🔄 **Our Impact on Urban Employment**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 😔 **Before JobConnect**
        - 📱 Job seekers struggled to find reliable work
        - 🏠 Employers had difficulty finding trusted help
        - ⏰ Time-consuming manual searching process
        - 💸 High agency fees and commissions
        - 🔍 Limited job visibility and opportunities
        - 📋 No proper verification system
        - 🤝 Lack of direct communication
        """)
        
    with col2:
        st.markdown("""
        #### 🌟 **After JobConnect**
        - 🎯 Easy access to verified job opportunities
        - 🔐 Secure platform with identity verification
        - 💻 Digital profiles showcase skills & experience
        - 💰 Fair salary expectations and transparency
        - 📲 Direct communication between parties
        - ⭐ Rating and review system for quality
        - 🚀 Quick job matching and applications
        """)
    
    # Job Categories Section
    st.markdown("---")
    st.markdown("### 💼 **Available Job Categories**")
    st.write("Find opportunities in various domestic and professional services:")
    
    job_categories = {
        "🧹 Cleaning Services": ["Maid", "Cleaner", "Deep Cleaning Specialist"],
        "👨‍🍳 Kitchen & Food": ["Cook", "Chef", "Kitchen Helper", "Catering Assistant"],
        "🚗 Transportation": ["Driver", "Delivery Person", "Chauffeur"],
        "👶 Childcare": ["Babysitter", "Nanny", "Child Caretaker"],
        "🌱 Home Maintenance": ["Gardener", "Plumber", "Electrician"],
        "🛡️ Security": ["Security Guard", "Watchman", "Home Security"]
    }
    
    cols = st.columns(3)
    for i, (category, jobs) in enumerate(job_categories.items()):
        with cols[i % 3]:
            with st.expander(category):
                for job in jobs:
                    # Show count of job seekers in this category
                    job_count = len([u for u in job_seekers if job.lower() in [skill.lower() for skill in u.get('work_type', [])]])
                    st.write(f"• {job} {f'({job_count} available)' if job_count > 0 else ''}")
    
    # Success Stories (if users exist)
    if len(users) > 0:
        st.markdown("---")
        st.markdown("### 🎉 **Platform Growth**")
        
        recent_job_seekers = len([u for u in job_seekers if u.get('city')])
        cities_represented = len(set([u.get('city', '').lower() for u in users if u.get('city')]))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"🌍 **{cities_represented if cities_represented > 0 else 1}+ Cities** covered across India")
        with col2:
           st.info(f"💼 **{len(set([skill for u in job_seekers for skill in u.get('work_type', [])]))} Skills** available on platform")
        with col3:
            avg_experience = "Entry to Expert" if job_seekers else "All Levels"
            st.info(f"📈 **{avg_experience}** experience levels")
    
    # Call to Action
    st.markdown("---")
    st.markdown("### 🚀 **Get Started Today!**")
    st.write("Join thousands of job seekers and employers who have found success through our platform.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 I want a Job", key="job_button", use_container_width=True, type="primary"):
            st.session_state.role = "job"
            go_to("auth_choice")
            
        st.markdown("""
        <div style='text-align: center; margin-top: 1rem; padding: 1rem; background-color: #a1f8fe; border-radius: 10px;'>
            <strong>Perfect for:</strong><br>
            🏠 Domestic workers<br>
            🔧 Skilled professionals<br>
            👨‍🎓 Students seeking part-time work
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🏢 I want to Hire", key="hire_button", use_container_width=True, type="secondary"):
            st.session_state.role = "hire"
            go_to("auth_choice")
            
        st.markdown("""
        <div style='text-align: center; margin-top: 1rem; padding: 1rem; background-color: #a1f8fe; border-radius: 10px;'>
            <strong>Perfect for:</strong><br>
            🏠 Families & individuals<br>
            🏢 Small businesses<br>
            🏭 Corporate organizations
        </div>
        """, unsafe_allow_html=True)
    
    # Footer with additional info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        💡 <strong>Why Choose JobConnect?</strong><br>
        ✅ Verified profiles • 🔒 Secure platform • 💰 Fair pricing • ⭐ Quality assurance
    </div>
    """, unsafe_allow_html=True)

def auth_choice():
    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    st.title(f"Welcome {role_name}")
    st.write("Please choose an option:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 Login", key="login_choice", use_container_width=True):
            go_to("login")
    
    with col2:
        if st.button("📝 Register", key="register_choice", use_container_width=True):
            go_to("register")
    
    # Back button
    st.write("")
    if st.button("← Back to Role Selection", key="back_to_landing"):
        st.session_state.role = None
        go_to("landing")

def login_page():
    login_user(st.session_state.role)

def register_page():
    register_user(st.session_state.role)

def dashboard_page():
    if not st.session_state.current_user:
        st.error("Please login first")
        go_to("landing")
        return
    
    user = st.session_state.current_user
    st.title(f"Welcome, {user['name']}!")
    
    if user['role'] == 'job':
        st.write("🔍 **Job Seeker Dashboard**")
        st.write("Here you can:")
        st.write("- Search for available jobs")
        st.write("- Apply to positions")
        st.write("- View your applications")
    else:
        st.write("🏢 **Employer Dashboard**")
        st.write("Here you can:")
        st.write("- Post job openings")
        st.write("- View applications")
        st.write("- Manage your listings")
    
    # Logout button
    st.write("")
    if st.button("🚪 Logout", key="logout_btn"):
        st.session_state.current_user = None
        st.session_state.role = None
        go_to("landing")

def main():
    # Page navigation
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "auth_choice":
        auth_choice()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()
    else:
        # Fallback to landing page
        st.session_state.page = "landing"
        landing_page()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Job Portal",
        page_icon="💼",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    main()