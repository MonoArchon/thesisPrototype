import streamlit as st
from streamlit_option_menu import option_menu
from src.home_guideline import home, guideline
from src.input_result_page import page_one, page_two


st.set_page_config(page_title="Thesis", layout="wide")


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

page = st.session_state["page"]

if page == "home":
    home()
elif page == "guideline":
    guideline()
elif page == "input":
    page_one()
elif page == "results":
    page_two()