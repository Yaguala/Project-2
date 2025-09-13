# Nos packages
import streamlit as st
import datetime
from streamlit_option_menu import option_menu
import pandas as pd
import textwrap
from streamlit_searchbox import st_searchbox
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # , MinMaxScaler,
from sklearn.neighbors import NearestNeighbors

# ------ set page config ----------
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
# Remove side bar navigation------
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)


## Bar naviagation ----------------------------------
with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Suggestion", "Enfants", "Contacts"],
        icons=[],  # No icons
        default_index=2,
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
    selected = "Enfants"


#----------------------------------------------------


# Titre principal de l'application (affiché en haut de la page)
# Set colluns to arrange title page
a, b, c = st.columns(3)
a.title('')
b.title("ENFANTS")
c.title(' ')

st.subheader(' ', divider='green')
#--------------------Load Data ---------------

df_movies = pd.read_csv("data/films_final.csv")

# Selection of animation

df_movies_ani = df_movies[df_movies['genres'].str.contains("Animation")]

#------------------------ Multi Tabs ----------------------
tab1, tab2 = st.tabs(["Sugestion", "Tous les films"])

#------------------------ All films TAB 1-------------------
with tab1:
    dummies = df_movies_ani.genres.str.get_dummies(sep=',').drop(columns="Comedy")
    genres = dummies.columns.to_list()
    df_movies_ani = pd.concat([df_movies_ani, dummies], axis=1)

    cols = ['budget', 'revenue', 'popularity', 'startYear', 'runtimeMinutes',
            'averageRating', 'numVotes'] + genres


    # Function sugestion de filme:
    def recherche(tconst, cols):

        # colonne ml

        # Defenir les X_class en colluns
        X_class = df_movies_ani[cols]

        # Indiquer le filme au model
        X_test_c = df_movies_ani.loc[df_movies_ani["tconst"] == tconst, cols]

        # Standardiser toutes ces features
        scaler_knn = StandardScaler()
        X_knn_scaled = scaler_knn.fit_transform(X_class)

        # Nombre de voisins à trouver k et indiquer le numero de recumendations
        k = 5
        nn_model = NearestNeighbors(n_neighbors=k).fit(X_knn_scaled)

        # Standardiser toutes ces features
        X_test_c_scaled_knn = scaler_knn.transform(X_test_c)

        # Sélectionner les 3 premiers points de X_test_c (qui sont non
        # standardisés)
        sample_points_scaled = X_test_c_scaled_knn[:3, :]

        # .kneighbors() prend les points standardisés et retourne distances et
        # indices
        distances, indices = nn_model.kneighbors(sample_points_scaled)

        # Find the index
        indicies = indices[0].tolist()

        return df_movies_ani.iloc[indicies[1:]]


    # Funtion to search the title of filme in the dataframe:
    def search_film(searchterm):
        # Search for the searchterm
        results = df_movies_ani[df_movies_ani["title"].str.contains(searchterm, case=False,
                                                            na=False)]
        return results["title"].tolist()


    # Search function from streamlit_searchbox and disgn of the box search
    selected_value = st_searchbox(
        search_film,
        placeholder="Recherchez votre film d'animation préféré..... ",
        # Text in the search box if nothing inside
        # key="my_key", #No parametre info
    )

    # If nothing in search box "selected_value' the return of carrousel is
    # controled here:
    if isinstance(selected_value, str) and selected_value.strip() != "":
        film_id = df_movies[df_movies["title"].str.contains(selected_value, case=False, na=False)]

        if not film_id.empty and film_id["title"].iloc[0] in df_movies_ani["title"].values:
            # Acess the links of poster films
            df_sugest_enf = recherche(film_id["tconst"].iloc[0], cols)
            st.header("Sugestion Films Animation", divider="green")
            colist = ["col1", "col2", "col3", "col4"]
            colist = st.columns(4)
            for col, i in enumerate(df_sugest_enf.index):
                with colist[col % 4]:
                #st.write(df_movies_ani.primaryName[i])
                    st.image(df_movies_ani.poster_path[i], width=180)
                    if st.button(textwrap.shorten(df_movies_ani.title[i], width=19,  placeholder="…"), use_container_width=True,  key = f"btn_{tab1}_{i}"):
                        st.session_state.selected_film = df_movies_ani.tconst[i]
                        st.session_state.page_enfants = True
                        st.switch_page("pages/film.py")
        else:
            st.write("Le film choisi n'est pas un film d'animation.")


#------------------------ All films TAB 2-------------------
with tab2:
    st.header("Films Animation", divider="green")
    colist = ["col1", "col2", "col3", "col4"]
    colist = st.columns(4)
    for col, i in enumerate(df_movies_ani.index):
        with colist[col % 4]:
        #st.write(df_movies_ani.primaryName[i])
            st.image(df_movies_ani.poster_path[i], width=150)
            if st.button(textwrap.shorten(df_movies_ani.title[i], width=19,  placeholder="…"), use_container_width=True,  key=f"btn_{i}"):
                st.session_state.selected_film = df_movies_ani.tconst[i]
                st.session_state.page_enfants = True
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