import streamlit as st

def show_menu():
    if st.session_state.is_shared_view:
        st.sidebar.page_link("pages/profile_view.py", label="📝 Profile")
        return
    
    if st.session_state.show_other_pages:
        st.sidebar.page_link("app.py", label="🏢 Home")
        st.sidebar.page_link("pages/profile_view.py", label="📝 Profile")
        st.sidebar.page_link("pages/profile_editor.py", label="✏️ Editor")
        st.sidebar.page_link("pages/data_view.py", label="📊 JSON View")
        return
    
    st.sidebar.page_link("app.py", label="🏢 Home") 
    
