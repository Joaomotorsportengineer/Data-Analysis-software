
# --------------------------------------------------------------------------------------------------
# LIBRARY IMPORT
# --------------------------------------------------------------------------------------------------
from groq import Groq
import io  # ADICIONE NO TOPO DO SCRIPT
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp

from dotenv import load_dotenv
import os


# --------------------------------------------------------------------------------------------------
# TÍTULO DA PÁGINA
# --------------------------------------------------------------------------------------------------
st.title("Vital Signal Analysis")

# --------------------------------------------------------------------------------------------------
# VERIFICA SE OS LOGS E PILOTOS FORAM CARREGADOS
# --------------------------------------------------------------------------------------------------
if "arquivos_carregados" not in st.session_state or not st.session_state["arquivos_carregados"]:
    st.warning("🚨 Nenhum log carregado.")
    st.stop()

if "selected_drivers" not in st.session_state or not st.session_state["selected_drivers"]:
    st.warning("🚨 Nenhum piloto selecionado.")
    st.stop()

# --------------------------------------------------------------------------------------------------
# FUNÇÃO PARA LOCALIZAR O LOG DO PILOTO
# --------------------------------------------------------------------------------------------------


def localizar_log_piloto(piloto):
    for nome_arquivo in st.session_state["arquivos_carregados"]:
        if nome_arquivo.lower().startswith(piloto.lower()):
            try:
                conteudo = st.session_state["arquivos_carregados"][nome_arquivo]
                return pd.read_csv(io.StringIO(conteudo))
            except Exception as e:
                st.error(f"Erro ao ler o log de {piloto}: {e}")
                return None
    st.warning(f"Log não encontrado para o piloto: {piloto}")
    return None


# --------------------------------------------------------------------------------------------------
# ABA PRINCIPAL COM MULTITABS
# --------------------------------------------------------------------------------------------------
abas = st.tabs(["📊 KPI", "📈 X/Y Analysis", "⛽ Oil Pressure",
               "📉 RPM Trend"])

# --------------------------------------------------------------------------------------------------
# ABA KPI
# --------------------------------------------------------------------------------------------------


with abas[0]:
    st.subheader("📊 KPI reports of vital signal")

    # Função com quadrado alinhado usando flexbox
    def format_with_indicator(valor, unidade, lim, precision=1):
        if valor > lim["high"]:
            cor = "#ff1900"  # Red
        elif lim["medium"][0] <= valor <= lim["medium"][1]:
            cor = "#00ff37"  # Green
        else:
            cor = "#0099ff"  # Blue

        return f"""
        <div style="display: flex; align-items: center; gap: 20px; font-family: monospace; padding: 4px 0;">
            <div style="min-width: 70px;">{valor:.{precision}f} {unidade}</div>
            <div style="width: 12px; height: 12px; background-color: {cor}; border-radius: 2px;"></div>
        </div>
        """

    for piloto in st.session_state["selected_drivers"]:
        df_log = localizar_log_piloto(piloto)
        if df_log is None:
            continue

        # Caixinha com nome do piloto
        st.markdown(
            f"""
            <div style="
                display: inline-block;
                padding: 8px 20px;
                margin-top: 0px;
                background-color: #666262;
                border-radius: 4px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                font-size: 16px;
                color: #fcfcfc;
                text-align: center;">
                Driver: {piloto}
            </div>
            """,
            unsafe_allow_html=True
        )

        df_log = df_log.apply(pd.to_numeric, errors='coerce').fillna(0)
        filtered_df = df_log[df_log['Tensão_da_Bateria'] >= 6]

        # Definição dos parâmetros
        thresholds = {
            "Temp._do_motor": {
                "label": "Engine temperature",
                "high": 100, "medium": (70, 100), "unit": "°C"
            },
            "Pressão_de_Óleo": {
                "label": "Engine oil pressure",
                "high": 10, "medium": (1, 10), "unit": "bar"
            },
            "Pressão_de_Combustível": {
                "label": "Fuel pressure",
                "high": 3.5, "medium": (2, 3.5), "unit": "bar"
            },
            "Tensão_da_Bateria": {
                "label": "Battery voltage",
                "high": 14, "medium": (11.5, 14), "unit": "V"
            }
        }

        # Layout visual com colunas
        col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

        with col1:
            st.write("**Type**")
            for var in thresholds:
                st.markdown(
                    f"<div style='padding: 4px 0;'>{thresholds[var]['label']}:</div>", unsafe_allow_html=True)

        with col2:
            st.write("**Max**")
            for var, lim in thresholds.items():
                val = df_log[var].max()
                st.markdown(format_with_indicator(
                    val, lim["unit"], lim), unsafe_allow_html=True)

        with col3:
            st.write("**Min**")
            for var, lim in thresholds.items():
                val = filtered_df[var].min()
                st.markdown(format_with_indicator(
                    val, lim["unit"], lim), unsafe_allow_html=True)

        with col4:
            st.write("**Avg**")
            for var, lim in thresholds.items():
                val = df_log[var].mean()
                st.markdown(format_with_indicator(
                    val, lim["unit"], lim), unsafe_allow_html=True)

        st.divider()


with abas[1]:
    st.subheader("📈 X/Y Analysis")

    # Layout em duas colunas: gráfico + comentários
    col_grafico, col_obs = st.columns([4, 1])

    with col_grafico:
        # Mapeamento de nomes bonitos
        variable_driving_Log = ['RPM', 'T.Motor',
                                'Bateria', 'P.Óleo', 'P.Combustível']
        variable_map = {
            'RPM': 'RPM',
            'T.Motor': 'Temp._do_motor',
            'Bateria': 'Tensão_da_Bateria',
            'P.Óleo': 'Pressão_de_Óleo',
            'P.Combustível': 'Pressão_de_Combustível'
        }
        labels = {
            'RPM': 'RPM',
            'T.Motor': 'Engine Temp.',
            'Bateria': 'Battery',
            'P.Óleo': 'Oil Pres.',
            'P.Combustível': 'Fuel Pres.'
        }

        # Thresholds usados para linhas limite
        thresholds = {
            "Temp._do_motor": {"high": 100, "medium": (70, 100)},
            "Pressão_de_Óleo": {"high": 10, "medium": (1, 10)},
            "Pressão_de_Combustível": {"high": 4, "medium": (2, 4)},
            "Tensão_da_Bateria": {"high": 14, "medium": (10, 14)}
        }

        fig = sp.make_subplots(
            rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.06
        )

        colors = {
            "Jenifer": "blue",
            "Muniz": "red",
            "Rafael": "green",
            "Piloto4": "purple"
        }

        for driver in st.session_state["selected_drivers"]:
            df = localizar_log_piloto(driver)
            if df is None or "Distância" not in df.columns:
                st.warning(f"❌ Missing or malformed data for driver: {driver}")
                continue

            df = df.apply(pd.to_numeric, errors='coerce').fillna(
                0).astype(float)
            driver_color = colors.get(driver, 'orange')

            for i, var in enumerate(variable_driving_Log):
                signal = variable_map[var]
                y = df[signal]

                fig.add_trace(go.Scatter(
                    x=df['Distância'],
                    y=y,
                    mode='lines',
                    name=f"{driver} – {labels[var]}",
                    line=dict(color=driver_color),
                    showlegend=True if i == 0 else False
                ), row=i+1, col=1)

                # Adiciona limites, se aplicável
                if signal in thresholds:
                    lim = thresholds[signal]

                    fig.add_trace(go.Scatter(
                        x=df['Distância'],
                        y=[lim['high']] * len(df),
                        mode='lines',
                        name=f"{labels[var]} max",
                        line=dict(color='orange', dash='dot', width=1),
                        showlegend=(i == 0)
                    ), row=i+1, col=1)

                    fig.add_trace(go.Scatter(
                        x=df['Distância'],
                        y=[lim['medium'][0]] * len(df),
                        mode='lines',
                        name=f"{labels[var]} min",
                        line=dict(color='lightblue', dash='dot', width=1),
                        showlegend=(i == 0)
                    ), row=i+1, col=1)

        fig.update_layout(
            title="Vital Signal Analysis",
            hovermode="x unified",
            height=700,
            showlegend=True,
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font=dict(color="white"),
            legend=dict(orientation="v", y=1, x=1,
                        xanchor="left", yanchor="top")
        )

        # Ocultar ticks e nomear cada subplot
        fig.update_yaxes(showticklabels=False)
        for j, var in enumerate(variable_driving_Log, start=1):
            fig.update_yaxes(title_text=labels[var], row=j, col=1)

        st.plotly_chart(fig, use_container_width=True)

    with col_obs:
        if "xy_analysis_notes" not in st.session_state:
            st.session_state["xy_analysis_notes"] = ""

        if "temp_xy_analysis_notes" not in st.session_state:
            st.session_state["temp_xy_analysis_notes"] = st.session_state["xy_analysis_notes"]

        def salvar_xy_notes():
            st.session_state["xy_analysis_notes"] = st.session_state["temp_xy_analysis_notes"]

        st.markdown("### 📝 Engineer's Notes")

        st.text_area(
            label="Observations on signal behavior:",
            key="temp_xy_analysis_notes",
            height=500,
            placeholder="Write technical insights, anomalies, or expected trends here...",
            on_change=salvar_xy_notes
        )


with abas[2]:
    st.subheader("⛽ Oil Pressure Analysis")

    curva_minima = {
        'RPM': [0, 1000, 1500, 3000, 4500, 6000, 7500, 9000, 10500],
        'OilMin': [0, 0.7, 0.85, 1.3, 2.3, 3.9, 4.5, 4.8, 5]
    }

    def interpolar_pressao_minima(rpm):
        return np.interp(rpm, curva_minima['RPM'], curva_minima['OilMin'])

    for driver in st.session_state["selected_drivers"]:
        df = localizar_log_piloto(driver)
        if df is None:
            continue

        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
        df['Pressao_Minima_Interpolada'] = interpolar_pressao_minima(df['RPM'])

        # Cálculos de acelerações
        sample_time = 1 / 100
        g = 9.81
        df['AccLongitudinal'] = (
            (df['Velocidade_de_referência'] / 3.6).diff() / sample_time) / g
        cond_erro_spike = (df['Velocidade_de_referência'] > 30) & (
            df['AccLongitudinal'].abs() <= 10)
        cond_parado = df['AccLongitudinal'].abs() <= 0.05
        cond_vel_alta_sem_acc = (df['Velocidade_de_referência'] > 30) & (
            df['AccLongitudinal'].abs() <= 0.05)
        cond_erro_vel = cond_vel_alta_sem_acc | cond_erro_spike

        df['Velocidade_corrigida'] = df['Velocidade_de_referência']
        df.loc[cond_parado, 'Velocidade_corrigida'] = np.nan
        df.loc[cond_vel_alta_sem_acc, 'Velocidade_corrigida'] = 0

        df['Velocidade_corrigida'] = df['Velocidade_corrigida'].interpolate().fillna(
            method='bfill').fillna(method='ffill')
        df['Velocidade_corrigida'] = df['Velocidade_corrigida'].rolling(
            window=80, center=True).mean().fillna(method='bfill').fillna(method='ffill')

        df['AccLongitudinal'] = (
            (df['Velocidade_corrigida'] / 3.6).diff() / sample_time) / g
        raio_skidpad = 8.5
        df['AccLateral'] = (
            ((df['Velocidade_corrigida'] / 3.6) ** 2) / raio_skidpad) / g
        df['G_Comb'] = np.sqrt(df['AccLongitudinal'] **
                               2 + df['AccLateral'] ** 2)

        df['AccLongitudinal'] = df['AccLongitudinal'].rolling(
            window=30, center=True).mean().fillna(method='bfill').fillna(method='ffill')
        df['AccLateral'] = df['AccLateral'].rolling(
            window=20, center=True).mean().fillna(method='bfill').fillna(method='ffill')
        df['G_Comb'] = df['G_Comb'].rolling(window=30, center=True).mean().fillna(
            method='bfill').fillna(method='ffill')

        df['Alerta_Pressao'] = df['Pressão_de_Óleo'] < df['Pressao_Minima_Interpolada']
        alerts = df[df['Alerta_Pressao']].copy()

        col_graf, col_obs = st.columns([4, 1])

        with col_graf:
            st.markdown(f"### 👤 Driver: {driver}")

            opcao = st.selectbox(
                f"📊 Select chart for {driver}",
                options=[
                    "Pressure vs Distance",
                    "Oil Pressure vs RPM with Trend",
                    "Critical Points: Pressure vs Accelerations"
                ],
                key=f"chart_option_{driver}"
            )

            if opcao == "Pressure vs Distance":
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=df['TIME'], y=df['Pressão_de_Óleo'],
                                          mode='lines', name='Oil Pres.', line=dict(color='blue')))
                fig1.add_trace(go.Scatter(x=df['TIME'], y=df['Pressao_Minima_Interpolada'],
                                          mode='lines', name='Oil Pres. Min', line=dict(color='darkcyan', dash='dot')))
                fig1.update_layout(title="Oil Pressure vs. Distance",
                                   xaxis_title="Distance (m)", yaxis_title="Pressure (bar)",
                                   plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                                   font=dict(color='white'))
                st.plotly_chart(fig1, use_container_width=True)

            elif opcao == "Oil Pressure vs RPM with Trend":
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=df['RPM'], y=df['Pressão_de_Óleo'],
                                          mode='markers', name='Oil Pres.',
                                          marker=dict(size=4, color=driver_color)))
                coef = np.polyfit(df['RPM'], df['Pressão_de_Óleo'], 2)
                poly = np.poly1d(coef)
                rpm_lin = np.linspace(df['RPM'].min(), df['RPM'].max(), 100)
                fig3.add_trace(go.Scatter(x=rpm_lin, y=poly(rpm_lin),
                                          mode='lines', name='Trend',
                                          line=dict(color='lightblue', dash='dash')))
                fig3.add_trace(go.Scatter(x=df['RPM'], y=df['Pressao_Minima_Interpolada'],
                                          mode='markers', name='Oil Pres. Min',
                                          marker=dict(color='darkcyan', symbol='x')))
                fig3.update_layout(title="Oil Pressure vs. RPM with Trend",
                                   xaxis_title="RPM", yaxis_title="Pressure (bar)",
                                   plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                                   font=dict(color='white'))
                st.plotly_chart(fig3, use_container_width=True)

            elif opcao == "Critical Points: Pressure vs Accelerations":
                fig_alertas = sp.make_subplots(
                    rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.09
                )

                fig_alertas.add_trace(go.Scatter(x=df['TIME'], y=df['AccLongitudinal'],
                                                 mode='lines', name='Acc. Longitudinal',
                                                 line=dict(color='blue')), row=1, col=1)

                fig_alertas.add_trace(go.Scatter(x=alerts['TIME'], y=alerts['AccLongitudinal'],
                                                 mode='markers', name='Critical – Long',
                                                 marker=dict(color='red', size=6)), row=1, col=1)

                fig_alertas.add_trace(go.Scatter(x=df['TIME'], y=df['AccLateral'],
                                                 mode='lines', name='Acc. Lateral',
                                                 line=dict(color='cyan')), row=2, col=1)

                fig_alertas.add_trace(go.Scatter(x=alerts['TIME'], y=alerts['AccLateral'],
                                                 mode='markers', name='Critical – Lat',
                                                 marker=dict(color='red', size=6)), row=2, col=1)

                fig_alertas.add_trace(go.Scatter(x=df['TIME'], y=df['G_Comb'],
                                                 mode='lines', name='G_Comb',
                                                 line=dict(color='green')), row=3, col=1)

                fig_alertas.add_trace(go.Scatter(x=alerts['TIME'], y=alerts['G_Comb'],
                                                 mode='markers', name='Critical – G_Comb',
                                                 marker=dict(color='red', size=6)), row=3, col=1)

                fig_alertas.update_layout(
                    title="🚨 Critical Points: Oil Pressure vs Accelerations",
                    height=800,
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    font=dict(color='white'),
                    showlegend=True
                )
                fig_alertas.update_yaxes(
                    title_text="Long. Acc (g)", row=1, col=1)
                fig_alertas.update_yaxes(
                    title_text="Lat. Acc (g)", row=2, col=1)
                fig_alertas.update_yaxes(
                    title_text="Comb. Acc (g)", row=3, col=1)
                fig_alertas.update_xaxes(title_text="Time (s)", row=3, col=1)

                st.plotly_chart(fig_alertas, use_container_width=True)

        with col_obs:
            if "Oil_Pressure_Analysis_note" not in st.session_state:
                st.session_state["Oil_Pressure_Analysis_note"] = ""

            if "temp_Oil_Pressure_Analysis_note" not in st.session_state:
                st.session_state["temp_Oil_Pressure_Analysis_note"] = st.session_state["Oil_Pressure_Analysis_note"]

            def salvar_xy_notes():
                st.session_state["Oil_Pressure_Analysis_note"] = st.session_state["temp_Oil_Pressure_Analysis_note"]

            st.markdown("### 📝 Engineer's Notes")

            st.text_area(
                label="Observations on signal behavior:",
                key="temp_Oil_Pressure_Analysis_note",
                height=500,
                placeholder="Write technical insights, anomalies, or expected trends here...",
                on_change=salvar_xy_notes
            )


with abas[3]:
    st.subheader("📉 RPM Trend")

    for driver in st.session_state["selected_drivers"]:
        df = localizar_log_piloto(driver)
        if df is None or "RPM" not in df.columns:
            st.warning(f"❌ Missing or invalid data for driver: {driver}")
            continue

        df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)
        driver_color = colors.get(driver, 'orange')

        fig_rpm = go.Figure()
        fig_rpm.add_trace(go.Histogram(
            x=df['RPM'],
            nbinsx=80,
            marker=dict(color=driver_color),
            name=f'{driver} - RPM'
        ))

        fig_rpm.update_layout(
            title='RPM Distribution Histogram',
            xaxis_title='RPM',
            yaxis_title='Occurrences',
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='white'),
            height=400
        )

        st.markdown(f"### 👤 Driver: {driver}")
        st.plotly_chart(fig_rpm, use_container_width=True)
