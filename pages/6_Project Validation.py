#  ----------------------------------------------------------------------------------------------------------------------#
# LIBRARY IMPORT
# ----------------------------------------------------------------------------------------------------------------------#

# Import library
import streamlit as st  # Streamlit library
import pandas as pd  # Pandas library is used for exporting Excel data.
from streamlit_option_menu import option_menu
# ----------------------------------------------------------------------------------------------------------------------#


# ----------------------------------------------------------------------------------------------------------------------#
# Update ST.SESSION STATE with value
# ----------------------------------------------------------------------------------------------------------------------#
if "Project_Engineer" not in st.session_state:
    st.session_state["Project_Engineer"] = ""

if "Project_Description" not in st.session_state:
    st.session_state["Project_Description"] = ""


def Project_Engineer():
    st.session_state["Project_Engineer"] = st.session_state["temp_Project_Engineer"]


def Project_Description():
    st.session_state["Project_Description"] = st.session_state["Temp_Project_Description"]


# ----------------------------------------------------------------------------------------------------------------------#
st.title("Project Validation")

st.write("")

st.divider()


st.text_input(
    "Project Engineer:",
    key="temp_Project_Engineer",
    value=st.session_state["Project_Engineer"],
    on_change=Project_Engineer
)

st.text_area(
    "Project Description:",
    key="Temp_Project_Description",
    value=st.session_state["Project_Description"],
    height=120,
    placeholder="Write down the project, what you intend to evaluate, and the expected results.Compare the results obtained in the tests with the desired ones.",
    on_change=Project_Description
)
