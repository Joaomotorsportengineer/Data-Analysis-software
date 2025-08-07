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

tabs = st.tabs(["Theoretical data of chassi",
               "Torsional stiffness test", "-", "-"])

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

        st.text_input(
            "Material:",
            key="temp_Material",
            value=st.session_state.get("Material", ""),
            on_change=lambda: st.session_state.update(
                {"Material": st.session_state["temp_Material"]}
            )
        )
        st.text_input(
            "Elastic Modulus :",
            key="temp_Elastic Modulus ",
            value=st.session_state.get("Elastic Modulus ", ""),
            on_change=lambda: st.session_state.update(
                {"Elastic Modulus ": st.session_state["temp_Elastic Modulus "]}
            )
        )
        st.text_input(
            "Critical point 1:",
            key="temp_Critical_point",
            value=st.session_state.get("Critical_point", ""),
            on_change=lambda: st.session_state.update(
                {"Critical_point": st.session_state["temp_Critical_point"]}
            )
        )
        st.text_input(
            "Critical point 2:",
            key="temp_Critical_point2",
            value=st.session_state.get("Critical_point2", ""),
            on_change=lambda: st.session_state.update(
                {"Critical_point2": st.session_state["temp_Critical_point2"]}
            )
        )
        st.text_input(
            "Critical point 3:",
            key="temp_Critical_point3",
            value=st.session_state.get("Critical_point3", ""),
            on_change=lambda: st.session_state.update(
                {"Critical_point3": st.session_state["temp_Critical_point3"]}
            )
        )
        st.text_input(
            "Applied load:",
            key="temp_Load",
            value=st.session_state.get("Load", ""),
            on_change=lambda: st.session_state.update(
                {"Load": st.session_state["temp_Load"]}
            )
        )
