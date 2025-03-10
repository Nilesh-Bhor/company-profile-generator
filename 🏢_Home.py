import json
import base64
import streamlit as st
from dotenv import load_dotenv
from CompanyProfile import CompanyProfile
from utils.utility import decode_profile_data
from styles.styles import side_bar_hide_style

# Load environment variables
load_dotenv()

# Initialize session state for page visibility if not exists
if 'show_other_pages' not in st.session_state:
    st.session_state.show_other_pages = False
if 'is_shared_view' not in st.session_state:
    st.session_state.is_shared_view = False

# Hide all pages by default in streamlit configuration
st.set_page_config(page_title="Profile Generator", page_icon="🏢", layout="centered", initial_sidebar_state="collapsed")

# Hide other pages if no profile is generated or if it's a shared view
if not st.session_state.show_other_pages or st.session_state.is_shared_view:
    st.markdown(side_bar_hide_style(), unsafe_allow_html=True)

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

# Check if this is a shared profile
shared_data = st.query_params.get("share", None)

if shared_data:
    clear_session_state()
    decoded_data = decode_profile_data(shared_data)
    
    if decoded_data:
        st.session_state.profile_data = decoded_data
        company_profile = CompanyProfile(decoded_data["company_overview"]["name"])
        st.session_state.profile = company_profile.format_profile(decoded_data)
        st.session_state.profile_data = company_profile.profile_data
        st.session_state.ppt_buffer = company_profile.get_ppt()
        st.session_state.pdf_buffer = company_profile.get_pdf()
        st.session_state.is_shared_view = True
        st.switch_page("pages/2_📝_Profile.py")
    else:
        st.error("Invalid shared profile data")
else:            
    # Display title and subtitle
    st.markdown(f'<h1 class="custom-title">🏢 Company Profile Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Enter a company name to get its detailed profile</p>', unsafe_allow_html=True)

    # Create a container for input fields
    with st.container():        
        # Input field for company name
        company_name = st.text_input("Company Name", placeholder="Enter company name (e.g., Microsoft, Apple)")

        # Input field for company website
        company_website = st.text_input("Company Website (optional)", placeholder="Enter company website (e.g., www.company.com)")

        # Generate button
        if st.button("Generate Profile"):
            if company_name:
                clear_session_state()
                with st.spinner("Generating company profile..."):
                    company_profile = CompanyProfile(company_name, company_website)
                    st.session_state.profile = company_profile.get_company_profile()
                    st.session_state.profile_data = company_profile.profile_data
                    st.session_state.ppt_buffer = company_profile.get_ppt()
                    st.session_state.pdf_buffer = company_profile.get_pdf()
                    # Show other pages after profile generation
                    st.session_state.show_other_pages = True
                    # Redirect to profile view
                    st.switch_page("pages/2_📝_Profile.py")
            else:
                st.warning("Please enter a company name")
                clear_session_state()
                st.session_state.show_other_pages = False
                
        st.markdown('</div>', unsafe_allow_html=True)

# Add footer
st.markdown("---")
st.markdown("Powered by Google Gemini AI")
