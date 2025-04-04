import menu
import streamlit as st
import styles.styles as cssStyles
from ProfileGenerator import ProfileGenerator

# Check if pages should be shown
if not st.session_state.get('show_other_pages', False):
    st.switch_page("app.py")

st.set_page_config(page_title="Profile Editor", page_icon="✏️", layout="wide")
st.markdown(cssStyles.editor_styles(), unsafe_allow_html=True)

menu.show_menu()

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
    
    
    with preview_col:
        st.markdown('<h3>Preview</h3>', unsafe_allow_html=True)
        st.markdown(edited_markdown, unsafe_allow_html=True)
    
    # Update button with better styling
    if edited_markdown != st.session_state.profile:
        col1, col2, col3 = st.columns([3, 3, 3])
        with col2:
            if st.button("💾 Save Changes", type="primary"):
                st.session_state.profile = edited_markdown
                
                profile_generator = ProfileGenerator(st.session_state.profile_data["overview"]["name"])
                profile_generator.profile_data = st.session_state.profile_data
                profile_generator.update_profile_with_markdown(edited_markdown)
                
                st.session_state.profile_data = profile_generator.profile_data
                st.session_state.ppt_buffer = profile_generator.generate_ppt()
                st.session_state.pdf_buffer = profile_generator.generate_pdf()
                
                st.success("✅ Profile updated successfully!")
                st.rerun()

else:
    st.warning("No profile available. Please generate a profile first.")
    st.switch_page("app.py") 