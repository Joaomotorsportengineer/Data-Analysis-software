#  ----------------------------------------------------------------------------------------------------------------------#
# LIBRARY IMPORT
# ----------------------------------------------------------------------------------------------------------------------#

# Import library
import streamlit as st  # Streamlit library
import pandas as pd  # Pandas library is used for exporting Excel data.
from streamlit_option_menu import option_menu
# ----------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------------------------------#
st.title("Brake")
st.divider()

tabs = st.tabs(["Theoretical data of the brake system",
               "Brake Eficiece", "-", "-"])
