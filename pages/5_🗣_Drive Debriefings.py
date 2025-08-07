import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------
st.set_page_config(page_title="Driver Feedback", layout="wide")
st.title("📋 Driver Feedback")

# -----------------------------
# CRITÉRIOS E AVALIAÇÕES
# -----------------------------
criteria = [
    "Throttle response",
    "Steering",
    "Braking",
    "Gear shifting",
    "Seat + pedal adjustment comfort"
]

ratings = {
    0: "Very Poor",
    1: "Poor",
    2: "Below Average",
    3: "Average",
    4: "Good",
    5: "Very Good",
    6: "Excellent"
}

# -----------------------------
# INICIALIZA session_state PARA FEEDBACK
# -----------------------------
if "driver_feedback" not in st.session_state:
    st.session_state["driver_feedback"] = {}

selected_drivers = st.session_state.get("selected_drivers", [])

if selected_drivers:
    all_tabs = selected_drivers + ["🏎️ Race Pace"]
    tabs = st.tabs(all_tabs)

    for i, driver in enumerate(selected_drivers):
        with tabs[i]:
            st.subheader(f"👤 Evaluation – {driver}")

            # Garante estrutura de armazenamento
            st.session_state["driver_feedback"].setdefault(driver, {})
            st.session_state["driver_comments"] = st.session_state.get(
                "driver_comments", {})

            col_lap, col_left, col_right = st.columns([1, 1, 1.5])
            with col_lap:
                st.markdown("#### 📄 Lap Info")

                if "driver_laps" not in st.session_state:
                    st.session_state["driver_laps"] = {}

                if driver not in st.session_state["driver_laps"]:
                    st.session_state["driver_laps"][driver] = pd.DataFrame({
                        "Lap": [""],
                        "Lap Time (s)": [""]
                    })

                edited_df = st.data_editor(
                    st.session_state["driver_laps"][driver],
                    use_container_width=True,
                    num_rows="dynamic",
                    key=f"{driver}_lap_editor"
                )
                st.session_state["driver_laps"][driver] = edited_df

            with col_left:
                st.markdown("#### 🎚️ Performance Rating")
                for item in criteria:
                    previous_value = st.session_state["driver_feedback"][driver].get(
                        item, 3)
                    st.session_state["driver_feedback"][driver][item] = st.slider(
                        label=item + ":",
                        min_value=0,
                        max_value=6,
                        value=previous_value,
                        key=f"{driver}_{item}_slider"
                    )

            with col_right:
                st.markdown("#### 📈 Radar Chart")
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=[st.session_state["driver_feedback"][driver][c]
                        for c in criteria],
                    theta=criteria,
                    fill='toself',
                    name=driver,
                    line=dict(color='dodgerblue')
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 6])),
                    showlegend=False,
                    margin=dict(t=30, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### 📝 General Comments")
            comment_key = f"{driver}_comment"
            st.session_state["driver_comments"][driver] = st.text_area(
                label="Comment:",
                value=st.session_state["driver_comments"].get(driver, ""),
                key=comment_key,
                height=120,
                placeholder="Write general observations for this driver..."
            )

    with tabs[-1]:  # Última aba: Race Pace
        st.subheader("🏎️ Race Pace Overview")

        all_lap_data = []

        colors = {
            "Jenifer": "blue",
            "Muniz": "red",
            "Rafael": "green",
            "Piloto4": "purple",
            "Piloto5": "orange",
            "Piloto6": "cyan"
        }

        for driver in selected_drivers:
            driver_df = st.session_state.get(
                "driver_laps", {}).get(driver, pd.DataFrame())
            if not driver_df.empty and "Lap" in driver_df.columns and "Lap Time (s)" in driver_df.columns:
                try:
                    df_clean = driver_df.dropna().copy()
                    df_clean["Lap"] = df_clean["Lap"].astype(str)
                    df_clean["Lap Time (s)"] = pd.to_numeric(
                        df_clean["Lap Time (s)"], errors="coerce")
                    df_clean = df_clean.dropna()

                    if not df_clean.empty:
                        all_lap_data.append((driver, df_clean))
                except Exception as e:
                    st.warning(
                        f"⚠️ Could not process lap data for {driver}: {e}")

        if all_lap_data:
            fig = go.Figure()
            for driver, df in all_lap_data:
                fig.add_trace(go.Scatter(
                    x=df["Lap"],
                    y=df["Lap Time (s)"],
                    mode='lines+markers',
                    name=driver,
                    line=dict(color=colors.get(driver, "gray"), width=2)
                ))

            fig.update_layout(
                title="Race Pace Comparison",
                xaxis_title="Lap",
                yaxis_title="Lap Time (s)",
                height=500,
                margin=dict(t=50, b=40),
                legend_title="Driver"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ No valid lap data found to plot Race Pace.")

else:
    st.info("⚠️ No drivers selected. Please select drivers in the main interface.")
