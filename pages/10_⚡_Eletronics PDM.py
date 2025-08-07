import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st
import os

# ----------------------------------------------------------------------------------------------------------------------#
# CONFIG PAGE
# ----------------------------------------------------------------------------------------------------------------------#
st.set_page_config(page_title="Power Distribution Module", layout="wide")
st.title("Power Distribution Module")
st.divider()
tabs = st.tabs(["12V load test", "12V Ripple"])

with tabs[0]:
    # ----------------------------------------------------------------------------------------------------------------------#
    # LAYOUT (PLOT + NOTAS)
    # ----------------------------------------------------------------------------------------------------------------------#
    col_plot, col_obs = st.columns([2.5, 1])

    with col_plot:
        # ----------------------------------------------------------------------------------------------------------------------#
        # CONFIGURAÇÃO DOS ARQUIVOS
        # ----------------------------------------------------------------------------------------------------------------------#
        base_path = r"C:\Users\João Vitor\Desktop\Joao Vitor Rodrigues\FACULDADE\Iron Races\Software de analise de dados\PDM"
        arquivos = ["12_1A.csv", "12V_2A.csv", "12V_3A.csv", "12V_4A.csv"]

        cores = ["cyan", "magenta", "orange", "lime"]
        fig = sp.make_subplots(
            rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.06)

        for nome_arquivo, cor in zip(arquivos, cores):
            caminho = os.path.join(base_path, nome_arquivo)

            if not os.path.exists(caminho):
                st.warning(f"❌ File not found: {nome_arquivo}")
                continue

            df = pd.read_csv(caminho, header=None)

            try:
                df = df.iloc[:, -3:-1]  # antepenúltima e penúltima
                df.columns = ['time', 'voltage']
                df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

                # Alinha o tempo inicial para zero
                df['time'] = df['time'] - df['time'].iloc[0]

                # Adiciona ao gráfico
                fig.add_trace(go.Scatter(
                    x=df['time'],
                    y=df['voltage'],
                    mode='lines',
                    name=nome_arquivo.replace(".csv", ""),
                    line=dict(color=cor, width=2)
                ), row=1, col=1)

            except Exception as e:
                st.error(f"⚠️ Error reading file {nome_arquivo}: {e}")

        # ----------------------------------------------------------------------------------------------------------------------#
        # CONFIGURAÇÃO VISUAL DO GRÁFICO
        # ----------------------------------------------------------------------------------------------------------------------#
        fig.update_layout(
            title="Load increase",
            hovermode="x unified",
            height=500,
            showlegend=True,
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font=dict(color="white"),
            margin=dict(l=20, r=20, t=40, b=30),
            legend=dict(orientation="h", y=1.1, x=0.5,
                        xanchor="center", yanchor="bottom")
        )

        fig.update_xaxes(
            title_text="Time [s]", showgrid=True, gridcolor="gray", zeroline=False)
        fig.update_yaxes(
            title_text="Voltage [V]", showgrid=True, gridcolor="gray", zeroline=False)

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------------------------------------------------------------------------#
    # PAINEL DE NOTAS
    # ----------------------------------------------------------------------------------------------------------------------#
    with col_obs:
        if "pdm_notes" not in st.session_state:
            st.session_state["pdm_notes"] = ""

        if "temp_pdm_notes" not in st.session_state:
            st.session_state["temp_pdm_notes"] = st.session_state["pdm_notes"]

        def salvar_pdm_notes():
            st.session_state["pdm_notes"] = st.session_state["temp_pdm_notes"]

        st.markdown("### 📝 Engineer's Notes")

        st.text_area(
            label="Observations on voltage behavior:",
            key="temp_pdm_notes",
            height=400,
            placeholder="Write technical insights, anomalies, or trends...",
            on_change=salvar_pdm_notes
        )

with tabs[1]:
    # ----------------------------------------------------------------------------------------------------------------------#
    # LAYOUT (PLOT + NOTAS)
    # ----------------------------------------------------------------------------------------------------------------------#
    col_plot, col_obs = st.columns([2.5, 1])

    with col_plot:
        # Lê o arquivo ripple (apenas os dados)
        ripple_path = os.path.join(base_path, "teste_ripple.csv")

        try:
            df_ripple = pd.read_csv(ripple_path, skiprows=2, header=None)
            df_ripple = df_ripple.iloc[:, [3, 4]]  # colunas de tempo e ripple
            df_ripple.columns = ['time', 'ripple']
            df_ripple = df_ripple.apply(
                pd.to_numeric, errors='coerce').dropna()

            # Cria gráfico do ripple
            fig_ripple = go.Figure()
            fig_ripple.add_trace(go.Scatter(
                x=df_ripple['time'],
                y=df_ripple['ripple'],
                mode='lines',
                name="Ripple",
                line=dict(color='lime', width=2)
            ))

            # Layout do gráfico
            fig_ripple.update_layout(
                title="Voltage Ripple (Stationary regime)",
                xaxis_title="Time [s]",
                yaxis_title="Ripple [V]",
                height=500,
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
                font=dict(color="white"),
                hovermode="x unified",
                showlegend=True,
                margin=dict(l=20, r=20, t=40, b=30),
                legend=dict(orientation="h", y=1.1, x=0.5,
                            xanchor="center", yanchor="bottom")
            )

            fig_ripple.update_xaxes(
                showgrid=True, gridcolor="gray", zeroline=False)
            fig_ripple.update_yaxes(
                showgrid=True, gridcolor="gray", zeroline=False)

            st.plotly_chart(fig_ripple, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Erro ao ler teste_ripple.csv: {e}")

    with col_obs:
        if "ripple_notes" not in st.session_state:
            st.session_state["ripple_notes"] = ""

        if "temp_ripple_notes" not in st.session_state:
            st.session_state["temp_ripple_notes"] = st.session_state["ripple_notes"]

        def salvar_ripple_notes():
            st.session_state["ripple_notes"] = st.session_state["temp_ripple_notes"]

        st.markdown("### 📝 Engineer's Notes")
        st.text_area(
            label="Observations on ripple behavior:",
            key="temp_ripple_notes",
            height=400,
            placeholder="Note spikes, oscillations, filtering issues, etc.",
            on_change=salvar_ripple_notes
        )
