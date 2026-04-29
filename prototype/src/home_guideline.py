import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

anchor_ids = ["Input", "Guideline"]

def custom_css(file_name) -> None:
    css_path = Path(__file__).parent / file_name
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def home() -> None:
    st.markdown('<div id="Home"></div>', unsafe_allow_html=True)
    custom_css("style.css")
    
    col1, col2, col3 = st.columns(3, gap="xsmall")
    with col1:
        st.markdown("<h1 class='title'>Ensemble LSTM-XGBoost for Improving Univariate Precipitation Time Series Forecasting</h1>", unsafe_allow_html=True)
        if st.button("Get Started", use_container_width=True):
                components.html(
                """
                <script>
                    window.parent.document.getElementById('Input').scrollIntoView({behavior: 'smooth'});
                </script>
                """,
                height=0
            )
        if st.button("Guideline", use_container_width=True):
                components.html(
                """
                <script>
                    window.parent.document.getElementById('Guideline').scrollIntoView({behavior: 'smooth'});
                </script>
                """,
                height=0
            )
    # with col2:
    #     if st.button("Get Started", use_container_width=True):
    #         st.session_state["page"] = "input"
    #         st.rerun()
    # with col3:
    #     if st.button("Guideline", use_container_width=True):
    #         st.session_state["page"] = "guideline"
    #         st.rerun()

def guideline() -> None:
    st.markdown('<div id="Guideline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="back-button-container">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("Guideline for Precipitation Values")

    custom_css("style.css")

    # --- Data ---
    rainfall_data = [
        ("1 inch", "Light to moderate rain<br>• Usually manageable, minor puddles<br>• Beneficial for crops", "#d4edda", "#59cc74"),
        ("2 inches", "Moderate rain<br>• Some street flooding possible<br>• Drains may start to struggle", "#c3e6cb", "#4cc969"),
        ("3 inches", "Heavy rain<br>• Localized flooding begins<br>• Small rivers/creeks may rise", "#ffeeba", "#d1b04d"),
        ("4 inches", "Very heavy rain<br>• Flooding likely in low-lying areas<br>• Travel disruptions possible", "#ffdf7e", "#c09e36"),
        ("5 inches", "Intense rainfall<br>• Flash flooding risk increases<br>• Drainage systems overwhelmed", "#f5c6cb", "#c55e67"),
        ("6 inches", "Severe rainfall<br>• Widespread flooding likely<br>• Roads may become impassable", "#f1b0b7", "#cf555f"),
        ("7 inches", "Very severe<br>• Flash floods + river flooding<br>• Possible evacuations", "#ea868f", "#d64c58"),
        ("8 inches", "Extreme rainfall<br>• Major flooding expected<br>• Infrastructure damage possible", "#e35d6a", "#d32133"),
        ("9 inches", "Dangerous / rare<br>• Severe flooding<br>• Landslides possible", "#dc3545", "#d48189"),
        ("10 inches", "Catastrophic rainfall<br>• Life-threatening floods<br>• Disaster-level impact", "#b02a37", "#cfa2a7"),
    ]

    # --- Layout (2 cards per row) ---
    for i in range(0, len(rainfall_data), 2):
        col1, col2, col3 = st.columns([1,1,1], gap="xxsmall")

        for col, item in zip([col1, col3], rainfall_data[i:i+2]):
            inch, desc, color, bdr_color = item
            st.markdown(f"<br>", unsafe_allow_html=True)
            with col:
                st.markdown(
                    f"""
                    <div class="card" style="
                    background-color:{color};
                    border: 2px solid {bdr_color};
                    box-shadow: 0 0 10px {bdr_color}, 0 0 20px {bdr_color};">
                        <h4>{inch}</h4>
                        <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
