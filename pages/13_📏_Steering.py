#  ----------------------------------------------------------------------------------------------------------------------#
# LIBRARY IMPORT
# ----------------------------------------------------------------------------------------------------------------------#

# Import library
import streamlit as st  # Streamlit library
import pandas as pd  # Pandas library is used for exporting Excel data.
from streamlit_option_menu import option_menu
# ----------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------------------------------#
st.title("Chassi")
st.divider()

tabs = st.tabs(["Theoretical data of steering",
               "Steering wheel steering angle", "-", "-"])

with tabs[0]:
    col_info, col_img = st.columns([1, 3])

    with col_info:
        # Inicializar estado persistente
        if "selected_software" not in st.session_state:
            st.session_state["selected_software"] = "Ansys Fluent"

        if "temp_selected_software" not in st.session_state:
            st.session_state["temp_selected_software"] = st.session_state["selected_software"]

        def update_selected_software():
            st.session_state["selected_software"] = st.session_state["temp_selected_software"]
        # Box seletor do software de simulação
        simulation_softwares = ["Ansys Fluent", "OptimusLap",
                                "SolidWorks ",  "N/A"]
        st.selectbox(
            "Simulation software used:",
            options=simulation_softwares,
            key="temp_selected_software",
            index=simulation_softwares.index(
                st.session_state["selected_software"]),
            on_change=update_selected_software
        )
