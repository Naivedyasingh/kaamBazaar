# register.py
import streamlit as st
from utils import write_json, read_json, validate_password, validate_phone, validate_aadhaar, get_next_user_id

def register_user(role):
    st.title(f"📝 Register as {'Job Seeker' if role == 'job' else 'Employer'}")
    
    # Add informative description
    if role == "job":
        st.info("🔍 **Job Seeker Registration** - Create your profile to find amazing job opportunities!")
        st.write("As a job seeker, you'll be able to:")
        st.write("• Browse available job listings")
        st.write("• Apply for positions that match your skills")
        st.write("• Track your job applications")
        st.write("• Get notifications about new opportunities")
    else:
        st.info("🏢 **Employer Registration** - Join our platform to find the perfect candidates!")
        st.write("As an employer, you'll be able to:")
        st.write("• Post job openings and requirements")
        st.write("• Review and manage applications")
        st.write("• Contact qualified candidates directly")
        st.write("• Build your company profile")
    
    st.markdown("---")
    st.subheader("👤 Personal Information")
    
    # Basic Information
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("📛 Full Name *", placeholder="Enter your full name", key=f"reg_name_{role}")
    with col2:
        phone = st.text_input("📱 Phone Number *", placeholder="10-digit mobile number", key=f"reg_phone_{role}")
    
    # Email and Location
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com", key=f"reg_email_{role}")
    with col2:
        city = st.text_input("🏙️ City", placeholder="Your city", key=f"reg_city_{role}")
    
    # Age and Gender for job seekers
    if role == "job":
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("🎂 Age", min_value=16, max_value=70, value=25, key=f"reg_age_{role}")
        with col2:
            gender = st.selectbox("👤 Gender", ["Select", "Male", "Female", "Other"], key=f"reg_gender_{role}")
    
    # Experience and Skills for job seekers
    if role == "job":
        st.markdown("---")
        st.subheader("💼 Professional Information")
        
        col1, col2 = st.columns(2)
        with col1:
            experience = st.selectbox("📈 Experience Level", 
                                    ["Select", "Fresher (0-1 years)", "Experienced (1-3 years)", 
                                     "Senior (3-5 years)", "Expert (5+ years)"], 
                                    key=f"reg_experience_{role}")
        with col2:
            work_type = st.multiselect("🛠️ Skills/Work Types", 
                                     ["Maid", "Cook", "Driver", "Cleaner", "Babysitter", 
                                      "Gardener", "Security Guard", "Electrician", "Plumber", "Other"],
                                     key=f"reg_work_type_{role}")
        
        expected_salary = st.slider("💰 Expected Monthly Salary (₹)", 
                                  min_value=5000, max_value=50000, value=15000, step=1000,
                                  key=f"reg_salary_{role}")
        
        availability = st.multiselect("⏰ Availability", 
                                    ["Full Time", "Part Time", "Weekends Only", "Night Shifts"],
                                    key=f"reg_availability_{role}")
    
    # Company information for employers
    elif role == "hire":
        st.markdown("---")
        st.subheader("🏢 Company Information")
        
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("🏢 Company/Organization Name", 
                                       placeholder="Your company name", 
                                       key=f"reg_company_{role}")
        with col2:
            company_type = st.selectbox("🏭 Company Type", 
                                      ["Select", "Individual/Family", "Small Business", 
                                       "Medium Enterprise", "Large Corporation", "NGO/Non-Profit"],
                                      key=f"reg_company_type_{role}")
        
        company_address = st.text_area("📍 Company Address", 
                                     placeholder="Full address of your company/residence",
                                     key=f"reg_address_{role}")
    
    st.markdown("---")
    st.subheader("🔐 Security Information")
    
    # Security Information
    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input("🔒 Password *", type="password", 
                                placeholder="Create a strong password", 
                                key=f"reg_password_{role}",
                                help="Password must be 8+ characters with uppercase, lowercase, digit, and special character")
        
        # Password strength indicator
        if password:
            strength_score = 0
            feedback = []
            
            if len(password) >= 8:
                strength_score += 1
            else:
                feedback.append("At least 8 characters")
            
            if any(c.isupper() for c in password):
                strength_score += 1
            else:
                feedback.append("One uppercase letter")
                
            if any(c.islower() for c in password):
                strength_score += 1
            else:
                feedback.append("One lowercase letter")
                
            if any(c.isdigit() for c in password):
                strength_score += 1
            else:
                feedback.append("One number")
                
            if any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
                strength_score += 1
            else:
                feedback.append("One special character")
            
            # Display strength
            if strength_score == 5:
                st.success("🔐 Strong password!")
            elif strength_score >= 3:
                st.warning(f"⚠️ Medium strength. Missing: {', '.join(feedback)}")
            else:
                st.error(f"❌ Weak password. Need: {', '.join(feedback)}")
                
    with col2:
        confirm_password = st.text_input("🔒 Confirm Password *", type="password", 
                                       placeholder="Re-enter your password", 
                                       key=f"reg_confirm_password_{role}")
        
        # Password match indicator
        if password and confirm_password:
            if password == confirm_password:
                st.success("✅ Passwords match!")
            else:
                st.error("❌ Passwords don't match")
    
    # Aadhaar for job seekers only
    if role == "job":
        st.markdown("📋 **Identity Verification**")
        aadhaar = st.text_input("🆔 Aadhaar Number (12 digits) *", 
                              placeholder="Enter your 12-digit Aadhaar number", 
                              key=f"reg_aadhaar_{role}",
                              help="Your Aadhaar number will be used for identity verification. We keep this information secure and confidential.")
        
        # Aadhaar format helper
        if aadhaar and len(aadhaar) > 0:
            if len(aadhaar) == 12 and aadhaar.isdigit():
                st.success("✅ Valid Aadhaar format")
            elif len(aadhaar) != 12:
                st.warning(f"⚠️ Aadhaar should be 12 digits (currently: {len(aadhaar)})")
            elif not aadhaar.isdigit():
                st.error("❌ Aadhaar should contain only numbers")
        
        st.caption("🔒 Your Aadhaar information is encrypted and used only for verification purposes as per government guidelines.")
    else:
        aadhaar = None
    
    # Terms and conditions
    st.markdown("---")
    agree_terms = st.checkbox("✅ I agree to the Terms and Conditions and Privacy Policy", 
                            key=f"reg_terms_{role}")
    
    # Register button
    if st.button("🚀 Create Account", key=f"register_btn_{role}", 
                 type="primary", use_container_width=True):
        
        # Basic validation
        required_fields = [name.strip(), phone.strip(), password.strip()]
        if role == "job":
            required_fields.extend([aadhaar.strip() if aadhaar else ""])
        
        if not all(required_fields):
            st.error("❌ Please fill all required fields marked with *")
            return
        
        if not agree_terms:
            st.error("❌ Please accept the Terms and Conditions to continue.")
            return
        
        if password != confirm_password:
            st.error("❌ Passwords do not match. Please try again.")
            return
        
        # Role-specific validation
        if role == "job":
            if gender == "Select":
                st.error("❌ Please select your gender.")
                return
            if experience == "Select":
                st.error("❌ Please select your experience level.")
                return
            if not work_type:
                st.error("❌ Please select at least one skill/work type.")
                return
            if not availability:
                st.error("❌ Please select your availability.")
                return
        
        if role == "hire":
            if not company_name.strip():
                st.error("❌ Please enter your company/organization name.")
                return
            if company_type == "Select":
                st.error("❌ Please select your company type.")
                return
        
        # Validate Aadhaar for job seekers
        if role == "job" and not validate_aadhaar(aadhaar):
            st.error("❌ Invalid Aadhaar Number. Must be exactly 12 digits.")
            return
        
        # Validate phone number
        if not validate_phone(phone):
            st.error("❌ Invalid Phone Number. Must be exactly 10 digits.")
            return
        
        # Validate password
        password_error = validate_password(password)
        if password_error:
            st.error(f"❌ {password_error}")
            return
        
        # Check if phone already exists
        users = read_json("data/users.json")
        if any(u["phone"] == phone for u in users):
            st.error("❌ Phone number already registered. Please use a different number or try logging in.")
            return
        
        # Create new user with all information
        user_id = get_next_user_id(users)
        user_data = {
            "id": user_id,
            "role": role,
            "name": name.strip(),
            "phone": phone.strip(),
            "password": password.strip(),
            "email": email.strip() if email else "",
            "city": city.strip() if city else ""
        }
        
        if role == "job":
            user_data.update({
                "aadhaar": aadhaar.strip(),
                "age": age,
                "gender": gender,
                "experience": experience,
                "work_type": work_type,
                "expected_salary": expected_salary,
                "availability": availability
            })
        else:  # employer
            user_data.update({
                "company_name": company_name.strip(),
                "company_type": company_type,
                "company_address": company_address.strip() if company_address else ""
            })
        
        # Save user data
        users.append(user_data)
        write_json("data/users.json", users)
        
        st.success("🎉 Registration successful! Welcome to our platform!")
        st.balloons()
        
        # Show next steps
        st.info(f"✨ **Next Steps for {user_data['name']}:**")
        if role == "job":
            st.write("• Complete your profile with additional details")
            st.write("• Upload your resume/documents")
            st.write("• Start browsing available jobs")
        else:
            st.write("• Set up your company profile")
            st.write("• Post your first job opening")
            st.write("• Start receiving applications")
        
        # Add some space and show login button
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Go to Login", key=f"go_to_login_{role}", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with col2:
            if st.button("🏠 Go to Home", key=f"go_to_home_{role}", use_container_width=True):
                st.session_state.page = "landing"
                st.session_state.role = None
                st.rerun()
    
    # Back button at the bottom
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Login/Register Choice", key=f"back_to_auth_{role}", 
                     use_container_width=True):
            st.session_state.page = "auth_choice"
            st.rerun()