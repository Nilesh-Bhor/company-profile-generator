import json
import streamlit as st
from dotenv import load_dotenv
from CompanyProfile import CompanyProfile


# Load environment variables
load_dotenv()

def clear_session_state():
    st.session_state.profile = None
    st.session_state.ppt_buffer = None
    st.session_state.profile_data = None

# Streamlit UI
st.title("Company Profile Generator")
st.write("Enter a company name to get its detailed profile")

# Input field for company name
company_name = st.text_input("Company Name")

# Streamlit UI
if 'profile' not in st.session_state:
    clear_session_state()

# Generate button
if st.button("Generate Profile"):
    if company_name:
        clear_session_state()
        with st.spinner("Generating company profile..."):
            company_profile = CompanyProfile(company_name)
            st.session_state.profile = company_profile.get_company_profile()
            st.session_state.profile_data = company_profile.profile_data
            st.session_state.ppt_buffer = company_profile.get_ppt()
            st.session_state.pdf_buffer = company_profile.get_pdf()
    else:
        st.warning("Please enter a company name")
        clear_session_state()
        

# Display profile and download button if available
if st.session_state.profile is not None and st.session_state.profile_data is not None:
    try:
        # Create tabs for different views
        markdown_tab, json_tab = st.tabs(["Formatted View", "JSON View"])

        with markdown_tab:
            st.markdown(st.session_state.profile, unsafe_allow_html=True)
            
            # Add a button to download the PPT
            if st.session_state.ppt_buffer is not None:
                st.download_button(
                    label="Download PPT",
                    data=st.session_state.ppt_buffer,
                    file_name=f"{company_name}_profile.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
            
            # Add a button to download the PDF
            if st.session_state.pdf_buffer is not None:
                st.download_button(
                    label="Download PDF",
                    data=st.session_state.pdf_buffer,
                    file_name=f"{company_name}_profile.pdf",
                    mime="application/pdf"
                )

        with json_tab:
            st.json(st.session_state.profile_data)        
        
    except json.JSONDecodeError:
        st.error("Invalid JSON response received")

# Add footer
st.markdown("---")
st.markdown("Powered by Google Gemini AI")
