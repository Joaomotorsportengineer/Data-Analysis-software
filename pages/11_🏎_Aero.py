import streamlit as st
from PIL import Image
from pathlib import Path


# Carregar vídeo ou imagem
try:
    video_path = "./Videos/aero.mp4"
except FileNotFoundError:
    video_path = None

# Inicializar estado persistente
if "selected_software" not in st.session_state:
    st.session_state["selected_software"] = "Ansys Fluent"

if "temp_selected_software" not in st.session_state:
    st.session_state["temp_selected_software"] = st.session_state["selected_software"]


def update_selected_software():
    st.session_state["selected_software"] = st.session_state["temp_selected_software"]


st.title("Aerodynamics")
st.divider()

tabs = st.tabs(["Theoretical data of aero",
               "Straightline testing - Drag measurement", "-", "-"])

with tabs[0]:
    col_info, col_img = st.columns([1, 3])

    with col_info:
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

        # Campo de entrada de velocidade de simulação
        st.text_input(
            "Simulation speed (km/h):",
            key="temp_simulation_speed",
            value=st.session_state.get("simulation_speed", ""),
            on_change=lambda: st.session_state.update(
                {"simulation_speed": st.session_state["temp_simulation_speed"]}
            )
        )

        # Campo de entrada de área frontal
        st.text_input(
            "Front area (m²):",
            key="temp_front_area",
            value=st.session_state.get("front_area", ""),
            on_change=lambda: st.session_state.update(
                {"front_area": st.session_state["temp_front_area"]}
            )
        )

        # Campo de entrada de força de arrasto
        st.text_input(
            "Drag force (N):",
            key="temp_drag_force",
            value=st.session_state.get("drag_force", ""),
            on_change=lambda: st.session_state.update(
                {"drag_force": st.session_state["temp_drag_force"]}
            )
        )

        # Campo de entrada do coeficiente Cd
        st.text_input(
            "Cd coefficient:",
            key="temp_cd_coefficient",
            value=st.session_state.get("cd_coefficient", ""),
            on_change=lambda: st.session_state.update(
                {"cd_coefficient": st.session_state["temp_cd_coefficient"]}
            )
        )

        # Campo de entrada da densidade do ar
        st.text_input(
            "Air density (kg/m³):",
            key="temp_air_density",
            value=st.session_state.get("air_density", ""),
            on_change=lambda: st.session_state.update(
                {"air_density": st.session_state["temp_air_density"]}
            )
        )

        # Campo de entrada da massa do veículo
        st.text_input(
            "Vehicle mass (kg):",
            key="temp_vehicle_mass",
            value=st.session_state.get("vehicle_mass", ""),
            on_change=lambda: st.session_state.update(
                {"vehicle_mass": st.session_state["temp_vehicle_mass"]}
            )
        )

    with col_img:
     #    video_path = Path("./Videos/aero.mp4")
        #      if video_path.exists():
       #          st.video(str(video_path))
      #       else:
      #           st.warning("⚠️ Vídeo 'aero.mp4' não encontrado na pasta ./Videos/")

        # Verifica se a imagem existe e exibe
        image_path = Path("./Videos/Aero.png")

        if image_path.exists():
            image = Image.open(image_path)
            st.image(image, caption="Aero Simulation",
                     use_container_width=True)

        else:
            st.warning("⚠️ Imagem 'Aero.png' não encontrada na pasta ./Images/")
