#  ----------------------------------------------------------------------------------------------------------------------#
# LIBRARY IMPORT
# ----------------------------------------------------------------------------------------------------------------------#

# Import library
import streamlit as st  # Streamlit library
import pandas as pd  # Pandas library is used of export excel data.
from streamlit_option_menu import option_menu
from PIL import Image
import json
# ----------------------------------------------------------------------------------------------------------------------#


#  ----------------------------------------------------------------------------------------------------------------------#
# Setup setting
# ----------------------------------------------------------------------------------------------------------------------#
st.title("General Conditions")
# Created mult tabs
tabs = st.tabs(["Weight Information", "External Temperatures"])

with tabs[0]:  # Weight Information
    Imagem_Car = Image.open('./Images/CarroBranco.png')
    Imagem_Drive = Image.open('./Images/PilotoBranca.png')
    Imagem_Fuel = Image.open('./Images/combustivelBranco.png')

    # Initialize dictionary to store data
    if "driver_data" not in st.session_state:
        st.session_state["driver_data"] = {}

    for i, driver in enumerate(st.session_state.selected_drivers):
        if i >= 1:
            st.divider()

        st.markdown(f"### 👤 Driver: {driver}")
        Colune1, Colune2, Colune3 = st.columns(3)

        with Colune1:
            Col1a, Col1b = st.columns([0.7, 0.3])
            with Col1a:
                car_weight = st.number_input(
                    f"Car (Kg) – {driver}",
                    min_value=0.0,
                    step=0.5,
                    value=st.session_state["driver_data"].get(
                        driver, {}).get("Car (Kg)", 0.0),
                    key=f"car_{driver}"
                )
            with Col1b:
                st.image(Imagem_Car, use_container_width=False, width=60)

        with Colune2:
            Col2a, Col2b = st.columns([0.7, 0.3])
            with Col2a:
                driver_weight = st.number_input(
                    f"Driver (Kg) – {driver}",
                    min_value=0.0,
                    step=0.5,
                    value=st.session_state["driver_data"].get(
                        driver, {}).get("Driver (Kg)", 0.0),
                    key=f"driver_{driver}"
                )
            with Col2b:
                st.image(Imagem_Drive, use_container_width=False, width=50)

        with Colune3:
            Col3a, Col3b = st.columns([0.7, 0.3])
            with Col3a:
                fuel = st.number_input(
                    f"Fuel (L) – {driver}",
                    min_value=0.0,
                    step=0.5,
                    value=st.session_state["driver_data"].get(
                        driver, {}).get("Fuel (L)", 0.0),
                    key=f"fuel_{driver}"
                )
            with Col3b:
                st.image(Imagem_Fuel, use_container_width=False, width=50)

        # ✅ Updates data in session_state with current values
        st.session_state["driver_data"][driver] = {
            "Car (Kg)": car_weight,
            "Driver (Kg)": driver_weight,
            "Fuel (L)": fuel
        }


with tabs[1]:  # External Temperatures
    Imagem_Track = Image.open('./Images/PistaBranca.png')
    Imagem_AirTemp = Image.open('./Images/TemperaturaBranca.png')

    # Initialize dictionary to store data
    if "external_temps" not in st.session_state:
        st.session_state["external_temps"] = {}

    for i, driver in enumerate(st.session_state.selected_drivers):
        if i >= 1:
            st.divider()

        st.markdown(f"### 👤 Drive: {driver}")
        Colune1, Colune2 = st.columns(2)

        with Colune1:
            Col1a, Col1b = st.columns([0.7, 0.3])
            with Col1a:
                track_temp = st.number_input(
                    f"Track temperature (℃) – {driver}",
                    min_value=-10.0,
                    max_value=100.0,
                    step=0.5,
                    value=st.session_state["external_temps"].get(
                        driver, {}).get("Track (℃)", 0.0),
                    key=f"track_temp_{driver}"
                )
            with Col1b:
                st.image(Imagem_Track, use_container_width=False, width=50)

        with Colune2:
            Col2a, Col2b = st.columns([0.7, 0.3])
            with Col2a:
                air_temp = st.number_input(
                    f"Air temperature (℃) – {driver}",
                    min_value=-10.0,
                    max_value=100.0,
                    step=0.5,
                    value=st.session_state["external_temps"].get(
                        driver, {}).get("Air (℃)", 0.0),
                    key=f"air_temp_{driver}"
                )
            with Col2b:
                st.image(Imagem_AirTemp, use_container_width=False, width=50)

        # ✅ Saves data in session_state
        st.session_state["external_temps"][driver] = {
            "Track (℃)": track_temp,
            "Air (℃)": air_temp
        }
