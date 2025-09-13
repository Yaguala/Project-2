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
from streamlit_carousel import carousel
from streamlit_option_menu import option_menu


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
with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Suggestion", "Enfants", "Contacts", "Film"],
        icons=[],  # No icons
        default_index=4,
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
    st.switch_page("pages/Sugestion.py")
if selected == "Contacts":
    st.switch_page("pages/Contacts.py")
if selected == "Enfants":
    st.switch_page("pages/Enfants.py")
if selected == 'Film':
    selected = 'Film'




#----------------------------------------------------


# Affichage par defaut
titre_du_film = "Film par defaut"

# -------- Load the data -------------
df_movies = pd.read_csv("data/films_final.csv")
df_intervenant = pd.read_csv("data/intervenantes_final.csv")
df_intervenant_1950 = pd.read_csv("data/intervenant_tmdb_find_by_ID_1950_r5.csv")

#--------------- Selection film from carrousell-----------------
name = st.query_params.get("name", None)

if name:
    st.session_state["selected_intervenant"] = name
    titre_du_film = "Film par defaut dans if"

#if "selected_intervenant" not in st.session_state:
#    st.session_state["selected_intervenant"] = "nm0000091" # A changer pour une film base

if st.session_state.selected_film :
    tconst = st.session_state.selected_film    
    df_inter = df_movies[df_movies['tconst'] == tconst]
    titre_du_film = df_inter['title'].iloc[0]
else :        
    tconst = "tt10196398"    # le film affiché par defaut "Adieu les cons"
    df_inter = df_movies[df_movies['tconst'] == tconst]
    titre_du_film = df_inter['title'].iloc[0]
    
# st.header("Titre du film : "+titre_du_film, divider="green")



# ------ Set a background image of the filme --------------------
# 
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] > .stMain {{
        background-color: #070E19;
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.2), #070E19),
          url("{df_inter.backdrop_path.iloc[0]}");
        
        background-size: 100% 800px;
        background-repeat: no-repeat;
        background-position: center top;
        background-attachment: local;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------------------------

# Le bloc de 3 parties de présentation : l'affiche, le resume et les autres infos

left, right = st.columns([0.4, 0.6], border=True)
left.image(df_inter.poster_path.iloc[0])
# middle.write("Résumé :")
# middle.write(df_inter.overview.iloc[0])
right.header(titre_du_film, divider="green")
right.write("Popularité : "+str(df_inter.popularity.iloc[0]))
right.write("Année de sortie : "+str(df_inter.startYear.iloc[0]))
right.write("Genre : "+str(df_inter.genres.iloc[0]).replace(",", ", "))
right.write("Rating : "+str(df_inter.averageRating.iloc[0])+" sur "+str(df_inter.numVotes.iloc[0])+" votant(s)")
# Button retour page sugestion
page_embeding = st.session_state.get("page_embeding", False)
page_enfants = st.session_state.get("page_enfants", False)
if right.button("Revenir aux suggestions", use_container_width=True):
    if page_embeding :
        st.switch_page("pages/embeding.py")
    elif page_enfants :
        st.switch_page("pages/Enfants.py")
    else:
        st.switch_page("pages/standardscaler.py")

#st.write("id film : "+tconst)
#notre_condition = "tt1399664" in df_intervenant.knownForTitles
#st.write(notre_condition)

#-----Band the anounce ---------------------------

# On teste si il y a une bande annonce. Si il y en a pas, on affiche le message d'absence, sinon on affiche la video
if df_inter.bande_annonce.iloc[0] == "pas disponible":
    st.write("Désolè, pas de bande annonce disponible")
else:
    st.video(df_inter.bande_annonce.iloc[0])
# -----------------------------------------------------------------------


tab1, tab2 = st.tabs(["Résumé", "Intervenant(s)"])

with tab1:
    st.header("Résumé", divider="green")
    st.write(df_inter.overview.iloc[0])


with tab2:
    #for list_intervenant in df_intervenant.knownForTitles:
    #    if "tt1399664" in list_intervenant:
    #        st.write(list_intervenant)
            #st.write(list_nom)

    #option = ['tt1399664,tt0411270,tt0464913,tt1285246']
    #option = ['tt1399664']
    #option = 'tt1399664'
    df_resultat = df_intervenant.loc[df_intervenant.knownForTitles.str.contains(tconst)]

    # On teste si on a des intervenants 
    if (df_resultat.notnull().values.sum() > 0) :
        st.header("Intervenants", divider="green")
        colist = ["col1", "col2", "col3", "col4"]
        colist = st.columns(4)
        for col, i in enumerate(df_resultat.index):
            with colist[col % 4]:
            #st.write(df_resultat.primaryName[i])
                st.image(df_resultat.profile_photo[i], width=160)
                if st.button(df_resultat.primaryName[i], use_container_width=True):
                    st.session_state.selected_intervenant = df_resultat.nconst[i]
                    st.switch_page("pages/intervenant.py")
    else :
        st.write("Désolé; nous n'avons pas d'intervenant à afficher")

    st.write("-------")

    #if st.button("nm0000003"):
    #    st.session_state.selected_intervenant = "nm0000003"
    #    st.switch_page("pages/intervenant.py")
    #if st.button("nm0000079"):
    #    st.session_state.selected_intervenant = "nm0000079"
    #    st.switch_page("pages/intervenant.py")

    #st.divider()

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