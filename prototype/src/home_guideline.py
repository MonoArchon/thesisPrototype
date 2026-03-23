import streamlit as st
# from streamlit_option_menu import option_menu

# selected = option_menu(
#     menu_title=None,
#     options=["Home", "Input", "Guideline"],
#     icons=["house", "upload", "book"],
#     orientation="horizontal"
# )



def custom_css(file_name) -> None:
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def home() -> None:
    custom_css("style.css")
    

    col1, col2, col3 = st.columns(3, gap="xsmall")
    with col1:
        st.markdown("<h1 class='title'>Ensemble LSTM-XGBoost for Improving Univariate Precipitation Time Series Forecasting</h1>", unsafe_allow_html=True)
        # st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("Get Started", use_container_width=True):
            st.session_state["page"] = "input"
            st.rerun()

        if st.button("Guideline", use_container_width=True):
            st.session_state["page"] = "guideline"
            st.rerun()
    # with col2:
    #     if st.button("Get Started", use_container_width=True):
    #         st.session_state["page"] = "input"
    #         st.rerun()
    # with col3:
    #     if st.button("Guideline", use_container_width=True):
    #         st.session_state["page"] = "guideline"
    #         st.rerun()

def guideline() -> None:
    st.button("← Back to Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.title("Guideline for Precipitation Values")

    custom_css("style.css")

    # --- Data ---
    rainfall_data = [
        ("1 inch", "Light to moderate rain<br>• Usually manageable, minor puddles<br>• Beneficial for crops", "#d4edda"),
        ("2 inches", "Moderate rain<br>• Some street flooding possible<br>• Drains may start to struggle", "#c3e6cb"),
        ("3 inches", "Heavy rain<br>• Localized flooding begins<br>• Small rivers/creeks may rise", "#ffeeba"),
        ("4 inches", "Very heavy rain<br>• Flooding likely in low-lying areas<br>• Travel disruptions possible", "#ffdf7e"),
        ("5 inches", "Intense rainfall<br>• Flash flooding risk increases<br>• Drainage systems overwhelmed", "#f5c6cb"),
        ("6 inches", "Severe rainfall<br>• Widespread flooding likely<br>• Roads may become impassable", "#f1b0b7"),
        ("7 inches", "Very severe<br>• Flash floods + river flooding<br>• Possible evacuations", "#ea868f"),
        ("8 inches", "Extreme rainfall<br>• Major flooding expected<br>• Infrastructure damage possible", "#e35d6a"),
        ("9 inches", "Dangerous / rare<br>• Severe flooding<br>• Landslides possible", "#dc3545"),
        ("10 inches", "Catastrophic rainfall<br>• Life-threatening floods<br>• Disaster-level impact", "#b02a37"),
    ]

    # --- Layout (2 cards per row) ---
    for i in range(0, len(rainfall_data), 2):
        col1, col2 = st.columns(2)

        for col, item in zip([col1, col2], rainfall_data[i:i+2]):
            inch, desc, color = item
            with col:
                st.markdown(
                    f"""
                    <div class="card" style="background-color:{color};">
                        <h4>{inch}</h4>
                        <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
