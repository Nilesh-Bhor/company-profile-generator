import streamlit as st
from CompanyProfile import CompanyProfile

# Check if pages should be shown
if not st.session_state.get('show_other_pages', False):
    st.switch_page("🏢_Profile_Generator.py")

st.set_page_config(page_title="Company Profile Editor", page_icon="✏️", layout="wide")

# Add custom CSS for StackEdit-like interface
st.markdown("""
<style>
    /* Editor container */
    .stApp {
        background-color: #fafafa;
    }
    
    /* Editor styling */
    .editor-container {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Preview styling */
    .preview-container {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    
    .preview-content {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        line-height: 1.6;
        color: #333;
    }
    
    .preview-content h1, .preview-content h2, .preview-content h3 {
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.25;
    }
    
    .preview-content p {
        margin-bottom: 16px;
    }
    
    /* Status bar */
    .status-bar {
        margin-top: 10px;
        padding: 5px 10px;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 12px;
        color: #666;
    }
    
    /* Custom textarea */
    .stTextArea textarea {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
        font-size: 14px;
        line-height: 1.5;
        padding: 15px;
    }
    
    /* Toolbar button styling */
    .stButton button {
        margin: 0 2px;
        padding: 2px 8px;
    }
</style>
""", unsafe_allow_html=True)

def insert_text_at_cursor(text: str, before: str = "", after: str = ""):
    """Helper function to insert text at cursor position or wrap selected text"""
    if 'cursor_position' not in st.session_state:
        st.session_state.cursor_position = 0
    
    current_text = st.session_state.get('original_markdown', '')
    position = st.session_state.cursor_position
    
    new_text = current_text[:position] + before + text + after + current_text[position:]
    return new_text

if 'profile' in st.session_state and st.session_state.profile is not None:
    st.title("✏️ Company Profile Editor")
    
    # Create columns for the editor layout
    editor_col, preview_col = st.columns([1, 1])
    
    with editor_col:
        st.markdown('<h3>Editor</h3>', unsafe_allow_html=True)

        # Add the text editor
        if 'original_markdown' not in st.session_state:
            st.session_state.original_markdown = st.session_state.profile
        
        edited_markdown = st.text_area(
            "",  # Remove label
            value=st.session_state.original_markdown,
            height=600,  # Set minimum height for editor
            key="markdown_editor"
        )
        
        # Update cursor position when text changes
        if edited_markdown != st.session_state.original_markdown:
            st.session_state.original_markdown = edited_markdown
        
        # Status bar
        word_count = len(edited_markdown.split())
        char_count = len(edited_markdown)
        st.markdown(f'<div class="status-bar">Words: {word_count} | Characters: {char_count}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with preview_col:
        st.markdown('<h3>Preview</h3>', unsafe_allow_html=True)
        st.markdown(edited_markdown, unsafe_allow_html=True)
    
    # Update button with better styling
    if edited_markdown != st.session_state.profile:
        col1, col2, col3 = st.columns([3, 3, 3])
        with col2:
            if st.button("💾 Save Changes", type="primary"):
                st.session_state.profile = edited_markdown
                company_profile = CompanyProfile(st.session_state.profile_data["company_overview"]["name"])
                company_profile.profile_data = st.session_state.profile_data
                company_profile.update_profile_with_markdown(edited_markdown)
                st.session_state.profile_data = company_profile.profile_data
                st.session_state.ppt_buffer = company_profile.get_ppt()
                st.session_state.pdf_buffer = company_profile.get_pdf()
                st.success("✅ Profile updated successfully!")
                st.rerun()

else:
    st.warning("No profile available. Please generate a profile first.")
    st.switch_page("🏢_Profile_Generator.py") 