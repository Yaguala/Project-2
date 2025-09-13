import pandas as pd
import streamlit as st

# ------ set page config ----------
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
# Remove side bar navigation------
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Bar naviagation ----------------------------------
from streamlit_option_menu import option_menu

with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Suggestion", "Enfants", "Contacts"],
        icons=[],  # No icons
        default_index=1,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#05335F",
                "class": "navbar-fixed",  # Add fixed class
            },
            "nav-link": {
                "color": "white",
                "font-size": "16px",
                "margin": "0px",
                "padding": "10px",
            },
            "nav-link-selected": {
                "background-color": "#1B4F72"
            },
        }
    )
if selected == "Home":
    st.switch_page("index.py")
if selected == "Suggestion":
    selected = 'Suggestion'
if selected == "Contacts":
    st.switch_page("pages/Contacts.py")
if selected == "Enfants":
    st.switch_page("pages/Enfants.py")




# ----------------------------------------------------
# -------------------------Reset session_state ----------------
st.session_state.page_embeding = False
st.session_state.page_enfants = False

# --------------------Buttons standardscaler --- embeding ----------------------
right,mid, left = st.columns([3.3,8,3.3])

with mid:
    st.header("SUGESTIONS DE FILMS")
st.subheader('Bienvenue dans la section Suggestion ! Ici, vous pouvez découvrir des films recommandés selon vos goûts, grâce à deux approches diferents', divider='green')

right,mid, left = st.columns([4.5,1,4.5])

with right:
    st.write('Sélectionnez un film que vous avez aimé, et notre système vous proposera automatiquement des films similaires')
    if st.button("Film Préféré", use_container_width=True):
        st.switch_page("pages/standardscaler.py")

with left:
    st.write('Décrivez le type de film que vous avez envie de voir, et notre système vous proposerales films les plus proches de vos envies.')
    if st.button("Description Personnalisée", use_container_width=True):
        st.switch_page("pages/embeding.py")










# --------------------------- bas de page -----------------
st.markdown('<div class="footer">© 2025 SAPEM CONSEIL. All rights reserved.</div>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
        color: #A0A0A0;
    }
    </style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------