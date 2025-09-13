# Nos packages
import streamlit as st
import pandas as pd
import datetime
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # , MinMaxScaler
from sklearn.neighbors import NearestNeighbors
# Search box need to pip install streamlit_searchbox
# Makes a search box for title de filme
from streamlit_searchbox import st_searchbox
from streamlit_option_menu import option_menu


#Set page config -------------------------
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# Remove side bar navigation------
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Bar naviagation ----------------------------------

left, midel, right = st.columns([1,1.2,1])

with midel.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Suggestion", "Enfants", "Contacts"],
        icons=[],  # No icons
        default_index=0,
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
    selected = "Home"
if selected == "Suggestion":
    st.switch_page("pages/Sugestion.py")
if selected == "Contacts":
    st.switch_page("pages/Contacts.py")
if selected == "Enfants":
    st.switch_page("pages/Enfants.py")




#----------------------------------------------------


# Titre principal de l'application (affiché en haut de la page)
left, midel, right = st.columns([1,1.2,1])
midel.title("🏠 ACTUELLEMENT EN SALLE 🌎")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Code pour telecharger le fichier csv
df_movies = pd.read_csv("data/films_final.csv")
# ------------ Films en sale les dernier sortie anne 2024 + ---------
df_movies_filt = df_movies[(df_movies['startYear'] > 2023) & (df_movies['averageRating'] > 6)]
df_movies_filt = df_movies_filt.sort_values(by=['popularity'], ascending=False)
backdrop = df_movies_filt.backdrop_path.tolist()
col1, col2, col3, col4, col5, col6 = backdrop[:6]
titles = df_movies_filt['title'].str.upper().tolist()
title1, title2, title3, title4, title5, title6 = titles[:6]


#Carousel doc https://pypi.org/project/st-ant-carousel/
from st_ant_carousel import st_ant_carousel

# Define the content with images
content = [
    {
        "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
        "content":f'<b2>{title1}</b2><img src="{col1}" width="2000" height="700">'
    },
    {
        "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
        "content": f'<b2>{title2}</b2><img src="{col2}" width="2000" height="700">'
    },
    {
        "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
        "content": f'<b2>{title3}</b2><img src="{col3}" width="2000" height="700">'
    },
    {
        "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
        "content": f'<b2>{title4}</b2><img src="{col4}" width="2000" height="700" style="cursor: pointer;">'
    },
    {
         "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
        "content": f'<b2>{title5}</b2><img src="{col5}" width="2000" height="700" style="cursor: pointer;">'
    },
    {
        "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
        "content": f'<b2>{title6}</b2><img src="{col6}" width="2000" height="700">'
    }
]

# Define carousel styling
carousel_style = {
    "width": "100%",
    "height": "700px",
    "background-color": "#12980300",
}

# Display the carousel


st_ant_carousel(
    content,
    carousel_style=carousel_style,
    autoplay=True,
    autoplaySpeed=3000,
    dotPosition="bottom",
    dots=True,
    waitForAnimate=True,
    easing="ease-in-out",
    effect="scrollx",
    pauseOnDotsHover=True,
    pauseOnHover=True,
    animationSpeed=5000,
    vertical=False,
    adaptiveHeight=True, 
    height=700
)

# -------------------------- Films in salle ---------------------------
import textwrap
st.header("", divider="green")
colist = ["col1", "col2", "col3"]
colist = st.columns(6)
for col, i in enumerate(df_movies_filt.index[:6]):
    with colist[col % 6]:
    #st.write(df_movies_filt.primaryName[i])
        st.image(df_movies_filt.poster_path[i], width=300)
        if st.button(textwrap.shorten(df_movies_filt.title[i], width=22,  placeholder="…"), use_container_width=True,  key=f"btn_{i}"):
            st.session_state.selected_film = df_movies_filt.tconst[i]
            st.switch_page("pages/film.py")


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