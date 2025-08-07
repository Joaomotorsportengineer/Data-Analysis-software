# PROJECT BY JOÃO VITOR RODRIGUES
# Streamlit app for Iron Racers – Formula SAE
# Run using: streamlit run Performance.py

import streamlit as st
import pandas as pd
from datetime import date, time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import StringIO
import json

# ----------------------------- SETTINGS -----------------------------
st.set_page_config(page_title="Data Analysis - Formula Student",
                   page_icon="🏁", layout="wide")

# ----------------------------- SHEETS SETUP -----------------------------


def salvar_em_google_sheets(df, worksheet_name="Performance"):
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "cred.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1gML92gsUXIW68o7EEtP8ltmnCQgD4oR8-dXLibGbhcE")

    try:
        worksheet = sheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(
            title=worksheet_name, rows="100", cols="20")

    existing_data = worksheet.get_all_values()
    planilha_vazia = all([all(cell == "" for cell in row)
                         for row in existing_data]) or len(existing_data) == 0

    headers = df.columns.tolist()
    rows = df.values.tolist()

    if planilha_vazia:
        worksheet.insert_row(headers, index=1)
        next_row = 2
    else:
        next_row = len(existing_data) + 1

    for i, row in enumerate(rows):
        worksheet.insert_row(row, index=next_row + i)


def ler_google_sheets(worksheet_name="Performance"):
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "cred.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1gML92gsUXIW68o7EEtP8ltmnCQgD4oR8-dXLibGbhcE")
    worksheet = sheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# ----------------------------- SESSION STATE -----------------------------


def init_session():
    default_drivers = ["Jenifer", "Muniz", "Rafael"]

    st.session_state.setdefault("selected_drivers", ["Jenifer"])
    st.session_state.setdefault("Goal", "")
    st.session_state.setdefault("Planing", pd.DataFrame({
        "Description": [""],
        "Time": [""],
        "Responsible": [""],
        "Done": [False]
    }))
    st.session_state.setdefault("Local", "")
    st.session_state.setdefault("temp_local", st.session_state["Local"])
    st.session_state.setdefault("general_report", "")
    st.session_state.setdefault("start_time", time(9, 0))
    st.session_state.setdefault("end_time", time(17, 0))
    st.session_state.setdefault(
        "temp_start_time", st.session_state["start_time"])
    st.session_state.setdefault("temp_end_time", st.session_state["end_time"])
    st.session_state.setdefault("session_date", date.today())


init_session()

# ----------------------------- PLANNING FIELDS -----------------------------
st.title("Data Analysis Software")
tabs = st.tabs(["📝 Test Planning", "📊 Data Log & Save"])

with tabs[0]:  # Weight Information
    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.text_input("Test goal:", key="temp_goal", value=st.session_state["Goal"], on_change=lambda: st.session_state.update(
            {"Goal": st.session_state["temp_goal"]}))
        st.text_input("Test location:", key="temp_local", value=st.session_state["Local"], on_change=lambda: st.session_state.update(
            {"Local": st.session_state["temp_local"]}))
        st.session_state["selected_drivers"] = st.multiselect("Select the drivers:", [
            "Jenifer", "Muniz", "Rafael"], default=st.session_state["selected_drivers"], max_selections=6, key="season_drivers")

        st.date_input("Select the date:", value=st.session_state["session_date"], key="date_picker", on_change=lambda: st.session_state.update(
            {"session_date": st.session_state["date_picker"]}))

        c1, c2 = st.columns(2)
        with c1:
            st.time_input("Start time:", key="temp_start_time", value=st.session_state["temp_start_time"], on_change=lambda: st.session_state.update(
                {"start_time": st.session_state["temp_start_time"]}))
        with c2:
            st.time_input("End time:", key="temp_end_time", value=st.session_state["temp_end_time"], on_change=lambda: st.session_state.update(
                {"end_time": st.session_state["temp_end_time"]}))

    with col2:
        st.text("Test Planing:")
        df_editado = st.data_editor(
            st.session_state["Planing"], num_rows="dynamic", use_container_width=True)

        if st.button("💾 Confirm planing"):
            st.session_state["Planing_pending_save"] = df_editado
            st.rerun()

        if "Planing_pending_save" in st.session_state:
            st.session_state["Planing"] = st.session_state.pop(
                "Planing_pending_save")
            st.success("✅ Planning saved successfully!")

    st.text_area("General Reports:", key="temp_relatorio", value=st.session_state["general_report"], height=120, placeholder="Write...", on_change=lambda: st.session_state.update(
        {"general_report": st.session_state["temp_relatorio"]}))
with tabs[1]:  # Weight Information

    # ----------------------------- UPLOAD E LOGS -----------------------------
    st.markdown("### 📂 Uploaded files")
    uploaded_files = st.file_uploader("Select log", accept_multiple_files=True)

    if uploaded_files:
        st.session_state.setdefault("arquivos_carregados", {})
        for file in uploaded_files:
            try:
                conteudo = file.read().decode("utf-8")
            except:
                conteudo = "<Erro ao ler arquivo como texto>"
            st.session_state["arquivos_carregados"][file.name] = conteudo
        st.success("Files loaded and saved successfully!")

    if "arquivos_carregados" in st.session_state and st.session_state["arquivos_carregados"]:
        for nome in st.session_state["arquivos_carregados"]:
            c1, c2, c3 = st.columns([0.05, 0.8, 0.15])
            with c1:
                st.markdown("📄")
            with c2:
                with st.expander(nome):
                    st.text_area(
                        f"Conteúdo de {nome}", st.session_state["arquivos_carregados"][nome], height=200)
            with c3:
                if st.button(f"❌ Remover", key=f"remover_{nome}"):
                    del st.session_state["arquivos_carregados"][nome]
                    st.rerun()
    else:
        st.info("No files uploaded yet.")

    # ----------------------------- SAVE AND LOAD -----------------------------
    st.divider()
    st.markdown("### 📗 Google Sheets Data File")

    def gerar_dataframe_de_registro():
        arquivos = ", ".join(st.session_state.get(
            "arquivos_carregados", {}).keys())
        planing_text = st.session_state["Planing"].to_csv(index=False)

        return pd.DataFrame({
            "Select the date": [str(st.session_state["session_date"])],
            "Test goal": [st.session_state["Goal"]],
            "Test location": [st.session_state["Local"]],
            "Select the drivers": [", ".join(st.session_state["selected_drivers"])],
            "Start time": [str(st.session_state["start_time"])],
            "End time": [str(st.session_state["end_time"])],
            "Test Planing": [planing_text],
            "General Reports": [st.session_state["general_report"]],
            "Uploaded files": [arquivos],
            "Driver data": [json.dumps(st.session_state.get("driver_data", {}))],
            "External temps": [json.dumps(st.session_state.get("external_temps", {}))],
            "XY Notes": [st.session_state.get("xy_analysis_notes", "")],
            "Oil Pressure Notes": [st.session_state.get("Oil_Pressure_Analysis_note", "")]
        })

    if st.button("📤 Send to Google Sheets"):
        try:
            df_envio = gerar_dataframe_de_registro()
            salvar_em_google_sheets(df_envio)
            st.success("✅ Data successfully uploaded to Google Sheets!")
        except Exception as e:
            st.error(f"❌ Error sending: {e}")

    with st.expander("📂 Load data"):
        df_salvos = ler_google_sheets()
        if not df_salvos.empty:
            opcoes = df_salvos["Select the date"].astype(
                str) + " - " + df_salvos["Test goal"] + " - " + df_salvos["Select the drivers"]
            indice = st.selectbox(
                "Select a saved test:", options=opcoes.index, format_func=opcoes.__getitem__)
            if st.button("🔁 Load selected data"):
                linha = df_salvos.iloc[indice]
                st.session_state["xy_analysis_notes"] = linha.get(
                    "XY Notes", "")
                st.session_state["Oil_Pressure_Analysis_note"] = linha.get(
                    "Oil Pressure Notes", "")

                st.session_state["session_date"] = pd.to_datetime(
                    linha["Select the date"]).date()
                st.session_state["Goal"] = linha["Test goal"]
                st.session_state["Local"] = linha["Test location"]
                st.session_state["selected_drivers"] = [p.strip()
                                                        for p in linha["Select the drivers"].split(",")]
                st.session_state["start_time"] = pd.to_datetime(
                    linha["Start time"]).time()
                st.session_state["end_time"] = pd.to_datetime(
                    linha["End time"]).time()
                st.session_state["Planing"] = pd.read_csv(
                    StringIO(linha["Test Planing"]))
                st.session_state["general_report"] = linha["General Reports"]
                st.session_state["driver_data"] = json.loads(
                    linha["Driver data"])
                st.session_state["external_temps"] = json.loads(
                    linha["External temps"])
                st.success("✅ Data loaded successfully!")
