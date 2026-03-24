import streamlit as st
from src.home_guideline import home, guideline, custom_css
from src.input_result_page import page_one, page_two

st.set_page_config(page_title="Thesis", layout="wide")
custom_css("style.css")

def _init_state():
    defaults = {
        "page": "home",
        "source_df": None,
        "baseline_value_col": None,
        "ensemble_value_col": None,
        "date_col": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

_init_state()

sections = ["Home", "Input", "Guideline"]

nav_container = st.container()
with nav_container:
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    cols = st.columns(len(sections))
    for i, sec in enumerate(sections):
        is_active = st.session_state["page"] == sec.lower()
        button_type = "primary" if is_active else "secondary"
        
        if cols[i].button(
            sec,
            key=f"nav_{sec}",
            type=button_type,
            use_container_width=True
        ):
            st.session_state["page"] = sec.lower()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
        
page = st.session_state["page"]

if page == "home":
    home()
elif page == "guideline":
    guideline()
elif page == "input":
    page_one()
elif page == "results":
    page_two()