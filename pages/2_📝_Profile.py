import streamlit as st
from CompanyProfile import CompanyProfile
from utils.utility import encode_profile_data, decode_profile_data
from styles.styles import side_bar_hide_style, profile_view_style

def clear_session_state():
    st.session_state.profile = None
    st.session_state.ppt_buffer = None
    st.session_state.pdf_buffer = None
    st.session_state.profile_data = None
    st.session_state.company_website = None
    st.session_state.is_shared_view = False
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
    else:
        st.error("Invalid shared profile data")

# Add custom CSS for profile view
if 'is_shared_view' in st.session_state and st.session_state.is_shared_view:
    st.set_page_config(page_title="Company Profile View", page_icon="📋", layout="centered")
    st.markdown(side_bar_hide_style(), unsafe_allow_html=True)    
else:
    st.set_page_config(page_title="Company Profile View", page_icon="📋", layout="wide")

st.markdown(profile_view_style(), unsafe_allow_html=True)

def create_download_buttons(include_share=True):
    left, middle, right = st.columns(3, gap="small")
    # Add a button to download the PPT
    if st.session_state.ppt_buffer is not None:
        left.download_button(
            label="Download PPT",
            data=st.session_state.ppt_buffer,
            file_name=f"{st.session_state.profile_data['company_overview']['name']}_profile.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    
    # Add a button to download the PDF
    if st.session_state.pdf_buffer is not None:
        middle.download_button(
            label="Download PDF",
            data=st.session_state.pdf_buffer,
            file_name=f"{st.session_state.profile_data['company_overview']['name']}_profile.pdf",
            mime="application/pdf"
        )
    
    # Add share button only if not in shared view
    if include_share and not st.session_state.is_shared_view:
        base_url = st.request_url_root if hasattr(st, 'request_url_root') else '/'
        share_url = f"{base_url}Profile?share={encode_profile_data(st.session_state.profile_data)}"
        right.markdown(f'<a href="{share_url}" target="_blank"><button style="padding: 0.5rem 1rem; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">Share Profile</button></a>', unsafe_allow_html=True)


def display_profile(profile_content, company_name=None):
    """Display the profile in a well-structured layout"""
    # Profile content
    st.markdown(profile_content, unsafe_allow_html=True)

if 'profile' in st.session_state and st.session_state.profile is not None:
    # Display the profile
    display_profile(st.session_state.profile, st.session_state.profile_data["company_overview"]["name"])
    
    # Add download and share buttons
    create_download_buttons()
else:
    st.warning("No profile available. Please generate a profile first.")
    st.switch_page("🏢_Home.py")