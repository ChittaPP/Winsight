# Modules
import pyrebase
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Winsight", page_icon=":tada:", layout="wide")

# Configuration Key
firebaseConfig = {
    'apiKey': "AIzaSyAy-hRZahCTA-kJOdoidH9wakCM-pK7Zhc",
    'authDomain': "winsight-a7b3d.firebaseapp.com",
    'projectId': "winsight-a7b3d",
    'databaseURL': "https://winsight-a7b3d-default-rtdb.europe-west1.firebasedatabase.app",
    'storageBucket': "winsight-a7b3d.appspot.com",
    'messagingSenderId': "1059424693014",
    'appId': "1:1059424693014:web:bf88ae2311083eb47a7e37",
    'measurementId': "G-0TXY441NJX"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Initialize Streamlit Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar
st.sidebar.title("Our community app")

# Authentication Section
if not st.session_state['logged_in']:
    # Login or Signup Selection
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])

    # Input Fields
    email = st.sidebar.text_input('Email')
    password = st.sidebar.text_input('Password', type='password')

    if choice == 'Sign up':
        handle = st.sidebar.text_input('Handle name', value='Default')
        submit = st.sidebar.button('Create Account')

        if submit:
            try:
                # Create User with Email and Password
                user = auth.create_user_with_email_and_password(email, password)
                st.success('Account created successfully!')
                st.balloons()
                
                # Sign in after account creation
                user = auth.sign_in_with_email_and_password(email, password)
                
                # Store additional user data
                db.child(user['localId']).child("Handle").set(handle)
                db.child(user['localId']).child("ID").set(user['localId'])
                
                st.title(f'Welcome, {handle}!')
                st.info('Please login using the login dropdown.')
            
            except Exception as e:
                st.error(f'Failed to create account: {str(e)}')

    elif choice == 'Login':
        login_button = st.sidebar.button('Login')

        if login_button:
            try:
                # Sign in with Email and Password
                user = auth.sign_in_with_email_and_password(email, password)
                
                # Update session state
                st.session_state['logged_in'] = True
                st.balloons()
                
                # Clear login section
                st.sidebar.empty()
                
                # Import and call function after successful login
                from winsight import chitta
                chitta()
            
            except Exception as e:
                st.error(f'Failed to login: {str(e)}')

# Conditional rendering based on login status
if st.session_state['logged_in']:
    from winsight import chitta
    chitta()
