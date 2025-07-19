# utils.py
import json
import os
import re
from datetime import datetime

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def read_json(filename):
    """Read JSON file, return empty list if file doesn't exist"""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding='utf-8') as file:
            data = json.load(file)
            # Ensure we return a list
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, FileNotFoundError, Exception):
        return []

def write_json(filename, data):
    """Write data to JSON file"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
        return False

def get_next_user_id(users):
    """Get next available user ID - handles missing IDs gracefully"""
    if not users or not isinstance(users, list):
        return 1
    
    # Collect all valid IDs
    valid_ids = []
    for user in users:
        if isinstance(user, dict) and 'id' in user:
            try:
                user_id = int(user['id'])
                if user_id > 0:
                    valid_ids.append(user_id)
            except (ValueError, TypeError):
                continue
    
    # Return next available ID
    return max(valid_ids) + 1 if valid_ids else 1
    
    # Collect all valid IDs
    valid_ids = []
    users_needing_repair = []
    
    for i, user in enumerate(users):
        if not isinstance(user, dict):
            continue
            
        if 'id' in user:
            try:
                user_id = int(user['id'])
                if user_id > 0:
                    valid_ids.append(user_id)
                else:
                    users_needing_repair.append(i)
            except (ValueError, TypeError):
                users_needing_repair.append(i)
        else:
            users_needing_repair.append(i)
    
    # Auto-repair users without valid IDs
    next_repair_id = max(valid_ids) + 1 if valid_ids else 1
    for user_index in users_needing_repair:
        users[user_index]['id'] = next_repair_id
        valid_ids.append(next_repair_id)
        next_repair_id += 1
        print(f"Auto-assigned ID {users[user_index]['id']} to user: {users[user_index].get('name', 'Unknown')}")
    
    # Return next available ID
    return max(valid_ids) + 1 if valid_ids else 1

def validate_password(password):
    """Validate password strength - returns None if valid, error message if invalid"""
    if not password or not isinstance(password, str):
        return "Password is required."
    
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must include at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must include at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must include at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must include at least one special character."
    return None  # Valid password

def validate_phone(phone):
    """Validate 10-digit phone number"""
    if not phone:
        return False
    # Remove any spaces, dashes, or other non-digit characters except +
    cleaned_phone = re.sub(r'[^\d+]', '', str(phone))
    
    # Handle international format (+91)
    if cleaned_phone.startswith('+91'):
        cleaned_phone = cleaned_phone[3:]
    elif cleaned_phone.startswith('91') and len(cleaned_phone) == 12:
        cleaned_phone = cleaned_phone[2:]
    
    return cleaned_phone.isdigit() and len(cleaned_phone) == 10

def validate_aadhaar(aadhaar):
    """Validate 12-digit Aadhaar number"""
    if not aadhaar:
        return False
    # Remove any spaces or dashes
    cleaned_aadhaar = re.sub(r'[^\d]', '', str(aadhaar))
    return cleaned_aadhaar.isdigit() and len(cleaned_aadhaar) == 12

def validate_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email.strip()))

def authenticate_user(name, password, role):
    """Authenticate user by name, password and role"""
    if not all([name, password, role]):
        return None
        
    users = read_json("data/users.json")
    for user in users:
        if (isinstance(user, dict) and 
            user.get("name") == name and 
            user.get("password") == password and 
            user.get("role") == role):
            return user
    return None

def find_user_by_email(users, email):
    """Find user by email address"""
    if not users or not email:
        return None
    
    email = email.lower().strip()
    for user in users:
        if isinstance(user, dict) and user.get("email", "").lower().strip() == email:
            return user
    return None

def find_user_by_phone(users, phone):
    """Find user by phone number"""
    if not users or not phone:
        return None
    
    # Normalize phone number for comparison
    normalized_phone = re.sub(r'[^\d]', '', str(phone))
    if normalized_phone.startswith('91') and len(normalized_phone) == 12:
        normalized_phone = normalized_phone[2:]
    
    for user in users:
        if isinstance(user, dict):
            user_phone = re.sub(r'[^\d]', '', str(user.get("phone", "")))
            if user_phone.startswith('91') and len(user_phone) == 12:
                user_phone = user_phone[2:]
            if user_phone == normalized_phone:
                return user
    return None

def sanitize_user_input(data):
    """Clean and sanitize user input data"""
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Strip whitespace and normalize
            sanitized[key] = value.strip()
            # Special handling for email
            if key == 'email':
                sanitized[key] = value.lower().strip()
        elif isinstance(value, list):
            # Clean list items
            sanitized[key] = [item.strip() if isinstance(item, str) else item for item in value]
        else:
            sanitized[key] = value
    
    return sanitized

def create_user_record(user_data, user_id=None):
    """Create a complete user record with all required fields"""
    # Load existing users to get next ID if not provided
    if user_id is None:
        users = read_json("data/users.json")
        user_id = get_next_user_id(users)
    
    # Sanitize input data
    clean_data = sanitize_user_input(user_data)
    
    # Create complete user record
    user_record = {
        "id": user_id,
        "name": clean_data.get("name", ""),
        "email": clean_data.get("email", "").lower(),
        "phone": clean_data.get("phone", ""),
        "password": clean_data.get("password", ""),
        "role": clean_data.get("role", ""),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "is_active": True
    }
    
    # Add role-specific fields
    if clean_data.get("role") == "job":
        user_record.update({
            "aadhaar": clean_data.get("aadhaar", ""),
            "city": clean_data.get("city", ""),
            "address": clean_data.get("address", ""),
            "work_type": clean_data.get("work_type", []),
            "experience": clean_data.get("experience", ""),
            "expected_salary": clean_data.get("expected_salary", ""),
            "availability": clean_data.get("availability", ""),
            "skills": clean_data.get("skills", []),
            "languages": clean_data.get("languages", []),
            "profile_completed": True
        })
    elif clean_data.get("role") == "hire":
        user_record.update({
            "company_name": clean_data.get("company_name", ""),
            "city": clean_data.get("city", ""),
            "address": clean_data.get("address", ""),
            "job_postings": [],
            "profile_completed": True
        })
    
    return user_record

def save_user(user_data):
    """Save user to database with proper validation"""
    try:
        # Validate required fields
        required_fields = ["name", "email", "phone", "password", "role"]
        for field in required_fields:
            if not user_data.get(field):
                return False, f"Missing required field: {field}"
        
        # Validate email format
        if not validate_email(user_data["email"]):
            return False, "Invalid email format"
        
        # Validate phone
        if not validate_phone(user_data["phone"]):
            return False, "Invalid phone number format"
        
        # Validate password
        password_error = validate_password(user_data["password"])
        if password_error:
            return False, password_error
        
        # Load existing users
        users = read_json("data/users.json")
        
        # Check for duplicate email
        if find_user_by_email(users, user_data["email"]):
            return False, "Email already registered"
        
        # Check for duplicate phone
        if find_user_by_phone(users, user_data["phone"]):
            return False, "Phone number already registered"
        
        # Create user record
        user_record = create_user_record(user_data)
        
        # Add to users list
        users.append(user_record)
        
        # Save to file
        success = write_json("data/users.json", users)
        
        if success:
            return True, user_record
        else:
            return False, "Failed to save user data"
            
    except Exception as e:
        return False, f"Error saving user: {str(e)}"

def update_user_data(filepath="data/users.json"):
    """Update existing user data to ensure all users have proper IDs"""
    users = read_json(filepath)
    if not users:
        return True
    
    # This will automatically fix any users missing IDs
    get_next_user_id(users)
    
    # Save the updated data
    return write_json(filepath, users)

# Constants
ROLES = ["job", "hire"]  # Using lowercase for consistency
ROLE_LABELS = {"job": "Job Seeker", "hire": "Employer"}
WORK_TYPES = [
    "Maid", "Cook", "Driver", "Cleaner", "Babysitter", "Gardener", 
    "Security Guard", "Caretaker", "Housekeeper", "Nanny", "Butler",
    "Personal Assistant", "Laundry Service", "Pet Care"
]
CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur",
    "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad"
]
EXPERIENCE_LEVELS = ["Entry Level (0-1 years)", "Mid Level (2-5 years)", "Senior Level (5+ years)"]
AVAILABILITY_OPTIONS = ["Full Time", "Part Time", "Weekends Only", "Flexible Hours"]
LANGUAGES = ["Hindi", "English", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi"]

PASSWORD_MIN_LENGTH = 8
PHONE_LENGTH = 10
AADHAAR_LENGTH = 12