#  ----------------------------------------------------------------------------------------------------------------------#
# LIBRARY IMPORT
# ----------------------------------------------------------------------------------------------------------------------#

# Import library
import streamlit as st  # Streamlit library
import pandas as pd  # Pandas library is used of export excel data.
from streamlit_option_menu import option_menu
from PIL import Image

# ----------------------------------------------------------------------------------------------------------------------#


#  ----------------------------------------------------------------------------------------------------------------------#
# Setup setting
# ----------------------------------------------------------------------------------------------------------------------#
st.title("Setup Settings")


# Inicializa o dicionário de setup manual se ainda não existir
if "setup_manual" not in st.session_state:
    st.session_state["setup_manual"] = {}

Brake = Image.open('./Images/FreioBranco.png')
Camber = Image.open('./Images/CamberPos.png')
Toe = Image.open('./Images/ToeIn.png')
Coil_Spring = Image.open('./Images/Coil_Spring.png')
Rebound = Image.open('./Images/Rebound.png')
Compression = Image.open('./Images/Compression.png')
DHX = Image.open('./Images/DHX.png')


tabs = st.tabs(["Brake", "Suspension", "Compression"])

for i, driver in enumerate(st.session_state.selected_drivers):

    if i >= 1:
        st.divider()

    setup_data = st.session_state["setup_manual"].get(driver, {})

    # ───────────────────────────────
    # TAB 1 – BRAKE
    # ───────────────────────────────
    with tabs[0]:

        st.markdown(f"### 🎯 Driver: {driver}")

        col1, col2 = st.columns(2)

        with col1:
            c1, c2 = st.columns([0.75, 0.25])
            with c1:
                brake_front = st.number_input(
                    f"Brake Bias Front (%) – {driver}",
                    min_value=0.0, max_value=100.0, step=0.5,
                    value=setup_data.get("Brake Bias Front", 60.0),
                    key=f"brake_front_{driver}"
                )
            with c2:
                st.image(Brake, width=50)

        with col2:
            brake_rear = 100 - brake_front
            c1, c2 = st.columns([0.75, 0.25])
            with c1:
                st.number_input(
                    f"Brake Bias Rear (%) – {driver}",
                    value=brake_rear,
                    disabled=True,
                    key=f"brake_rear_{driver}"
                )
            with c2:
                st.image(Brake, width=50)

    # ───────────────────────────────
    # TAB 2 – SUSPENSION
    # ───────────────────────────────
    with tabs[1]:
        st.markdown(f"### 🎯 Driver: {driver}")

        col1, col2, col3 = st.columns(3)

        with col1:
            a, b = st.columns([0.75, 0.25])
            with a:
                toe = st.number_input(
                    f"Toe (%) – {driver}", min_value=-10.0, max_value=10.0, step=0.1,
                    value=setup_data.get("Toe", 0.0),
                    key=f"toe_{driver}"
                )
            with b:
                st.image(Toe, width=100)

        with col2:
            a, b = st.columns([0.75, 0.25])
            with a:
                camber_front = st.number_input(
                    f"Camber Front (%) – {driver}", min_value=-10.0, max_value=0.0, step=0.1,
                    value=setup_data.get("Camber Front", -1.5),
                    key=f"camber_front_{driver}"
                )
            with b:
                st.image(Camber, width=100)

        with col3:
            a, b = st.columns([0.75, 0.25])
            with a:
                camber_rear = st.number_input(
                    f"Camber Rear (%) – {driver}", min_value=-10.0, max_value=0.0, step=0.1,
                    value=setup_data.get("Camber Rear", -2.0),
                    key=f"camber_rear_{driver}"
                )
            with b:
                st.image(Camber, width=100)

        col1, col2, col3 = st.columns(3)

        with col1:
            a, b = st.columns([0.75, 0.25])
            with a:
                rebound = st.number_input(
                    f"Rebound (Clicks) – {driver}", min_value=0, max_value=30, step=1,
                    value=setup_data.get("Rebound", 10),
                    key=f"rebound_{driver}"
                )
            with b:
                st.image(Rebound, width=100)

        with col2:
            a, b = st.columns([0.75, 0.25])
            with a:
                preload_rear = st.number_input(
                    f"Preload Rear (mm) – {driver}", min_value=0.0, max_value=50.0, step=0.5,
                    value=setup_data.get("Preload Rear", 10.0),
                    key=f"preload_rear_{driver}"
                )
            with b:
                st.image(Coil_Spring, width=50)

        with col3:
            a, b = st.columns([0.75, 0.25])
            with a:
                preload_front = st.number_input(
                    f"Preload Front (mm) – {driver}", min_value=0.0, max_value=50.0, step=0.5,
                    value=setup_data.get("Preload Front", 10.0),
                    key=f"preload_front_{driver}"
                )
            with b:
                st.image(Coil_Spring, width=50)

    # ───────────────────────────────
    # TAB 3 – COMPRESSION
    # ───────────────────────────────
    with tabs[2]:
        st.markdown(f"### 🎯 Driver: {driver}")

        col1, col2, col3 = st.columns(3)

        with col1:
            a, b = st.columns([0.75, 0.25])
            with a:
                dhx = st.number_input(
                    f"DHX RC4 Air Assist (Psi) – {driver}", min_value=0, max_value=300, step=5,
                    value=setup_data.get("DHX", 100),
                    key=f"dhx_{driver}"
                )
            with b:
                st.image(DHX, width=50)

        with col2:
            a, b = st.columns([0.75, 0.25])
            with a:
                low_comp = st.number_input(
                    f"Low Speed Compression (Clicks) – {driver}", min_value=0, max_value=30, step=1,
                    value=setup_data.get("Low Compression", 8),
                    key=f"low_comp_{driver}"
                )
            with b:
                st.image(Compression, width=100)

        with col3:
            a, b = st.columns([0.75, 0.25])
            with a:
                high_comp = st.number_input(
                    f"High Speed Compression (Clicks) – {driver}", min_value=0, max_value=30, step=1,
                    value=setup_data.get("High Compression", 10),
                    key=f"high_comp_{driver}"
                )
            with b:
                st.image(Compression, width=100)

    st.session_state["setup_manual"][driver] = {
        "Brake Bias Front": brake_front,
        "Brake Bias Rear": brake_rear,
        "Toe": toe,
        "Camber Front": camber_front,
        "Camber Rear": camber_rear,
        "Rebound": rebound,
        "Preload Rear": preload_rear,
        "Preload Front": preload_front,
        "DHX": dhx,
        "Low Compression": low_comp,
        "High Compression": high_comp
    }
