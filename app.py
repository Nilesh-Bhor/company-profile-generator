import menu
import streamlit as st
from dotenv import load_dotenv
from ProfileGenerator import ProfileGenerator

# Load environment variables
load_dotenv()

# Initialize session state for page visibility if not exists
if 'show_other_pages' not in st.session_state:
    st.session_state.show_other_pages = False
if 'is_shared_view' not in st.session_state:
    st.session_state.is_shared_view = False
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""

st.set_page_config(page_title="Company Profile Generator", page_icon="🏢", layout="centered", initial_sidebar_state="collapsed")

menu.show_menu()

def clear_session_state():
    st.session_state.profile = None
    st.session_state.ppt_buffer = None
    st.session_state.pdf_buffer = None
    st.session_state.profile_data = None
    st.session_state.company_website = None
    st.session_state.is_shared_view = False
    # Don't clear custom name when clearing other states
    if 'custom_name' not in st.session_state:
        st.session_state.custom_name = None

# Display title and subtitle
st.markdown(f'<h1 class="custom-title">🏢 Company Profile Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter a company name to get its detailed profile</p>', unsafe_allow_html=True)

# Create a container for input fields
with st.container():        
    # Input field for company name
    company_name = st.text_input("Company Name", placeholder="Enter company name (e.g., Microsoft, Apple)", value=st.session_state.company_name)

    # Input field for company website
    company_website = st.text_input("Company Website (optional)", placeholder="Enter company website (e.g., www.company.com)")

    # Generate button
    if st.button("Generate Profile"):
        if company_name:
            st.session_state.company_name = company_name
            clear_session_state()
            with st.spinner("Generating company profile..."):
                profile_generator = ProfileGenerator(company_name, company_website)
                st.session_state.profile = profile_generator.generate_profile()
                st.session_state.profile_data = profile_generator.profile_data
                st.session_state.ppt_buffer = profile_generator.generate_ppt()
                st.session_state.pdf_buffer = profile_generator.generate_pdf()
                # Show other pages after profile generation
                st.session_state.show_other_pages = True
                # Redirect to profile view
                st.switch_page("pages/profile_view.py")
        else:
            st.warning("Please enter a company name")
            clear_session_state()
            st.session_state.show_other_pages = False
            
    st.markdown('</div>', unsafe_allow_html=True)

# Add footer
st.markdown("---")
st.markdown("Powered by AI")
