import streamlit as st
import pandas as pd
import requests
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
        options=["Home", "Suggestion", "Enfants", "Contacts", "Intervenant"],
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
if selected == 'Intervenant':
    selected = 'intervenant'

#----------------------------------------------------

df_inter = pd.read_csv('data/intervenantes_final.csv')

# Show the dataframe to explorer
# st.write(df_inter)

#Variable persona chose the intervenant
name = st.query_params.get("name", None)

if name:
    st.session_state["selected_intervenant"] = name

if "selected_intervenant" not in st.session_state:
    st.session_state["selected_intervenant"] = "nm0000091"

persona = st.session_state.selected_intervenant
df_inter = df_inter[df_inter['nconst'] == persona]




st.header('Intervenants', divider="green")
# st.divider()

# Def 2 col in intervenant
col1, col2 = st.columns(2)


# Col1 intervenant
col1.image(df_inter['profile_photo'].iloc[0])


# Col2 intervenant
# Preparation text to descrive intervenant
if df_inter['deathYear'].isna is True:
    dead = " Elle est décédée le " + {int(df_inter['deathYear'].iloc[0])} + "."
else:
    dead = "."

if df_inter['place_of_birth'].iloc[0] == "inconnue":
    place = "dans une ville " + df_inter['place_of_birth'].iloc[0]
else:
    place = "dans la ville de " + df_inter['place_of_birth'].iloc[0]

if pd.isna(df_inter['birthYear'].iloc[0]):
    birth = ' né(e) '
else:
    birth = f"né(e) le {int(df_inter['birthYear'].iloc[0])}"

texte = (f"""{df_inter['primaryName'].iloc[0]},{birth}
        {place}, était un intervenante reconnue dans le domaine du {df_inter['known_for_department'].iloc[0]}
        {dead}""")


col2.header(df_inter['primaryName'].iloc[0], divider="green")
col2.markdown("""<style>.big-font {font-size:20px !important;}</style>""",
              unsafe_allow_html=True)
col2.markdown(f'<p class="big-font">{texte}</p>', unsafe_allow_html=True)

#Col2----------- retour au film --------------
# Load the film 
df_movie = pd.read_csv("data/films_final.csv")
if st.session_state.selected_film :
    tconst = st.session_state.selected_film    
    df_movie = df_movie[df_movie['tconst'] == tconst]
    titre_du_film = df_movie['title'].iloc[0]
if col2.button(f"Retour au filme: {titre_du_film}", use_container_width=True):
    st.switch_page("pages/film.py")
                    
# ---------------------------------------

tab1, tab2 = st.tabs(["Biography", "Autres films"])

with tab1:
    st.header("Biography", divider="green")
    st.write(df_inter['biography'].iloc[0])

with tab2:

    col1, col2, col3, col4 = st.columns(4)

    # GraphQL endpoint
    url = "https://graph.imdbapi.dev/v1"

    # GraphQL query with variable
    query = """
    query exampleMultiTitleIDsx($ids: [String!]!) {
    titles(ids: $ids) {
        id
        primary_title
        original_title
        posters {
        url
        width
        height
        }
    }
    }
    """

    # IDs from DataFrame
    imdb_ids = df_inter['knownForTitles'].iloc[0].split(',')
    variables = {"ids": imdb_ids}
    # st.write(f"imdb ids {imdb_ids}")

    # Send the request
    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"}
    )

    # Results lists
    result_title = []
    result_poster = []

    # Json
    if response.status_code == 200:
        data = response.json()
        titles = data.get("data").get("titles")
        # st.write("Titres récupérés :", titles)

        for title in titles:
            if bool(title.get('original_title')) is True:
                result_title.append(title.get('original_title'))
                posters = title.get("posters")
                if posters:
                    result_poster.append(posters[0].get('url'))
                else:
                    result_poster.append("assets/no_poster.jpg")
            else:
                result_title.append(title.get('primary_title'))
                posters = title.get("posters")
                if posters:
                    result_poster.append(posters[0].get('url'))
                else:
                    result_poster.append("assets/no_poster.jpg")

        # Show
        # st.write(f"films {result_title}")
        # st.write(f"poster {result_poster}")

    else:
        st.write("❌ Requête échouée :", response.status_code)
        st.write(response.text)  # pour diagnostiquer l'erreur

    col1.write(result_title[0])
    col2.write(result_title[1])
    col3.write(result_title[2])
    col4.write(result_title[3])

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.image(result_poster[0])
    col2.image(result_poster[1])
    col3.image(result_poster[2])
    col4.image(result_poster[3])

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