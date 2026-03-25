import streamlit as st
from src.home_guideline import home, guideline, custom_css
from src.input_result_page import page_one, page_two
from streamlit_scroll_navigation import scroll_navbar

st.set_page_config(page_title="Thesis", layout="wide")
custom_css("style.css")

anchor_ids = ["Home", "Input", "Guideline"]
anchor_labels = ["Home", "Forecasting", "Guideline"]

with st.sidebar:
    st.subheader("Navigation")
    scroll_navbar(anchor_ids, anchor_labels=anchor_labels, orientation="vertical", key="sidebar_navbar")

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
    guideline()
    page_one()
elif page == "results":
    page_two()