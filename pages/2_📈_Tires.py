# TIRES ANALYSIS WITH MANUAL INPUT
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# -----------------------------
# INITIAL SETUP
# # -----------------------------
Tires_Temp_Tangent = 85
Tires_Pressu_Tangent = 28
Variation = 5
SurfaceTires = ['Outside', 'Middle', 'Inside']

if "tires_temp_manual" not in st.session_state:
    st.session_state["tires_temp_manual"] = {}

if "tires_press_manual" not in st.session_state:
    st.session_state["tires_press_manual"] = {}

if "setup_manual" not in st.session_state:
    st.session_state["setup_manual"] = {
        driver: {
            "Camber Front": -1.5,
            "Camber Rear": -2.0
        } for driver in st.session_state.get("selected_drivers", ["Jenifer"])
    }

selected_drivers = st.session_state.get("selected_drivers", ["Jenifer"])
st.title("Tires Performance")

# -----------------------------
# TABS
# -----------------------------
tabs = st.tabs(["📝 Manual Input", "📈 Temperature Graphs", "📊 KPIs"])

# -----------------------------
# TAB 1 – MANUAL INPUT
# -----------------------------
with tabs[0]:

    for driver in selected_drivers:
        st.markdown(f"### 👤 Driver: {driver}")

        for momento in ["Start", "End"]:
            st.markdown(
                f"#### 🕒 {'Before Test' if momento == 'Start' else 'After Test'}")

            # Obtem dados anteriores se já existirem
            tire_temp_data = st.session_state["tires_temp_manual"].get(
                driver, {}).get(momento, {})
            tire_press_data = st.session_state["tires_press_manual"].get(
                driver, {}).get(momento, {})

            col_esq, col_dir = st.columns(2)

            # Lado esquerdo
            for tire in ["Rear left", "Front left"]:
                with col_esq:
                    cols = st.columns(5)
                    with cols[0]:
                        st.text(tire)
                    temp_values = []
                    for i, surface in enumerate(SurfaceTires):
                        with cols[i+1]:
                            key = f"{driver}_{momento}_{tire}_temp_{surface}"
                            val = st.number_input(
                                f"{tire} Temp - {surface}",
                                min_value=0.0,
                                max_value=150.0,
                                step=0.5,
                                key=key,
                                label_visibility="collapsed",
                                value=tire_temp_data.get((tire, surface), 80.0)
                            )
                            temp_values.append(val)
                    for surface, val in zip(SurfaceTires, temp_values):
                        st.session_state["tires_temp_manual"].setdefault(
                            driver, {}).setdefault(momento, {})[(tire, surface)] = val

                    press_key = f"{driver}_{momento}_{tire}_pressure"
                    pressure = st.number_input(
                        f"{tire} Pressure (psi)",
                        min_value=0.0,
                        max_value=50.0,
                        step=0.1,
                        key=press_key,
                        value=tire_press_data.get(tire, 28.0)
                    )
                    st.session_state["tires_press_manual"].setdefault(
                        driver, {}).setdefault(momento, {})[tire] = pressure

            # Lado direito
            for tire in ["Rear right", "Front right"]:
                with col_dir:
                    cols = st.columns(5)
                    with cols[0]:
                        st.text(tire)
                    temp_values = []
                    for i, surface in enumerate(SurfaceTires):
                        with cols[i+1]:
                            key = f"{driver}_{momento}_{tire}_temp_{surface}"
                            val = st.number_input(
                                f"{tire} Temp - {surface}",
                                min_value=0.0,
                                max_value=150.0,
                                step=0.5,
                                key=key,
                                label_visibility="collapsed",
                                value=tire_temp_data.get((tire, surface), 80.0)
                            )
                            temp_values.append(val)
                    for surface, val in zip(SurfaceTires, temp_values):
                        st.session_state["tires_temp_manual"].setdefault(
                            driver, {}).setdefault(momento, {})[(tire, surface)] = val

                    press_key = f"{driver}_{momento}_{tire}_pressure"
                    pressure = st.number_input(
                        f"{tire} Pressure (psi)",
                        min_value=0.0,
                        max_value=50.0,
                        step=0.1,
                        key=press_key,
                        value=tire_press_data.get(tire, 28.0)
                    )
                    st.session_state["tires_press_manual"].setdefault(
                        driver, {}).setdefault(momento, {})[tire] = pressure


# -----------------------------
# TAB 2 – TEMPERATURE GRAPHS
# -----------------------------
with tabs[1]:
    st.markdown("### 📊Temperature Graphs")

    data = []
    for driver in selected_drivers:
        tire_data = st.session_state["tires_temp_manual"][driver].get("End", {
        })
        data.append({
            "Surface": SurfaceTires,
            "Rear_left": [tire_data.get(("Rear left", s), 0.0) for s in SurfaceTires],
            "Rear_right": [tire_data.get(("Rear right", s), 0.0) for s in SurfaceTires],
            "Front_left": [tire_data.get(("Front left", s), 0.0) for s in SurfaceTires],
            "Front_right": [tire_data.get(("Front right", s), 0.0) for s in SurfaceTires],
            "Driver": [driver] * len(SurfaceTires)
        })

    combined_df = pd.concat([pd.DataFrame(d) for d in data])
    pilot_colors = {"Jenifer": "blue", "Muniz": "red", "Rafael": "green"}

    def plot_tire_temp(col_name, label):
        fig = go.Figure()
        for driver in combined_df["Driver"].unique():
            df = combined_df[combined_df["Driver"] == driver]
            fig.add_trace(go.Scatter(
                x=df["Surface"],
                y=df[col_name],
                name=driver,
                fill="tozeroy",
                line=dict(color=pilot_colors.get(driver, "gray"))
            ))
        fig.update_layout(title=label, xaxis_title="Surface",
                          yaxis_title="Temperature (°C)")
        return fig

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(plot_tire_temp("Rear_left", "Rear Left"))
    with col2:
        st.plotly_chart(plot_tire_temp("Rear_right", "Rear Right"))
    with col3:
        st.plotly_chart(plot_tire_temp("Front_left", "Front Left"))
    with col4:
        st.plotly_chart(plot_tire_temp("Front_right", "Front Right"))


# -----------------------------
# TAB 3 – KPIs
# -----------------------------
with tabs[2]:
    st.markdown("### 📊 KPIs")

    for driver in selected_drivers:
        st.markdown(f"#### 👤 Drive: {driver}")
        st.markdown("**Pressure analysis:**")

        pressures = st.session_state["tires_press_manual"][driver].get("End", {
        })
        cols = st.columns(4)
        for i, tire in enumerate(["Rear left", "Rear right", "Front left", "Front right"]):
            press = pressures.get(tire, 0.0)
            if abs(press - Tires_Pressu_Tangent) <= 1:
                status = "Ideal 🟢"
            elif press > Tires_Pressu_Tangent:
                status = "Alta 🔴"
            else:
                status = "Baixa 🔵"
            with cols[i]:
                st.metric(label=tire, value=f"{press:.1f} psi", delta=status)

        tire_data = st.session_state["tires_temp_manual"][driver].get("End", {
        })
        setup_data = st.session_state["setup_manual"].get(driver, {})

        df_temp = pd.DataFrame({
            "Rear_left": [tire_data.get(("Rear left", s), 0.0) for s in SurfaceTires],
            "Rear_right": [tire_data.get(("Rear right", s), 0.0) for s in SurfaceTires],
            "Front_left": [tire_data.get(("Front left", s), 0.0) for s in SurfaceTires],
            "Front_right": [tire_data.get(("Front right", s), 0.0) for s in SurfaceTires],
            "Position": [1, 2, 3]
        })

        def calc_camber_diff(lst):
            return lst[2] - lst[0]

        camber_real = {
            "Rear_left": calc_camber_diff(df_temp["Rear_left"].tolist()),
            "Rear_right": calc_camber_diff(df_temp["Rear_right"].tolist()),
            "Front_left": calc_camber_diff(df_temp["Front_left"].tolist()),
            "Front_right": calc_camber_diff(df_temp["Front_right"].tolist()),
        }
        st.markdown("**Camber analysis:**")

        def camber_result(real, ref):
            if real == ref:
                return "Ok 🟢"
            elif real > ref:
                return "Too Little 🔵"
            else:
                return "Too Much 🔴 "

        camber_ref = {
            "Rear_left": setup_data.get("Camber Rear", -2.0),
            "Rear_right": setup_data.get("Camber Rear", -2.0),
            "Front_left": setup_data.get("Camber Front", -1.5),
            "Front_right": setup_data.get("Camber Front", -1.5)
        }

        c1, c2, c3, c4 = st.columns(4)
        for col, tire in zip([c1, c2, c3, c4], camber_real):
            col.metric(label=tire.replace("_", " ").title(),
                       value=f"{camber_real[tire]:.1f}°",
                       delta=camber_result(camber_real[tire], camber_ref[tire]))

        st.markdown("**Temperature Window Analysis:**")
        temp_max = Tires_Temp_Tangent * 1.05
        temp_min = Tires_Temp_Tangent * 0.95

        def avg_status(v):
            if v < temp_min:
                return "Cold 🔵"
            elif v > temp_max:
                return "Hot 🔴"
            return "Ok 🟢"

        avg_vals = {k: round(df_temp[k].mean(), 1)
                    for k in df_temp.columns if k != "Position"}

        c1, c2, c3, c4 = st.columns(4)
        for col, tire in zip([c1, c2, c3, c4], avg_vals):
            col.metric(label=tire.replace("_", " ").title(),
                       value=f"{avg_vals[tire]}°C",
                       delta=avg_status(avg_vals[tire]))

        st.markdown("**Tire Inflation Analysis:**")

        def inflation_status(t):
            result = (t[1] - t[0]) - (t[2] - t[1])
            if result == 0:
                return "Ok 🟢"
            elif result > 0:
                return "Over 🔴"
            else:
                return "Under 🔵"

        infl_ind = {
            "Rear_left": inflation_status(df_temp["Rear_left"].tolist()),
            "Rear_right": inflation_status(df_temp["Rear_right"].tolist()),
            "Front_left": inflation_status(df_temp["Front_left"].tolist()),
            "Front_right": inflation_status(df_temp["Front_right"].tolist()),
        }

        c1, c2, c3, c4 = st.columns(4)
        for col, tire in zip([c1, c2, c3, c4], infl_ind):
            col.metric(label=tire.replace(
                "_", " ").title(), value=infl_ind[tire])
        st.divider()
