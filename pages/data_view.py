import menu
import streamlit as st

# Check if pages should be shown
if not st.session_state.get('show_other_pages', False):
    st.switch_page("app.py")


st.set_page_config(page_title="JSON View", page_icon="📊", layout="wide")
menu.show_menu()

if 'profile_data' in st.session_state and st.session_state.profile_data is not None:
    st.title("📊 JSON View")
    st.json(st.session_state.profile_data)
else:
    st.warning("No profile data available. Please generate a profile first.")
    st.switch_page("app.py") 