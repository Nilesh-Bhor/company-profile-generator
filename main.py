import json
import base64
import streamlit as st
from dotenv import load_dotenv
from CompanyProfile import CompanyProfile

# Load environment variables
load_dotenv()

def clear_session_state():
    st.session_state.profile = None
    st.session_state.ppt_buffer = None
    st.session_state.pdf_buffer = None
    st.session_state.profile_data = None
    st.session_state.company_website = None

def encode_profile_data(data):
    json_str = json.dumps(data)
    return base64.urlsafe_b64encode(json_str.encode()).decode()

def decode_profile_data(encoded_data):
    try:
        json_str = base64.urlsafe_b64decode(encoded_data.encode()).decode()
        return json.loads(json_str)
    except:
        return None

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
    
    # Add share button
    if include_share:
        base_url = st.request_url_root if hasattr(st, 'request_url_root') else '/'
        share_url = f"{base_url}?share={encode_profile_data(st.session_state.profile_data)}"
        right.markdown(f'<a href="{share_url}" target="_blank"><button style="padding: 0.5rem 1rem; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">Share Profile</button></a>', unsafe_allow_html=True)


# Check if this is a shared profile
shared_data = st.query_params.get("share", None)

if shared_data:
    clear_session_state()
    # This is a shared profile view
    #st.title("Company Profile")
    decoded_data = decode_profile_data(shared_data)
    
    if decoded_data:
        st.session_state.profile_data = decoded_data
        company_profile = CompanyProfile(decoded_data["company_overview"]["name"])
        st.session_state.profile = company_profile.format_profile(decoded_data)
        st.session_state.ppt_buffer = company_profile.get_ppt()
        st.session_state.pdf_buffer = company_profile.get_pdf()
    else:
        st.error("Invalid shared profile data")
else:
    # Normal profile generation view
    st.title("Company Profile Generator")
    st.write("Enter a company name to get its detailed profile")

    # Input field for company name
    company_name = st.text_input("Company Name")

    # Input field for company website
    company_website = st.text_input("Company Website (optional)")

    # Initialize session state
    if 'profile' not in st.session_state:
        clear_session_state()

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
        else:
            st.warning("Please enter a company name")
            clear_session_state()

# Display profile and download buttons if available
if st.session_state.profile is not None and st.session_state.profile_data is not None:
    try:
        if shared_data is None:
            # Create tabs for different views
            markdown_tab, json_tab = st.tabs(["Formatted View", "JSON View"])

            with markdown_tab:
                st.markdown(st.session_state.profile, unsafe_allow_html=True)
                create_download_buttons()                

            with json_tab:
                st.json(st.session_state.profile_data)
            
        else:
            st.markdown(st.session_state.profile, unsafe_allow_html=True)
            create_download_buttons(include_share=False)
        
    except json.JSONDecodeError:
        st.error("Invalid JSON response received")

# Add footer
st.markdown("---")
st.markdown("Powered by Google Gemini AI")
