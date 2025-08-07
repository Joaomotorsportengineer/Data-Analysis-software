#  ----------------------------------------------------------------------------------------------------------------------#
# LIBRARY IMPORT
# ----------------------------------------------------------------------------------------------------------------------#

# Import library
import streamlit as st  # Streamlit library
import pandas as pd  # Pandas library is used of export excel data.
from streamlit_option_menu import option_menu
import io  # ADICIONE NO TOPO DO SCRIPT
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
import plotly.express as px


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


# ----------------------------------------------------------------------------------------------------------------------#


# Função para interpolar o valor de OilMin para uma rotação específica
# Carrega os dados da planilha de pressões mínimas de óleo
Oil_Pressure_Min = {
    'RPM': [0, 1000, 1500, 3000, 4500, 6000, 7500, 9000, 10500],
    'OilMin': [0, 0.7, 1, 1.5, 2.4, 3.9, 4.5, 4.8, 5]
}


def interpolar_pressao_minima(rpm_atual):
    return np.interp(rpm_atual, Oil_Pressure_Min['RPM'], Oil_Pressure_Min['OilMin'])


#  ----------------------------------------------------------------------------------------------------------------------#
# Setup setting
# ----------------------------------------------------------------------------------------------------------------------#
st.title("Driver Data Analysis")

colors = {
    "Jenifer": "blue",
    "Muniz": "red",
    "Rafael": "green",
    "Piloto4": "purple",
    # Adicione mais pilotos e cores conforme necessário
}

row_heights = [1, 1.5, 0.5, 0.3]

fig = sp.make_subplots(rows=4, cols=1, shared_xaxes=True,
                       vertical_spacing=0.06, row_heights=row_heights)


for i, driver in enumerate(st.session_state.selected_drivers):

    df = localizar_log_piloto(driver)
    if df is None:
        continue
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)


tabs = st.tabs(
    ["Driving Influences", "Throttle", "Analysis acceleration", "Trends"])

with tabs[0]:
    st.subheader("Driving Influences")

    col_grafico, col_obs = st.columns([4, 1])

    with col_grafico:
        fig = sp.make_subplots(
            rows=4, cols=1, shared_xaxes=True,
            vertical_spacing=0.06, row_heights=row_heights
        )

        for i, driver in enumerate(st.session_state.selected_drivers):
            df = localizar_log_piloto(driver)
            if df is None:
                continue
            df = df.apply(pd.to_numeric, errors='coerce').fillna(
                0).astype(float)

            driver_color = colors.get(driver, 'Orange')

            fig.add_trace(go.Scatter(x=df['Distância'], y=df['RPM'],
                                     mode='lines', name=f'{driver} - RPM', line=dict(color=driver_color)),
                          row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Distância'], y=df['Velocidade_de_referência'],
                                     mode='lines', name=f'{driver} - Speed', line=dict(color=driver_color)),
                          row=2, col=1)
            fig.add_trace(go.Scatter(x=df['Distância'], y=df['TPS'],
                                     mode='lines', name=f'{driver} - TPS', line=dict(color=driver_color)),
                          row=3, col=1)

        fig.update_layout(
            title={
                'text': 'Data analysis driving',
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top',
                'font': {'size': 32}
            },
            showlegend=False,
            hovermode="x unified",
            height=600,
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='white')
        )
        fig.update_yaxes(showticklabels=False)
        for j, variable in enumerate(['RPM', 'Speed', 'TPS'], start=1):
            fig.update_yaxes(title_text=variable, row=j, col=1)

        st.plotly_chart(fig, use_container_width=True)

    with col_obs:

        if "xy_drive_notes" not in st.session_state:
            st.session_state["xy_drive_notes"] = ""

        if "temp_xy_drive_notes" not in st.session_state:
            st.session_state["temp_xy_drive_notes"] = st.session_state["xy_drive_notes"]

        def xy_drive_notes():
            st.session_state["xy_drive_notes"] = st.session_state["temp_xy_drive_notes"]

        st.markdown("### 📝 Engineer's Notes")

        st.text_area(
            label="Observations on driver influences:",
            key="temp_xy_drive_notes",
            height=300,
            placeholder="Write drive influences...",
            on_change=xy_drive_notes
        )


with tabs[1]:

    st.subheader("Throttle Influences")
    fig = sp.make_subplots(rows=4, cols=1, shared_xaxes=True,
                           vertical_spacing=0.06, row_heights=row_heights)

    for i, driver in enumerate(st.session_state.selected_drivers):
        df = localizar_log_piloto(driver)
        if df is None:
            continue
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)

        # Cria uma coluna que verifica se o TPS está acima de 95%
        df['TPS_above_95'] = df['TPS'] > 90
        sample_interval = 1 / 50  # 50 Hz -> 0.02 segundos
        # Cria uma coluna que acumula o tempo em que o TPS está acima de 95% ao longo da volta
        df['t100%TPS'] = df['TPS_above_95'].cumsum() * \
            sample_interval

        tLap = df['Distância'].iloc[-1]  # calcular A VOLTA tLap

        # Calcular a porcentagem de TPS
        TPSPorcentagem = 100 * \
            (df['t100%TPS'].iloc[-1] / df['Distância'].iloc[-1])

        # Calcular a derivada do TPS em relação ao tempo
        # Calcule a diferença no TPS e divida pelo intervalo de tempo
        df['vTP(t)'] = df['TPS'].diff() / sample_interval

        # Para lidar com o NaN na primeira linha que resulta da operação diff()
        df['vTP(t)'] = df['vTP(t)'].fillna(
            0)  # ou algum valor apropriado, como 0

        # Exibir as colunas desejadas

        variable_driving_Log = [
            'Speed', 'TPS', 'F. TPS', 'S. TPS']

        row_heights = [2, 0.2, 0.2, 2]
        # Use 'Orange' como padrão se o piloto não estiver no dicionário
        driver_color = colors.get(driver, 'Orange')

        fig.add_trace(go.Scatter(x=df['Distância'], y=df['Velocidade_de_referência'],
                                 mode='lines', name=f'{driver} - Speed',  line=dict(color=driver_color)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Distância'], y=df['TPS'], mode='lines',  name=f'{
            driver} - TPS',  line=dict(color=driver_color)), row=2, col=1)
        fig.add_trace(go.Scatter(x=df['Distância'], y=df['t100%TPS'], mode='lines', name=f'{
            driver} - Full TPS',  line=dict(color=driver_color)), row=3, col=1)
        fig.add_trace(go.Scatter(x=df['Distância'], y=df['vTP(t)'], mode='lines',  name=f'{
            driver} - Speed TPS',  line=dict(color=driver_color)), row=4, col=1)

        # Configura o layout do gráfico
        fig.update_layout(
            # Adiciona um título
            title={
                'text': f'Data analysis driving',
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top',
                'font': {'size': 32}
            },
            showlegend=False,
            hovermode="x unified",
            height=600,
            # Cor de fundo do gráfico (área de plotagem)
            plot_bgcolor='#0E1117',
            # Cor de fundo do papel (área fora do gráfico)
            paper_bgcolor='#0E1117'
        )
        # Oculta os eixos y para os 6 gráficos de linha gerados
        fig.update_yaxes(showticklabels=False)

        # Adiciona os nomes das variáveis no eixo Y para os 6 gráficos de linha gerados
        for j, variable_driving in enumerate(variable_driving_Log, start=1):
            fig.update_yaxes(title_text=variable_driving, row=j, col=1)

    # Usa o st.plotly_chart para exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    # ----------------------------
    # GRIP FACTOR SELECTORS ABOVE GRAPH
    # ----------------------------

    st.markdown("#### Select Grip Factors")
    col1, col2, col3 = st.columns(3)
    with col1:
        show_aero = st.checkbox("Aero Grip", True)
        show_braking = st.checkbox("Straightline Braking Grip", True)
    with col2:
        show_traction = st.checkbox("Traction Grip", True)
        show_trail = st.checkbox("Trail Braking Grip", True)
    with col3:
        show_cornering = st.checkbox("Cornering Grip", True)
    # Layout
    col_grafico, col_obs = st.columns([4, 1])

    with col_grafico:
        st.subheader("Longitudinal vs Lateral Acceleration")

        fig = go.Figure()

        for driver in st.session_state.selected_drivers:
            df = localizar_log_piloto(driver)
            if df is None:
                continue

            df = df.apply(pd.to_numeric, errors='coerce').fillna(
                0).astype(float)

            # Correção e suavização da velocidade
            df['Velocidade_corrigida'] = df['Velocidade_de_referência'].interpolate(
                method='linear').fillna(method='bfill').fillna(method='ffill')
            df['Velocidade_corrigida'] = df['Velocidade_corrigida'].rolling(
                window=80, center=True).mean().fillna(method='bfill').fillna(method='ffill')

            # Cálculo das acelerações
            sample_time = 1 / 100  # 100 Hz
            g = 9.81
            raio_skidpad = 8.5

            df['AccLongitudinal'] = (
                (df['Velocidade_corrigida'] / 3.6).diff() / sample_time) / g
            df['AccLateral'] = (
                ((df['Velocidade_corrigida'] / 3.6) ** 2) / raio_skidpad) / g
            df['G_Comb'] = np.sqrt(df['AccLongitudinal']
                                   ** 2 + df['AccLateral']**2)

            # Suavização
            df['AccLongitudinal'] = df['AccLongitudinal'].rolling(
                window=30, center=True).mean().fillna(method='bfill').fillna(method='ffill')
            df['AccLateral'] = df['AccLateral'].rolling(
                window=20, center=True).mean().fillna(method='bfill').fillna(method='ffill')

            # Cor por piloto
            driver_color = colors.get(driver, 'orange')

            # Plot por piloto com nome
            fig.add_trace(go.Scatter(
                x=df['AccLateral'],
                y=df['AccLongitudinal'],
                mode='markers',
                name=driver,
                marker=dict(color=driver_color, size=6, opacity=0.6),
            ))

            # Regions
            if show_aero:
                fig.add_shape(type="rect", x0=1.3, x1=3, y0=-2, y1=2,
                              fillcolor="gray", opacity=0.2, layer="below", line_width=0)
                df_aero = df[(df['AccLateral'].abs() > 1.3) &
                             (df['Velocidade_corrigida'] > 38)]
                fig.add_trace(go.Scatter(
                    x=df_aero['AccLateral'],
                    y=df_aero['AccLongitudinal'],
                    mode='markers',
                    name=f'{driver} – Aero Grip',
                    marker=dict(color='gold', size=6, symbol='x', opacity=0.9)))

            if show_braking:
                fig.add_shape(type="rect", x0=-0.4, x1=0.4, y0=-2, y1=-0.8,
                              fillcolor="gray", opacity=0.2, layer="below", line_width=0)
                df_brake = df[(df['AccLongitudinal'] < -0.8) &
                              (df['AccLateral'].abs() < 0.4)]
                fig.add_trace(go.Scatter(
                    x=df_brake['AccLateral'],
                    y=df_brake['AccLongitudinal'],
                    mode='markers',
                    name=f'{driver} – Braking Grip',
                    marker=dict(color='cyan', size=6, symbol='triangle-down', opacity=0.9)))

            if show_traction:
                fig.add_shape(type="rect", x0=1, x1=3, y0=0.2, y1=3,
                              fillcolor="gray", opacity=0.2, layer="below", line_width=0)
                df_traction = df[(df['AccLongitudinal'] > 0.2) & (
                    df['AccLateral'].abs() > 1) & (df['Velocidade_corrigida'] < 40)]
                fig.add_trace(go.Scatter(
                    x=df_traction['AccLateral'],
                    y=df_traction['AccLongitudinal'],
                    mode='markers',
                    name=f'{driver} – Traction Grip',
                    marker=dict(color='violet', size=6, symbol='circle', opacity=0.9)))

            if show_trail:
                fig.add_shape(type="rect", x0=0.8, x1=2, y0=-0.4, y1=-2,
                              fillcolor="gray", opacity=0.2, layer="below", line_width=0)
                df_trail = df[(df['AccLongitudinal'] < -0.4) &
                              (df['AccLateral'].abs() > 0.8)]
                fig.add_trace(go.Scatter(
                    x=df_trail['AccLateral'],
                    y=df_trail['AccLongitudinal'],
                    mode='markers',
                    name=f'{driver} – Trail Braking',
                    marker=dict(color='deepskyblue', size=6, symbol='star', opacity=0.9)))

            if show_cornering:
                fig.add_shape(type="rect", x0=1, x1=3, y0=-0.4, y1=0.4,
                              fillcolor="gray", opacity=0.2, layer="below", line_width=0)
                df_cornering = df[(df['AccLongitudinal'].abs() < 0.4) & (
                    df['AccLateral'].abs() > 1)]
                fig.add_trace(go.Scatter(
                    x=df_cornering['AccLateral'],
                    y=df_cornering['AccLongitudinal'],
                    mode='markers',
                    name=f'{driver} – Cornering Grip',
                    marker=dict(color='orange', size=6, symbol='square', opacity=0.9)))

        fig.update_layout(
            title='Grip Factors – Acceleration Plane',
            xaxis_title='Lateral Acceleration (g)',
            yaxis_title='Longitudinal Acceleration (g)',
            hovermode="closest",
            height=750,
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='white'),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_obs:
        if "acc_plane_notes" not in st.session_state:
            st.session_state["acc_plane_notes"] = ""

        if "temp_acc_plane_notes" not in st.session_state:
            st.session_state["temp_acc_plane_notes"] = st.session_state["acc_plane_notes"]

        def salvar_acc_plane_notes():
            st.session_state["acc_plane_notes"] = st.session_state["temp_acc_plane_notes"]

        st.markdown("### 📝 Engineer's Notes")

        st.text_area(
            label="Observations on signal behavior:",
            key="temp_acc_plane_notes",
            height=500,
            placeholder="Observations on acceleration behavior...",
            on_change=salvar_acc_plane_notes
        )


with tabs[3]:

    st.subheader("Trend")
    # Criação da figura
    # Criação do histograma
    fig_hist = go.Figure()

    for i, driver in enumerate(st.session_state.selected_drivers):
        df = localizar_log_piloto(driver)
        if df is None:
            continue
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)

        driver_color = colors.get(driver, 'Orange')

        # Adicionar o histograma de RPM
        fig_hist.add_trace(go.Histogram(
            x=df['Velocidade_de_referência'],
            nbinsx=50,  # Ajuste o número de bins conforme necessário
            marker=dict(color=driver_color),
            name=f'{driver} - Speed Trends'
        ))

        # Configurar o layout do gráfico
        fig_hist.update_layout(
            title='Histogram of Speed',
            xaxis_title='Speed',
            yaxis_title='Number of Occurrences',
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='black'),
            height=400  # Ajuste a altura conforme necessário
        )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_hist, use_container_width=True)\

    # Criação da figura
    # Criação do histograma
    fig_hist = go.Figure()

    for i, driver in enumerate(st.session_state.selected_drivers):
        df = localizar_log_piloto(driver)
        if df is None:
            continue
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)

        driver_color = colors.get(driver, 'Orange')

        # Adicionar o histograma de RPM
        fig_hist.add_trace(go.Histogram(
            x=df['TPS'],
            nbinsx=50,  # Ajuste o número de bins conforme necessário
            marker=dict(color=driver_color),
            name=f'{driver} - Throttle Trends'
        ))

        # Configurar o layout do gráfico
        fig_hist.update_layout(
            title='Histogram of throttle',
            xaxis_title='Throttle',
            yaxis_title='Number of Occurrences',
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='black'),
            height=400  # Ajuste a altura conforme necessário
        )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_hist, use_container_width=True)
